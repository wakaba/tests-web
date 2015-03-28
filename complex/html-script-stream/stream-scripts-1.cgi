#!/usr/bin/perl
use strict;
use warnings;

$| = 1;

sleep 1;

print q{Content-Type: text/html; charset=utf-8

<script>
  function j (m) {
    parent.postMessage (m, location.protocol + '//' + location.host);
  }
</script>
};

print q{<script>
  j (1);
</script>} . (' ' x 128);

sleep 1;

print q{<script>
  j (2);
</script>} . (' ' x 128);

sleep 1;

print q{<script>
  j (3);
</script>};