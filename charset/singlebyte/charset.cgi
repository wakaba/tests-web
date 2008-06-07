#!/usr/bin/perl
use strict;

my $name = $ENV{PATH_INFO};
$name =~ s!^/!!;
$name =~ s/%([0-9A-Fa-f]{2})/pack 'C', hex $1/ge;
$name =~ s/[\x00-\x1F]/ /g;

my $name_c = $name;
$name_c =~ s/[\\";\x20\x7F-\xFF]//g;

my $type = $ENV{QUERY_STRING} =~ /;plain\b/ ? 'plain' : 'html';

print "Content-Type: text/$type;  charset=$name_c

";

my $v = 0;
if ($ENV{QUERY_STRING} =~ /^(\d+)/) {
  $v = 0+$1;
}

print pack 'C', $v;
