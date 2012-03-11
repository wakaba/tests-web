#!/usr/bin/perl
use strict;
use Encode;
use CGI qw(param);

sub token ($) {
  my $s = shift;
  $s =~ s/[^0-9A-Za-z_+.-]//g;
  $s;
}
sub tokenlike ($) {
  my $s = shift;
  $s =~ s/[;"\\]//g;
  $s;
} # tokenlike
sub escape ($) {
  my $s = shift;
  $s =~ s/&/&amp;/g;
  $s =~ s/</&lt;/g;
  $s;
}
sub ascii_html ($) {
  my $s = shift;
  $s =~ s!([^\x20-\x7E])!sprintf '<code>%02X</code>', ord $1!ge;
  $s;
}
sub pe ($) {
  my $s = $_[0];
  $s =~ s/([^0-9A-Za-z_+.-])/sprintf '%%%02X', ord $1/ge;
  return $s;
} # pe
sub check ($$$) {
  my ($name, $label, $defval) = @_;
  qq(<label><input type="checkbox" name="@{[escape $name]}" @{[$defval eq 'on' ? 'checked="checked"' : '']} />@{[escape $label]}</label>);
}
sub select_options ($$$) {
  my ($name, $vals, $defval) = @_;
  my $r = qq(<select name="@{[escape $name]}">);
  for (@$vals) {
    $r .= qq(<option value="@{[escape $_]}">@{[escape $_]}</option>);
  }
  $r .= qq(</select>);
  $r;
}

my $filename = decode 'utf-8', q(ファイル×1);

my $charset = token param ('charset') || 'iso-8859-1';
my $charset_specify = param ('no-charset') ? 0 : 1;
my $disposition = token param ('disposition') || 'inline';

my $encode = param ('encode');
if ($encode eq 'bare-quoted') {
  $filename = 'filename="' . encode ($charset, $filename) . '"';
} elsif ($encode eq 'bare-token') {
  $filename = 'filename=' . tokenlike encode ($charset, $filename);
} elsif ($encode eq 'percent-quoted') {
  $filename = 'filename="' . (pe encode ($charset, $filename)) . '"';
} elsif ($encode eq 'percent-token') {
  $filename = 'filename=' . tokenlike pe encode ($charset, $filename);
} else {
  $filename = encode ($charset, $filename);
  $filename = "filename*=" . $charset . "''" . pe $filename;
}

print <<EOH;
Content-Type: text/html@{[$charset_specify?qq(; charset=$charset):'']}
Content-Disposition: $disposition; $filename

<!DOCTYPE html SYSTEM>
<title>Example file</title>
<style type="text/css" media="all">
  code { color: gray; text-decoration: underline }
</style>

File content

<pre>
Content-Type: text/html@{[$charset?escape qq(; charset=$charset):'']}
Content-Disposition: @{[escape $disposition]}; @{[ascii_html escape $filename]}
</pre>


<form action="@{[escape $ENV{SCRIPT_NAME}]}" method="post">
<dl>
<dl>Content Disposition type
  <dt>@{[select_options 'disposition', [qw/inline attachment form-data file x-unknown-value/], $disposition]}
<dt>Charset
  <dd>@{[select_options 'charset', [qw/iso-8859-1 us-ascii utf-8 iso-2022-jp euc-jp shift_jis/], $charset]}</dd>
  <dd>@{[check 'no-charset', 'Don\'t use charset parameter', not $charset_specify]}
<dt>Encoding
  <dd>@{[select_options 'encode', [qw/
    bare-token bare-quoted percent-token percent-quoted 2231
  /], $encode]}
<dt><input type="submit" />
</dl>
</form>
EOH

