# -*- coding: utf-8 -*-
"""Run:  python tools/build.py   (from the project root) to regenerate all HTML pages."""
import os, json, html, datetime, sys
sys.path.insert(0, os.path.dirname(__file__))
from content import *
from content_extra import *
SERVICES[:] = SERVICES[:-1] + NEW_SERVICES + SERVICES[-1:]
VIZ = {"ai-consulting":"radar","ai-agent-development":"loop","rag-chatbot-development":"stream","mcp-server-development":"hub","multi-agent-systems":"lanes","ai-automation-services":"belt","django-fullstack-development":"stack"}
for _s in SERVICES: _s.setdefault("viz", VIZ.get(_s["slug"], "loop"))
SVC_TECH = {"ai-consulting":[0,7,10],"ai-agent-development":[0,1,3],"rag-chatbot-development":[0,2,7],"mcp-server-development":[3,1,8],"multi-agent-systems":[1,0,5],"ai-automation-services":[1,3,7],"django-fullstack-development":[8,9,10],"ai-avatar-voice-agents":[4,0,8],"ml-model-training-deployment":[5,6,10],"data-engineering-analytics":[7,9,2]}

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
URL, EMAIL, PHONE = CONFIG["SITE_URL"], CONFIG["EMAIL"], CONFIG["PHONE"]
E = html.escape

ICONS = {
 "compass": '<circle cx="12" cy="12" r="9"/><path d="M15.5 8.5l-2 5-5 2 2-5z"/>',
 "bot": '<rect x="4" y="8" width="16" height="11" rx="3"/><path d="M12 8V4M9 13.5h.01M15 13.5h.01M9.5 16.5h5"/>',
 "chat": '<path d="M21 12a8 8 0 0 1-11.5 7.2L3 21l1.8-5.5A8 8 0 1 1 21 12z"/>',
 "plug": '<path d="M9 2v6M15 2v6M7 8h10v4a5 5 0 0 1-10 0zM12 17v5"/>',
 "layers": '<path d="M12 3l9 5-9 5-9-5z"/><path d="M3 13l9 5 9-5"/>',
 "zap": '<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>',
 "code": '<path d="M16 18l6-6-6-6M8 6l-6 6 6 6"/>',
 "chart": '<path d="M3 3v18h18M7 15l4-4 3 3 5-6"/>',
 "search": '<circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/>',
 "shield": '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/>',
 "db": '<ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v14c0 1.7 3.6 3 8 3s8-1.3 8-3V5M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3"/>',
 "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8zM14 2v6h6M9 13h6M9 17h6"/>',
 "users": '<path d="M17 21v-2a4 4 0 0 0-4-4H7a4 4 0 0 0-4 4v2"/><circle cx="10" cy="7" r="4"/><path d="M21 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8"/>',
 "rocket": '<path d="M12 15l-3-3a22 22 0 0 1 2-4 12 12 0 0 1 11-5c0 3-1 8-5 11a22 22 0 0 1-4 2z"/><path d="M9 12H4s.6-3 2-4c1.6-1 5 0 5 0M12 15v5s3-.6 4-2c1-1.6 0-5 0-5"/>',
 "network": '<circle cx="12" cy="5" r="2.2"/><circle cx="5" cy="19" r="2.2"/><circle cx="19" cy="19" r="2.2"/><path d="M12 7.2v4.8M12 12l-5.2 5.2M12 12l5.2 5.2"/>',
 "brain": '<path d="M12 3l1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9zM19 16l.8 2.2L22 19l-2.2.8L19 22l-.8-2.2L16 19l2.2-.8z"/>',
 "gear": '<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M4.2 4.2l2.1 2.1M17.7 17.7l2.1 2.1M2 12h3M19 12h3M4.2 19.8l2.1-2.1M17.7 6.3l2.1-2.1"/>',
 "scale": '<path d="M12 3v18M5 7h14M5 7l-3 7a3 3 0 0 0 6 0zM19 7l-3 7a3 3 0 0 0 6 0z"/>',
 "cart": '<circle cx="9" cy="20" r="1.5"/><circle cx="18" cy="20" r="1.5"/><path d="M2 3h3l2.7 12.4a2 2 0 0 0 2 1.6h7.7a2 2 0 0 0 2-1.5L21 7H6"/>',
 "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 "coins": '<circle cx="9" cy="9" r="6"/><path d="M15.5 9.3A6 6 0 1 1 9.3 15.5"/>',
 "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
 "phone": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/>',
 "pin": '<path d="M12 21s7-6.2 7-12a7 7 0 0 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="9" r="2.5"/>',
 "mic": '<rect x="9" y="3" width="6" height="12" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3"/>',
 "cpu": '<rect x="6" y="6" width="12" height="12" rx="2"/><path d="M9 2v4M15 2v4M9 18v4M15 18v4M2 9h4M2 15h4M18 9h4M18 15h4"/>',
 "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
}
def ic(n, extra=""):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" {extra}>{ICONS[n]}</svg>'

LEAF = '''<svg viewBox="0 0 64 64" aria-hidden="true"><path d="M33 2C16 13 6 28 9 44c2 8 9 13 17 14l1 5h5l-1-6c13-4 21-16 21-30C52 20 44 9 33 2z" fill="#2e8b3d"/><path d="M30 60V16M30 28l-11-12M30 28l11-9M30 40l-14-13M30 40l13-12M30 51l-11-9M30 51l10-8" stroke="#fff" stroke-width="2.6" stroke-linecap="round" fill="none"/></svg>'''
def brand():
    return f'<a class="brand" href="index.html" aria-label="{CONFIG["FULL"]} home">{LEAF}<span><b>{CONFIG["BRAND"]}</b></span></a>'

