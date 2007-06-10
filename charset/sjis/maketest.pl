#!/usr/bin/perl
use strict;

my $range = shift; # 0, 0x8..0xF

my $Table;
while (<>) {
  if (/^0x(\S+)\s+U\+(\S+)/) {
    $Table->{hex $1} = hex $2;
  }
}

my $table3 = {
  0x88B1 => 0xE9CB,
  0x89A7 => 0xE9F2,
  0x8A61 => 0xE579,
  0x8A68 => 0x9D98,
  0x8A96 => 0xE27D,
  0x8AC1 => 0x9FF3,
  0x8AD0 => 0xE67C,
  0x8C7A => 0xE8F2,
  0x8D7B => 0xE1E6,
  0x8EC7 => 0xE541,
  0x9078 => 0xE8D5,
  0x9147 => 0xE6CB,
  0x92D9 => 0x9AE2,
  0x9376 => 0xE1E8,
  0x938E => 0x9E8D,
  0x9393 => 0x9FB7,
  0x93F4 => 0xE78E,
  0x9488 => 0xE5A2,
  0x954F => 0x9E77,
  0x9699 => 0x98D4,
  0x96F7 => 0xE54D,
  0x9855 => 0xE2C4,
};
$table3 = {%$table3, reverse %$table3};

my $table4 = {
  0x81B8 => 1,
  0x81B9 => 1,
  0x81BA => 1,
  0x81BB => 1,
  0x81BC => 1,
  0x81BD => 1,
  0x81BE => 1,
  0x81BF => 1,
  0x81C8 => 1,
  0x81C9 => 1,
  0x81CA => 1,
  0x81CB => 1,
  0x81CC => 1,
  0x81CD => 1,
  0x81CE => 1,
  0x81DA => 1,
  0x81DB => 1,
  0x81DC => 1,
  0x81DD => 1,
  0x81DE => 1,
  0x81DF => 1,
  0x81E0 => 1,
  0x81E1 => 1,
  0x81E2 => 1,
  0x81E3 => 1,
  0x81E4 => 1,
  0x81E5 => 1,
  0x81E6 => 1,
  0x81E7 => 1,
  0x81E8 => 1,
  0x81F0 => 1,
  0x81F1 => 1,
  0x81F2 => 1,
  0x81F3 => 1,
  0x81F4 => 1,
  0x81F5 => 1,
  0x81F6 => 1,
  0x81FC => 1,
  0x849F => 1,
  0x84A0 => 1,
  0x84A1 => 1,
  0x84A2 => 1,
  0x84A3 => 1,
  0x84A4 => 1,
  0x84A5 => 1,
  0x84A6 => 1,
  0x84A7 => 1,
  0x84A8 => 1,
  0x84A9 => 1,
  0x84AA => 1,
  0x84AB => 1,
  0x84AC => 1,
  0x84AD => 1,
  0x84AE => 1,
  0x84AF => 1,
  0x84B0 => 1,
  0x84B1 => 1,
  0x84B2 => 1,
  0x84B3 => 1,
  0x84B4 => 1,
  0x84B5 => 1,
  0x84B6 => 1,
  0x84B7 => 1,
  0x84B8 => 1,
  0x84B9 => 1,
  0x84BA => 1,
  0x84BB => 1,
  0x84BC => 1,
  0x84BD => 1,
  0x84BE => 1,
};

my $table5 = {
  0x8BC4 => 0xEA9F,
  0x968A => 0xEAA0,
  0x9779 => 0xEAA1,
  0xE0F4 => 0xEAA2,
  0xEAA4 => 0xE086,
};
$table5 = {%$table5, reverse %$table5};

my $table6 = {
  0xEAA3 => 1,
};

## NOTE: JIS X 0208:1997 Annex 1 2. b) is difficult to understand
## and I don't know what it means exactly.

