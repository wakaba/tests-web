#!/usr/bin/perl
use strict;

my $html_header = q[<!DOCTYPE html><html>];
my $xhtml_header = q[<html xmlns="http://www.w3.org/1999/xhtml">];

my @type = ({id => 'noxml.html', header => $html_header},
            {id => 'noxml.xhtml', header => $xhtml_header});
for my $xv (
            [noversion => ''],
            ['v10' => ' version="1.0"'],
            ['v11' => ' version="1.1"'],
            [unknownversion1 => ' version="unKnown"'],
            [unknownversion2 => ' version="unknown"'],
            [illegalversion => qq[ version="\x{4E00}"]],
           ) {
  for my $xe (
              [noenc => '', ''],
              [httpenc1 => ' encoding="iso-2022-JP"', '.jis'],
              [httpenc2 => ' encoding="iso-2022-jp"', '.jis'],
              [incorrectenc => ' encoding="utf-16"', ''],
              [unknownenc => ' encoding="unknown-encoding-name"', ''],
              [illegalenc => qq[ encoding="\x{4E00}"], ''],
             ) {
    for my $xs (
                [nosa => '', ''],
                [sayes1 => ' standalone="yes"', ''],
                [sayes2 => ' standalone="Yes"', ''],
                [sayesinvalid => ' standalone="yes"',
                 '<!DOCTYPE html SYSTEM "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">'],
                [sano1 => ' standalone="no"',
                 '<!DOCTYPE html SYSTEM "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">'],
                [sano2 => ' standalone="nO"',
                 '<!DOCTYPE html SYSTEM "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">'],
                [sanoinvalid => ' standalone="no"', ''],
               ) {
      push @type, {id => qq[xml-$xv->[0]-$xe->[0]-$xs->[0].html$xe->[2]],
                   header => qq[<?xml$xv->[1]$xe->[1]$xs->[1]?>$xs->[2]$xhtml_header]};
      push @type, {id => qq[xml-$xv->[0]-$xe->[0]-$xs->[0].xhtml$xe->[2]],
                   header => qq[<?xml$xv->[1]$xe->[1]$xs->[1]?>$xs->[2]$xhtml_header]};
    }
  }
}

for my $prop (
              {id => 'xml-version', name => 'xmlVersion'},
              {id => 'xml-encoding', name => 'xmlEncoding'},
              {id => 'xml-standalone', name => 'xmlStandalone'},
             ) {
  for my $type (@type) {
    my $file_name = qq[$prop->{id}/get-$type->{id}];
    warn $file_name, "\n";
    open my $file, '>:encoding(iso-2022-jp)', $file_name
        or die "$0: $file_name: $!";
    print $file qq[$type->{header}<head>
<title>document.$prop->{name} Get</title>
<script src="../../../../support/result.js"></script>
</head>
<body>
<p id="result" class="FAIL">FAIL (not executed)</p>
<script> setResult ('result', document.$prop->{name}) </script>
</body>
</html>];
  }
}

for my $type (
              {id => '.html', header => $html_header,
               original_value => 'null'},
              {id => '-noxml.xhtml', header => $xhtml_header,
               original_value => '"1.0"'},
              {id => '-xml10.xhtml',
               header => '<?xml version="1.0"?>'.$xhtml_header,
               original_value => '"1.0"'},
              {id => '-xml11.xhtml',
               header => '<?xml version="1.1"?>'.$xhtml_header,
               original_value => '"1.1"'},
             ) {
  for my $new_value (
                     {id => 'null', new_value => 'null'},
                     {id => 'undefined', new_value => 'undefined'},
                     {id => 'empty', new_value => '""'},
                     {id => 'num1', new_value => '1.0'},
                     {id => 'num11', new_value => '1.1'},
                     {id => 'str10', new_value => '"1.0"'},
                     {id => 'str11', new_value => '"1.1"'},
                     {id => 'unknown', new_value => '"unknown"'},
                     {id => 'illegal', new_value => '"\1"'},
                    ) {
    my $file_name = qq[xml-version/set-$new_value->{id}$type->{id}];
    warn $file_name, "\n";
    open my $file, '>', $file_name or die "$0: $file_name: $!";
    print $file qq[$type->{header}<head>
<title>document.xmlVersion = $new_value->{new_value}</title>
<script src="../../../../support/result.js"></script>
</head>
<body>
<p id="result" class="FAIL">FAIL (not executed)</p>
<script>
  var result = document.getElementById ('result');
  result.firstChild.data = 'FAIL (script error)';
  if (document.xmlVersion === $type->{original_value}) {
    try {
      document.xmlVersion = $new_value->{new_value};
      var xv = document.xmlVersion;
      if (xv === $new_value->{new_value}) {
        result.firstChild.data = 'new value';
        result.className = 'see-detail';
      } else if (xv === $type->{original_value}) {
        result.firstChild.data = 'original value';
        result.className = 'see-detail';
      } else {
        setResult ('result', xv);
      }
    } catch (e) {
      result.firstChild.data = e.toString ();
      result.className = 'see-detail';
    }
  } else {
    result.firstChild.data = 'N/A';
    result.className = 'NA';
  }
</script>
</body>
</html>];
  }
}

