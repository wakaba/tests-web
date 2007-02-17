#!/usr/bin/perl
use strict;

while (<>) {
  s/\\x([0-9A-Fa-f][0-9A-Fa-f])/pack 'C', hex $1/ge;
  print;
}
