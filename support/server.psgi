# -*- perl -*-
use strict;
use warnings;
use Encode;
use Time::HiRes qw(time);
use Digest::SHA qw(sha1_hex);
use Path::Tiny;
use JSON::PS;
use Wanage::URL;
use Wanage::HTTP;
use Warabe::App;
use Promised::Command;

$ENV{LANG} = 'C';
$ENV{TZ} = 'UTC';
$Wanage::HTTP::UseXForwardedScheme = 1 if $ENV{USE_XFF};

my $RootPath = path (__FILE__)->parent->parent->absolute;

sub send_file ($$$$) {
  my ($app, $file, $mime, $filter) = @_;
  return $app->throw_error (404) unless $file->is_file;
  return $app->throw_error (500, reason_phrase => "Unknown filter |$filter|")
      if defined $filter and not {expand => 1}->{$filter};
  $app->http->set_response_header ('Content-Type' => $mime) if defined $mime;
  if (defined $filter and $filter eq 'expand') {
    my $body = $file->slurp;
    my $rand = {};
    $body =~ s{\@\@HEADER:([^:\s]+):\s*([^\x0D\x0A]*?)\@\@[\x0D\x0A]*}{
      $app->http->set_response_header ($1, $2);
      '';
    }ge;
    $body =~ s/\@\@RAND\(([A-Za-z0-9_-]+)\)\@\@/$rand->{$1} ||= int rand 10000000/ge;
    $body =~ s{\@\@BYTES:(.*?)\@\@}{
      my $v = $1;
      $v =~ s/\\x([0-9A-Fa-f]{2})/pack 'C', hex $1/ge;
      $v;
    }ge;
    $app->http->send_response_body_as_ref (\$body);
  } else {
    $app->http->set_response_last_modified ($file->stat->mtime);
    $app->http->send_response_body_as_ref (\($file->slurp));
  }
  return $app->http->close_response_body;
} # send_file

sub get_mime_type ($$) {
  my ($defs, $name) = @_;
  my $mime = undef;
  my $charset = undef;
  my $filter = undef;
  if ($name =~ /\.([^.]+)\z/ and $defs->{filter}->{$1}) {
    $filter = $defs->{filter}->{$1};
    $name =~ s/\.[^.]+\z//;
  }
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
  return ($mime, $filter);
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
    } elsif (s{^\s*RemoveCharset\s+}{}) {
      delete $defs->{charset}->{$_} for map { my $x = $_; $x =~ s/^\.//; $x } split /\s+/, $_;
    } elsif (s{^\s*AddFilter\s+(\S+)\s+}{}) {
      my $filter = $1;
      $defs->{filter}->{$_} = $filter for map { my $x = $_; $x =~ s/^\.//; $x } split /\s+/, $_;
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

my $HTTPLogRootPath = path (__FILE__)->parent->parent->child ('local/httplog');

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

    if (@$path == 3 and $path->[0] eq 'httplog') {
      my $key = sha1_hex encode 'utf-8', $path->[1];
      my $log_path = $HTTPLogRootPath->child ($key . '.log');
      if ($path->[2] eq 'ndjson' or $path->[2] eq 'ndjson.txt') {
        # /httplog/{id}/ndjson
        # /httplog/{id}/ndjson.txt
        if ($path->[2] eq 'ndjson.txt') {
          $app->http->set_response_header
              ('Content-Type' => 'text/plain; charset=utf-8');
        } else {
          $app->http->set_response_header
              ('Content-Type' => 'application/x-ndjson');
        }
        if ($log_path->is_file) {
          $app->http->send_response_body_as_ref (\($log_path->slurp));
        }
        return $app->http->close_response_body;
      } elsif ($path->[2] eq 'logging') {
        # /httplog/{id}/logging
        my $http = $app->http;
        my $data = {time => time,
                    client_ip_addr => $http->client_ip_addr->as_text,
                    method => $http->request_method,
                    url => $http->original_url->stringify,
                    #headers => [], # XXX
                    body => ${$http->request_body_as_ref // \undef}};
        $log_path->parent->mkpath;
        $log_path->append (perl2json_bytes $data);
        return $app->throw_error (204, reason_phrase => 'OK');
      }
    }

    my $file_path = @$path ? $RootPath->child (join '/', @$path) : $RootPath;
    if ($is_dir) {
      return $app->throw_error (404, reason_phrase => 'Directory not found')
          unless $file_path->is_dir;

      my $defs = load_defs $path;
      my $html = sprintf q{
        <!DOCTYPE HTML>
        <head>
        <link rel=stylesheet href=/support/directory.css>
        <meta name=viewport content="width=device-width">
        <meta name="google-site-verification" content="0eAhmbMnDYcNF9NNcvcBRmWj87LYwqcQWJ_4ovaMGKs" />
        <title>tests-web/%s</title><h1>tests-web/%s</h1>
        <nav class=protocol>
          <a href="javascript:location.href=location.href.replace(/^https:/, 'http:')">HTTP</a>
          <a href="javascript:location.href=location.href.replace(/^http:/, 'https:')">HTTPS</a>
        </nav>
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
        my ($mime, $filter) = get_mime_type $defs, $v;
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
        my ($mime, $filter) = get_mime_type $defs, $name;
        return send_file ($app, $file_path, $mime, $filter);
      }
    }
  });
};

=head1 LICENSE

Copyright 2015-2016 Wakaba <wakaba@suikawiki.org>.

This library is free software; you can redistribute it and/or modify
it under the same terms as Perl itself.

=cut
