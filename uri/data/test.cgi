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

print q[Content-Type: text/html; charset=utf-8

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
[irrelevant] {
  display: none;
}
</style>
<script>
  window.onload = function () {
    var anchors = document.getElementsByTagName ('a');
    var anchorsL = anchors.length;
    for (var i = 0; i < anchorsL; i++) {
      var anchor = anchors[i];
      if (!anchor.hasAttribute ('href')) {
        anchor.setAttribute ('href', '#tag=' + encodeURIComponent (anchor.textContent));
        anchor.onclick = function () {
          showTag (this.textContent);
        };
      }
    }

    var uri = location.href;
    if (uri.match (/#/)) {
      var hash = uri.substring (uri.indexOf ('#'));
      if (hash.match (/^#tag=/)) {
        showTag (decodeURIComponent (hash.substring (5)));
      }
    }
  }; // window.onload

  function showTag (tag) {
    var items = document.getElementsByTagName ('div');
    var itemsL = items.length;
    I: for (var i = 0; i < itemsL; i++) {
      var item = items[i];
      if (tag == '') {
        item.removeAttribute ('irrelevant');
      } else {
        var itemAs = item.getElementsByTagName ('a');
        var itemAsL = itemAs.length;
        for (var j = 0; j < itemAsL; j++) {
          if (itemAs[j].textContent == tag) {
            item.removeAttribute ('irrelevant');
            continue I;
          }
        }
        item.setAttribute ('irrelevant', '');
      }
    }
  }
</script><p><a href="#" onclick="showTag ('')">Show all</a></p>];

for (@item) {
  s/^#//;
  my %prop;
  for (split /\n#/, $_) {
    if (s/^([0-9A-Za-z-]+)(?>\n|\z)//s) {
      $prop{$1} = $_;
    }
  }

  my $id = htescape (get_id ($prop{data}));
  my $euri = htescape ($prop{data});
  print qq[<div class=item id=$id><p>URI: &lt;<a href="$euri">$euri</a>&gt;];
  for (qw/note conforming non-conforming source/) {
    next unless defined $prop{$_};
    print qq[<p>];
    print qq[<strong>Conforming</strong>: ] if $_ eq 'conforming';
    print qq[<strong>Non-conforming</strong>: ] if $_ eq 'non-conforming';
    print qq[Source: ] if $_ eq 'source';
    my $v = htescape ($prop{$_});
    $v =~ s[&lt;([^>]+)>][&lt;<a href="$1">$1</a>&gt;]g;
    print qq[<span class=note>] . $v . qq[</span>];
  }

  if (defined $prop{tag}) {
    my @tag = split /\n/, $prop{tag};
    print q[<p class=tags>Tags: ];
    print join ', ', map {'<a>' . htescape ($_) . '</a>'} @tag;
  }
  print qq[</div>];
}
