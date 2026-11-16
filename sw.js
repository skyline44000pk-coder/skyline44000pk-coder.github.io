const CACHE_NAME="skyline-app-v5";
const APP_SHELL=["/","/index.html","/marketplace.html","/properties.html","/services.html","/materials-guide.html","/project-guide.html","/resources.html","/public-tools.html","/pakistan-guide.html","/property-tax.html","/construction-quotation.html","/manifest.webmanifest","/skyline-logo.png","/app-icon.svg"];
self.addEventListener("install",event=>{
  event.waitUntil(caches.open(CACHE_NAME).then(cache=>cache.addAll(APP_SHELL)).then(()=>self.skipWaiting()));
});
self.addEventListener("activate",event=>{
  event.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(key=>key!==CACHE_NAME).map(key=>caches.delete(key)))).then(()=>self.clients.claim()));
});
self.addEventListener("fetch",event=>{
  const request=event.request;
  if(request.method!=="GET"||new URL(request.url).origin!==self.location.origin)return;
  event.respondWith(fetch(request).then(response=>{
    if(response&&response.ok){const copy=response.clone();caches.open(CACHE_NAME).then(cache=>cache.put(request,copy));}
    return response;
  }).catch(()=>caches.match(request).then(cached=>cached||caches.match("/index.html")));
});
