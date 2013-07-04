#!/usr/bin/perl
use strict;
#use warnings;

my $key = '';
my $value = '';
if ($ENV{QUERY_STRING} =~ /^([0-9A-Za-z]+)=([0-9A-Za-z]*)$/) {
  $key = $1;
  $value = $2;
}

print "Content-Type: text/plain; charset=utf-8\n";
print "Set-Cookie: test-logger-$key=$value\n";
print "\n";
