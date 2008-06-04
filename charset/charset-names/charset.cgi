#!/usr/bin/perl
use strict;

my $name = $ENV{PATH_INFO};
$name =~ s!^/!!;
$name =~ s/%([0-9A-Fa-f]{2})/pack 'C', hex $1/ge;
$name =~ s/[\x00-\x1F]/ /g;

my $name_c = $name;
$name_c =~ s/[\\";\x20\x7F-\xFF]//g;

print "Content-Type: text/html; charset=$name_c

";


my $s = q[<!DOCTYPE HTML>
<script charset=utf-8 src="../../../support/result0.js"></script>
<script charset=utf-8 src="../../../support/result.js"></script>

<h1>Before <code>onload</code></h1>
<noscript>FAIL (noscript)</noscript>
<script>
  document.write ('<p><code>document.charset</code>: ');
  writeResult (document.charset);

  document.write ('<p><code>document.characterSet</code>: ');
  writeResult (document.characterSet);

  document.write ('<p><code>document.inputEncoding</code>: ');
  writeResult (document.inputEncoding);

  document.write ('<hr>');

  document.write ('<p><code>document.defaultCharset</code>: ');
  writeResult (document.defaultCharset);

  document.write ('<p><code>document.xmlEncoding</code>: ');
  writeResult (document.xmlEncoding);

window.onload = function () {
  setResult ('result-charset', document.charset);
  setResult ('result-characterSet', document.characterSet);
  setResult ('result-inputEncoding', document.inputEncoding);
  setResult ('result-defaultCharset', document.defaultCharset);
  setResult ('result-xmlEncoding', document.xmlEncoding);
};
</script>

<h1>After <code>onload</code></h1>

<p><code>document.charset</code>: <span id=result-charset></span>
<p><code>document.characterSet</code>: <span id=result-characterSet></span>
<p><code>document.inputEncoding</code>: <span id=result-inputEncoding></span>
<hr>
<p><code>document.defaultCharset</code>: <span id=result-defaultCharset></span>
<p><code>document.xmlEncoding</code>: <span id=result-xmlEncoding></span>
];


print $s;
