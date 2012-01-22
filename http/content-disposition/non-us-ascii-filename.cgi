#!/usr/bin/perl
use strict;
use Encode;
use encoding qw(iso-2022-jp);
use CGI qw(param);

sub token ($) {
  my $s = shift;
  $s =~ s/[^0-9A-Za-z_+.-]//g;
  $s;
}
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

my $filename = q(ファイル×1);

my $charset = token param ('charset') || 'iso-8859-1';
my $charset_specify = param ('no-charset') ? 0 : 1;
my $disposition = token param ('disposition') || 'inline';

my $encode = param ('encode');
if ($encode eq 'bare') {
  $filename = 'filename="' . encode ($charset, $filename) . '"';
} else {
  $filename = encode ($charset, $filename);
  $filename =~ s/([^0-9A-Za-z_+.-])/sprintf '%%%02X', ord $1/ge;
  $filename = 'filename*=' . $filename;
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
  <dd>@{[select_options 'encode', [qw/bare 2231 /], $encode]}
<dt><input type="submit" />
</dl>
</form>
EOH

