# -*- perl -*-
use strict;
use warnings;
use Path::Tiny;
use Wanage::URL;
use Wanage::HTTP;
use Warabe::App;
use Promised::Command;

$ENV{LANG} = 'C';
$ENV{TZ} = 'UTC';

my $RootPath = path (__FILE__)->parent->parent->absolute;

sub send_file ($$$) {
  my ($app, $file, $mime) = @_;
  return $app->throw_error (404) unless $file->is_file;
  $app->http->set_response_header ('Content-Type' => $mime) if defined $mime;
  $app->http->set_response_last_modified ($file->stat->mtime);
  $app->http->send_response_body_as_ref (\($file->slurp));
  return $app->http->close_response_body;
} # send_file

sub get_mime_type ($$) {
  my ($defs, $name) = @_;
  my $mime = undef;
  my $charset = undef;
  if ($name =~ s/\.([^.]+)\z//) {
    if (defined $defs->{charset}->{$1}) {
      $charset = $defs->{charset}->{$1};
      if (defined $defs->{mime}->{$1}) {
        $mime = $defs->{mime}->{$1};
      } elsif ($name =~ s/\.([^.]+)\z//) {
        if (defined $defs->{mime}->{$1}) {
          $mime = $defs->{mime}->{$1};
        }
      }
      if (defined $charset) {
        $charset =~ s/(["\\])/\\$1/g;
        $mime = qq{$mime; charset="$charset"};
      }
    } elsif (defined $defs->{mime}->{$1}) {
      $mime = $defs->{mime}->{$1};
    }
  }
  return $mime;
} # get_mime_type

sub load_htaccess ($$) {
  my ($defs, $dir_path) = @_;
  my $path = $dir_path->child ('.htaccess');
  return unless $path->is_file;
  for (split /\x0D?\x0A/, $path->slurp) {
    if (m{^\s*#}) {
      #
    } elsif (s{^\s*AddType\s+(\S+)\s+}{}) {
      my $mime = $1;
      $defs->{mime}->{$_} = $mime for map { my $x = $_; $x =~ s/^\.//; $x } split /\s+/, $_;
    } elsif (s{^\s*AddCharset\s+(\S+)\s+}{}) {
      my $charset = $1;
      $defs->{charset}->{$_} = $charset for map { my $x = $_; $x =~ s/^\.//; $x } split /\s+/, $_;
    } elsif (s{^\s*AddDefaultCharset\s+(\S+)\s*$}{}) {
      my $charset = $1;
      $defs->{charset}->{$_} = $charset for qw(txt html xml css js);
    } elsif (m{\A\s*(?:Options|AddHandler|RemoveHandler|DirectoryIndex|AddIcon|IndexOptions)\s}) {
      #
    } elsif (m{\S}) {
      warn "$path: Unknown directive |$_|\n";
    }
  }
} # load_htaccess

sub load_defs ($) {
  my $path = $_[0];
  my $defs = {};

  my $dir_path = $RootPath;
  load_htaccess $defs, $dir_path;

  for (@$path) {
    $dir_path = $dir_path->child ($_);
    load_htaccess $defs, $dir_path;
  }

  return $defs;
} # load_defs

sub run_cgi ($$) {
  my ($app, $file_path) = @_;
  my $cmd = Promised::Command->new ([$RootPath->child ('perl'), $file_path]);
  $cmd->envs->{REQUEST_METHOD} = $app->http->request_method;
  $cmd->envs->{QUERY_STRING} = $app->http->original_url->{query};
  $cmd->envs->{CONTENT_LENGTH} = $app->http->request_body_length;
  $cmd->envs->{CONTENT_TYPE} = $app->http->get_request_header ('Content-Type');
  $cmd->envs->{HTTP_ACCEPT_LANGUAGE} = $app->http->get_request_header ('Accept-Language');
  $cmd->envs->{HTTP_ACCEPT_ENCODING} = $app->http->get_request_header ('Accept-Encoding');
  $cmd->envs->{HTTP_TE} = $app->http->get_request_header ('TE');
  $cmd->envs->{HTTP_ORIGIN} = $app->http->get_request_header ('Origin');
  $cmd->envs->{SERVER_NAME} = $app->http->url->{host};
  $cmd->envs->{SERVER_PORT} = $app->http->url->{port};
  #SCRIPT_NAME
  #$cmd->envs->{PATH_INFO} = join '/', '', @$path[1..$#$path];
  $cmd->wd ($file_path->parent);
  $cmd->stdin ($app->http->request_body_as_ref);
  my $stdout = '';
  my $out_mode = '';
  $cmd->stdout (sub {
    if ($out_mode eq 'body') {
      $app->http->send_response_body_as_ref (\($_[0]));
      return;
    }
    $stdout .= $_[0];
    while ($stdout =~ s/^([^\x0A]*[^\x0D\x0A])\x0D?\x0A//) {
      my ($name, $value) = split /:/, $1, 2;
      $name =~ tr/A-Z/a-z/;
      if ($name eq 'status') {
        $value =~ s/^\s+//;
        my ($code, $reason) = split /\s+/, $value, 2;
        $app->http->set_status ($code, reason_phrase => $reason);
      } else {
        $app->http->set_response_header ($name => $value);
      }
    }
    if ($stdout =~ s/^\x0D?\x0A//) {
      $out_mode = 'body';
      $app->http->send_response_body_as_ref (\$stdout);
    }
  });
  return $cmd->run->then (sub {
    return $cmd->wait;
  })->then (sub {
    $app->http->close_response_body;
    die $_[0] unless $_[0]->exit_code == 0;
  });
} # run_cgi

return sub {
  delete $SIG{CHLD} if defined $SIG{CHLD} and not ref $SIG{CHLD}; # XXX

  my $http = Wanage::HTTP->new_from_psgi_env ($_[0]);
  my $app = Warabe::App->new_from_http ($http);

  warn sprintf "[%s] %s %s\n",
      scalar gmtime, $http->request_method, $app->http->url->stringify;

  return $app->execute_by_promise (sub {
    my $path = [@{$app->path_segments}];

    my $is_dir = $path->[-1] eq '';
    pop @$path if $is_dir;

    if (grep { not m{\A[0-9A-Za-z][0-9A-Za-z_.-]*\z} } @$path) {
      return $app->throw_error (404, reason_phrase => 'Bad path');
    }

    my $file_path = @$path ? $RootPath->child (join '/', @$path) : $RootPath;
    if ($is_dir) {
      return $app->throw_error (404, reason_phrase => 'Directory not found')
          unless $file_path->is_dir;

      my $defs = load_defs $path;
      my $html = sprintf q{
        <!DOCTYPE HTML>
        <link rel=stylesheet href=/support/directory.css>
        <title>tests-web/%s</title><h1>tests-web/%s</h1>
        <table>
          <thead>
            <tr><th>File<th>MIME type
          <tbody>
            <tr><th><a href=..>..</a><td>
          <tbody>
      },
          (join '/', @$path),
          (join '/', @$path);
      $html .= join '', map {
        my $v = $_->basename;
        my $mime = get_mime_type $defs, $v;
        my $x = sprintf q{<tr><th><a href="%s"><code>%s</code></a><td>}, $v, $v;
        if (defined $mime) {
          $mime =~ s/&/&amp;/g;
          $mime =~ s/</&lt;/g;
          $x .= qq{<code>$mime</code>};
        }
        $x;
      } sort { $a cmp $b } $file_path->children (qr/\A[0-9A-Za-z][0-9A-Za-z_.-]*\z/);
      $html .= sprintf q{
        </table>
        <footer>
          <a href="https://github.com/wakaba/tests-web/tree/master/%s">GitHub</a>
        </footer>
      }, join '/', @$path;
      return $app->send_html ($html);
    } else { # file
      return $app->send_redirect ($path->[-1] . '/')
          if $file_path->is_dir;
      return $app->throw_error (404, reason_phrase => 'File not found')
          unless $file_path->is_file;

      my $name = pop @$path;
      if ($name =~ /\.cgi\z/) {
        return run_cgi ($app, $file_path);
      } else {
        my $defs = load_defs $path;
        my $mime = get_mime_type $defs, $name;
        return send_file ($app, $file_path, $mime);
      }
    }
  });
};

=head1 LICENSE

Copyright 2015 Wakaba <wakaba@suikawiki.org>.

This library is free software; you can redistribute it and/or modify
it under the same terms as Perl itself.

=cut
