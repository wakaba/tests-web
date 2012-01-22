#!/usr/bin/perl

if ($ENV{AUTH_TYPE} || $ENV{HTTP_AUTHORIZATION}) {
  print "Content-Type: text/plain; charset=us-ascii

AUTH_TYPE : $ENV{AUTH_TYPE}
HTTP_AUTHORIZATION : $ENV{HTTP_AUTHORIZATION}
REMOTE_USER : $ENV{REMOTE_USER}
";
} else {
  print qq(Status: 401 Unauthorized
Content-Type: text/plain; charset=us-ascii
WWW-Authenticate: basic realm="foo"

AUTH_TYPE : $ENV{AUTH_TYPE}
HTTP_AUTHORIZATION : $ENV{HTTP_AUTHORIZATION}
REMOTE_USER : $ENV{REMOTE_USER}
401);
}
