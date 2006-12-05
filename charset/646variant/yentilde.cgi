#!/usr/bin/perl

my $charset = 'iso-2022-jp';
my %charset = qw/iso-2022-jp 1 iso-2022-jp-1 1 iso-2022-jp-2 1 iso-2022-jp-3 1
                 iso-2022-jp-2004 1
                 euc-jp 1 euc-jisx0213 1 euc-jis-2004 1
                 shift_jis 1 shift_jisx0213 1
                 shift_jis-2004 1 windows-31j 1
                 us-ascii 1 iso-8859-1 1 utf-8 1/;

my $type = 'text/html';
my %type = qw!text/html 1 application/xhtml+xml 1
              application/vnd.wap.xhtml+xml 1
              application/vnd.pwg-xhtml-print+xml 1
              application/xv+xml 1
              application/xhtml+voice+xml 1
              application/xhtml-voice+xml 1
              application/x-xhtml+voice+xml 1
              text/xml 1 application/xml 1!;

for (split /[&;]/, $ENV{QUERY_STRING}) {
  my ($name, $val) = split /=/, $_, 2;
  $val =~ s/%([0-9A-Fa-f][0-9A-Fa-f])/chr hex $1/ge;
  if ($name eq 'charset') {
    $charset = $val if $charset{$val};
  } elsif ($name eq 'type') {
    $type = $val if $type{$val};
  }
}

use Encode;

my $thead = <<EOH;
<thead>
<tr><th></th><th>lang=ja</th><th>lang=en</th><th></th><th>name</th></tr>
</thead>
EOH

sub c ($) {
 qq(<td>$_[0]</td><td lang="ja" xml:lang="ja">$_[0]</td><td lang="en" xml:lang="en">$_[0]</td>);
}

my $ua = $ENV{HTTP_USER_AGENT};
$ua =~ s/([^\x20-\x24\x27-\x3B\x3D\x3F-\x7E])/sprintf '%%%02X', ord $1/ges;

print <<EOH;
Content-Type: $type; charset=$charset

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
                      "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<title>$type; charset=$charset</title>
<meta http-equiv="content-type" content="$type; charset=$charset" />
</head>
<body>
<table>
$thead
<tbody>
<tr>@{[c(qq(\x5C))]}<td>0x5C</td><td>@{[
     ({qw/shift_jis 1 shift_jisx0213 1 shift_jis-2004 1/}->{$charset})
     ? 'YEN SIGN'
     : (({qw/windows-31j 1/}->{$charset})
     ? 'REVERSE SOLIDUS (with glyph of YEN SIGN)'
     : 'REVERSE SOLIDUS') ]}</td></tr>
@{[ ({qw/iso-2022-jp 1 iso-2022-jp-1 1 iso-2022-jp-2 1
         iso-2022-jp-3 1 iso-2022-jp-2004 1/}->{$charset} ) ?
    qq{<tr>@{[c(qq{\x1B\x28\x4A\x5C\x1B\x28\x42})]}<td>ESC 02/08 04/10 05/12</td><td>YEN SIGN</td></tr>}
    :'']}
