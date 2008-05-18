#!/usr/bin/perl
use strict;

print qq[Content-Type: text/html; charset=utf-8\n\n];
print qq[<!DOCTYPE HTML>];
print qq[<p>U-01000401: ];
print qq[<span>\xf9\x80\x80\x90\x81</span>];
print q[
  <p id=result class=FAIL>FAIL (noscript)</p>
  <script>
    var r = document.getElementById ('result');
    r.firstChild.data = 'FAIL (script)';
    var s = document.getElementsByTagName ('span')[0];
    if (s.firstChild.data.match (/^\uFFFD{1,5}$/)) {
      r.firstChild.data = 'PASS';
      r.className = 'PASS';
    } else {
      r.firstChild.data = 'FAIL';
    }
  </script>
  <p>NOTE: IANA definition for <code>UTF-8</code> references RFC 3629,
  which in turn normatively references the Unicode Standard.  They don't
  allow characters greater than U+10FFFF.
];
