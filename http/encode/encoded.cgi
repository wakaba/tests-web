#!/usr/bin/perl

use strict;
my $self = q(/~wakaba/-temp/test/http/encode/encoded.cgi);
my $mode = $main::ENV{PATH_INFO};

my $src_hdr = <<EOH;
Content-Type: text/html
EOH
my $src = <<EOH;
<!DOCTYPE html SYSTEM>
<html>
<p>Test (@{[escape($mode)]}) success!</p>
<dl>
    <dt>Your Accept CE:</dt><dd>@{[escape($ENV{HTTP_ACCEPT_ENCODING})]}</dd>
    <dt>Your Accept TE:</dt><dd>@{[escape($ENV{HTTP_TE})]}</dd>
</dl>
<ul>
        <li><a href="$self/-/identity/">identity</a></li>
        <li><a href="$self/content/gzip/">ce:gzip</a></li>
        <li><a href="$self/transfer/gzip/">te:gzip</a></li>
    <li><a href="$self/content/x-gzip/">ce:x-gzip</a></li>
        <li><a href="$self/transfer/x-gzip/">te:x-gzip</a></li>

    <li><a href="$self/content/deflate/">ce:deflate</a></li>
        <li><a href="$self/transfer/deflate/">te:deflate</a></li>
    <li><a href="$self/content/x-deflate/">ce:x-deflate</a></li>
        <li><a href="$self/transfer/x-deflate/">te:x-deflate</a></li>

     <li><a href="$self/content/compress/">ce:compress</a></li>
        <li><a href="$self/transfer/compress/">te:compress</a></li>
    <li><a href="$self/content/x-compress/">ce:x-compress</a></li>
        <li><a href="$self/transfer/x-compress/">te:x-compress</a></li>

    <li><a href="$self/content/bzip/">ce:bzip</a></li>
        <li><a href="$self/transfer/bzip/">te:bzip</a></li>
    <li><a href="$self/content/x-bzip/">ce:x-bzip</a></li>
        <li><a href="$self/transfer/x-bzip/">te:x-bzip</a></li>
    <li><a href="$self/content/bzip2/">ce:bzip2</a></li>
        <li><a href="$self/transfer/bzip2/">te:bzip2</a></li>
    <li><a href="$self/content/x-bzip2/">ce:x-bzip2</a></li>
        <li><a href="$self/transfer/x-bzip2/">te:x-bzip2</a></li>

    <li><a href="$self/transfer/gzip-deflate/">te:gzip,deflate</a></li>
    <li><a href="$self/transfer/gzip-chunked/">te:gzip,chunked</a></li>
    <li><a href="$self/transfer/chunked-gzip/">te:chunked,gzip</a></li>
    <li><a href="$self/transfer/chunked-gzip-chunked/">te:chunked,gzip,chunked</a></li>
    <li><a href="$self/transfer/chunked-chunked/">te:chunked,chunked</a></li>

      <li><a href="$self/transfer/chunked/">te:chunked:crlf</a></li>
    <li><a href="$self/transfer/chunked/cr/">te:chunked:cr</a></li>
    <li><a href="$self/transfer/chunked/lf/">te:chunked:lf</a></li>
    <li><a href="$self/transfer/chunked/param/">te:chunked;param</a></li>
    <li><a href="$self/transfer/chunked/trailer/">te:chunked,trailer</a></li>

    <li><a href="$self/content/x-unknown/">ce:x-unknown</a></li>
        <li><a href="$self/transfer/x-unknown/">te:x-unknown</a></li>

</ul>
</html>
EOH

sub escape ($) {
    my $s  = shift;
    $s =~ s/&/&amp;/ge;
    $s =~ s/</&lt;/ge;
    $s =~ s/>/&gt;/ge;
    $s =~ s/"/&quot;/ge;
  $s;
}

