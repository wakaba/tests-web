#!/usr/bin/perl 
use strict;

require 'mixed-replace-generation.pl';

$| = 1;

my $mr = mixed_replace_generation->new;

$mr->output_cgi_header;

for my $i (1..10) {
  $mr->output_boundary;

  $mr->output_line ('Content-Type: text/plain; charset=us-ascii');

  $mr->output_line ('');

  $mr->output_line ('Part ' . $i . '/10');

  sleep 1;
}

$mr->output_last_boundary;
