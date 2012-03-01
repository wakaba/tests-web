#!/usr/bin/perl
print "Content-Type: text/plain; charset=utf-8\n";
print "Access-Control-Allow-Origin: *\n";
print "\n";
print $ENV{HTTP_ORIGIN};
