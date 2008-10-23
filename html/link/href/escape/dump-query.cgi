#!/usr/bin/perl
use strict;

print "Content-Type: text/html; charset=iso-8859-1\n\n<title>URL query of the Request-URI</title>";

my $q = $ENV{QUERY_STRING};

if (defined $q) {
  print "<code>";
  $q =~ s/&/&amp;/g;
  $q =~ s/</&lt;/g;
  print $q;
  print "</code>";
} else {
  print "(null)";
}