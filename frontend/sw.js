const CACHE_NAME = 'grahak-kavach-v3';
const ASSETS_TO_CACHE = [
  '/',
  '/index.html',
  '/scan.html',
  '/history.html',
  '/complaint.html',
  '/officer-login.html',
  '/officer-dashboard.html',
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
    fetch(event.request)
      .then((response) => {
        // Network success: cache the new response and return it
        const responseClone = response.clone();
        caches.open(CACHE_NAME).then((cache) => {
          cache.put(event.request, responseClone);
        });
        return response;
      })
      .catch(() => {
        // Network failure (offline): fallback to cache
        return caches.match(event.request);
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
