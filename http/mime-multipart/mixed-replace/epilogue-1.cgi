#!/usr/bin/perl 
use strict;

require 'mixed-replace-generation.pl';

$| = 1;

my $mr = mixed_replace_generation->new;

$mr->output_cgi_header;

$mr->output_boundary;
$mr->output_line ('Content-Type: text/plain; charset=us-ascii');
$mr->output_line ('');
$mr->output_line ('first part');

$mr->output_last_boundary;

$mr->output_line ('epilogue');