<tr>@{[c(qq{&#x5C;})]}<td>&amp;#x5C;</td><td>REVERSE SOLIDUS</td></tr>

@{[ ($charset eq 'utf-8') ?
qq(<tr>@{[c(Encode::encode ('utf8', "\xA5"))]}<td>0xA5</td><td>YEN SIGN</td></tr>)
    :($charset eq 'iso-8859-1')
    ?qq(<tr>@{[c(qq{\xA5})]}<td>U+00A5</td><td>YEN SIGN</td></tr>)
:'']}
<tr>@{[c(qq{&#xA5;})]}<td>&amp;#xA5;</td><td>YEN SIGN</td></tr>
<tr>@{[c(qq{&yen;})]}<td>&amp;yen;</td><td>YEN SIGN</td></tr>

@{[ ({qw/shift_jis 1 shift_jisx0213 1 shift_jis-2004 1/}->{$charset})
    ?qq(<tr>@{[c(qq{\x81\x5F})]}<td>0x815F</td><td>REVERSE SOLIDUS</td></tr>)
    :($charset eq 'windows-31j')
    ?qq(<tr>@{[c(qq{\x81\x5F})]}<td>0x815F</td><td>FULLWIDTH REVERSE SOLIDUS</td></tr>)
    :($charset =~ /iso-2022-jp/)
    ?qq{<tr>@{[c(qq{\x1B\x24\x42\x21\x40\x1B\x28\x42})]}<td>ESC 02/04 04/02 02/01 04/00</td><td>REVERSE SOLIDUS</td></tr>}
    :({qw/euc-jp 1 euc-jisx0213 1 euc-jis-2004 1/}->{$charset})
    ?qq(<tr>@{[c(qq{\xA1\xC0})]}<td>0xA1C0</td><td>(REVERSE SOLIDUS) or FULLWIDTH REVERSE SOLIDUS</td></tr>)
    :'']}
@{[ ($charset eq 'iso-2022-jp' || $charset eq 'iso-2022-jp-1'
    || $charset eq 'iso-2022-jp-2')
    ?qq{<tr>@{[c(qq{\x1B\x24\x40\x21\x40\x1B\x28\x42})]}<td>ESC 02/04 04/00 02/01 04/00</td><td>REVERSE SOLIDUS</td></tr>}
    :({qw/iso-2022-jp-3 1 iso-2022-jp-2004 1/}->{$charset})
    ?qq{<tr>@{[c(qq{\x1B\x24\x28\x4F\x21\x40\x1B\x28\x42})]}<td>ESC 02/04 04/15 02/01 04/00</td><td>REVERSE SOLIDUS</td></tr>}
    :'']}
@{[ 
    ({qw/iso-2022-jp-2004 1/}->{$charset})
    ?qq{<tr>@{[c(qq{\x1B\x24\x28\x51\x21\x40\x1B\x28\x42})]}<td>ESC 02/04 05/01 02/01 04/00</td><td>REVERSE SOLIDUS</td></tr>}
    :'']}

@{[ ({qw/shift_jis 1 shift_jisx0213 1 shift_jis-2004 1/}->{$charset})
    ?qq(<tr>@{[c(qq{\x81\x8F})]}<td>0x818F</td><td>(YEN SIGN) or FULLWIDTH YEN SIGN</td></tr>)
    :($charset eq 'windows-31j')
    ?qq(<tr>@{[c(qq{\x81\x8F})]}<td>0x818F</td><td>FULLWIDTH YEN SIGN</td></tr>)
    :($charset =~ /iso-2022-jp/)
    ?qq{<tr>@{[c(qq{\x1B\x24\x42\x21\x6F\x1B\x28\x42})]}<td>ESC 02/04 04/02 02/01 06/15</td><td>YEN SIGN</td></tr>}
    :({qw/euc-jp 1 euc-jisx0213 1 euc-jp-2004 1/}->{$charset})
    ?qq(<tr>@{[c(qq{\xA1\xEF})]}<td>0xA1EF</td><td>YEN SIGN</td></tr>)
    :'']}
@{[ ($charset eq 'iso-2022-jp' || $charset eq 'iso-2022-jp-1'
    || $charset eq 'iso-2022-jp-2')
    ?qq{<tr>@{[c(qq{\x1B\x24\x40\x21\x6F\x1B\x28\x42})]}<td>ESC 02/04 04/00 02/01 06/15</td><td>YEN SIGN</td></tr>}
    :({qw/iso-2022-jp-3 1 iso-2022-jp-2004 1/}->{$charset})
    ?qq{<tr>@{[c(qq{\x1B\x24\x28\x4F\x21\x6F\x1B\x28\x42})]}<td>ESC 02/04 04/15 02/01 06/15</td><td>YEN SIGN</td></tr>}
    :'']}
@{[ 
    ({qw/iso-2022-jp-2004 1/}->{$charset})
    ?qq{<tr>@{[c(qq{\x1B\x24\x28\x51\x21\x6F\x1B\x28\x42})]}<td>ESC 02/04 05/01 02/01 06/15</td><td>YEN SIGN</td></tr>}
    :'']}
@{[ ($charset eq 'iso-2022-jp-2')
    ?qq{<tr>@{[c(qq{\x1B\x2E\x41\x1B\x4E\x25\x1B\x28\x42})]}<td>ESC 02/14 04/01 SS2 02/05</td><td>YEN SIGN</td></tr>}
    :'']}

@{[($charset eq 'utf-8')
  ?qq(<tr>@{[c(Encode::encode('utf8',"\x{FF3C}"))]}<td>U+FF3C</td><td>FULLWIDTH REVERSE SOLIDUS</td></tr>)
  :'']}
<tr>@{[c(qq{&#xFF3C;})]}<td>&amp;#xFF3C;</td><td>FULLWIDTH REVERSE SOLIDUS</td></tr>
@{[($charset eq 'utf-8')
  ?qq(<tr>@{[c(Encode::encode('utf8',"\x{FFE5}"))]}<td>U+FFE5</td><td>FULLWIDTH YEN SIGN</td></tr>)
  :'']}
<tr>@{[c(qq{&#xFFE5;})]}<td>&amp;#xFFE5;</td><td>FULLWIDTH YEN SIGN</td></tr>

</tbody>
</table>

<table>
$thead
<tbody>
<tr>@{[c(qq(\x7E))]}<td>0x7E</td><td>@{[
     ({qw/shift_jis 1 shift_jisx0213 1 shift_jis-2004 1/}->{$charset})
     ? 'OVER LINE or OVER LINE with glyph of TILDE'
     : 'TILDE' ]}</td></tr>
@{[ ($charset eq 'iso-2022-jp' || $charset eq 'iso-2022-jp-1' || $charset eq 'iso-2022-jp-2') ?
    qq{<tr>@{[c(qq{\x1B\x28\x4A\x7E\x1B\x28\x42})]}<td>ESC 02/08 04/10 07/14</td><td>OVER LINE</td></tr>}
    :'']}
<tr>@{[c(qq{&#x7E;})]}<td>&amp;#x7E;</td><td>TILDE</td></tr>
<tr>@{[c(qq{&tilde;})]}<td>&amp;tilde;</td><td>TILDE</td></tr>

@{[ ({qw/shift_jis 1 shift_jisx0213 1 shift_jis-2004 1/}->{$charset})
    ?qq(<tr>@{[c(qq{\x81\x50})]}<td>0x8150</td><td>(OVER LINE) or FULLWIDTH OVER LINE</td></tr>)
    :($charset eq 'windows-31j')
    ?qq(<tr>@{[c(qq{\x81\x50})]}<td>0x8150</td><td>FULLWIDTH OVER LINE</td></tr>)
    :($charset =~ /iso-2022-jp/)
    ?qq{<tr>@{[c(qq{\x1B\x24\x42\x21\x31\x1B\x28\x42})]}<td>ESC 02/04 04/02 02/01 03/01</td><td>OVER LINE</td></tr>}
    :({qw/euc-jp 1 euc-jisx0213 1 euc-jis-2004 1/}->{$charset})
    ?qq(<tr>@{[c(qq{\xA1\xB1})]}<td>0xA1B1</td><td>OVER LINE</td></tr>)
    :'']}
@{[ ($charset eq 'iso-2022-jp' || $charset eq 'iso-2022-jp-1'
    || $charset eq 'iso-2022-jp-2')
    ?qq{<tr>@{[c(qq{\x1B\x24\x40\x21\x31\x1B\x28\x42})]}<td>ESC 02/04 04/00 02/01 03/01</td><td>OVER LINE</td></tr>}
    :({qw/iso-2022-jp-3 1 iso-2022-jp-2004 1/}->{$charset})
    ?qq{<tr>@{[c(qq{\x1B\x24\x28\x4F\x21\x31\x1B\x28\x42})]}<td>ESC 02/04 04/15 02/01 03/01</td><td>OVER LINE</td></tr>}
    :($charset eq 'utf-8')
    ?qq(<tr>@{[c(Encode::encode('utf8',"\x{203E}"))]}<td>U+203E</td><td>OVER LINE</td></tr>)
    :'']}
@{[ 
    ({qw/iso-2022-jp-2004 1/}->{$charset})
    ?qq{<tr>@{[c(qq{\x1B\x24\x28\x51\x21\x31\x1B\x28\x42})]}<td>ESC 02/04 05/01 02/01 03/01</td><td>OVER LINE</td></tr>}
    :'']}
<tr>@{[c(qq{&#x203E;})]}<td>&amp;#x203E;</td><td>OVER LINE</td></tr>

@{[ ({qw/shift_jis 1 shift_jisx0213 1 shift_jis-2004 1/}->{$charset})
    ?qq(<tr>@{[c(qq{\x81\x60})]}<td>0x8160</td><td>WAVE DASH</td></tr>)
    :($charset eq 'windows-31j')
    ?qq(<tr>@{[c(qq{\x81\x60})]}<td>0x8160</td><td>FULLWIDTH TILDE</td></tr>)
    :($charset =~ /iso-2022-jp/)
    ?qq{<tr>@{[c(qq{\x1B\x24\x42\x21\x41\x1B\x28\x42})]}<td>ESC 02/04 04/02 02/01 04/01</td><td>WAVE DASH</td></tr>}
    :({qw/euc-jp 1 euc-jisx0213 1 euc-jis-2004 1/}->{$charset})
    ?qq(<tr>@{[c(qq{\xA1\xC1})]}<td>0xA1C1</td><td>WAVE DASH</td></tr>)
    :'']}
@{[ ($charset eq 'iso-2022-jp' || $charset eq 'iso-2022-jp-1'
    || $charset eq 'iso-2022-jp-2')
    ?qq{<tr>@{[c(qq{\x1B\x24\x40\x21\x41\x1B\x28\x42})]}<td>ESC 02/04 04/00 02/01 04/01</td><td>WAVE DASH</td></tr>}
    :({qw/iso-2022-jp-3 1 iso-2022-jp-2004 1/}->{$charset})
    ?qq{<tr>@{[c(qq{\x1B\x24\x28\x4F\x21\x41\x1B\x28\x42})]}<td>ESC 02/04 04/15 02/01 04/01</td><td>WAVE DASH</td></tr>}
    :($charset eq 'utf-8')
    ?qq(<tr>@{[c(Encode::encode('utf8',"\x{301C}"))]}<td>U+301C</td><td>WAVE DASH</td></tr>)
    :'']}
@{[ 
    ({qw/iso-2022-jp-2004 1/}->{$charset})
    ?qq{<tr>@{[c(qq{\x1B\x24\x28\x51\x21\x41\x1B\x28\x42})]}<td>ESC 02/04 05/01 02/01 04/01</td><td>WAVE DASH</td></tr>}
    :'']}
<tr>@{[c(qq{&#x301C;})]}<td>&amp;#x301C;</td><td>WAVE DASH</td></tr>

@{[ ($charset eq 'shift_jisx0213' or $charset eq 'shift_jis-2004')
    ?qq(<tr>@{[c(qq{\x81\xB0})]}<td>0x81B0</td><td>TILDE</td></tr>)
    :($charset eq 'iso-2022-jp-3' or $charset eq 'iso-2022-jp-2004')
    ?qq{<tr>@{[c(qq{\x1B\x24\x28\x4F\x22\x32\x1B\x28\x42})]}<td>ESC 02/04 02/08 04/15 02/02 03/02</td><td>TILDE</td></tr>}
    :($charset eq 'euc-jisx0213' or $charset eq 'euc-jis-2004')
    ?qq(<tr>@{[c(qq{\xA2\xB2})]}<td>0xA2B2</td><td>(TILDE) or FULLWIDTH TILDE</td></tr>)
    :'']}

@{[ ({qw/iso-2022-jp-2004 1/}->{$charset})
    ?qq{<tr>@{[c(qq{\x1B\x24\x28\x51\x22\x32\x1B\x28\x42})]}<td>ESC 02/04 02/08 05/01 02/02 03/02</td><td>TILDE</td></tr>}
    :'']}

@{[ ($charset eq 'iso-2022-jp-2' || $charset eq 'iso-2022-jp-1')
    ?qq{<tr>@{[c(qq{\x1B\x24\x28\x44\x22\x37\x1B\x28\x42})]}<td>ESC 02/04 02/08 04/04 02/02 03/07</td><td>TILDE</td></tr>}
    :({qw/euc-jp 1 euc-jisx0213 1 euc-jis-2004 1/}->{$charset})
    ?qq(<tr>@{[c(qq{\x8F\xA2\xB7})]}<td>SS3 0xA2B7</td><td>TILDE or FULLWIDTH TILDE</td></tr>)
    :'']}


@{[($charset eq 'utf-8')
  ?qq(<tr>@{[c(Encode::encode('utf8',"\x{FF5E}"))]}<td>U+FF5E</td><td>FULLWIDTH TILDE</td></tr>)
  :'']}
<tr>@{[c(qq{&#xFF5E;})]}<td>&amp;#xFF5E;</td><td>FULLWIDTH TILDE</td></tr>

</tbody>
</table>

<p>Your User Agent Name : $ua</p>

<form action="yentilde.cgi" method="get">
<ul>
  <li><label>Type : <select name="type">@{[join "\n", sort map {qq(<option value="$_"@{[$_ eq $type?q( selected="selected"):'']}>$_</option>)} keys %type]}</select></label></li>
  <li><label>Charset : <select name="charset">@{[join "\n", sort map {qq(<option value="$_"@{[$_ eq $charset?q( selected="selected"):'']}>$_</option>)} keys %charset]}</select></label></li>
  <li><input type="submit" /></li>
</ul>
</form>

</body>
</html>
EOH

