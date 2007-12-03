#!/usr/bin/perl
use strict;

$| = 1;

print "Content-Type: text/html; charset=us-ascii\n\n";

print q[<!DOCTYPE HTML><html>
<head>
<style>
table {
  table-layout: fixed;
}
td {
  border: 1px black solid;
}
</style>
<title>table-layout: fixed</title>
</head>
<body>
<h1><code>table-layout: fixed</code></h1>

<table>
<tr><td style="width: 1em">X<td style="width: 2em">Y<td style="width: 4em">Z</tr>];

sleep (5);

print q[<tr><td>A<td>B<td>C</tr>];

sleep (5);

print q[<tr><td>I<td>J<td>K</tr>];

sleep (5);

print q[<tr><td>L<td>M<td>N</tr>];

sleep (5);

print q[</table><p><code>&lt;/table></code></p></body></html>];
