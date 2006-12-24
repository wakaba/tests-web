#!/usr/bin/perl 

print <<'EOH';
Content-Type: text/html; charset=us-ascii

<!DOCTYPE html>
<html>
<head>
<title>document.lastModified</title>
</head>
<body>
<h1><code>document.lastModified</code></h1>

<p>This document has no <code>Last-Modified:</code>
HTTP header field.</p>

<p><code>document.lastModified == '<script type="text/javascript">
  var s = document.lastModified;
  s = s.replace (/&/, '&amp;');
  s = s.replace (/</, '&lt;');
  document.write (s);
</script>'</code></p>

</body>
</html>
EOH
