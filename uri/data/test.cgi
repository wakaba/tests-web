#!/usr/bin/perl
use strict;

my $file_name = 'data-uris.txt';

my @item;
{
  open my $file, '<', $file_name;
  local $/ = undef;
  @item = split /\n\n#/, <$file>;
}

sub htescape ($) {
  my $s = shift;
  $s =~ s/&/&amp;/g;
  $s =~ s/</&lt;/g;
  $s =~ s/"/&quot;/g;
  return $s;
} # htescape

sub get_id ($) {
  my $s = shift;
  $s =~ s/([^0-9A-Za-z-])/sprintf '_%08X', ord $1/ge;
  return $s;
} # get_id

print qq[Content-Type: text/html; charset=utf-8

<!DOCTYPE HTML>
<html lang=en>
<title>data: URIs</title>
<style>
.note {

}
.item {
  margin: 1em;
  padding: 0.2em 0.7em;
  background-color: #F0F8FC;
  color: black;
}
</style>];

for (@item) {
  s/^#//;
  my %prop;
  for (split /\n#/, $_) {
    if (s/^(data|note|conforming|non-conforming)(?>\n|\z)//s) {
      $prop{$1} = $_;
    }
  }

  my $id = htescape (get_id ($prop{data}));
  my $euri = htescape ($prop{data});
  print qq[<div class=item id=$id><p>URI: &lt;<a href="$euri">$euri</a>&gt;];
  for (qw/note conforming non-conforming/) {
    next unless defined $prop{$_};
    print qq[<p>];
    print qq[<strong>Conforming</strong>: ] if $_ eq 'conforming';
    print qq[<strong>Non-conforming</strong>: ] if $_ eq 'non-conforming';
    my $v = htescape ($prop{$_});
    $v =~ s[&lt;([^>]+)>][&lt;<a href="$1">$1</a>&gt;]g;
    print qq[<span class=note>] . $v . qq[</span>];
  }
  print qq[</div>];
}
