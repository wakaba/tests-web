#!/usr/bin/perl
use strict;
use warnings;

print q{Content-Type: text/html
Content-Security-Policy: sandbox

<!DOCTYPE HTML>
<title>iframe content</title>

<p id=noscript>Script is not (yet?) executed.

<script>
  var pNoScript = document.getElementById ('noscript');
  pNoScript.parentNode.removeChild (pNoScript);
  document.write ('<p>Script is executed!');
</script>

<noscript>
  <p>Scripting is disabled at the time of parsing. <!--
</noscript>

<p>Scripting is enabled at the time of parsing.
};