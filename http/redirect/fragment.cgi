#!/usr/bin/perl
use strict;
use CGI;

my $path = $ENV{SCRIPT_NAME};
$path =~ s#[^/]+$##;

print "Status: @{[CGI::param('status')+0 || 302]} Redirection\n";
print "Location: http://$ENV{SERVER_NAME}:$ENV{SERVER_PORT}${path}redirected.ja.html#fragment\n";

print <<EOH;
Content-Type: text/html; charset=us-ascii

<!DOCTYPE html SYSTEM>
<html>
<title>HTTP Redirection with URI fragment identifier</title>
<body>
<p>See redirected URI (shown in Location header field)</p>
</body>
</html>
EOH

