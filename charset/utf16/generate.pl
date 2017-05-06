use strict;
use warnings;
use Path::Tiny;

my $dir_path = path (__FILE__)->parent;

$dir_path->child ('demo-1.html')->spew (qq{<?xml version="1.0" encoding="utf-16be"?>
ABCDEFG});

## License: Public Domain.
