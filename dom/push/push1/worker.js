skipWaiting ();

addEventListener ('push', function (ev) {
  var p = registration.showNotification ("pushed! 3 " + new Date);
  ev.waitUntil (p);
});