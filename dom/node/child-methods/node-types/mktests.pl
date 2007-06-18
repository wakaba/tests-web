#!/usr/bin/perl
use strict;

my @create_node = (
  [element => q{ function () { return doc.createElement ('e')  } }],
  [attr => q{ function () { return doc.createAttribute ('a')  } }],
  [textempty => q{ function () { return doc.createTextNode ('') } }],
  [textwsp => q{ function () { return doc.createTextNode ('  ') } }],
  [text => q{ function () { return doc.createTextNode ('abc') } }],
  [cdata => q{ function () { return doc.createCDATASection ('abc') } }],
  [comment => q{ function () { return doc.createComment ('') } }],
  [docfrag => q{ function () { return doc.createDocumentFragment () } }],
  [doctype => q{ function () {
    return doc.implementation.createDocumentType ('root', null, null);
  } }],
  [doctypeinuse => q{ function () {
    var doctype = doc.implementation.createDocumentType ('root', null, null);
    var newdoc = doc.implementation.createDocument (null, null, doctype);
    return doctype;
  } }],
  [newdoc => q{ function () { return doc.implementation.createDocument (null, null, null) } }],
  [newdocwithdoctype => q{ function () {
    var doctype = doc.implementation.createDocumentType ('root', null, null);
    return doc.implementation.createDocument (null, null, doctype);
  } }],
  [newdocwithelement => q{ function () {
    return doc.implementation.createDocument (null, 'e', null);
  } }],
  [newdocwithdoctypeelement => q{ function () {
    var doctype = doc.implementation.createDocumentType ('root', null, null);
    return doc.implementation.createDocument (null, 'e', doctype);
  } }],
  [newdocwithcomment => q{ function () {
    var newdoc = doc.implementation.createDocument (null, null, null);
    newdoc.appendChild (newdoc.createComment (''));
    return newdoc;
  } }],
  [entref => q{ function () { return doc.createEntityReference ('e') } }],
  [pi => q{ function () { return doc.createProcessingInstruction ('pi', 'a') } }],
);

my $table = q[<tbody>];
my @items;
for my $parent (@create_node) {
  $table .= qq[<tr><th scope="row">$parent->[0]</th>];
  for my $child (@create_node) {
    for my $method (
                    [appendchild => 'appendChild'],
                    [insertbefore => 'insertBefore'],
                   ) {
      my $file_name = "$method->[0]-$parent->[0]-$child->[0]";
      $table .= qq[<td><a href="$file_name.xhtml" id="$file_name" class="FAIL">FAIL (not executed)</a></td>];
      push @items, $file_name;
      my $file_content = qq{<head>
        <title>$parent->[0].$method->[1] ($child->[0])</title>
        </head>
        <body>
        <p id="result" class="FAIL">FAIL (not executed)</p>
        <script>// <![CDATA[
          var result = document.getElementById ('result');
          result.firstChild.data = 'N/A';
          result.className = 'NA';
          doc = document;
          var parent;
          var child;
          try {
            parent = ($parent->[1])();
            child = ($child->[1])();
          } catch (e) { }
          if (parent && child) {
          try {
            parent.$method->[1] (child, null);
            if (parent.lastChild === child) {
              if (child.parentNode === parent) {
                result.firstChild.data = '(appended)';
                result.className = 'see-detail';
              } else {
                result.firstChild.data = 'FAIL (in childNodes, but parentNode disagree)';
                result.className = 'FAIL';
              }
            } else {
              result.firstChild.data = '(not appended)';
              result.className = 'see-detail';
            }
          } catch (e) {
            result.firstChild.data = '(' + (e.code ? e.code : e.description) + ')';
            result.className = 'see-detail';
          }
          }
        // ]]></script>
        </body>
        </html>
      };
      open my $file, '>', "$file_name.html" or die "$0: $!: $file_name.html";
      print $file qq[<!DOCTYPE html><html>$file_content];
      open $file, '>', "$file_name.xhtml" or die "$0: $!: $file_name.xhtml";
      print $file qq[<html xmlns="http://www.w3.org/1999/xhtml">$file_content];
    }
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
  open my $file, '>', "child-test-list$type->[0]"
      or die "$0: child-test-list$type->[0]: $!";
  print $file qq[$type->[1]
<head>
<title>appendChild and insertBefore Test Result</title>
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
    <th scope="row">Child</th>
    @{[ map { qq[<th scope="col" colspan="2">$_->[0]</th>] } @create_node ]}
  </tr>
  <tr>
    <th scope="col">Parent</th>
    @{[ map { qq[<th scope="col"><code>appendChild</code></th><th scope="col"><code>insertBefore</code></th>] } @create_node ]}
  </tr>
  </thead>
  $table
  </table>
  <p><iframe></iframe></p>
  <script type="text/javascript">// <![CDATA[
    window.testItems = ["@{[ join '", "', @items ]}"];
    window.currentItem = window.testItems.pop ();
    var iframe = document.getElementsByTagName ('iframe')[0];
    var ol = function () {
      try {
        var result = iframe.contentWindow.document.getElementById ('result');
        var resultCell = document.getElementById (window.currentItem);
        resultCell.className = result.className;
        resultCell.firstChild.data = result.firstChild.data;
      } catch (e) { }
      while (testItems.length > 0) {
        window.currentItem = window.testItems.pop ();
        var resultCell = document.getElementById (window.currentItem);
        if (0) {
          resultCell.className = 'NA';
          resultCell.firstChild.data = 'N/A (skipped)';
        } else {
          iframe.src = window.currentItem + "$type->[0]";
          return;
        }
      }
      iframe.onload = null;
      iframe.onreadystatechange = null;
      iframe.style.display = 'none';
    };
    iframe.onload = ol;
    iframe.onreadystatechange = function () {
      if (this.readyState == 'complete') {
        ol ();
      }
    };
    iframe.src = window.currentItem + "$type->[0]";
  // ]]></script>
</body>
</html>];
}
