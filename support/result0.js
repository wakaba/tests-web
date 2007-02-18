function htescape (s) {
  return s.replace ('&', '&amp;').replace ('<', '&lt;');
} // htescape

function writeResult (value) {
  if (typeof (value) == 'undefined') {
    document.write ('<code>undefined</code>');
  } else if (value == null) {
    document.write ('<code>null</code>');
  } else if (value.toString) {
    var vString = value.toString ();
    if (vString == '') {
      document.write ('An empty string');
    } else {
      document.write ('<code>' + htescape (vString) + '</code>');
    }
    document.write (', type <code>' + htescape (typeof (value)) + '</code>');
  } else {
    var vString = '' + value;
    if (vString == '') {
      document.write ('An empty string');
    } else {
      document.write ('<code>' + htescape (vString) + '</code>');
    }
    document.write (', type <code>' + htescape (typeof (value)) + '</code>');
  }
} // writeResult

function setValueResult (obj, value) {
  var rvalue = '';
  if (typeof (value) == 'undefined') {
    rvalue = 'undefined';
  } else if (value == null) {
    rvalue = 'null';
  } else if (value.toString) {
    var vString = value.toString ();
    if (vString == '') {
      rvalue = 'An empty string';
    } else {
      rvalue = vString.replace (/%/, '%25').replace (/\u000D/, '%0D')
          .replace (/\u000A/, '%0A').replace (/\u000C/, '%0C');
    }
    rvalue += ', type ' + typeof (value);
  } else {
    var vString = '' + value;
    if (vString == '') {
      rvalue = 'An empty string';
    } else {
      rvalue = vString.replace (/%/, '%25').replace (/\u000D/, '%0D')
          .replace (/\u000A/, '%0A').replace (/\u000C/, '%0C');
    }
    rvalue += ', type ' + typeof (value);
  }
  obj.value = rvalue;
} // setValueResult
