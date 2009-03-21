#!/usr/bin/perl
use strict;
use warnings;
use CGI::Carp qw/fatalsToBrowser/;

use lib qw[/home/wakaba/work/manakai2/lib];

use Message::CGI::Util qw/htescape/;

require Message::CGI::HTTP;
my $cgi = Message::CGI::HTTP->new;
$cgi->{decoder}->{'#default'} = sub {
  return Encode::decode ('utf-8', $_[1]);
};

my $input = my $input_orig = $cgi->get_parameter ('s');
my $charset = $cgi->get_parameter ('c') || 'utf-8';
$input = Encode::encode ($charset, $input);

my $flags;
for (qw/check check-compatibility use-fuzzy/) {
  $flags->{$_} = $cgi->get_parameter ($_);
}

my $output = '';
if (length $input) {
  use IPC::Open3;

  my @flag = map {"--$_"} grep {$flags->{$_}} keys %$flags;

  my $pid = open3 my $in, my $out, my $err, qw/msgfmt -o - -/, @flag;
  my $mo = '';
  print $in $input;
  close $in;
  $mo .= $_ while <$out>; close $out;
  if ($err) { $output .= $_ while <$err>; close $err; }
  waitpid $pid, 0;
  if ($? >> 8) {
    $output .= $mo;
    $mo = '';
  } else {
    my $pid = open3 my $in, my $out, my $err, qw/msgunfmt -o - -/;
    print $in $mo;
    close $in;
    $output .= $_ while <$out>; close $out;
    if ($err) { $output .= $_ while <$err>; close $err; }
    waitpid $pid, 0;
    if ($? >> 8) {
      #
    }
  }
}

print qq[Content-Type: text/html; charset=utf-8

<!DOCTYPE HTML>
<html lang=en>
<title>PO Viewer</title>
<link rel=stylesheet href="/www/style/html/xhtml">
<style>
p {
  text-indent: 0 !important;
}

textarea {
  height: 10em;
}
</style>

<form action=live method=get accept-charset=utf-8>

<p><textarea name=s>@{[htescape $input_orig]}</textarea>

<label>Charset:</label> <select name=c>
  <option value=utf-8>UTF-8
  <option value=shift_jis>Shift_JIS
  <option value=euc-jp>EUC-JP
  <option value=iso-2022-jp>ISO-2022-JP
  <option value=windows-1252>Windows-1252
</select>
<script>
  document.forms[0].c.value = "@{[htescape $charset]}";
</script>

@{[
   join "\n", map {qq[<label><input type=checkbox name="@{[htescape $_]}" @{[$flags->{$_} ? 'checked' : '']}> <code>--@{[htescape $_]}</code></label>]} keys %$flags
]}

<button type=submit>Parse</button></p>
</form>

<h2>Result</h2>

<textarea id=result>
[PRE(code)[
@{[htescape $input]}
]PRE]

[PRE[
@{[htescape $output]}
]PRE]

</textarea>
<script>
  document.getElementById ('result').value += ';; <' + location.href + '>\\n';
</script>

];


