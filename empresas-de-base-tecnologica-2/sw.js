// Generado por armar.py: no editar a mano.
// Precachea el apunte completo. La version del cache sale del hash del
// contenido: el archivo solo cambia cuando cambia algo, y ahi el navegador
// reinstala el service worker y renueva el cache en la visita siguiente.
const CACHE = 'ebt2-530f40ffe188';
const ARCHIVOS = [
  "./",
  "./index.html",
  "./manifest.webmanifest",
  "./icon.svg",
  "./icon-192.png",
  "./icon-512.png",
  "./apple-touch-icon.png",
  "./img/etapas-crecimiento-startup.png",
  "./img/incoterms-responsabilidad.png",
  "./img/innovacion-abierta-vs-cerrada.png",
  "./img/lean-canvas-desde-bmc.png",
  "./img/lean-canvas.png",
  "./img/modelo-innovacion-abierta.png"
];

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(CACHE)
    .then((c) => c.addAll(ARCHIVOS))
    .then(() => self.skipWaiting()));
});

self.addEventListener('activate', (e) => {
  // El CacheStorage es por origen, no por scope: se borran solo los caches
  // viejos de ESTA materia, sin pisar los de los otros apuntes.
  e.waitUntil(caches.keys()
    .then((claves) => Promise.all(claves
      .filter((k) => k.startsWith('ebt2-') && k !== CACHE)
      .map((k) => caches.delete(k))))
    .then(() => self.clients.claim()));
});

self.addEventListener('fetch', (e) => {
  if (e.request.method !== 'GET') return;
  e.respondWith(caches.match(e.request, { ignoreSearch: true })
    .then((r) => r || fetch(e.request)));
});
