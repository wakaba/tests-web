#!/usr/bin/perl
use strict;

my $query = $ENV{QUERY_STRING};

print "Content-Type: text/css; charset=us-ascii\n\n";

print q[p { background-color: white; color: white }];

sub pd ($) {
  my $s = shift;
  $s =~ s/%([0-9A-Fa-f]{2})/pack 'C', hex $1/ge;
  return $s;
}

if ($query =~ /%/) {
  print q[#is-percent-encoded { color: black }];
  $query = pd $query;
}

if ($query eq pd '%E3%81%82%E3%81%84%E3%81%86%E3%81%88%E3%81%8A') {
  print q[#is-utf-8 { color: black }];
} elsif ($query eq pd '%82%A0%82%A2%82%A4%82%A6%82%A8') {
  print q[#is-shift-jis { color: black }];
} elsif ($query eq pd '%A4%A2%A4%A4%A4%A6%A4%A8%A4%AA') {
  print q[#is-euc-jp { color: black }];
} elsif ($query eq pd '%1B$B$%22$$$&$($*%1B(B') {
  print q[#is-iso-2022-jp { color: black }];
} else {
  print q[#unknown { color: black }];
}
