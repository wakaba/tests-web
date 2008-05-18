#!/usr/bin/perl
use strict;

print qq[Content-Type: text/html; charset=utf-8\n\n];
print qq[\xEF\xBB\xBFXXXXXX];
print q[
  <p id=result class=FAIL>FAIL (noscript)</p>
  <script>
    var r = document.getElementById ('result');
    r.firstChild.data = 'FAIL (script)';
    if (document.body.firstChild.data.match (/^XXXXXX/)) {
      r.firstChild.data = 'PASS';
      r.className = 'PASS';
    } else {
      r.firstChild.data = 'FAIL';
    }
  </script>
];
