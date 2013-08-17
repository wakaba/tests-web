#!/usr/bin/perl
use strict;
use warnings;

$| = 1;

print "Cache-Control: no-cache\n";
print "Content-Type: text/css; charset=utf-8\n\n";

print ".hoge { color: blue }";

sleep 2;

print ".hoge { color: green }";