print <<'EOH';
<!DOCTYPE html>
<html>
<head>
<title>Shift JIS Decoding Test</title>
<script type="text/javascript">
  window.onload = function () {
    var table = document.getElementsByTagName ('table')[0];
    var tbody = table.getElementsByTagName ('tbody')[0];
    var trs = tbody.childNodes;
    var trsLength = trs.length;
    var passNumber = 0;
    var passCondNumber = 0;
    var failNumber = 0;
    for (var i = 0; i < trsLength; i++) {
      var tr = trs[i];
      var actualTD = tr.firstChild.nextSibling;
      var actual = actualTD.innerText != null
          ? actualTD.innerText : actualTD.textContent;
      var expectedTD = tr.lastChild;
      var resultTD = expectedTD;
      var expectedClass = expectedTD.className;
      var expected = expectedTD.innerText != null
          ? expectedTD.innerText : expectedTD.textContent;
      var pass = false;
      var passIfDocumented = false;
      if (expectedClass == 'case1') {
        if (actual == "\uFFFD" + expected) {
          pass = true;
        } else if (actual.length > 1 &&
                   actual.substring (actual.length - 1) == '@') {
          passIfDocumented = true;
        }
      } else if (expectedClass == 'case2') {
        if (actual == "\uFFFD\uFFFD@") {
          pass = true;
        } else if (actual.length > 1) {
          passIfDocumented = true;
        }
      } else if (expectedClass == 'case3') {
        if (actual == "\uFFFD\uFFFD@") {
          pass = true;
        } else if (actual.length > 1) {
          passIfDocumented = true;
        }
      } else if (expectedClass == 'case4') {
        if (actual == "\uFFFD" + expected) {
          pass = true;
        } else if ((actual.substring (actual.length - expected.length) == expected ||
                    actual.substring (actual.length - 1) == '@') &&
                   actual.length > 1) {
          passIfDocumented = true;
        }
      } else if (expectedClass == 'case5') {
        if ((expected.length > 0 && actual == "\uFFFD" + expected) || (expected.length == 0 && actual == "\uFFFD\uFFFD") || (expected.length == 0 && actual == "\uFFFD\uFFFD\uFFFD")) {
          pass = true;
        } else if (actual.length > 1) {
          if (actual.substring (actual.length - 1) == '@') {
            passIfDocumented = true;
          } else if (expected.length > 0) {
            if (actual.substring (actual.length - expected.length) == expected) {
              passIfDocumented = true;
            }
          } else {
            passIfDocumented = true;
          }
        }
      } else if (expectedClass == 'case6') {
        if (actual == "\uFFFD@" || actual == "\uFFFD\uFFFD@") {
          pass = true;
        } else if (actual.length > 1 &&
                   actual.substring (actual.length - 1) == '@') {
          passIfDocumented = true;
        }
      } else if (expectedClass == 'case7') {
        if (expected.length > 0 && actual == expected) {
          pass = true;
        } else if (expected.length == 0) {
          if (actual == "\uFFFD@" || actual == "\uFFFD\uFFFD@") {
            pass = true;
          } else if (actual.length > 1 &&
                     actual.substring (actual.length - 1) == '@') {
            passIfDocumented = true;
          }
        }
      } else if (expectedClass == 'case8') {
        if (actual == expected) {
          pass = true;
        } else if (actual == expectedTD.title) {
          passIfDocumented = true;
        }
      } else if (expectedClass == 'case9') {
        if (actual == expected) {
          pass = true;
        } else if (actual == expectedTD.title ||
                   actual == "\uFFFD@" || actual == "\uFFFD\uFFFD@") {
          passIfDocumented = true;
        }
      } else if (expectedClass == 'case10') {
        if (actual == expected) {
          pass = true;
        } else if (actual == "\uFFFD@" || actual == "\uFFFD\uFFFD@") {
          passIfDocumented = true;
        }
      }
      if (pass) {
        resultTD.innerText = 'PASS';
        resultTD.textContent = 'PASS';
        resultTD.className = 'PASS';
        passNumber++;
      } else if (passIfDocumented) {
        resultTD.innerText = 'PASS if documented and consistent';
        resultTD.textContent = 'PASS if documented and consistent';
        resultTD.className = 'PASS-conditional';
        passCondNumber++;
      } else {
        var text = 'FAIL (' + encodeURIComponent (actual) + ')';
        resultTD.innerText = text;
        resultTD.textContent = text;
        resultTD.className = 'FAIL';
        failNumber++;
      }
    }
    var result = document.getElementById ('result');
    if (failNumber > 0) {
      var text = 'FAIL (' + failNumber + ' tests failed';
      if (failNumber + passNumber + passCondNumber != testNumber) {
        text += '; ' + (failNumber + passNumber + passCondNumber) +
           ' tests run while ' + testNumber + ' tests expected';
      }
      text += ')';
      result.innerText = text;
      result.textContent = text;
      result.className = 'FAIL';
    } else if (passNumber + passCondNumber != testNumber) {
      var text = 'FAIL (' + (passNumber + passCondNumber) +
           ' tests run while ' + testNumber + ' tests expected';
      result.innerText = text;
      result.textContent = text;
      result.className = 'FAIL';
    } else if (passCondNumber > 0) {
      result.innerText = 'PASS if documented and consistent';
      result.textContent = 'PASS if documented and consistent';
      result.className = 'PASS-conditional';
    } else {
      result.innerText = 'PASS';
      result.textContent = 'PASS';
      result.className = 'PASS';
    }
  };
