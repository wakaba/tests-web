use strict;
use warnings;
use MIME::Base64;
use JSON::PS;

my $Data = [];

sub e ($$) {
  push @$Data, [[map { ord $_ } split //, $_[0]], $_[1]];
} # e

my $Bytes = [0..255];

e '' => '';
for (@$Bytes) {
  my $b1 = pack 'C', $_;
  my $bytes = join '', $b1;
  my $encoded = encode_base64 $bytes, '';
  e $bytes => $encoded;
}
for (@$Bytes) {
  my $b1 = pack 'C', $_;
  for (@$Bytes) {
    my $b2 = pack 'C', $_;
    my $bytes = join '', $b1, $b2;
    my $encoded = encode_base64 $bytes, '';
    e $bytes => $encoded;
  }
}

srand 1;
for my $length (100, 255, 256, 1024, 1025, 4096, 4097) {
  my $bytes = '';
  $bytes .= $Bytes->[rand @$Bytes] for 0..$length;
  my $encoded = encode_base64 $bytes, '';
  e $bytes => $encoded;
}

print perl2json_bytes_for_record $Data;

## License: Public Domain.
