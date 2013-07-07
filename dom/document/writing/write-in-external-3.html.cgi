#!/usr/bin/perl
use strict;
use warnings;
$| = 1;

print q{Content-Type: text/html; charset=us-ascii

<!DOCTYPE html>
<title>document.write</title>
<style>
  #external { visibility: hidden }
  .PASS { color: green }
  .FAIL { color: red }
</style>

<p id=result class=FAIL>FAIL (noscript)</p>
<p id=loaded>External script not loaded yet</p>

<script>
  document.getElementById ('result').firstChild.data = 'FAIL (Testing...)';
</script>

<script><!--
  var el = document.createElement ('script');
  el.src = 'write-in-external-script-1.js';
  el.onload = function () {
    var loaded = document.getElementById ('loaded');
    loaded.firstChild.data = 'External script loaded';
    document.body.appendChild (loaded);
  };
  document.body.appendChild (el);
// --></script>
};

sleep 3;

print q{
<script>
  var el = document.getElementById ('external');
  var result = document.getElementById ('result');
  if (el) {
    result.firstChild.data = 'PASS';
    result.className = 'PASS';
  } else {
    result.firstChild.data = 'FAIL (not written)';
  }
</script>
};
