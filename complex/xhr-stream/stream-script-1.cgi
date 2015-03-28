#!/usr/bin/perl
use strict;
use warnings;

$| = 1;

print q{Content-Type: text/plain; charset=utf-8
Cache-Control: no-cache

1
};
print q{ } x 2048;
print "\n";

for (2..5) {
  sleep 1;
  print "$_\n";
}
