// Banco Arduino: funciona sin internet y se actualiza solo cuando hay conexión.
const CACHE = 'banco-arduino-v1';
const FILES = ['./', './index.html', './manifest.webmanifest', './icono-192.png', './icono-512.png'];
self.addEventListener('install', e => { e.waitUntil(caches.open(CACHE).then(c => c.addAll(FILES)).then(() => self.skipWaiting())); });
self.addEventListener('activate', e => { e.waitUntil(self.clients.claim()); });
self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET' || new URL(req.url).origin !== location.origin) return;
  // primero intenta la versión nueva de GitHub; si no hay internet, usa la guardada
  e.respondWith(fetch(req, {cache: 'no-store'}).then(res => {
    if (res.ok){ const copy = res.clone(); caches.open(CACHE).then(c => c.put(req, copy)); }
    return res;
  }).catch(() => caches.match(req).then(r => r || caches.match('./index.html'))));
});
