function setResult (id, value) {
  var rel = document.getElementById (id);
  rel.textContent = 'FAIL (script error)';
  rel.innerText = 'FAIL (script error)';
  rel.setAttributeNS (null, 'class', 'FAIL'); // NOTE: 'className' setter does not work in Firefox 2.
  var valueType = typeof value;
  if (value === undefined) {
    rel.textContent = '(undefined)';
    rel.innerText = '(undefined)';
  } else if (value === null) {
    rel.textContent = '(null)';
    rel.innerText = '(null)';
  } else if (value === '') {
    rel.textContent = '(empty)';
    rel.innerText = '(empty)';
  } else {
    value = '' + value;
    rel.textContent = '';
    rel.innerText = '';
    rel.appendChild (document.createElementNS
        ('http://www.w3.org/2000/svg', 'tspan'))
       .appendChild (document.createTextNode
                                (value.replace (/&/g, '&amp;')
                                      .replace (/\u0009/g, '&#x09;')
                                      .replace (/\u000A/g, '&#x0A;')
                                      .replace (/\u000D/g, '&#x0D;')));
  }
  rel.appendChild (document.createTextNode (', type ' + valueType));
  rel.setAttributeNS (null, 'class', 'see-detail');
}
