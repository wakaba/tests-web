#!/usr/bin/perl 

print <<'EOH';
Content-Type: text/html; charset=us-ascii
Last-Modified: Thu, 01 Jan 1970 00:00:00 GMT

<!DOCTYPE html>
<html>
<head>
<title>document.lastModified</title>
</head>
<body>
<h1><code>document.lastModified</code></h1>

<p>This document is marked as
<code>Last-Modified: Thu, 01 Jan 1970 00:00:00 GMT</code>.</p>

<p><code>document.lastModified == '<script type="text/javascript">
  var s = document.lastModified;
  s = s.replace (/&/, '&amp;');
  s = s.replace (/</, '&lt;');
  document.write (s);
</script>'</code></p>

</body>
</html>
EOH
