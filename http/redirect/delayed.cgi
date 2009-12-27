#!/usr/bin/perl
use strict;
use warnings;

print "Location: http://$ENV{SERVER_NAME}:$ENV{SERVER_PORT}$ENV{SCRIPT_NAME}/../redirected.ja.html\nContent-Type: text/plain; charset=us-ascii\n\n";

for my $i (1..100) {
  print "$i\n";
}
