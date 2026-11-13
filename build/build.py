import sys, os, shutil, json, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib
from lib import *
import pages_loans, pages_other

# clean generated dirs (keep assets)
for d in os.listdir(OUT):
    p = os.path.join(OUT, d)
    if d in ("assets", "build") or d.startswith("README"): continue
    shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)

pages_loans.build_all_loans()
pages_other.build_all_other()

# sitemap.xml
today = "2026-11-13"
urls = sorted(set(lib.PAGES), key=lambda x: (-float(x[1]), x[0]))
xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for path, pr in urls:
    xml.append(f"<url><loc>{BASE}{path}</loc><lastmod>{today}</lastmod><priority>{pr}</priority></url>")
xml.append("</urlset>")
write_raw("sitemap.xml", "\n".join(xml))
write_raw("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")
write_raw("manifest.webmanifest", json.dumps({"name": BRAND, "short_name": "NEXUS", "start_url": "/", "display": "standalone",
    "background_color": "#ffffff", "theme_color": "#07355F",
    "icons": [{"src": "/assets/icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "/assets/icon-512.png", "sizes": "512x512", "type": "image/png"}]}))
write_raw("_redirects", "# Netlify / Cloudflare Pages: serve the custom 404\n/*  /404.html  404\n")
write_raw("CNAME", "nexuslendingpartners.com\n")
print("pages:", len(lib.PAGES))