def header(active=""):
    dd = "".join(f'<li><a href="{s["slug"]}.html"><i>{ic(s["icon"])}</i>{E(s["name"])}</a></li>' for s in SERVICES)
    def a(href, label, key):
        return f'<li><a class="top{" active" if active==key else ""}" href="{href}">{label}</a></li>'
    return f'''<header class="site-header"><div class="wrap nav">{brand()}
<button class="burger" aria-label="Open menu" aria-expanded="false">{ic("menu")}</button>
<ul class="menu">
{a("index.html","Home","home")}
<li class="has-dd"><button class="top" aria-haspopup="true" aria-expanded="false">Services &#9662;</button><ul class="dd">{dd}</ul></li>
{a("projects.html","Projects","projects")}
{a("technologies.html","Technologies","tech")}
{a("index.html#process","How we work","process")}
{a("contact.html","Contact","contact")}
<li><a class="btn btn-primary btn-sm" href="contact.html">Get a free quote</a></li>
</ul></div></header>'''

def footer():
    sl = "".join(f'<li><a href="{s["slug"]}.html">{E(s["name"])}</a></li>' for s in SERVICES)
    return f'''<footer><div class="wrap"><div class="foot">
<div>{brand()}<p>We build AI agents, RAG chatbots, MCP integrations, multi-agent systems, automation and full-stack web apps – delivered on time and within budget.</p></div>
<div><h4>Services</h4><ul>{sl}</ul></div>
<div><h4>Company</h4><ul><li><a href="projects.html">Our projects</a></li><li><a href="technologies.html">Technologies &amp; method</a></li><li><a href="index.html#process">How we deliver</a></li><li><a href="index.html#faq">FAQ</a></li><li><a href="contact.html">Contact</a></li></ul></div>
<div><h4>Talk to us</h4><ul><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li>{PHONE}</li><li>{CONFIG["LOCATION"]}</li></ul></div>
</div><div class="copy"><span>&copy; {datetime.date.today().year} {CONFIG["FULL"]}. All rights reserved.</span><span>AI consulting, AI agents, RAG, MCP, automation &amp; Django development.</span></div></div></footer>
<script src="js/main.js"></script><script src="js/extras.js"></script>'''

def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + '</script>'

ORG = {"@type": "Organization", "@id": URL + "/#org", "name": CONFIG["FULL"], "alternateName": "JMINT", "url": URL + "/",
       "logo": URL + "/assets/favicon.svg", "email": EMAIL,
       "description": "AI consulting, AI agent development, RAG chatbots, MCP server integration, multi-agent systems, AI automation and full-stack Django development."}

def faq_ld(faq):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}

