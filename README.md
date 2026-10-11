# JMINT website (static HTML/CSS/JS)

Host as-is on GitHub Pages, Netlify or any static host. Upload every file in this folder.

## Before going live
1. Open `tools/content.py` and set SITE_URL, EMAIL, PHONE, LOCATION in CONFIG.
2. Run `python tools/build.py` once. It regenerates all pages, sitemap.xml, robots.txt and llms.txt.

## Where things live
- `tools/content.py`: original 7 services, projects, FAQs
- `tools/content_extra.py`: AI Avatars, Model Training, Data Engineering services, full technology list, delivery method
- `tools/build.py`: page templates and animations
- `css/extras.css`, `js/extras.js`: per-service hero animations, zig-zag train, avatar demo, ROI calculator