if ($mode =~ /gzip-deflate/) {
  require Compress::Zlib;
  $src = Compress::Zlib::compress(Compress::Zlib::memGzip ($src));
  print $src_hdr;
    print qq(Transfer-Encoding: gzip,deflate\n);
  print "\n";
  print $src;
} elsif ($mode =~ /chunked-gzip-chunked/) {
  require Compress::Zlib;
  $src = Compress::Zlib::memGzip (sprintf ('%X',length($src))."\x0D\x0A".$src."\x0D\x0A0\x0D\x0A\x0D\x0A");
  print $src_hdr;
      print qq(Transfer-Encoding: gzip,chunked\n);
    print "\n";
  print sprintf ('%X',length($src))."\x0D\x0A".$src."\x0D\x0A0\x0D\x0A\x0D\x0A";
} elsif ($mode =~ /gzip-chunked/) {
  require Compress::Zlib;
  $src = Compress::Zlib::memGzip ($src);
  print $src_hdr;
      print qq(Transfer-Encoding: gzip,chunked\n);
    print "\n";
  print sprintf ('%X',length($src))."\x0D\x0A".$src."\x0D\x0A0\x0D\x0A\x0D\x0A";
} elsif ($mode =~ /gzip-chunked/) {
  require Compress::Zlib;
  $src = Compress::Zlib::memGzip (sprintf ('%X',length($src))."\x0D\x0A".$src."\x0D\x0A0\x0D\x0A\x0D\x0A");
  print $src_hdr;
      print qq(Transfer-Encoding: gzip,chunked\n);
    print "\n";
  print $src;
} elsif ($mode =~ /gzip/) {
  require Compress::Zlib;
  $src = Compress::Zlib::memGzip ($src);
  print $src_hdr;
  my $e = 'gzip';
  $e = 'x-gzip' if $mode =~ /x-gzip/;
  if ($mode !~ /transfer/) {
    print qq(Content-Encoding: $e\n);
  } else {
    print qq(Transfer-Encoding: $e\n);
  }
  print "\n";
  print $src;
} elsif ($mode =~ /deflate/) {
  require Compress::Zlib;
  $src = Compress::Zlib::compress ($src);
  print $src_hdr;
  my $e = 'deflate';
  $e = 'x-deflate' if $mode =~ /x-deflate/;
  if ($mode !~ /transfer/) {
    print qq(Content-Encoding: $e\n);
  } else {
    print qq(Transfer-Encoding: $e\n);
  }
  print "\n";
  print $src;
} elsif ($mode =~ /bzip/) {
  print $src_hdr;
  my $e = 'bzip';
  $e .= '2' if $mode =~ /bzip2/;
  $e = 'x-'.$e if $mode =~ /x-bzip/;
  if ($mode !~ /transfer/) {
    print qq(Content-Encoding: $e\n);
  } else {
    print qq(Transfer-Encoding: $e\n);
  }
  print "\n";
  open BZ, "| bzip2";
    print BZ $src;
    while (<>) {
      print;
    }
  close BZ;
} elsif ($mode =~ /compress/) {
  print $src_hdr;
  my $e = 'compress';
  $e = 'x-'.$e if $mode =~ /x-compress/;
  if ($mode !~ /transfer/) {
    print qq(Content-Encoding: $e\n);
  } else {
    print qq(Transfer-Encoding: $e\n);
  }
  print "\n";
  open BZ, "| compress";
    print BZ $src;
    while (<>) {
      print;
    }
  close BZ;
} elsif ($mode =~ /deflate/) {
  print $src_hdr;
  if ($mode !~ /transfer/) {
    print qq(Content-Encoding: x-unknown\n);
  } else {
    print qq(Transfer-Encoding: x-unknown\n);
  }
  print "\n";
  print $src;
} elsif ($mode =~ /chunked-chunked/) {
  print $src_hdr;
  print qq(Transfer-Encoding: chunked,chunked

);
  $src = sprintf ('%X',length($src))."\x0D\x0A".$src."\x0D\x0A0\x0D\x0A\x0D\x0A";
  print sprintf ('%X',length($src))."\x0D\x0A".$src."\x0D\x0A0\x0D\x0A\x0D\x0A";
} elsif ($mode =~ /chunked/) {
  print $src_hdr;
  my $nl = $mode =~ m!/cr/! ? "\x0D" : $mode =~ m!/lf/! ? "\x0A" : "\x0D\x0A";
  my $param = "";
  $param  = "; x-param".$nl if $mode =~ m!/param/!;
  print qq(Transfer-Encoding: chunked

@{[sprintf '%X', length($src)]}).$nl.$param;
  print $src.$nl;
  print q(0).$nl.$param;
  print "Some-Header: test".$nl if $mode =~ /trailer/;
  print $nl;
} else {        # identity
  print $src_hdr;
  print "\n";
  print $src;            
}
