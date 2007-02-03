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
