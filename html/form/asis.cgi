#!/usr/bin/perl

use strict;
binmode STDOUT;

print <<EOH;
Content-Type: text/plain; charset=iso-8859-1

query:
___
$ENV{QUERY_STRING}
~~~

entity-body:
___
EOH

binmode STDIN;
read STDIN, my $body, $ENV{CONTENT_LENGTH};

print $body;
print "\n~~~\n";
