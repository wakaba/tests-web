<!DOCTYPE html>
<title>&lt;a ping></title>

<p><a href ping=/httplog/@@RAND(1)@@/logging target=testframe>Link</a>
<iframe hidden name=testframe></iframe>

<p><button type=button onclick="
  window.result.location.reload ();
">Reload</button>
<p><iframe src=/httplog/@@RAND(1)@@/ndjson.txt name=result></iframe>
