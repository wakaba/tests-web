#!/usr/bin/perl

$| = 1;
print "Content-Type: application/x-dom-event-stream\n\n";

for my $i (1..100) {
  print "Event: test-event-1
data: test-data-$i

";
  sleep 1;
}
