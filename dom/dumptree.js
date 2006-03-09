function dumptree (code) {
  var resultRoot = document.getElementById ('test-result');
  var node;
  try {
    node = code ();
    dumpnode (node, resultRoot);
  } catch (e) {
    resultRoot.appendChild (document.createTextNode (e));
  }

  var testCode = document.getElementById ('test-code');
  var testCodeText = testCode.textContent ? testCode.textContent
                                          : testCode.innerText;
  resultRoot.appendChild (document.createElement ('pre'))
          .appendChild (document.createTextNode (testCodeText));
} /* dumptree */

function dumpnode (node, parent) {
  parent.appendChild (document.createElement ('strong'))
        .appendChild (document.createTextNode (node.nodeName));
  var docl = parent.appendChild (document.createElement ('dl'));
  addinfo (docl, 'nodeType', document.createTextNode (node.nodeType));
  addinfo (docl, 'nodeValue', node.nodeValue == null
                                ? document.createTextNode ('(null)')
                                : document.createTextNode (node.nodeValue));
  if (node.childNodes.length > 0) {
    addinfo (docl, 'childNodes');
    for (var i = 0; i < node.childNodes.length; i++) {
      var ddel = docl.appendChild (document.createElement ('dd'));
      dumpnode (node.childNodes[i], ddel);
    }
  }
} /* dumpnode */

function addinfo (parent, dttext, dd) {
  parent.appendChild (document.createElement ('dt'))
        .appendChild (document.createTextNode (dttext));
  if (dd) {
    var ddel = parent.appendChild (document.createElement ('dd'));
    ddel.appendChild (dd);
  }
} /* addinfo */