def head(title, desc, path, extra="", keywords=""):
    can = f"{URL}/{path}" if path else f"{URL}/"
    return f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
{f'<meta name="keywords" content="{E(keywords)}">' if keywords else ''}
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{can}">
<meta property="og:type" content="website"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{can}"><meta property="og:site_name" content="{CONFIG["FULL"]}">
<meta name="twitter:card" content="summary"><meta name="theme-color" content="#2e8b3d">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=Figtree:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/style.css"><link rel="stylesheet" href="css/extras.css">
{extra}</head><body>'''

# ---------- visual blocks ----------
def mock(spec):
    kind, data = spec
    if kind == "chat":
        out = ""
        for i, m in enumerate(data):
            who = "u" if i % 2 == 0 else "b"
            txt, _, src = m.partition("|")
            out += f'<div class="bub {who} n{i+1}">{E(txt)}{f"<em>{E(src)}</em>" if src else ""}</div>'
        return f'<div class="mock" role="img" aria-label="Animated chatbot conversation preview"><div class="dots"><i></i><i></i><i></i></div>{out}</div>'
    if kind == "dash":
        k = "".join(f'<div>{E(l)}<b><u></u></b></div>' for l in data)
        hs = [40, 62, 48, 80, 58, 92, 70, 100]
        b = "".join(f'<i style="--h:{h}%"></i>' for h in hs)
        return f'<div class="mock" role="img" aria-label="Animated analytics dashboard preview"><div class="dots"><i></i><i></i><i></i></div><div class="kpis">{k}</div><div class="bars">{b}</div><div class="insight">Key insight ready for review</div></div>'
    if kind == "app":
        r = "".join("<i></i>" for _ in range(6))
        return f'<div class="mock" role="img" aria-label="Animated web application preview"><div class="dots"><i></i><i></i><i></i></div><div class="app"><div class="side"><i></i><i></i><i></i><i></i></div><div class="rows">{r}</div></div></div>'
    if kind == "flow":
        stages = [[x.strip() for x in s.split("|")] for s in data]
        n = len(stages); W, H, bw, bh = 460, 190, 92, 34
        xs = [10 + i * (W - 20 - bw) / (n - 1) for i in range(n)]
        cols = ["#3b82f6", "#7c5cf0", "#ec5fa5", "#2e8b3d"]
        pos = []
        for i, st in enumerate(stages):
            k = len(st)
            pos.append([(xs[i], 95 + (j - (k - 1) / 2) * 56) for j in range(k)])
        svg = ""; c = 0
        for i in range(n - 1):
            for (x1, y1) in pos[i]:
                for (x2, y2) in pos[i + 1]:
                    p = f"M{x1+bw:.0f} {y1:.0f} L{x2:.0f} {y2:.0f}"
                    svg += f'<path d="{p}" stroke="#cdd6f5" stroke-width="2" stroke-dasharray="5 5" fill="none"/><circle r="5" fill="{cols[c%4]}"><animateMotion dur="2.4s" begin="{(c%5)*.4:.1f}s" repeatCount="indefinite" path="{p}"/></circle>'
                    c += 1
        for i, st in enumerate(stages):
            for j, lab in enumerate(st):
                x, y = pos[i][j]
                col = cols[(i + j) % 4]
                svg += f'<rect x="{x:.0f}" y="{y-bh/2:.0f}" width="{bw}" height="{bh}" rx="10" fill="#fff" stroke="{col}" stroke-width="2"/><text x="{x+bw/2:.0f}" y="{y+4:.0f}" text-anchor="middle" font-size="12" font-weight="700" fill="#27305a" font-family="Figtree,sans-serif">{E(lab)}</text>'
        return f'<div class="mock" role="img" aria-label="Animated workflow diagram"><div class="dots"><i></i><i></i><i></i></div><svg class="flow" viewBox="0 0 {W} {H}">{svg}</svg></div>'
    if kind == "avatar":
        return f'<div class="mock" role="img" aria-label="Animated live AI avatar conversation"><div class="dots"><i></i><i></i><i></i></div><div class="avatar">{FACE}<div><p>{E(data[0])}</p><p>{E(data[1])}</p></div></div></div>'
    if kind == "eval":
        ws = [92, 78, 64]
        r = "".join(f'<div>{E(l)}<b style="--w:{ws[i%3]}%;animation-delay:{i*.3}s"></b></div>' for i, l in enumerate(data))
        return f'<div class="mock" role="img" aria-label="Animated model evaluation scores"><div class="dots"><i></i><i></i><i></i></div><div class="evalrows">{r}</div><div class="insight">Best model selected on accuracy and cost</div></div>'
    if kind == "curve":
        return f'<div class="mock" role="img" aria-label="Animated training curve"><div class="dots"><i></i><i></i><i></i></div><svg class="curve" viewBox="0 0 300 150"><path d="M10 20 C60 30 70 110 130 120 S230 130 290 128" stroke="#7c5cf0" stroke-width="3" fill="none"/><path d="M10 40 C60 52 80 100 140 108 S230 112 290 110" stroke="#2e8b3d" stroke-width="3" fill="none" style="animation-delay:.4s"/></svg><div class="insight">{E(data[0])} vs {E(data[1])}</div></div>'
    return ""

FACE = '''<svg class="face" viewBox="0 0 120 130" aria-hidden="true"><defs><linearGradient id="fg" x1="0" x2="1" y1="0" y2="1"><stop offset="0" stop-color="#7c5cf0"/><stop offset="1" stop-color="#ec5fa5"/></linearGradient></defs><rect x="8" y="10" width="104" height="112" rx="46" fill="url(#fg)"/><rect x="22" y="38" width="76" height="52" rx="26" fill="#fff"/><ellipse class="blink" cx="45" cy="60" rx="7" ry="8" fill="#27305a"/><ellipse class="blink" cx="75" cy="60" rx="7" ry="8" fill="#27305a"/><rect class="mouth" x="50" y="76" width="20" height="4" rx="2" fill="#ec5fa5"/><path d="M60 10V2" stroke="#2e8b3d" stroke-width="4" stroke-linecap="round"/><circle cx="60" cy="3" r="4" fill="#2e8b3d"/></svg>'''

def layout(kind, n):
    import math
    pts = []
    for i in range(n):
        if kind in ("radar", "loop", "hub"):
            r = {"radar": 39, "loop": 41, "hub": 42}[kind]; a = math.radians(i * 360 / n + (30 if kind == "hub" else 0))
            pts.append((50 + r * math.sin(a), 50 - r * math.cos(a)))
        elif kind == "stream": pts.append((24 + (i % 2) * 52, 8 + i * 13))
        elif kind == "lanes": pts.append((26, 12 + i * 15))
        elif kind == "belt": pts.append((0, 72))
        elif kind == "stack": pts.append((50, 90 - i * 11.5))
        elif kind == "wave": pts.append((24 if i % 2 == 0 else 76, 12 + (i // 2) * 28 + (i % 2) * 10))
        elif kind == "curve": pts.append((12 + i * 15, 18 + 62 * (1 - math.exp(-i * .7)) * 1.05))
        elif kind == "rain": pts.append((10 + (i * 37) % 80, 0))
        else: pts.append((50, 50))
    return pts

def hero_viz(s):
    kind = s["viz"]; chips = s["chips"]; n = len(chips); pts = layout(kind, n)
    nodes = "".join(f'<a class="node" href="#sub-{i}" style="--x:{x:.1f}%;--y:{y:.1f}%;--k:{i}" title="Jump to {E(c)}"><span>{E(c)}</span></a>' for i, (c, (x, y)) in enumerate(zip(chips, pts)))
    bars = "".join(f'<i style="--k:{i}"></i>' for i in range(16)) if kind == "wave" else ""
    core = FACE if kind == "wave" else ic(s["icon"])
    return f'<div class="viz v-{kind}"><div class="vbg">{bars}</div><div class="vcore">{core}</div>{nodes}<div class="hint">Tap any bubble to jump to that service</div></div>'

def orbit(icon, chips, dense=False):
    cols = ["var(--blue)", "var(--violet)", "var(--pink)", "var(--leaf)"]
    n = len(chips); out = ""
    for i, c in enumerate(chips):
        lab, href = c if isinstance(c, tuple) else (c, None)
        inner = f'<a href="{href}" style="--c:{cols[i%4]}"><span style="--c:{cols[i%4]}">{E(lab)}</span></a>' if href else f'<span style="--c:{cols[i%4]}">{E(lab)}</span>'
        out += f'<div class="chip" style="--a:{i*360//n}deg">{inner}</div>'
    return f'<div class="orbit{" dense" if dense else ""}"><div class="ring">{out}</div><div class="core">{ic(icon)}</div></div>'

def proj_block(p, svc, link=True):
    tags = "".join(f'<span class="tag">{E(t)}</span>' for t in p["tags"])
    ln = f'<p style="margin-top:16px"><a class="btn btn-ghost btn-sm" href="{svc["slug"]}.html">Explore {E(svc["short"])}</a></p>' if link else ""
    return f'''<article class="proj rv" data-cat="{svc["slug"]}" id="{p["id"]}">{mock(p["mock"])}
