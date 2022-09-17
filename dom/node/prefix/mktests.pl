#!/usr/bin/perl
use strict;

my @create_target;
for my $uri (
  [null => 'null'],
  [absuri => '"http://test/"'],
  [xmluri => '"http://www.w3.org/XML/1998/namespace"'],
  [xmlnsuri => '"http://www.w3.org/2000/xmlns/"'],
) {
  for my $prefix (
    [null => '"localName"', 'null', '"localName"'],
    [xml10ncname => '"originalPrefix:localName"',
     '"originalPrefix"', '"localName"'],
    [xml => '"xml:lang"', '"xml"', '"lang"'],
    [xmlns => '"xmlns"', 'null', '"xmlns"'],
    [xmlnsprefix => '"xmlns:declaredPrefix"', '"xmlns"', '"declaredPrefix"'],
  ) {
    push @create_target, ['Attr', $uri->[0], $prefix->[0], qq[
      var el;
      try {
        el = document.createAttributeNS ($uri->[1], $prefix->[1]);
      } catch (e) { }
      if (!el) {
        try {
          el = document.createAttributeNS ($uri->[1], $prefix->[3]);
          el.prefix = $prefix->[2];
        } catch (e) { }
      }
      var ok = (el && el.prefix == $prefix->[2] &&
                el.namespaceURI == $uri->[1]);
    ]];
    push @create_target, ['Element', $uri->[0], $prefix->[0], qq[
      var el;
      try {
        el = document.createAttributeNS ($uri->[1], $prefix->[1]);
      } catch (e) { }
      if (!el) {
        try {
          el = document.createAttributeNS ($uri->[1], $prefix->[3]);
          el.prefix = $prefix->[2];
        } catch (e) { }
      }
      var ok = (el && el.prefix == $prefix->[2] &&
                el.namespaceURI == $uri->[1]);
    ]];
  }
}

my @set_value = (
  ['null', 'null'],
  ['undefined', 'undefined'],
  ['empty', '""'],
  ['nonxmlname', '"12345"'],
  ['xml10name', '"new:Prefix"'],
  ['xml10ncname', '"newPrefix"'],
  ['xml', '"xml"'],
  ['xmlns', '"xmlns"'],
);

my $table = q[<tbody>];
my @items;
for my $create_target (@create_target) {
  $table .= qq[<tr><th scope="row">$create_target->[0]</th>
               <th scope="row">$create_target->[1]</th>
               <th scope="row">$create_target->[2]</th>];
  for my $set_value (@set_value) {
    my $file_name = lc ($create_target->[0]) . '-' . $create_target->[1] .
        '-' . $create_target->[2] . '-' . $set_value->[0];
    warn $file_name, "\n";
    $table .= qq[<td><a href="$file_name.xhtml" id="$file_name" class="FAIL"
        title="@{[ ($create_target->[1] eq 'xmlnsuri' and
                    $create_target->[2] !~ 'xmlns') ? 'noopera' : '' ]}">FAIL (not executed)</a></td>];
    push @items, $file_name;
    my $file_content = qq[<head>
      <title>$create_target->[0].prefix = $set_value->[0]</title>
    </head><body>
      <p id="result" class="FAIL">FAIL (not executed)</p>
      <script type="text/javascript">// <![CDATA[
        var result = document.getElementById ('result');
        result.firstChild.data = 'FAIL (script error)';
        $create_target->[3]
        if (ok) {
          try {
            el.prefix = $set_value->[1];
            result.className = '';
            result.firstChild.data = el.prefix + ', type ' + typeof (el.prefix);
          } catch (e) {
            result.className = '';
            result.firstChild.data = e.toString ();
          }
        } else {
          result.className = 'NA';
          result.firstChild.data = 'N/A';
        }
      // ]]></script>
    </body></html>
    ];
    open my $file, '>', "$file_name.html" or die "$0: $file_name.html: $!";
    print $file "<!DOCTYPE html><html>$file_content";
    open $file, '>', "$file_name.xhtml" or die "$0: $file_name.xhtml: $!";
    print $file qq'<html xmlns="http://www.w3.org/1999/xhtml">$file_content';
  }
  $table .= q[</tr>];
}
$table .= q[</tbody>];

for my $type (
  ['.html' => '<!DOCTYPE html><html>'],
  ['.xhtml' => '<html xmlns="http://www.w3.org/1999/xhtml">'],
) {
  my $table = $table;
  $table =~ s/\.xhtml\b/$type->[0]/g;
  open my $file, '>', "set-prefix-list$type->[0]"
      or die "$0: set-prefix-list$type->[0]: $!";
  print $file qq[$type->[1]
<head>
<title>prefix Attribute Test Result</title>
<style type="text/css">
  a {
    color: blue;
  }
  a.NA {
    color: gray;
  }
  a.FAIL {
    color: red;
  }
</style>
</head>
<body>
  <table>
  <thead>
  <tr>
    <th scope="col" colspan="3">Original</th>
    @{[ map { qq[<th scope="col">$_->[0]</th>] } @set_value ]}
  </tr>
  <tr>
    <th scope="col"><var>Node</var></th>
    <th scope="col"><code>namespaceURI</code></th>
    <th scope="col"><code>prefix</code></th>
  </tr>
  </thead>
  $table
  </table>
  <p><iframe></iframe></p>
  <script type="text/javascript">// <![CDATA[
    window.testItems = ["@{[ join '", "', @items ]}"];
    window.currentItem = window.testItems.pop ();
    var iframe = document.getElementsByTagName ('iframe')[0];
    iframe.onload = function () {
      try {
        var result = this.contentWindow.document.getElementById ('result');
        var resultCell = document.getElementById (window.currentItem);
        resultCell.className = result.className;
        resultCell.firstChild.data = result.firstChild.data;
      } catch (e) { }
      while (testItems.length > 0) {
        window.currentItem = window.testItems.pop ();
        var resultCell = document.getElementById (window.currentItem);
        if (window.opera && resultCell.title == 'noopera') {
          /* Don't test since Opera dies with create*NS
             <https://suika.suikawiki.org/gate/2005/sw/createAttributeNS> */
          resultCell.className = 'NA';
          resultCell.firstChild.data = 'N/A (skipped)';
        } else {
          this.src = window.currentItem + "$type->[0]";
          return;
        }
      }
      this.onload = null;
      this.style.display = 'none';
    };
    iframe.src = window.currentItem + "$type->[0]";
  // ]]></script>
</body>
</html>];
}
