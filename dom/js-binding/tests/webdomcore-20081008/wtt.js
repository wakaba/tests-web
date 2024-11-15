
function WttFail () {
  //
} // WttFail

function WttSkip (message) {
  this.message = message;
} // WttSkip

function wttGetGlobal () {
  return window;
} // wttGetGlobal

function wttAssertTrue (condition, localId) {
  if (!condition) {
    wttSetStatus ('FAIL', localId + ' false (true expected)');
    throw new WttFail ();
  }

  // condition is true.
} // wttAssertTrue


function wttAssertFalse (condition, localId) {
  if (condition) {
    wttSetStatus ('FAIL', localId + ' true (false expected)');
    throw new WttFail ();
  }

  // condition is true.
} // wttAssertFalse

function wttAssertEquals (actual, expected, localId) {
  if (actual !== expected) {
    wttSetStatus ('FAIL', localId + ' got ' + dumpValue (actual) +
                  ' where ' + dumpValue (expected) + ' is expected');
    throw new WttFail ();
  }
  
  // actual === expected
} // wttAssertEquals

function wttAssertDontEnum (object, propName, localId) {
  for (var n in object) {
    if (n === propName) {
      wttSetStatus ('FAIL', localId + ' (DontEnum expected)');
      throw new WttFail ();
    }
  }
  
  // object[propName] is {DontEnum}.
} // wttAssertDontEnum

function wttAssertDontDelete (object, propName, localId) {
  var propValue = object[propName];
  
  if (!delete object[propName]) {
    wttSetStatus ('FAIL', localId + ' (delete returns true)');
    throw new WttFail ();
    // According to ECMA 262, [[Delete]] returns false if DontDelete is set.
  }

  if (!(propName in object)) {
    wttSetStatus ('FAIL', localId + ' (delete does delete the property)');
    throw new WttFail ();
  }

  if (object[propName] !== propValue) {
    wttSetStatus ('FAIL', localId + ' (delete change the value to ' +
                  dumpValue (object[propName]) + ' where ' +
                  dumpValue (propValue) + ' is expected)');
    throw new WttFail ();
    
    /* The WebIDL specification does not change semantics of the
       [[Delete]] internal method from the ECMA 262 3rd edition.
       In ECMA 262, [[Delete]] does not do anything except for returning
       a |false| value in case the {DontDelete} attribute is set to the
       attribute.  Therefore, the property value must not be changed
       before and after the |delete| operation, which just invokes the
       [[Delete]] method.
    */
  }
} // wttAssertDontDelete

function wttAssertReadOnly (object, propName, localId) {
  /*
    Note that this function returns a wrong result when the [[Put]]
    or [[CanPut]] method of /object/ is replaced by another steps
    from those defined in ECMA 262.  According to WebIDL spec,
    objects conforming to that specification does not modify those
    methods unless explicitly defined (e.g. for objects with [NamedSetter]).
  */

  var propValue = object[propName];

  try {
    object[propName] = 'abcdefg';
  } catch (e) {
    /* 
      According to the [[Put]] algorithms of ECMA 262 and WebIDL, assigning
      a value to a read-only property should not raise an exception.
      However, since testing the behavior of [[Put]] is not the purpose of
      this test, we catch any exception thrown by the assignment.
      Note that it might also catch any exception thrown by non-standard
      setter extension, if any.
    */
  }
  if (object[propName] === 'abcdefg') {
    wttSetStatus ('FAIL', localId + ' (value changed)');
    throw new WttFail ();
  }
  
  if (object[propName] !== propValue) {
    wttSetStatus ('FAIL', localId + ' (putting changes value from ' +
                  dumpValue (propValue) + ' to ' +
                  dumpValue (object[propName]) + ')');
    throw new WttFail ();
  }

  // The property seems read only.
} // wttAssertReadOnly

function wttOk () {
  wttSetStatus ('PASS');
} // wttOk

function wttSetStatus (s, t) {
  var result = document.getElementById ('result');
  result.firstChild.data
      = s + ' (' + globalId + (t != null ? '-' + t : '') + ')';
  result.className = s;
} // wttSetStatus

function dumpValue (v) {
  return '"' + v + '", type ' + typeof (v);
} // dumpValue