<div><h3>{E(p["title"])}</h3><div class="tags">{tags}</div>
<dl><dt>The challenge</dt><dd>{E(p["problem"])}</dd><dt>What we built</dt><dd>{E(p["solution"])}</dd><dt>The outcome</dt><dd>{E(p["result"])}</dd></dl>{ln}</div></article>'''

def train():
    w = '<span class="wagon eng"><b>JMINT Express</b><small>Click any wagon to open the project</small></span>'
    k = 0
    for sv in SERVICES:
        for p in sv["projects"]:
            w += f'<a class="wagon c{k%4}" href="projects.html#{p["id"]}" title="{E(p["title"])}"><b>{E(p["title"])}</b><small>{E(sv["short"])}</small></a>'; k += 1
    w = w.replace('<span class="wagon eng">', '<a class="wagon eng" href="projects.html">').replace('</small></span>', '</small></a>', 1)
    return f'''<div class="rail-scene" aria-label="Animated train carrying our projects along a zig-zag track"><svg class="track" aria-hidden="true"></svg><div class="cars">{w}</div></div><p class="rail-hint">Hover to pause. Every wagon links to its project.</p>'''

def river():
    cols = {"blue": "var(--blue)", "violet": "var(--violet)", "pink": "var(--pink)", "green": "var(--leaf)"}
    banks = ""
    for i, (t, d, c) in enumerate(STEPS):
        step = f'<div class="step" style="--c:{cols[c]}"><span class="n">{i+1}</span><h4>{E(t)}</h4><p>{E(d)}</p></div>'
        if i % 2 == 0:
            banks += f'<div class="bank"><div class="slot t">{step}</div><div class="slot b"></div></div>'
        else:
            banks += f'<div class="bank"><div class="slot t"></div><div class="slot b">{step}</div></div>'
    p = "M0 75 C 100 10, 200 140, 300 75 S 500 10, 600 75 S 800 140, 900 75 S 1100 10, 1200 75"
    svg = f'''<svg class="river-svg" viewBox="0 0 1200 150" preserveAspectRatio="none" aria-hidden="true"><defs><linearGradient id="rg" x1="0" x2="1"><stop offset="0" stop-color="#bcd8ff"/><stop offset=".5" stop-color="#d9ccff"/><stop offset="1" stop-color="#ffd0e8"/></linearGradient></defs>
<path d="{p}" stroke="url(#rg)" stroke-width="84" fill="none" stroke-linecap="round"/>
<path d="{p}" stroke="#fff" stroke-opacity=".75" stroke-width="3" fill="none" stroke-dasharray="14 22"><animate attributeName="stroke-dashoffset" from="72" to="0" dur="1.6s" repeatCount="indefinite"/></path>
<path d="{p}" stroke="#fff" stroke-opacity=".5" stroke-width="2" fill="none" transform="translate(0 -20)" stroke-dasharray="8 30"><animate attributeName="stroke-dashoffset" from="76" to="0" dur="2.2s" repeatCount="indefinite"/></path>
<path d="{p}" stroke="#fff" stroke-opacity=".5" stroke-width="2" fill="none" transform="translate(0 20)" stroke-dasharray="10 28"><animate attributeName="stroke-dashoffset" from="76" to="0" dur="1.9s" repeatCount="indefinite"/></path></svg>'''
    boat = '<div class="boat" aria-hidden="true"><svg viewBox="0 0 52 44"><path d="M6 30h40l-6 10H12z" fill="#2e8b3d"/><path d="M26 6v24M26 8l16 18H26z" fill="#fff" stroke="#7c5cf0" stroke-width="2"/><path d="M26 12L12 28h14z" fill="#ffeaf4" stroke="#ec5fa5" stroke-width="2"/></svg></div>'
    return f'<div class="river" role="list" aria-label="Our delivery process">{svg}{boat}<div class="banks">{banks}</div></div>'

def tech_chips(idx):
    return "".join(f'<a class="tag" href="technologies.html#cat-{i}" style="text-decoration:none">{E(t)}</a>' for i in idx for t in TECH[i][2][:6])

def tech_marquee():
    pills = "".join(f'<a href="technologies.html#cat-{ci}">{E(t)}</a>' for ci, c in enumerate(TECH) for t in c[2])
    half = len(pills)
    rows = []
    items = [(ci, t) for ci, c in enumerate(TECH) for t in c[2]]
    a = "".join(f'<a href="technologies.html#cat-{ci}">{E(t)}</a>' for ci, t in items[0::2])
    b = "".join(f'<a href="technologies.html#cat-{ci}">{E(t)}</a>' for ci, t in items[1::2])
    return f'<div class="marq"><div class="tr">{a}{a}</div></div><div class="marq rev"><div class="tr">{b}{b}</div></div>'

def stats_block():
    nums = [("40-70%", "Typical time saved on repetitive back-office work we automate"), ("6-12 wks", "First call to a working pilot on most projects"), (str(len(SERVICES)), "Specialist service lines under one roof"), ("100%", "Source code and documentation handed to you")]
    return '<div class="stats">' + "".join(f'<div class="stat rv"><b>{a}</b><span>{E(b)}</span></div>' for a, b in nums) + '</div>'

def avatar_demo():
    return f'''<div class="demo rv" id="avatar-demo"><div>{FACE}<div class="eqbar" aria-hidden="true">{"".join(f'<i style="--k:{i}"></i>' for i in range(14))}</div></div>