</script>
<style type="text/css">
  .PASS {
    color: green;
  }
  .PASS-conditional {
    color: blue;
  }
  .FAIL {
    color: red;
  }
</style>
</head>
<body>
<p id="result" class="FAIL">FAIL (not executed)</p>
EOH
print "<table><tbody>";

my $i = 0;

$Table->{0x00} = 0xFFFD;
$Table->{0x0D} = 0x000A;
$Table->{0x8150} = 0xFFFD; # FULLWIDTH OVERLINE

if ($range == 0) {
  for (0x00..0x7F, 0xA1..0xDF) {
    printf q[<tr><th scope="row">0x%02X</th><td>%s</td><td class="case7">&#%d;</td></tr>],
        $_, chr $_, $Table->{$_};
    $i++;
  }
}

my @range;
if ($range < 0x10 and $range > 0x7) {
  push @range, $range * 0x10 + $_ for 0x0..0xF;
}
if ($range == 0xA) {
  @range = (0xA0)
}
for my $s1 (@range) {
  for my $s2 (0x00..0xFF) {
    if ($s1 == 0x80 or $s1 == 0xA0 or $s1 > 0xEF) {
      if ($s2 < 0x40 or $s2 == 0x7F or (0xA1 <= $s2 and $s2 <= 0xDF)) {
        ## PASS: ($s1=undefined)($s2)(@)
        ## PASS if documented: ($s1=char)($s2)(@)
        ## PASS if documented: ($s1,$s2=undefined/char)(@)
        printf q[<tr><th scope="row">0x%02X%02X</th><td>%s%s@</td><td class="case1">&#%d;@</td></tr>],
            $s1, $s2, (pack 'C', $s1), (pack 'C', $s2), $Table->{$s2};
      } elsif ($s2 > 0xFC) {
        ## PASS: ($s1=undefined)($s2=undefined)(@)
        ## PASS if documented: ($s1=undefined/char)($s2=undefined/char)(@)
        ## PASS if documented: ($s1=undefined/char)($s2,0x40=undefined/char)
        ## PASS if documented: ($s1,$s2=undefined/char)(@)
        printf q[<tr><th scope="row">0x%02X%02X</th><td>%s%s@</td><td class="case2"></td></tr>],
            $s1, $s2, (pack 'C', $s1), (pack 'C', $s2);
      } elsif ($s2 == 0x80 or $s2 > 0xEF) {
        ## PASS: ($s1=undefined)($s2=undefined)(@)
        ## PASS if documented: ($s1=undefined/char)($s2=undefined/char)(@)
        ## PASS if documented: ($s1=undefined/char)($s2,0x40=undefined/char)
        ## PASS if documented: ($s1,$s2=undefined/char)(@)
        printf q[<tr><th scope="row">0x%02X%02X</th><td>%s%s@</td><td class="case3"></td></tr>],
            $s1, $s2, (pack 'C', $s1), (pack 'C', $s2);
      } elsif ($s2 < 0x7F) {
        ## PASS: ($s1=undefined)($s2=char)(@)
        ## PASS if documented: ($s1=char)($s2=char)(@)
        ## PASS if documented: ($s1,$s2=undefined/char)(@)
        printf q[<tr><th scope="row">0x%02X%02X</th><td>%s%s@</td><td class="case4">&#%d;@</td></tr>],
            $s1, $s2, (pack 'C', $s1), (pack 'C', $s2),
            $Table->{$s2};
      } else { # $s2 in [0x81, 0x9F] or [0xE0, 0xEF]
        ## PASS: ($s1=undefined)($s2,0x40=undefined/char)
        ## PASS if documented: ($s1=char)($s2,0x40=undefined/char)
        ## PASS if documented: ($s1,$s2=undefined/char)(@)
        printf q[<tr><th scope="row">0x%02X%02X</th><td>%s%s@</td><td class="case5">%s</td></tr>],
            $s1, $s2, (pack 'C', $s1), (pack 'C', $s2),
            $Table->{$s2 * 0x100 + 0x40}
                ? '&#' . $Table->{$s2 * 0x100 + 0x40} . ';' : '';
        ## NOTE: $table3..$table6 has no entry with 0x??40
      }
    } else {
      if ($s2 < 0x40 or $s2 == 0x7F or $s2 > 0xFC) {
        ## PASS: ($s1,$s2=undefined/char)(@)
        printf q[<tr><th scope="row">0x%02X%02X</th><td>%s%s@</td><td class="case6"></td></tr>],
            $s1, $s2, (pack 'C', $s1), (pack 'C', $s2);
      } else {
        if ($table3->{$s1 * 0x100 + $s2}) {
          ## PASS: ($s1,$s2=char)(@)
          ## PASS if documented: ($s1,$s2=alternate)(@)
          printf q[<tr><th scope="row">0x%02X%02X</th><td>%s%s@</td><td class="case8" title="&#%s;@">&#%s;@</td></tr>],
              $s1, $s2, (pack 'C', $s1), (pack 'C', $s2),
              $Table->{$table3->{$s1 * 0x100 + $s2}},
              $Table->{$s1 * 0x100 + $s2};
        } elsif ($table5->{$s1 * 0x100 + $s2}) {
          ## PASS: ($s1,$s2=char)(@)
          ## PASS if documented: ($s1,$s2=alternate)(@)
          ## PASS if documented: ($s1,$s2=undefined)(@)
          printf q[<tr><th scope="row">0x%02X%02X</th><td>%s%s@</td><td class="case9" title="&#%s;@">&#%s;@</td></tr>],
              $s1, $s2, (pack 'C', $s1), (pack 'C', $s2),
              $Table->{$table5->{$s1 * 0x100 + $s2}},
              $Table->{$s1 * 0x100 + $s2};
        } elsif ($table4->{$s1 * 0x100 + $s2} or $table5->{$s1 * 0x100 + $s2}) {
          ## PASS: ($s1,$s2=char)(@)
          ## PASS if documented: ($s1,$s2=undefined)(@)
          printf q[<tr><th scope="row">0x%02X%02X</th><td>%s%s@</td><td class="case10">&#%s;@</td></tr>],
              $s1, $s2, (pack 'C', $s1), (pack 'C', $s2),
              $Table->{$s1 * 0x100 + $s2};
        } else {
          ## PASS: ($s1,$s2=undefined/char)(@)
          printf q[<tr><th scope="row">0x%02X%02X</th><td>%s%s@</td><td class="case7">%s</td></tr>],
              $s1, $s2, (pack 'C', $s1), (pack 'C', $s2),
              $Table->{$s1 * 0x100 + $s2}
                  ? '&#'.$Table->{$s1 * 0x100 + $s2}.';@' : '';
        }
      }
    }
    $i++;
  }
}

print <<"EOH";
</tbody></table>
<script type="text/javascript">
  window.testNumber = $i;
</script>
</body>
</html>
EOH
