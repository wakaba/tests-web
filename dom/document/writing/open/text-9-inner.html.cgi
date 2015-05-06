#!/usr/bin/perl
use strict;
use warnings;

print q{Content-Type: text/html; charset=utf-8
Cache-Control: no-cache

<!DOCTYPE HTML>
<title>inner</title>

<p>Inner

<script>
  document.write (Math.random ());
</script>
};