<div><h3>Say hello to Mia, a demo avatar</h3><p>Pick a question and watch her answer. This is a scripted preview of the live avatars we build; real ones listen, speak and use your own knowledge base.</p>
<div class="says" aria-live="polite">Hi, I am Mia. Ask me something below.</div>
<div class="opts"><button data-q="pricing">How is pricing set?</button><button data-q="data">Is my data safe?</button><button data-q="time">How long does it take?</button><button data-q="human">Can I talk to a person?</button></div>
<p style="margin-top:12px"><label><input type="checkbox" id="voice"> Speak answers aloud</label></p>
<p style="margin-top:12px"><a class="btn btn-primary btn-sm" href="ai-avatar-voice-agents.html">Explore AI avatars</a></p></div></div>'''

def roi_calc():
    return '''<form class="calc rv" id="roi-calc" onsubmit="return false"><div><h3 style="margin-bottom:16px">Estimate what automation could save you</h3>
<label>Hours per person each week on the task <output for-o="hrs">10 h</output><input type="range" name="hrs" min="1" max="40" value="10"></label>
<label>Cost per hour (INR) <output for-o="rate">500</output><input type="range" name="rate" min="100" max="3000" step="50" value="500"></label>
<label>Share we can realistically automate <output for-o="pct">50%</output><input type="range" name="pct" min="10" max="90" step="5" value="50"></label>
<label>People doing this task <output for-o="ppl">5</output><input type="range" name="ppl" min="1" max="100" value="5"></label></div>
<div class="res"><small>Indicative yearly saving</small><b>INR <span id="roi-out">0</span></b><small>about <span id="roi-hrs">0</span> of staff time freed. A rough guide only: the audit gives you a real, costed figure.</small><a class="btn alt" href="contact.html" style="margin-top:10px">Get an exact estimate</a></div></form>'''

def method_block(s):
    if not s.get("method"): return river()
    return '<div class="timeline">' + "".join(f'<div class="tl rv"><h3>{i+1}. {E(t)}</h3><p>{E(d)}</p></div>' for i, (t, d) in enumerate(s["method"])) + '</div><p style="text-align:center;margin-top:20px" class="rv"><a class="btn btn-ghost btn-sm" href="technologies.html#method">See our full delivery method</a></p>'

def faq_block(faq):
    return '<div class="faq">' + "".join(f'<details class="rv"><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in faq) + '</div>'

def cta(title="Ready to build something that works?", text="Tell us what you want to achieve. We reply within one working day with a clear plan, timeline and fixed-price estimate."):
    return f'''<section><div class="wrap"><div class="cta rv"><h2>{E(title)}</h2><p>{E(text)}</p><a class="btn" href="contact.html">Get a free quote</a><a class="btn alt" href="mailto:{EMAIL}">Email us</a></div></div></section>'''

def why_cards():
    return '<div class="grid g4">' + "".join(f'<div class="card promise rv c-{c}"><div class="ico">{ic(i)}</div><h3>{E(t)}</h3><p>{E(d)}</p></div>' for i, t, d, c in WHY) + '</div>'

def write(name, content):
    with open(os.path.join(ROOT, name), "w", encoding="utf-8") as f:
        f.write(content)

all_pages = []

# ---------- HOME ----------
def home():
    ai = SERVICES[:-1]; dj = SERVICES[-1]
    sc = ""
    for s in ai:
        subs = "".join(f"<li>{E(x[0])}</li>" for x in s["subs"][:4])
        sc += f'<a class="card svc-card rv c-{s["color"]}" href="{s["slug"]}.html"><div class="ico">{ic(s["icon"])}</div><h3>{E(s["name"])}</h3><p>{E(s["lead"][:150].rsplit(" ",1)[0])}…</p><ul>{subs}</ul><span class="more">Explore {E(s["short"])}</span></a>'
    sc += f'<a class="card svc-card main rv c-{dj["color"]}" href="{dj["slug"]}.html" style="grid-column:1/-1"><div class="ico">{ic(dj["icon"])}</div><h3>{E(dj["name"])}</h3><p>{E(dj["lead"])}</p><span class="more">Explore {E(dj["short"])}</span></a>'
    fall = ""
    for i, s in enumerate(SERVICES):
        fall += f'<div class="fall-row rv c-{s["color"]}" style="--c:var(--{ {"violet":"violet","blue":"blue","pink":"pink","green":"leaf"}[s["color"]] })"><a class="card svc-card" href="{s["slug"]}.html"><h3>{E(s["name"])}</h3><p>{E(s["subs"][0][2])}</p><span class="more">Dive in</span></a><div class="dot">{ic(s["icon"])}</div></div>'
    feat = []
    for s in SERVICES:
        for p in s["projects"]:
            if p["id"] in ("accounting-agent", "rag-docs", "avatar-concierge", "eval-harness", "mcp-multi", "parallel-agents", "elt-warehouse"):
                feat.append((p, s))
    fp = "".join(proj_block(p, s) for p, s in feat)
    chips = ["AI Agents", "RAG Chatbots", "MCP", "Multi-Agent", "Automation", "Django"]
    page = head("JMINT Consulting Services | AI Consulting, AI Agents, RAG Chatbots & MCP Development",
        "AI solutions company: AI consulting, custom AI agent development, RAG chatbots, MCP integration, multi-agent systems, AI automation and Django full-stack apps. On time, budget-friendly.",
        "", ld({"@context": "https://schema.org", "@graph": [ORG, {"@type": "WebSite", "@id": URL + "/#site", "url": URL + "/", "name": CONFIG["FULL"], "publisher": {"@id": URL + "/#org"}}]}) + ld(faq_ld(HOME_FAQ)),
        "AI consulting, AI agent development, RAG chatbot, MCP server development, multi-agent systems, AI automation, Django development company")
    page += header("home")
    page += f'''<main><section class="hero"><canvas id="net"></canvas><div class="wrap"><div>
