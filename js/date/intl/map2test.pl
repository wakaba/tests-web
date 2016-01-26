use strict;
use warnings;
use Encode;
binmode STDOUT, qw(:encoding(utf-8));

local $/ = undef;
my $data = decode 'utf-8', <>;

print q{<!DOCTYPE HTML>
<title>ja-JP-u-ca-japanese</title>
<style>
  .PASS { background-color: green; color: white }
  .FAIL { background-color: red; color: white }
</style>

<table>
<thead>
  <tr>
    <th>Date
    <th>Era
    <th>Year
<tbody>};

for (split /\n/, $data) {
  next unless length;
  my ($g, $v) = split /\t/, $_;
  if ($v =~ /^(\S+) (\d+)$/) {
    printf q{<tr><th><code>%s</code><td data-value="%s"><td data-value="%d">},
        $g, $1, $2;
  }
}

print q{</table>
<script>
  function ymd2n (y, m, d) {
    var month = (m - 1 + 10) % 12;
    var year = y - Math.floor (month / 10);
    return 1000*60*60*24*
           ((365 * year)
            + Math.floor (year/4)
            - Math.floor (year/100)
            + Math.floor (year/400)
            + Math.floor (((month * 306) + 5) / 10)
            + d) - 62162121600000;
  } // ymd2n

  var rows = document.querySelector ('tbody').rows;
  Array.prototype.forEach.call (rows, function (row) {
    var date = row.cells[0].firstChild.textContent;
    var m = date.match (/^(-?[0-9]+)-([0-9]+)-([0-9]+)$/);
    var d = new Date (ymd2n (parseInt (m[1]), parseInt (m[2]), parseInt (m[3])));
    var result = d.toLocaleString ("ja-JP-u-ca-japanese", {timeZone: 'UTC'});
    var n = result.match (/^([^\d-]*)(-?[0-9]+)/);
    var eraCell = row.cells[1];
    var expectedEra = eraCell.getAttribute ('data-value');
    if (n[1] === expectedEra) {
      eraCell.textContent = 'PASS';
      eraCell.className = 'PASS';
    } else {
      eraCell.textContent = 'FAIL ('+n[1]+', expected: '+expectedEra+')';
      eraCell.className = 'FAIL';
    }
    var yearCell = row.cells[2];
    var expectedYear = parseInt (yearCell.getAttribute ('data-value'));
    if (parseInt (n[2]) === expectedYear) {
      yearCell.textContent = 'PASS';
      yearCell.className = 'PASS';
    } else {
      yearCell.textContent = 'FAIL ('+n[2]+', expected: '+expectedYear+')';
      yearCell.className = 'FAIL';
    }
  });
</script>
};
