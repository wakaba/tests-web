#!/usr/bin/perl
use strict;
use warnings;

$| = 1;

print qq[Content-Type: text/html; charset=utf-8

<!DOCTYPE HTML>
<html style="border: blue 0.5em solid; padding: 0.5em; cursor: pointer"
    onclick="
      var head = document.createElement ('head');
      head.setAttribute ('style', 'border: orange 0.5em solid; padding: 0.5em; display: block; margin: 0.5em');
      head.setAttribute ('data-source', 'html/\@onclick');
      document.documentElement.appendChild (head);
    ">];

sleep 2;

print qq[<head data-source="html/head" style="border: blue 0.5em solid; padding: 0.5em; display: block; margin: 0.5em">];

sleep 2;

print q[<body style="border: blue 0.5em solid; padding: 0.5em; margin: 0.5em">];

sleep 2;

print q[<p><a href="javascript:alert (document.innerHTML || document.documentElement.outerHTML || document.documentElement.innerHTML)">Check DOM of this page!</a>];

print q[<p>] . rand;