<h1>AI solutions that ship <span class="g-text">on time</span> and stay within budget</h1>
<p class="lead">JMINT builds AI agents, RAG chatbots, MCP integrations, multi-agent systems and automation for businesses – plus reliable full-stack web apps in Django. Clear scope, weekly demos, fixed pricing.</p>
<div class="hero-cta"><a class="btn btn-primary" href="contact.html">Get a free quote</a><a class="btn btn-ghost" href="projects.html">See our projects</a></div>
<ul class="assure"><li>Fixed-price projects</li><li>Prototype in days</li><li>Weekly progress demos</li><li>Post-launch support</li></ul></div>
{orbit("brain", [(x["short"], x["slug"] + ".html") for x in SERVICES], True)}</div></section>
<div class="strip"><div class="wrap">
<div>{ic("clock")}<p><b>Delivered on schedule</b><span>Milestones you can track</span></p></div>
<div>{ic("coins")}<p><b>Budget-friendly</b><span>Transparent, fixed pricing</span></p></div>
<div>{ic("shield")}<p><b>Secure by design</b><span>Your data stays yours</span></p></div>
<div>{ic("users")}<p><b>Real project experience</b><span>Agents, RAG, MCP, Django</span></p></div></div></div>

<section><div class="wrap"><div class="sec-head center rv"><h2>Projects on the move</h2><p>A few of the AI and web projects we have delivered. Hover to pause the train and read a wagon.</p></div>{train()}</div></section>

<section><div class="wrap"><div class="sec-head center rv"><h2>Numbers that matter to a budget owner</h2><p>What clients can usually expect when they work with us.</p></div>{stats_block()}</div></section>

<section class="tint-blue" id="services"><div class="wrap"><div class="sec-head rv"><h2>AI services built for real business results</h2><p>Every service has its own page with sub-services, project examples and answers to common questions. Pick the one that matches your goal.</p></div>
<div class="grid g3">{sc}</div></div></section>

<section><div class="wrap"><div class="sec-head center rv"><h2>Projects we have built</h2><p>Real problems, practical AI solutions. Here are some highlights – the full list is on our projects page.</p></div>{fp}
<p style="text-align:center"><a class="btn btn-grad" href="projects.html">View all projects</a></p></div></section>

<section class="tint-pink"><div class="wrap"><div class="sec-head center rv"><h2>Try a live AI avatar</h2><p>Faces and voices make software easier to use. Here is a small taste.</p></div>{avatar_demo()}</div></section>

<section id="stack"><div class="wrap"><div class="sec-head center rv"><h2>The tools and frameworks behind our work</h2><p>Click any technology to see where we use it. <a href="technologies.html">See the full stack and method</a>.</p></div>{tech_marquee()}</div></section>

<section class="tint-violet" id="technologies"><div class="wrap"><div class="sec-head center rv"><h2>Follow the flow to the technology you need</h2><p>Our expertise cascades from strategy down to production code. Follow the water and open any service.</p></div>
<div class="fall"><div class="stream" aria-hidden="true"></div>{fall}</div></div></section>

<section id="process"><div class="wrap"><div class="sec-head center rv"><h2>Our delivery river: six stops from idea to launch</h2><p>The same proven process on every project keeps scope clear, budgets fixed and delivery on time.</p></div>{river()}</div></section>

<section class="tint-green"><div class="wrap"><div class="split"><div class="rv"><h2>Why businesses trust JMINT with their AI projects</h2><p style="margin-top:14px">We are engineers first. We only promise what we have built before, we show working software early and we keep communication simple.</p>
<ul class="checks"><li><b>Fixed scope and price</b> agreed before development starts.</li><li><b>Quick wins first</b> so you see value in weeks, not quarters.</li><li><b>Right-sized AI models</b> that keep running costs low.</li><li><b>You own the code</b> and documentation we deliver.</li><li><b>Support after launch</b> with clear maintenance plans.</li></ul></div>
<div>{why_cards()}</div></div></div></section>

<section class="tint-green"><div class="wrap"><div class="sec-head center rv"><h2>What could AI automation be worth to you?</h2><p>Move the sliders to get a rough yearly figure.</p></div>{roi_calc()}</div></section>

<section id="faq"><div class="wrap"><div class="sec-head center rv"><h2>Frequently asked questions about our AI services</h2></div>{faq_block(HOME_FAQ)}</div></section>
{cta()}</main>'''
    page += footer() + "</body></html>"
    write("index.html", page); all_pages.append("")

# ---------- SERVICE PAGES ----------
def service(s):
    subs = "".join(f'<div id="sub-{i}" class="card rv c-{s["color"] if i%4==0 else ["blue","violet","pink","green"][i%4]}"><div class="ico">{ic(ic_n)}</div><h3>{E(t)}</h3><p>{E(d)}</p><ul>{"".join(f"<li>{E(b)}</li>" for b in bl)}</ul></div>' for i, (t, ic_n, d, bl) in enumerate(s["subs"]))
    pr = "".join(proj_block(p, s, link=False) for p in s["projects"])
    kw = "".join(f'<span class="tag">{E(k)}</span>' for k in s["keywords"])
    others = "".join(f'<a class="btn btn-ghost btn-sm" href="{o["slug"]}.html" style="margin:5px">{E(o["short"])}</a>' for o in SERVICES if o["slug"] != s["slug"])
    svc_ld = {"@context": "https://schema.org", "@type": "Service", "name": s["name"], "serviceType": s["short"], "description": s["desc"],
              "url": f'{URL}/{s["slug"]}.html', "areaServed": "Worldwide", "provider": {"@id": URL + "/#org"},
              "hasOfferCatalog": {"@type": "OfferCatalog", "name": s["name"], "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": x[0], "description": x[2]}} for x in s["subs"]]}}
    bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": URL + "/"},
        {"@type": "ListItem", "position": 2, "name": s["name"], "item": f'{URL}/{s["slug"]}.html'}]}
    page = head(s["title"], s["desc"], s["slug"] + ".html", ld(svc_ld) + ld(faq_ld(s["faq"])) + ld(bc), ", ".join(s["keywords"]))
    page += header("")
    page += f'''<main><section class="hero page-hero"><canvas id="net"></canvas><div class="wrap"><div>
