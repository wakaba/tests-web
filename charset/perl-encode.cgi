#!/usr/bin/perl
use strict;
use warnings;
use Encode;
use CGI::Carp qw(fatalsToBrowser);

sub htescape ($) {
  my $s = shift;
  $s =~ s/&/&amp;/g;
  $s =~ s/</&lt;/g;
  $s =~ s/>/&gt;/g;
  $s =~ s/"/&quot;/g;
  return $s;
} # htescape

sub udecode ($) {
  my $s = shift;
  $s =~ s/\\(u[0-9A-Fa-f]{4}|U[0-9A-Fa-f]{8})/chr hex substr $1, 1/ge;
  return $s;
} # udecode

sub uencode ($) {
  my $s = shift;
  $s =~ s/([^\x20-\x5B\x5D-\x7E])/sprintf '\U%08X', ord $1/ge;
  return $s;
} # uencode

sub bencode ($) {
  my $s = shift;
  $s =~ s/([^\x21-\x5B\x5D-\x7E])/sprintf '\x%02X', ord $1/ge;
  return $s;
} # bencode

my $params = { map { s/%([0-9A-Fa-f]{2})/pack 'C', hex $1/ge; decode 'utf8', $_ } map { split /=/, $_, 2 } split /[&;]/, $ENV{QUERY_STRING} // '' };

my $s = udecode ($params->{s} // '');
my $c = $params->{c} // 'utf8';

my $encoded = encode $c, $s;

binmode STDOUT, ':encoding(utf-8)';
print qq[Content-Type: text/html; charset=utf-8

<!DOCTYPE HTML>
<html lang=en>
<title>Perl Encoder</title>
<link rel=stylesheet href="http://suika.fam.cx/www/style/html/xhtml">
<h1>Perl Encoder</h1>

<form action method=get accept-charset=utf-8>
  <p><label>Input charset: <input type=text name=c value="@{[htescape $c]}"></label>
  <p><label>Input chars: <input type=text name=s value="@{[htescape uencode $s]}"></label>
  <p><button type=submit>OK</button>

  <p><label>Chars: <output>@{[htescape $s]}</output></label>
  <p><label>Bytes: <output>@{[htescape bencode $encoded]}</output></label>
</form>
];
