function setResult (id, value) {
  var rel = document.getElementById (id);
  if (value == null) {
    rel.textContent = '(null)';
    rel.innerText = '(null)';
  } else if (value == '') {
    rel.textContent = '(empty)';
    rel.innerText = '(empty)';
  } else {
    rel.textContent = '';
    rel.innerText = '';
    rel.appendChild (document.createElement ('code'))
       .appendChild (document.createTextNode
                                (value.replace (/&/, '&amp;')
                                      .replace (/\u0009/, '&#x09;')
                                      .replace (/\u0020/, '&#x20;')
                                      .replace (/\u000A/, '&#x0A;')
                                      .replace (/\u000D/, '&#x0D;')));
  }
}
