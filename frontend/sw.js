const CACHE_NAME = 'grahak-kavach-v2';
const ASSETS_TO_CACHE = [
  '/',
  '/index.html',
  '/scan.html',
  '/history.html',
  '/complaint.html',
  '/officer-login.html',
  '/officer-dashboard.html',
  '/css/style.css',
  '/css/glassmorphism.css',
  '/js/main.js',
  '/js/api.js',
  '/assets/logo.svg'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(ASSETS_TO_CACHE);
    })
  );
});

self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;
  // Ignore API requests and non-http/https schemes (like chrome-extension://)
  if (event.request.url.includes('/api/')) return;
  if (!event.request.url.startsWith('http')) return;
  
  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      if (cachedResponse) {
        return cachedResponse;
      }
      return fetch(event.request).then((response) => {
        return caches.open(CACHE_NAME).then((cache) => {
          cache.put(event.request, response.clone());
          return response;
        });
      });
    })
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((name) => {
          if (name !== CACHE_NAME) {
            return caches.delete(name);
          }
        })
      );
    })
  );
});