var wttInstanceInfo = {
  "DOMException": [
    {
      "id": "append-child-hierarchy",
      "code": " var a = document.createElement ('a'); var b = document.createElement ('b'); a.appendChild (b); var x = null; try { b.appendChild (a); } catch (e) { x = e; } x;"
    }
  ],
  "DOMImplementation": [
    {
      "id": "implementation",
      "code": "document.implementation;"
    }
  ],
  "DocumentFragment": [
    {
      "id": "create-document-fragment",
      "code": "document.createDocumentFragment ();"
    }
  ],
  "Document": [
    {
     "id": "create-document",
     "code": " document.implementation.createDocument (null, null, null); "
    },
    {
     "id": "document",
     "code": " document; "
    }
  ],
  "NodeList": [
    {
     "id": "get-elements-by-tag-name",
     "code": "document.getElementsByTagName ('*');"
    },
    {
     "id": "get-elements-by-tag-name-ns",
     "code": "document.getElementsByTagNameNS ('*', '*');"
    },
    {
     "id": "child-nodes",
     "code": "document.body.childNodes;"
    }
  ],
  "NamedNodeMap": [
    {
     "id": "attributes",
     "code": "document.body.attributes;"
    }
  ],
  "Attr": [
    {
     "id": "get-attribute",
     "code": "document.getElementById ('result').getAttributeNode ('id');"
    }
  ],
  "Element": [
    {
     "id": "create-element",
     "code": "document.createElement ('test');"
    },
    {
     "id": "create-element-ns",
     "code": "document.createElementNS (null, 'test');"
    }
  ],
  "Text": [
    {
     "id": "create-text-node",
     "code": "document.createTextNode ('xyz');"
    }
  ],
  "Comment": [
    {
     "id": "create-comment",
     "code": "document.createComment ('xyz');"
    }
  ],
  "DocumentType": [
    {
     "id": "create-document-type",
     "code": "document.implementation.createDocumentType ('html', null, null);"
    },
    {
     "id": "create-document-create-document-type",
     "code": "document.implementation.createDocument (null, null, null).implementation.createDocumentType ('a', null, null);"
    }
  ],
  "ProcessingInstruction": [
    {
     "id": "create-pi",
     "code": "document.createProcessingInstruction ('a', 'b');"
    },
    {
     "id": "create-document-create-pi",
     "code": "document.implementation.createDocument (null, null, null).createProcessingInstruction ('a', 'b');"
    }
  ],
  "_crash": {
    "node-instance-create-document-type-attr-child-nodes-dont-delete": [
      "AppleWebKit/525\\.1[3-9]"
    ],
    "node-instance-create-document-type-attr-child-nodes-read-only": [
      "AppleWebKit/525\\.1[3-9]"
    ],
    "node-instance-create-document-create-document-type-attr-child-nodes-dont-delete": [
      "AppleWebKit/525\\.1[3-9]"
    ],
    "node-instance-create-document-create-document-type-attr-child-nodes-read-only": [
      "AppleWebKit/525\\.1[3-9]"
    ]
  }
}
;
function wttGetInstance (interface, id) {
  var giCodes = wttInstanceInfo[interface];
  if (!giCodes) {
    wttSetStatus ('FAIL',
                  'broken testcase - no code for ' + interface + ' ' + id);
    throw new WttFail ();
  }
  
  for (var i in giCodes) {
    if (giCodes[i].id == id) {
      var v;
      var message;
      try {
        v = eval (giCodes[i].code);
      } catch (e) {
        v = null;
        message = '' + e;
      }
      if (!v) {
        throw new WttSkip ('cannot obtain instance by ' + id +
                           (message ? ' (' + message + ')' : ''));
      }
      return v;
    }
  }

  if (!giCodes) {
    wttSetStatus ('FAIL',
                  'broken testcase - no code for ' + interface + ' ' + id);
    throw new WttFail ();
  }
} // wttGetInstance

var crashInfo = {"node-instance-create-document-type-attr-child-nodes-read-only":["AppleWebKit/525\\.1[3-9]"],"node-instance-create-document-type-attr-child-nodes-dont-delete":["AppleWebKit/525\\.1[3-9]"],"node-instance-create-document-create-document-type-attr-child-nodes-dont-delete":["AppleWebKit/525\\.1[3-9]"],"node-instance-create-document-create-document-type-attr-child-nodes-read-only":["AppleWebKit/525\\.1[3-9]"]};
function wttCheckCrash (testId) {
  var entry = crashInfo[testId];
  if (!entry) return;

  var ua = navigator.userAgent;
  for (var i = 0; i < entry.length; i++) {
    var reg = new RegExp (entry[i]);
    if (ua.match (reg)) {
      wttSetStatus ('FAIL',
                    'Skipped because it is known that this test case would crash the browser in use');
      throw new WttFail ();
    }
  }
} // wttCheckCrash