<div class="crumbs"><a href="index.html">Home</a> / {E(s["name"])}</div>
<h1>{E(s["h1"])}</h1><p class="lead">{E(s["lead"])}</p>
<div class="hero-cta"><a class="btn btn-primary" href="contact.html">Get a free quote</a><a class="btn btn-ghost" href="#projects">See project examples</a></div>
<ul class="assure"><li>Fixed price</li><li>On-time delivery</li><li>Weekly demos</li></ul></div>{hero_viz(s)}</div></section>

<section><div class="wrap"><div class="split"><div class="rv"><h2>What is {E(s["short"].lower() if s["slug"]!="mcp-server-development" else "MCP development")}?</h2><p style="margin-top:14px">{E(s["intro"])}</p><div class="tags">{kw}</div></div>
<div class="rv"><ul class="checks"><li><b>Delivered on time:</b> milestone plan, early prototype and weekly demos.</li><li><b>Budget-friendly:</b> fixed pricing and cost-efficient AI model choices.</li><li><b>Genuine expertise:</b> we have already built and shipped solutions like these.</li><li><b>Secure and private:</b> access control, encryption and private hosting options.</li><li><b>Support included:</b> training, documentation and post-launch help.</li></ul></div></div></div></section>

<section class="tint-{s["color"] if s["color"]!="green" else "green"}"><div class="wrap"><div class="sec-head rv"><h2>{E(s["name"])}: what we offer</h2><p>Choose a single sub-service or combine several into one complete solution.</p></div><div class="grid g3">{subs}</div></div></section>

<section id="projects"><div class="wrap"><div class="sec-head center rv"><h2>{E(s["short"])} projects we have delivered</h2><p>A look at how we solved real problems in this area.</p></div>{pr}</div></section>

<section id="tech"><div class="wrap"><div class="sec-head center rv"><h2>Technology we use for {E(s["short"].lower())}</h2><p>Tools chosen per project, never by habit. <a href="technologies.html">View the complete stack</a>.</p></div><div class="tags rv" style="justify-content:center">{tech_chips(SVC_TECH[s["slug"]])}</div></div></section>

<section class="tint-blue" id="process"><div class="wrap"><div class="sec-head center rv"><h2>How we deliver your {E(s["short"].lower())} project</h2><p>The same six-step river for every project: clear requirements, fixed plan, early prototype and a safe launch.</p></div>{method_block(s)}</div></section>

<section><div class="wrap"><div class="sec-head center rv"><h2>{E(s["short"])}: your questions answered</h2></div>{faq_block(s["faq"])}
<div style="text-align:center;margin-top:44px" class="rv"><p style="margin-bottom:10px"><b>Explore our other services</b></p>{others}</div></div></section>
{cta()}</main>'''
    page += footer() + "</body></html>"
    write(s["slug"] + ".html", page); all_pages.append(s["slug"] + ".html")

# ---------- PROJECTS ----------
def projects():
    fb = '<button class="on" data-f="all">All projects</button>' + "".join(f'<button data-f="{s["slug"]}">{E(s["short"])}</button>' for s in SERVICES)
    body = "".join(proj_block(p, s) for s in SERVICES for p in s["projects"])
    desc = "AI agent, RAG chatbot, MCP integration, multi-agent, automation and Django projects delivered by JMINT Consulting Services."
    page = head("AI & Web Development Projects | Case Studies – JMINT", desc, "projects.html", ld({"@context": "https://schema.org", "@type": "CollectionPage", "name": "JMINT projects", "url": URL + "/projects.html"}))
    page += header("projects")
    page += f'''<main><section class="hero page-hero"><canvas id="net"></canvas><div class="wrap" style="grid-template-columns:1fr"><div><div class="crumbs"><a href="index.html">Home</a> / Projects</div><h1>Projects that prove what AI can do for your business</h1><p class="lead">From accounting insight agents to RAG chatbots, MCP integrations, parallel multi-agent pipelines and full-stack Django apps – explore what we have built.</p></div></div></section>
<section><div class="wrap"><div class="filters" role="group" aria-label="Filter projects">{fb}</div>{body}</div></section>{cta()}</main>'''
    page += footer() + "</body></html>"
    write("projects.html", page); all_pages.append("projects.html")

# ---------- CONTACT ----------
def contact():
    opts = "".join(f"<option>{E(s['name'])}</option>" for s in SERVICES) + "<option>Not sure yet – need advice</option>"
    page = head("Contact JMINT | Get a Free AI Project Quote", "Contact JMINT Consulting Services for AI consulting, AI agents, RAG chatbots, MCP integration, automation and Django development. Free quote within one working day.", "contact.html")
    page += header("contact")
    page += f'''<main><section class="hero page-hero"><canvas id="net"></canvas><div class="wrap"><div class="rv in"><div class="crumbs"><a href="index.html">Home</a> / Contact</div><h1>Tell us your idea. Get a clear plan and fixed quote.</h1><p class="lead">Share a few details and we will reply within one working day with next steps, a timeline and a budget range.</p>
