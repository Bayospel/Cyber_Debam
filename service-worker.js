self.addEventListener('install', (e) => {
  console.log('Debam Service Worker Installed');
});

self.addEventListener('fetch', (e) => {
  e.respondWith(fetch(e.request));
});
