importScripts('https://storage.googleapis.com/workbox-cdn/releases/4.2.0/workbox-sw.js');

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
//Workbox
if (workbox) {
  workbox.googleAnalytics.initialize();
  workbox.routing.registerRoute(
    /\.js$/,
    new workbox.strategies.StaleWhileRevalidate({
      cacheName:'js-medusaii'
    })
  );
  workbox.routing.registerRoute(
    'https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css',
    new workbox.strategies.StaleWhileRevalidate()
  );
  workbox.routing.registerRoute(
    'https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css',
    new workbox.strategies.StaleWhileRevalidate()
  );
  workbox.routing.registerRoute(
    'https://use.fontawesome.com/releases/v5.8.1/css/all.css',
    new workbox.strategies.StaleWhileRevalidate()
  );
  workbox.routing.registerRoute(
    'https://code.jquery.com/jquery-3.3.1.slim.min.js',
    new workbox.strategies.StaleWhileRevalidate()
  );
  workbox.routing.registerRoute(
    'https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js',
    new workbox.strategies.StaleWhileRevalidate()
  );
  workbox.routing.registerRoute(
    'https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js',
    new workbox.strategies.StaleWhileRevalidate()
  );
  workbox.routing.registerRoute(
    /\.css$/,
    // Use cache but update in the background.
    new workbox.strategies.StaleWhileRevalidate({
      // Use a custom cache name.
      cacheName: 'css-medusaii',
    })
  );
  workbox.routing.registerRoute(
  // Cache image files.
  /\.(?:png|jpg|jpeg|svg|gif|woff2)$/,
  // Use the cache if it's available.
  new workbox.strategies.CacheFirst({
    // Use a custom cache name.
    cacheName: 'image-medusaii',
    plugins: [
      new workbox.expiration.Plugin({
        // Cache only 20 images.
        maxEntries: 20,
        // Cache for a maximum of a week.
        maxAgeSeconds: 7 * 24 * 60 * 60,
        })
      ],
    })
  );
} else {
  console.log('Boo! Workbox didnt load.');
}

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
