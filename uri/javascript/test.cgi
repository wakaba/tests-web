#!/usr/bin/perl
use strict;

my $file_name = 'javascript-uris.txt';

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
<title>javascript: URIs</title>
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
    var tags = {};
    var anchors = document.getElementsByTagName ('a');
    var anchorsL = anchors.length;
    for (var i = 0; i < anchorsL; i++) {
      var anchor = anchors[i];
      if (!anchor.hasAttribute ('href')) {
        var tagName = anchor.textContent;
        anchor.setAttribute ('href', '#tag=' + encodeURIComponent (tagName));
        anchor.onclick = function () {
          showTag (this.textContent);
        };
        tags[tagName] = true;
      }
    }

    var uri = location.href;
    if (uri.match (/#/)) {
      var hash = uri.substring (uri.indexOf ('#'));
      if (hash.match (/^#tag=/)) {
        showTag (decodeURIComponent (hash.substring (5)));
      }
    }

    var tagsEl = document.getElementById ('tags');
    var tagList = [];
    for (var v in tags) {
      tagList.push (v);
    }
    tagList = tagList.sort ();
    for (var i = 0; i < tagList.length; i++) {
      tagsEl.appendChild (document.createTextNode (', '));
      var a = tagsEl.appendChild (document.createElement ('a'));
      a.href = '#tag=' + encodeURIComponent (tagList[i]);
      a.textContent = tagList[i];
      a.onclick = function () {
        showTag (this.textContent);
      };
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
</script><p id=tags>Tags: <a href="#" onclick="showTag ('')">All</a></p>];

for (@item) {
  s/^#//;
  my %prop;
  for (split /\n#/, $_) {
    if (s/^([0-9A-Za-z-]+)(?>\n|\z)//s) {
      $prop{$1} = $_;
    } elsif (s/^([0-9A-Za-z-]+)\s+escaped(?>\n|\z)//s) {
      my $t = $1;
      s/&#x([0-9A-Fa-f]+);/chr hex $1/ge;
      $prop{$t} = $_;
    }
  }

  my $id = htescape (get_id ($prop{data}));
  my $euri = htescape ($prop{data});
  print qq[<div class=item id=$id><p>URI: &lt;<a href="$euri">$euri</a>&gt;];
  for (qw/note conforming non-conforming source/) {
    next unless defined $prop{$_};
    print qq[<p>];
    print qq[<strong>Conforming <code>javascript:</code> URI</strong>: ] if $_ eq 'conforming';
    print qq[<strong>Non-conforming <code>javascript:</code> URI</strong>: ] if $_ eq 'non-conforming';
    print qq[Source: ] if $_ eq 'source';
    my $v = htescape ($prop{$_});
    $v =~ s[&lt;([^>]+)>][&lt;<a href="$1">$1</a>&gt;]g;
    print qq[<span class=note>] . $v . qq[</span>];
  }

  if (defined $prop{tags}) {
    my @tag = sort {$a cmp $b} split /\n/, $prop{tags};
    print q[<p class=tags>Tags: ];
    print join ', ', map {'<a>' . htescape ($_) . '</a>'} @tag;
  }
  print qq[</div>];
}