<ul class="checks"><li>Free discovery call</li><li>No-obligation fixed-price estimate</li><li>Your information stays confidential</li></ul></div>
<div class="card" style="padding:30px"><form id="contact-form" data-to="{EMAIL}">
<label>Your name<input name="name" required autocomplete="name"></label>
<label>Email<input type="email" name="email" required autocomplete="email"></label>
<label>Service needed<select name="service">{opts}</select></label>
<label>Approximate budget<select name="budget"><option>Not decided</option><option>Small (quick win / prototype)</option><option>Medium project</option><option>Large / long-term programme</option></select></label>
<label>Project details<textarea name="message" required placeholder="What would you like to build or automate?"></textarea></label>
<button class="btn btn-primary" type="submit">Send enquiry</button>
<p style="font-size:.85rem">This opens your email app with the message ready to send.</p></form></div></div></section>
<section><div class="wrap"><div class="grid g3">
<div class="card c-blue"><div class="ico">{ic("mail")}</div><h3>Email</h3><p><a href="mailto:{EMAIL}">{EMAIL}</a></p></div>
<div class="card c-green"><div class="ico">{ic("phone")}</div><h3>Phone</h3><p>{PHONE}</p></div>
<div class="card c-pink"><div class="ico">{ic("pin")}</div><h3>Location</h3><p>{CONFIG["LOCATION"]}</p></div></div></div></section></main>'''
    page += footer() + "</body></html>"
    write("contact.html", page); all_pages.append("contact.html")

def technologies():
    cats = "".join(f'<div class="techcat rv" id="cat-{i}"><h3>{ic(ic_n)}{E(t)}</h3><div class="tags">' + "".join(f'<span class="tag">{E(x)}</span>' for x in items) + '</div></div>' for i, (t, ic_n, items) in enumerate(TECH))
    tl = "".join(f'<div class="tl rv"><h3>{i+1}. {E(t)}</h3><p>{E(d)}</p></div>' for i, (t, d) in enumerate(METHOD))
    models = [("Fixed-price project", "Best when scope is clear. Milestone payments, defined deliverables, no surprise invoices."), ("Dedicated engineers", "A small team that works as part of yours, with weekly planning and monthly review."), ("Retainer and support", "Monitoring, fixes, model updates and small improvements after launch for a monthly fee.")]
    mo = "".join(f'<div class="card rv c-{c}"><h3>{E(t)}</h3><p>{E(d)}</p></div>' for (t, d), c in zip(models, ["blue", "violet", "green"]))
    page = head("Technologies, Skills & Delivery Method | AI, Django, Data – JMINT", "Full list of the AI, LLM, agent, RAG, MCP, voice, model training, data engineering and Django technologies JMINT works with, plus our delivery method and ROI approach.", "technologies.html", ld({"@context": "https://schema.org", "@type": "CollectionPage", "name": "JMINT technologies and method", "url": URL + "/technologies.html"}))
    page += header("tech")
    page += f'''<main><section class="hero page-hero"><canvas id="net"></canvas><div class="wrap" style="grid-template-columns:1fr"><div><div class="crumbs"><a href="index.html">Home</a> / Technologies</div><h1>Skills, tools and the method behind every project</h1><p class="lead">From language models and agents to Django, data pipelines and private GPU deployment. This is everything we work with and how we turn it into a result you can measure.</p></div></div></section>
<section><div class="wrap"><div class="sec-head center rv"><h2>Technology and framework stack</h2><p>Grouped by what they are used for. Each service page shows the subset that applies.</p></div><div class="techgrid">{cats}</div></div></section>
<section class="tint-violet" id="method"><div class="wrap"><div class="sec-head center rv"><h2>Our delivery method</h2><p>Six stages. Every one ends with something you can see, test or sign off.</p></div><div class="timeline">{tl}</div></div></section>
<section><div class="wrap"><div class="sec-head center rv"><h2>Results and return on investment</h2><p>We size the value before we build, and track it after launch.</p></div>{stats_block()}<div style="margin-top:36px">{roi_calc()}</div></div></section>
<section class="tint-blue"><div class="wrap"><div class="sec-head center rv"><h2>Ways to work with us</h2></div><div class="models">{mo}</div></div></section>{cta()}</main>'''
    page += footer() + "</body></html>"
    write("technologies.html", page); all_pages.append("technologies.html")

def extras():
    write("404.html", head("Page not found – JMINT", "Page not found", "404.html") + header("") + '<main><section><div class="wrap" style="text-align:center"><h1>This page took a different river.</h1><p style="margin:16px 0 26px">The page you are looking for does not exist.</p><a class="btn btn-primary" href="index.html">Back to home</a></div></section></main>' + footer() + "</body></html>")
    today = datetime.date.today().isoformat()
    urls = "".join(f'<url><loc>{URL}/{p}</loc><lastmod>{today}</lastmod><priority>{"1.0" if p=="" else "0.8"}</priority></url>' for p in all_pages)
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {URL}/sitemap.xml\n")
    llm = f"# {CONFIG['FULL']}\n\n> AI consulting, AI agent development, RAG chatbots, MCP server development, multi-agent systems, AI automation and Django full-stack development. Fixed-price, on-time, budget-friendly delivery.\n\n## Services\n"
    for s in SERVICES:
        llm += f"- [{s['name']}]({URL}/{s['slug']}.html): {s['desc']}\n"
    llm += f"\n## Other\n- [Technologies and method]({URL}/technologies.html)\n- [Projects]({URL}/projects.html)\n- [Contact]({URL}/contact.html)\n"
    write("llms.txt", llm)
    write("assets/favicon.svg", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><path d="M33 2C16 13 6 28 9 44c2 8 9 13 17 14l1 5h5l-1-6c13-4 21-16 21-30C52 20 44 9 33 2z" fill="#2e8b3d"/><path d="M30 60V16M30 28l-11-12M30 28l11-9M30 40l-14-13M30 40l13-12M30 51l-11-9M30 51l10-8" stroke="#fff" stroke-width="2.6" stroke-linecap="round" fill="none"/></svg>')
    write(".nojekyll", "")

home(); [service(s) for s in SERVICES]; projects(); technologies(); contact(); extras()
print("Built", len(all_pages) + 1, "pages")
