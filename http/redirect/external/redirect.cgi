#!/usr/bin/perl
use strict;

my $path = $ENV{SCRIPT_NAME};
$path =~ s#[^/]+$##;

my $query = $ENV{QUERY_STRING};
$query =~ s/([^0-9A-Za-z_.-])//gs;

print <<EOH;
Status: 302 Found
Location: http://$ENV{SERVER_NAME}:$ENV{SERVER_PORT}${path}dir/$query

EOH
