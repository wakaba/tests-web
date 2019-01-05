use strict;
use warnings;
use MIME::Base64;
use JSON::PS;

my $Data = [];

sub d ($$) {
  push @$Data, [$_[0], [map { ord $_ } split //, $_[1]]];
} # d

my $Bytes = [0..255];

my $base64url = (shift // '') eq 'base64url';

d '' => '';
for (@$Bytes) {
  my $b1 = pack 'C', $_;
  my $bytes = join '', $b1;
  my $encoded = encode_base64 $bytes, '';
  $encoded =~ tr{+/=}{-_}d if $base64url;
  d $encoded => $bytes;
}
for (@$Bytes) {
  my $b1 = pack 'C', $_;
  for (@$Bytes) {
    my $b2 = pack 'C', $_;
    my $bytes = join '', $b1, $b2;
    my $encoded = encode_base64 $bytes, '';
    $encoded =~ tr{+/=}{-_}d if $base64url;
    d $encoded => $bytes;
  }
}

srand 1;
for my $length (3, 4, 5, 100, 255, 256, 1024, 1025, 4096, 4097) {
  my $bytes = '';
  $bytes .= $Bytes->[rand @$Bytes] for 0..$length;
  my $encoded = encode_base64 $bytes, '';
  $encoded =~ tr{+/=}{-_}d if $base64url;
  d $encoded => $bytes;
}

print perl2json_bytes_for_record $Data;

## License: Public Domain.
