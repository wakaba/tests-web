#!/usr/bin/perl
use strict;

sub escape ($) {
  my $s = shift;
  $s =~ s/([^\x20-\x5B\x5D-\x7E])/sprintf '\x%02X', ord $1/ge;
  return $s;
} # escape

print "Content-Type: text/plain; charset=us-ascii\n\n";

print "Request-Method: {", escape ($ENV{REQUEST_METHOD}), "}\n\n";

print "Request-URI: {", escape ($ENV{REQUEST_URI}), "}\n\n";

print "HTTP header fields:\n";
for (sort {$a cmp $b} ('CONTENT_TYPE', grep /^HTTP_/, keys %ENV)) {
  print "{", escape ($_), "}: {", escape ($ENV{$_}), "}\n";
}
print "\n";

print "Request-body:\n";
if (defined $ENV{CONTENT_LENGTH}) {
  my $size = $ENV{CONTENT_LENGTH};
  $size = 10 * 1024 if $size > 10 * 1024;
  read STDIN, my $bytes, $size;
  $bytes = escape ($bytes);
  $bytes =~ s/\\x0A/\\x0A\n/g;
  print "[", $bytes, ($size == 10 * 1024 ? "..." : "}"), "\n";
}
print "\n";
