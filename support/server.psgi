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
  $app->http->set_response_header ('Content-Type' => $mime);
  $app->http->set_response_header
      ('X-Content-Type-Options' => 'nosniff');
  $app->http->set_response_last_modified ($file->stat->mtime);
  $app->http->send_response_body_as_ref (\($file->slurp));
  return $app->http->close_response_body;
} # send_file

return sub {
  delete $SIG{CHLD} if defined $SIG{CHLD} and not ref $SIG{CHLD}; # XXX

  my $http = Wanage::HTTP->new_from_psgi_env ($_[0]);
  my $app = Warabe::App->new_from_http ($http);

  return $app->execute_by_promise (sub {
    my $path = [@{$app->path_segments}];

    $http->set_response_header
        ('Strict-Transport-Security' => 'max-age=2592000; includeSubDomains; preload');

    my $is_dir = $path->[-1] eq '';
    pop @$path if $is_dir;

    if (grep { not m{\A[0-9A-Za-z][0-9A-Za-z_.-]*\z} } @$path) {
      return $app->throw_error (404, reason_phrase => 'Bad path');
    }

    my $file_path = @$path ? $RootPath->child (join '/', @$path) : $RootPath;
    if ($is_dir) {
      return $app->throw_error (404, reason_phrase => 'Directory not found')
          unless $file_path->is_dir;

      my $html = sprintf q{<!DOCTYPE HTML><title>%s</title><h1>%s</h1><ul><li><a href=..>..</a>},
          (join '/', @$path),
          (join '/', @$path);
      $html .= join '', map {
        my $v = $_->basename;
        sprintf q{<li><a href="%s"><code>%s</code></a>}, $v, $v;
      } sort { $a cmp $b } $file_path->children (qr/\A[0-9A-Za-z][0-9A-Za-z_.-]*\z/);
      $html .= q{</ul>};
      return $app->send_html ($html);
    } else { # file
      return $app->send_redirect ($path->[-1] . '/')
          if $file_path->is_dir;
      return $app->throw_error (404, reason_phrase => 'File not found')
          unless $file_path->is_file;
      my $mime = 'application/octet-stream';
      return send_file ($app, $RootPath->child ($path->[0]), $mime);
    }

    if (0) {
      my $cmd = Promised::Command->new ([$RootPath->child ('perl'), $RootPath->child ("$path->[0].cgi")]);
      $cmd->envs->{REQUEST_METHOD} = $app->http->request_method;
      $cmd->envs->{QUERY_STRING} = $app->http->original_url->{query};
      $cmd->envs->{CONTENT_LENGTH} = $app->http->request_body_length;
      $cmd->envs->{CONTENT_TYPE} = $app->http->get_request_header ('Content-Type');
      $cmd->envs->{HTTP_ACCEPT_LANGUAGE} = $app->http->get_request_header ('Accept-Language');
      $cmd->envs->{PATH_INFO} = join '/', '', @$path[1..$#$path];
      $cmd->stdin ($app->http->request_body_as_ref);
      my $stdout = '';
      my $out_mode = '';
      $cmd->stdout (sub {
        if ($out_mode eq 'body') {
          $app->http->send_response_body_as_ref (\($_[0]));
          return;
        }
        $stdout .= $_[0];
        while ($stdout =~ s/^([^\x0A]+)\x0A//) {
          my ($name, $value) = split /:/, $1, 2;
          $name =~ tr/A-Z/a-z/;
          if ($name eq 'status') {
            my ($code, $reason) = split /\s+/, $value, 2;
            $app->http->set_status ($code, reason_phrase => $reason);
          } else {
            $app->http->set_response_header ($name => $value);
          }
        }
        if ($stdout =~ s/^\x0A//) {
          $out_mode = 'body';
          $app->http->send_response_body_as_ref (\$stdout);
        }
      });
      return $cmd->run->then (sub {
        return $cmd->wait;
      })->then (sub {
        die $_[0] unless $_[0]->exit_code == 0;
        $app->http->close_response_body;
      });
    }

  });
};

=head1 LICENSE

Copyright 2015 Wakaba <wakaba@suikawiki.org>.

This library is free software; you can redistribute it and/or modify
it under the same terms as Perl itself.

=cut
