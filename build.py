# Rakentaa: dist/ (GitHub Pages -versio) ja artifact.html (esikatselu).
import pathlib, json
root = pathlib.Path(__file__).parent
app = (root/"src/app.html").read_text().replace("/*SPECIES*/", (root/"src/species.js").read_text())

dist = root
head = ('<!doctype html><html lang="fi"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
        '<meta name="theme-color" content="#2c5c4c"><link rel="manifest" href="manifest.json">'
        '<link rel="icon" href="icon.svg"><link rel="apple-touch-icon" href="icon-192.png">'
        '<meta name="apple-mobile-web-app-capable" content="yes"></head><body>')
(dist/"index.html").write_text(head + app + "</body></html>")
(dist/"manifest.json").write_text(json.dumps({
  "name":"Lintuhavainnot","short_name":"Linnut","lang":"fi","start_url":"./","display":"standalone",
  "background_color":"#eef2ee","theme_color":"#2c5c4c",
  "icons":[{"src":"icon.svg","sizes":"any","type":"image/svg+xml"},
           {"src":"icon-192.png","sizes":"192x192","type":"image/png"},
           {"src":"icon-512.png","sizes":"512x512","type":"image/png"}]}, ensure_ascii=False, indent=1))
(dist/"sw.js").write_text("""const C='lintu-v1';
self.addEventListener('install',e=>e.waitUntil(caches.open(C).then(c=>c.addAll(['./','index.html','manifest.json','icon.svg']))));
self.addEventListener('activate',e=>e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x!==C).map(x=>caches.delete(x))))));
self.addEventListener('fetch',e=>{if(e.request.method!=='GET')return;e.respondWith(fetch(e.request).then(r=>{const cp=r.clone();caches.open(C).then(c=>c.put(e.request,cp));return r}).catch(()=>caches.match(e.request)))});
""")
(dist/"icon.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><rect width="512" height="512" rx="96" fill="#2c5c4c"/><path d="M120 300c40-90 130-140 220-120l50-40 10 50c30 20 40 50 30 80-60-10-110 0-150 30-40 30-100 40-160 0z" fill="#eef2ee"/><circle cx="360" cy="215" r="10" fill="#2c5c4c"/><path d="M200 340l-20 70M250 335l-10 75" stroke="#c9952a" stroke-width="14" stroke-linecap="round"/></svg>')
print("ok")
