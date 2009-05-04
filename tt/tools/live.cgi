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

print "Content-Type: text/html; charset=utf-8\n\n";

my $output = '';
if (length $input) {
  require Template;
  my $template = Template->new ({
    INCLUDE_PATH => '/tmp/no-such-directory/',
  });
  $template->process (\$input, {}, \$output) or $output = $template->error;
}

print qq[<!DOCTYPE HTML>
<html lang=en>
<title>TT Viewer</title>
<link rel=stylesheet href="/www/style/html/xhtml">
<style>
p {
  text-indent: 0 !important;
}

textarea {
  height: 10em;
}

textarea#result {
  height: 30em;
}
</style>

<form action=live method=get accept-charset=utf-8>

<p><textarea name=s>@{[htescape $input_orig]}</textarea>

<button type=submit>Process</button></p>
</form>

<h2>Result</h2>

<textarea id=result>
Input:
[PRE(code)[
@{[htescape $input]}
]PRE]

Result:
[PRE(code)[
@{[htescape $output]}
]PRE]

</textarea>
<script>
  document.getElementById ('result').value += ';; <' + location.href + '>\\n';
</script>

];


