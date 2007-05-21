#!/usr/bin/perl
use strict;

generate_test ($_) for
  qw/
    body comment head header html footer plaintext isindex
    meta title aside blockquote details div h1 h2 h3 h4 h5 h6
    map nav section address figure p dd dl dt li label caption
    col colgroup tbody td tfoot thead tr bdo rb rbc rp rt rtc ruby
    sub sup abbr acronym cite code dfn em kbd m meter progress q
    samp strong span time var del ins a base link nextid
    applet area audio canvas embed video frame iframe image img noembed
    object param bgsound xml frameset noframes form fieldset legend
    button command datagrid datalist input keygen dir menu ul ol 
    option output textarea select event-source script noscript
    server basefont b big blackface blink bt font i s shadow strike
    small tt u br center hr layer ilayer listing xmp marquee multicol
    nobr wbr nolayer pre spacer
    commentdecl dldtdd ulli olli menuli dirli basictable simpleruby
  /;

sub generate_test ($) {
  my $element = shift;

  my $text1 = {
               a => '<a href="/">WWW</a>',
               br => '<br>',
               img => '<img src="../../../support/1.png" alt="WWW">',
               image => '<image src="../../../support/1.png" alt="WWW">',
               isindex => '<isindex>',
               meta => '<meta name="keywords" content="WWW">',
               link => '<link href="/" rel="author" title="WWW">',
               col => '<col>',
               nextid => '<nextid n="1">',
               area => '<area alt="WWW">',
               frame => '<frame src="404">',
               param => '<param name="n" value="v">',
               bgsound => '<bgsound src="404">',
               input => '<input type="text" value="WWW">',
               'event-source' => '<event-source src="404">',
               script => '<script>document.write ("WWW")</script>',
               hr => '<hr>',
               wbr => '<wbr>',
               spacer => '<spacer>',
               commentdecl => '<!-- WWW -->',
               dldtdd => '<dl><dt>WWW</dt><dd>www</dd></dl>',
               ulli => '<ul><li>WWW</li></ul>',
               olli => '<ol><li>WWW</li></ol>',
               menuli => '<menu><li>WWW</li></menu>',
               dirli => '<dir><li>WWW</li></dir>',
               basictable => '<table><tr><td>WWW</td></tr></table>',
               simpleruby => '<ruby><rb>WWW</rb><rt>www</rt></ruby>',
              }->{$element} || qq[<$element>WWW</$element>];

  open my $file, '>', "$element-1-norb.html";
  print $file qq[<!DOCTYPE html>
<html>
<head>
<title>$element in rp</title>
</head>
<body>
<ruby>YYYYYYYY<rp>a${text1}b</rp><rt>XXX</rt></ruby>
</body>
</html>];

  open my $file, '>', "$element-2-norb.html";
  print $file qq[<!DOCTYPE html>
<html>
<head>
<title>$element in rp</title>
</head>
<body>
<p><ruby>YYYYYYYY<rp>a${text1}b</rp><rt>XXX</rt></ruby></p>
</body>
</html>];
} # generate_test
