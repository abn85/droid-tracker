self.addEventListener('push', function(event) {
  const data = event.data ? event.data.json() : {};
  const title = data.title || "New Droid Deal on gonk.tools!";
  const options = {
    body: data.body || "A new limited deal is live!",
    icon: 'icon.png'
  };
  
  event.waitUntil(
    self.registration.showNotification(title, options)
  );
});
