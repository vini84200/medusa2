var CACHE_NAME = 'medusa2-v1';
var urlsToCache = [
  '/base_layout',
];

// Baixa para o cache dados novos
self.addEventListener('install', function(event) {
  // Perform install steps
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function(cache) {
        console.log('Opened cache');
        return cache.addAll(urlsToCache);
      })
  );
});

// Apaga Cache que de versões antigas.
caches.keys().then(function(cacheNames) {
  return Promise.all(
    cacheNames.map(function(cacheName) {
      if(cacheName != CACHE_NAME) {
        return caches.delete(cacheName);
      }
    })
  );
});

//self.addEventListener('fetch', function(event) {
//  var requestUrl = new URL(event.request.url);
//    if (requestUrl.origin === location.origin) {
//      if ((requestUrl.pathname === '/')) {
//        event.respondWith(caches.match('/base_layout'));
//        return;
//      }
//    }
//    event.respondWith(
//      caches.match(event.request).then(function(response) {
//        return response || fetch(event.request);
//      })
//    );
//});