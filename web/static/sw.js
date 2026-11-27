// Fintra service worker
// 🔐 Кэшируем ТОЛЬКО статические файлы и офлайн-страницу.
// Страницы с финансовыми данными (расходы, план, чат, API) никогда не сохраняются на телефоне.
const CACHE = "fintra-static-v1";
const STATIC_FILES = ["/static/offline.html", "/static/icon-192.png", "/static/logo-icon.png"];

self.addEventListener("install", (event) => {
  event.waitUntil(caches.open(CACHE).then((cache) => cache.addAll(STATIC_FILES)));
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  // Удаляем старые версии кэша
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener("fetch", (event) => {
  const request = event.request;
  if (request.method !== "GET") return;          // POST (формы, чат) идут напрямую на сервер

  // Открытие страницы: всегда из сети, а без интернета — офлайн-страница
  if (request.mode === "navigate") {
    event.respondWith(fetch(request).catch(() => caches.match("/static/offline.html")));
    return;
  }

  // Статические файлы из нашего списка: сначала кэш
  const url = new URL(request.url);
  if (url.origin === location.origin && STATIC_FILES.includes(url.pathname)) {
    event.respondWith(caches.match(request).then((cached) => cached || fetch(request)));
  }
  // Всё остальное (данные, графики, API) — только из сети, без кэша
});
