use strict;
use warnings;
use Path::Tiny;

my $dir_path = path (__FILE__)->parent;

$dir_path->child ('demo-1.html.xud')->spew ("abc
\xA1\xA2\xA3");

$dir_path->child ('demo-2.html.xud')->spew ("<iframe src=demo-2-content.html></iframe>");
$dir_path->child ('demo-2-content.html')->spew ("abc
\xA1\xA2\xA3");

$dir_path->child ('demo-3.html')->spew ("<meta charset=x-user-defined>abc
\xA1\xA2\xA3");

$dir_path->child ('demo-4.html')->spew (qq{<?xml version="1.0" encoding="x-user-defined"?>abc
\xA1\xA2\xA3});

$dir_path->child ('demo-5.html')->spew (qq{
  <link rel=stylesheet href=demo-5-style.css.xud>
  <p>::after
});
$dir_path->child ('demo-5-style.css.xud')->spew (qq{
  p::after { content: "abc\xA1\xA2\xA3" }
});

$dir_path->child ('demo-6.html')->spew (qq{
  <link rel=stylesheet href=demo-6-style.css>
  <p>::after
});
$dir_path->child ('demo-6-style.css')->spew (qq{\@charset "x-user-defined";
  p::after { content: "abc\xA1\xA2\xA3" }
});

$dir_path->child ('demo-7.html.xud')->spew (qq{
  <link rel=stylesheet href=demo-7-style.css>
  <p>::after
});
$dir_path->child ('demo-7-style.css')->spew (qq{
  p::after { content: "abc\xA1\xA2\xA3" }
});

$dir_path->child ('demo-8.xml')->spew (qq{<?xml version="1.0" encoding="x-user-defined"?>
<html xmlns="http://www.w3.org/1999/xhtml"><body>
abc
\xA1\xA2\xA3
</body></html>
});

$dir_path->child ('demo-9.xml.xud')->spew (qq{
<html xmlns="http://www.w3.org/1999/xhtml"><body>
abc
\xA1\xA2\xA3
</body></html>
});

$dir_path->child ('demo-10.xml.xud')->spew (qq{<?xml version="1.0" encoding="x-user-defined"?>
<html xmlns="http://www.w3.org/1999/xhtml"><body>
abc
\xA1\xA2\xA3
</body></html>
});

## License: Public Domain.
