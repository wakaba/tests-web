#!/usr/bin/perl
use strict;
use warnings;

sub l ($) { my $s = $_[0]; $s =~ s/\x0A/\x0D\x0A/g; $s }

print l q{Content-Type: multipart/related

Content-Type: multipart/related; boundary=a; start="<x@test>"; type="text/html"

--a
Content-Type: text/html
Content-ID: <x@test>

<p>HTML document
--a--
};
