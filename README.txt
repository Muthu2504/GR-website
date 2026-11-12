Groods static website
=====================
Files:  index.html (the whole page)  |  favicon.svg  |  assets/ (images)

To go live: upload this whole folder to any static host (Netlify, Vercel,
Cloudflare Pages, GitHub Pages, or your domain's cPanel public_html).
index.html must stay at the top of the folder next to the assets folder.

Contact number used everywhere: 90 921 621 70
  Call link:      tel:+919092162170
  WhatsApp link:  https://wa.me/919092162170
Search index.html for "919092162170" to change it.

Sub-pages (service pages, restaurant pages, /restaurants/, biryani post)
are generated. Do not edit them by hand. Change index.html or the text in
tools/build_pages.py, then run:

  python tools/build_pages.py --sitemap

To add a restaurant: add its 480x360 .webp to assets/partners/, copy a
restaurant card in the partners section of index.html, edit it, then run
the command above. Full steps are at the top of tools/build_pages.py.
