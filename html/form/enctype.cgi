#!/usr/bin/perl
use strict;

sub unencode ($) {
  my $s = shift;
  $s =~ tr/+/ /;
  $s =~ s/%([0-9A-Fa-f][0-9A-Fa-f])/chr hex $1/ge;
  $s;
}

my %query;
for (split /[&;]/, $ENV{QUERY_STRING}) {
  my ($name, $val) = split '=', $_, 2;
  $query{$name} = unencode $val;
}

my $body = '';
my %body;
  binmode STDIN;
  read STDIN, $body, $ENV{CONTENT_LENGTH};
if ($ENV{CONTENT_TYPE} =~ m#^application/(?:x-www|sgml)-form-urlencoded#) {
  for (split /[&;]/, $body) {
    my ($name, $val) = split '=', $_, 2;
    $body{$name} = unencode $val;
  }
}

my $charset = $query{charset} || $body{charset};
$charset =~ s/[^0-9A-Za-z_.-]//g;
$charset ||= 'iso-8859-1';

my $accept_charset = $query{accept_charset} || $body{accept_charset};
$accept_charset =~ s/[^0-9A-Za-z. ,-]//g;

my $method = $query{method} || $body{method};
$method =~ s/[^A-Za-z]//g;

my $enctype = $query{enctype} || $body{enctype};
$enctype =~ s/[^\x09\x20-\x7E]//g;

sub escape ($) { my $s = shift; $s =~ s/&/&amp;/g; $s =~ s/</&lt;/g;
                 $s =~ s/"/&quot;/g;
                 $s =~ s!([^\x20-\x7E])!sprintf '<code>&amp;#x%02X;</code>', ord $1!ge;
                 $s };
sub mescape ($) { my $s = escape shift;
                  $s =~ s!(?:(?:<code>&amp;#x0D;</code>)?<code>&amp;#x0A;</code>|<code>&amp;#x0D;</code>)!$1<br />!g;
                  $s }

sub sel ($$@) {
  my ($name, $val, @options) = @_;
  my $r = q(<select name=").escape ($name).q(">);
  for (@options) {
    if ($_ eq '(none)') {
      $r .= q(<option value="">(none)</option>);
    } else {
      $r .= qq(<option value="@{[escape$_]}" @{[$_ eq $val?'selected':'']}>@{[escape$_]}</option>);
    }
  }
  $r .= q(</select>);
  $r;
}

print <<EOH;
Content-Type: text/html; charset=$charset

<!DOCTYPE body SYSTEM>

<h1>Form enctype test</h1>

<h2>Your request</h2>

<dl>
<dt>Request-Method</dt> <dd>@{[escape $ENV{REQUEST_METHOD}]}</dd>
<dt>Media type</dt>     <dd>@{[escape $ENV{CONTENT_TYPE}]}</dd>
@{[do { my $r = '';
  for (sort grep {/^HTTP_CONTENT_/} keys %ENV) {
    $r .= q(<dt>).escape ($_).q(</dt><dd>).escape ($ENV{$_}).q(</dd>);
  }
$r }]}
<dt>Query</dt>          <dd>@{[mescape $ENV{QUERY_STRING}]}</dd>
<dt>Request body</dt>   <dd>@{[mescape $body]}</dd>
</dl>

<h2>An example form</h2>

<form action="@{[escape $ENV{SCRIPT_NAME}]}" method="$method"
      @{[$enctype?qq(enctype="@{[escape $enctype]}"):'']}
      @{[$accept_charset?qq(accept-charset="$accept_charset"):'']}>

<dl>
<dt>Enctype</dt>  <dd>@{[escape $enctype]}</dd>
<dt>Accept charset (form)</dt>  <dd>$accept_charset</dd>
<dt>Method</dt>  <dd>$method</dd>
</dl>

<dl>
<dt>Enctype</dt> <dd>@{[sel 'enctype', $enctype,
                        qw!(none)
                           application/x-www-form-urlencoded
                           APPLICATION/X-WWW-FORM-URLENCODED
                           Application/X-WWW-Form-URLEncoded
                           application/x-www-form-urlencoded;charset=utf-8
                           application/x-www-form-urlencoded;charset=iso-2022-jp
                           application/x-www-form-urlencoded;x-unknown=unknown
                           appliaction/sgml-form-urlencoded
                           application/sgml-form-urlencoded;x-unknown=unknown
                           multipart/form-data
                           MULTIPART/FORM-DATA
                           Multipart/Form-Data
                           multipart/form-data;boundary=a
                           multipart/form-data;x-unknown=unknown
                           multipart/form-data;charset=iso-2022-jp
                           multipart/mixed
                           text/plain
                           text/plain;charset=utf-8
                           text/plain;charset=iso-2022-jp
                           text/plain;format=flowed
                           text/plain;format=fixed
                           text/plain;format=fixed;charset=iso-2022-jp
                           text/plain;charset=iso-2022-jp;format=flowed
                           text/html
                           text/html;charset=iso-2022-jp
                           application/x-www-form+xml
                           application/x-www-form+xml;charset=iso-2022-jp
                           text/xml
                           text/xml;charset=iso-2022-jp
                           application/xml
                           application/xml;charset=iso-2022-jp!]}</dd>
<dt>Accept-charset</dt><dd>@{[sel 'accept_charset', $accept_charset,
                           qw!(none) us-ascii iso-8859-1 utf-8
                              iso-2022-jp euc-jp shift_jis
                              utf-8,iso-2022-jp
                              euc-jp,iso-2022-jp
                              x-unknown,us-ascii
                              iso-8859-1,shift_jis
                              !]}</dd>
<dt>Form charset</dt><dd>@{[sel 'charset', $charset,
                            qw!us-ascii iso-8859-1 shift_jis
                               euc-jp iso-2022-jp utf-8!]}</dd>
<dt>Method</dt><dd>@{[sel 'method', $method,
                      qw!GET get Get POST post Post HEAD head PUT put
                         OPTIONS options
                         DELETE delete M-GET m-get M-POST m-post!]}</dd>
<dt>Something text</dt><dd><input type="text" name="something-text" value="test&#x4E00;.??&amp;&amp;" /></dd>
<dt>Something check</dt><dd><input type="checkbox" name="something-check" checked /> <input type="checkbox" name="something-check2" /></dd>
<dt>Something non-ASCII named</dt><dd><input type="text" name="something&#x4E00;" value="&#x4E00;&#x3002;" /></dd>
<dt>Something file</dt>
    <dd><input type="file" name="file1" /></dd>
    <dd><input type="file" name="file2" /></dd>
<dt>Submit: <input type="hidden" name="_charset_" /></dt>
    <dd><input type="image" name="image" src="/admin/logo" /></dd>
    <dd><input type="submit" name="submit" /></dd>
</dl>

</form>
EOH
