#!/usr/bin/perl 
use strict;

require 'mixed-replace-generation.pl';

$| = 1;

my $mr = mixed_replace_generation->new;

$mr->output_cgi_header;

for my $i (1..10) {
  $mr->output_boundary;

  $mr->output_line ('Content-Type: text/html; charset=us-ascii');

  $mr->output_line ('');

  $mr->output_line ('<script src="../../../support/result0.js"></script>');
  $mr->output_line ('<p>Part ' . $i . '/10</p>');
  $mr->output_line ('<p><code>location.href</code> is <script type="text/javascript">writeResult (location.href)</script>.</p>');
  $mr->output_line ('<p><a id="a">view-source:<var>this</var></a></p>');
  $mr->output_line ('<script>document.getElementById ("a").href = "view-source:" + location.href</script>');

  sleep 1;
}

$mr->output_last_boundary;
