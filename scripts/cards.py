import html
import json
import os
import urllib.request
from datetime import date
from pathlib import Path

USER = os.environ.get("GH_USER", "Rehaan15790")
HERE = Path(__file__).resolve().parent
ASSETS = HERE.parent / "assets"
ICONS = json.loads((HERE / "icons.json").read_text())
W = 860
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Consolas,'Liberation Mono',Menlo,monospace"
HEAT = ["#ffffff", "#5c1a08", "#a32800", "#ff4500", "#ffb000"]
LEVEL = {"NONE": 0, "FIRST_QUARTILE": 1, "SECOND_QUARTILE": 2, "THIRD_QUARTILE": 3, "FOURTH_QUARTILE": 4}
ACCENTS = ["#ff4500", "#ff8c00", "#ffd166", "#ff6b35"]
STACK = [
    ("Languages", [("Python", "python"), ("Go", "go"), ("JavaScript", "javascript"), ("TypeScript", "typescript"), ("HTML5", "html5")]),
    ("AI & voice", [("Ollama", "ollama"), ("faster-whisper", "wave"), ("ElevenLabs", "elevenlabs"), ("FastAPI", "fastapi")]),
    ("Web & 3D", [("React", "react"), ("Next.js", "nextdotjs"), ("three.js", "threedotjs")]),
    ("Data & infra", [("NumPy", "numpy"), ("PostgreSQL", "postgresql"), ("SQLite", "sqlite"), ("Docker", "docker"),
                      ("pytest", "pytest"), ("GitHub Actions", "githubactions"), ("Git", "git")]),
]
TERMINAL = [
    ("whoami --verbose", [
        ("name", "Rehaan Taherbhoy"),
        ("study", "B.Tech, Artificial Intelligence & Data Science, year 1"),
        ("builds", "local-first AI: voice, LLM tooling, agents"),
        ("cares", "the security around them"),
        ("writes", "Python · Go · JavaScript · TypeScript"),
    ]),
    ("cat focus.txt", [
        ("local-first AI", "models, speech and data stay on the machine"),
        ("AI security", "sandboxing, prompt-injection defences, permission gates"),
        ("data + viz", "turning scientific data into something you can explore"),
    ]),
]
BANNER_LINES = [
    ("whoami", "rehaan · b.tech ai & data science · year one"),
    ("ls projects/", "belphegor/ ultron/ oceanlens-3d/ productivity-app/"),
    ("cat focus.txt", "local-first AI · AI security · data viz"),
]

QUERY = """
query($login: String!) {
  user(login: $login) {
    repositories(ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC, first: 100) {
      totalCount
      nodes {
        stargazerCount
        languages(first: 20, orderBy: {field: SIZE, direction: DESC}) { edges { size node { name color } } }
      }
    }
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date weekday contributionCount contributionLevel } }
      }
    }
  }
  release: repository(owner: $login, name: "ultron") { latestRelease { tagName } }
}
"""

CSS = """
text { font-family: %s; }
.mono { font-family: %s; }
.orb-a { animation: fa 9s ease-in-out infinite; }
.orb-b { animation: fb 11s ease-in-out infinite 1.1s; }
.orb-c { animation: fc 13s ease-in-out infinite .6s; }
.in { animation: in .6s ease-out both; }
.grow { animation: grow 1.1s ease-out both; transform-box: fill-box; transform-origin: left; }
.comet { animation: comet 9s linear infinite; }
.wave { animation: wave 5s ease-in-out infinite; }
.tw { animation: tw 3.2s ease-in-out infinite; }
.blip { opacity: 0; animation: blip 60ms linear; }
.blink { animation: blink 1.1s step-end infinite; }
@keyframes fa { 50%% { transform: translate(28px,-18px); opacity: .9; } }
@keyframes fb { 50%% { transform: translate(-24px,16px); opacity: .75; } }
@keyframes fc { 50%% { transform: translate(18px,-10px); opacity: .6; } }
@keyframes in { from { opacity: 0; transform: translateY(6px); } }
@keyframes grow { from { transform: scaleX(0); } }
@keyframes comet { from { stroke-dashoffset: 0; } to { stroke-dashoffset: -1000; } }
@keyframes wave { 0%%, 14%%, 100%% { stroke-opacity: .55; fill-opacity: .05; } 7%% { stroke-opacity: 1; fill-opacity: .16; } }
@keyframes tw { 50%% { opacity: .4; } }
@keyframes blip { from, to { opacity: 1; } }
@keyframes hide { from, to { opacity: 0; } }
@keyframes blink { 50%% { opacity: 0; } }
@media (prefers-reduced-motion: reduce) { * { animation: none !important; } .comet { opacity: 0; } }
""" % (SANS, MONO)


def text_w(s, size, spacing=0):
    return len(s) * (size * 0.6 + spacing) - spacing


def anim(attr, T, pts):
    keys = ";".join(f"{t / T:.4f}" for t, _ in pts)
    vals = ";".join(str(v) for _, v in pts)
    return f'<animate attributeName="{attr}" dur="{T}s" repeatCount="indefinite" calcMode="discrete" keyTimes="{keys}" values="{vals}"/>'


def show(T, on, off=None):
    pts = [(0, 0), (on, 1)] if on > 0 else [(0, 1)]
    return anim("opacity", T, pts + ([(off, 0)] if off is not None and off < T else []))


def typed(uid, x, y, text, t0, T, fs, color, cps=0.065):
    cw = fs * 0.6
    ts = [t0 + (k + 1) * cps for k in range(len(text))]
    full = len(text) * cw
    widths = [(0, 0)] + [(t, round((k + 1) * cw, 1)) for k, t in enumerate(ts)]
    xs = [(0, round(x, 1))] + [(t, round(x + (k + 1) * cw, 1)) for k, t in enumerate(ts)]
    svg = (
        f'<clipPath id="{uid}"><rect x="{x:.1f}" y="{y - fs}" width="{full + 2:.1f}" height="{fs * 1.6:.1f}">{anim("width", T, widths)}</rect></clipPath>'
        f'<text x="{x:.1f}" y="{y}" class="mono" font-size="{fs}" font-weight="600" fill="{color}" clip-path="url(#{uid})" '
        f'textLength="{full:.1f}" lengthAdjust="spacingAndGlyphs">{html.escape(text)}</text>'
        f'<rect x="{x:.1f}" y="{y - fs * .85:.1f}" width="{cw:.1f}" height="{fs * 1.05:.1f}" fill="#ffd166" opacity="0">'
        f'{anim("x", T, xs)}{anim("opacity", T, [(0, 0), (t0, 1), (ts[-1] + .3, 0)])}</rect>'
    )
    return svg, ts[-1]


def orb(i, color, peak):
    return (f'<radialGradient id="o{i}"><stop offset="0%" stop-color="{color}" stop-opacity="{peak}"/>'
            f'<stop offset="58%" stop-color="{color}" stop-opacity=".18"/>'
            f'<stop offset="100%" stop-color="{color}" stop-opacity="0"/></radialGradient>')


def comet(x, y, w, h, rx, dur=9):
    return (f'<rect class="comet" style="animation-duration:{dur}s" x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="none" '
            f'stroke="url(#fire)" stroke-width="2.5" stroke-linecap="round" pathLength="1000" stroke-dasharray="70 930"/>')


def card(h, title, sub, body, aside="", head=None, css=""):
    t = html.escape(title)
    top = head if head is not None else (
        f'<text x="46" y="64" font-size="28" font-weight="800" fill="url(#fire)">{t}</text>'
        f'<text x="48" y="88" font-size="13" font-weight="600" letter-spacing="1.2" fill="#ff8c61">{html.escape(sub)}</text>'
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}" role="img" aria-label="{t}">
<title>{t}</title>
<style>{CSS}{css}</style>
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#000"/><stop offset="54%" stop-color="#280000"/><stop offset="100%" stop-color="#000"/></linearGradient>
<linearGradient id="fire" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="#ff4500"/><stop offset="60%" stop-color="#ff8c00"/><stop offset="100%" stop-color="#ffd166"/></linearGradient>
<linearGradient id="shine" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="#fff" stop-opacity="0"/><stop offset="50%" stop-color="#fff" stop-opacity=".55"/><stop offset="100%" stop-color="#fff" stop-opacity="0"/></linearGradient>
<linearGradient id="scan" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="#ffb000" stop-opacity="0"/><stop offset="65%" stop-color="#ffb000" stop-opacity=".25"/><stop offset="88%" stop-color="#fff1e8" stop-opacity=".45"/><stop offset="100%" stop-color="#fff1e8" stop-opacity="0"/></linearGradient>
{orb(0, "#ff4500", .72)}{orb(1, "#ff8c00", .5)}{orb(2, "#ffd166", .6)}{orb(3, "#cc0000", .72)}
<clipPath id="clip"><rect width="{W}" height="{h}" rx="20"/></clipPath>
</defs>
<g clip-path="url(#clip)">
<rect width="{W}" height="{h}" fill="url(#bg)"/>
<ellipse class="orb-a" cx="140" cy="40" rx="220" ry="110" fill="url(#o0)" opacity=".6"/>
<ellipse class="orb-b" cx="660" cy="50" rx="240" ry="100" fill="url(#o1)" opacity=".45"/>
<ellipse class="orb-c" cx="480" cy="{h}" rx="320" ry="80" fill="url(#o2)" opacity=".35"/>
<ellipse class="orb-b" cx="840" cy="{h - 50}" rx="180" ry="100" fill="url(#o3)" opacity=".45"/>
<rect x="26" y="26" width="{W - 52}" height="{h - 52}" rx="20" fill="#08080c" fill-opacity=".5" stroke="#ff4500" stroke-opacity=".55"/>
{comet(26, 26, W - 52, h - 52, 20)}
{top}{aside}{body}
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{h - 1}" rx="19.5" fill="none" stroke="#ff4500" stroke-opacity=".62"/>
</svg>
'''


def icon(name, x, y, size, color):
    if name == "linkedin":
        return (f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="{size * .18:.1f}" fill="{color}"/>'
                f'<text x="{x + size / 2:.1f}" y="{y + size * .8:.1f}" text-anchor="middle" font-size="{size * .78:.1f}" '
                f'font-family="{SANS}" font-weight="900" letter-spacing="0" fill="#0a0000">in</text>')
    if name == "wave":
        bars = [(3, 9), (7, 5), (11, 2), (15, 6), (19, 10)]
        return "".join(f'<rect x="{x + bx * size / 24:.1f}" y="{y + by * size / 24:.1f}" width="{size * 2.4 / 24:.1f}" '
                       f'height="{size * (24 - 2 * by) / 24:.1f}" rx="{size / 24:.1f}" fill="{color}"/>' for bx, by in bars)
    return (f'<svg x="{x}" y="{y}" width="{size}" height="{size}" viewBox="0 0 24 24">'
            f'<path d="{ICONS[name]}" fill="{color}"/></svg>')


def badge(label, value, icon_name=None, h=22):
    fs, ls = (12, 1) if h >= 28 else (11, .8)
    lw, vw = text_w(label.upper(), fs, ls), text_w(value, fs, ls)
    isz = round(h * .5)
    lx = 10 + (isz + 7 if icon_name else 0)
    split = lx + lw + 10
    w = split + vw + 20
    ty = h / 2 + fs * .35
    alt = html.escape(f"{label}: {value}")
    travel = w - split + 40
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w:.0f}" height="{h}" viewBox="0 0 {w:.1f} {h}" role="img" aria-label="{alt}">
<title>{alt}</title>
<defs>
<linearGradient id="fire" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="#ff4500"/><stop offset="100%" stop-color="#ff8c00"/></linearGradient>
<linearGradient id="sh" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="#fff" stop-opacity="0"/><stop offset="50%" stop-color="#fff" stop-opacity=".5"/><stop offset="100%" stop-color="#fff" stop-opacity="0"/></linearGradient>
<clipPath id="c"><rect width="{w:.1f}" height="{h}" rx="6"/></clipPath>
<clipPath id="v"><rect x="{split:.1f}" width="{w - split:.1f}" height="{h}"/></clipPath>
</defs>
<g clip-path="url(#c)" font-family="{MONO}" font-size="{fs}" font-weight="700" letter-spacing="{ls}">
<rect width="{split:.1f}" height="{h}" fill="#0a0000"/>
<rect x="{split:.1f}" width="{w - split:.1f}" height="{h}" fill="url(#fire)"/>
{icon(icon_name, 10, (h - isz) / 2, isz, "#ff6b35") if icon_name else ""}
<text x="{lx}" y="{ty:.1f}" fill="#ff8c61" textLength="{lw:.1f}" lengthAdjust="spacingAndGlyphs">{html.escape(label.upper())}</text>
<text x="{split + 10:.1f}" y="{ty:.1f}" fill="#140300" textLength="{vw:.1f}" lengthAdjust="spacingAndGlyphs">{html.escape(value)}</text>
<g clip-path="url(#v)"><rect x="{split - 40:.1f}" width="40" height="{h}" fill="url(#sh)"><animateTransform attributeName="transform" type="translate" values="0 0;{travel:.1f} 0;{travel:.1f} 0" keyTimes="0;.3;1" dur="5s" repeatCount="indefinite"/></rect></g>
</g>
<rect x=".5" y=".5" width="{w - 1:.1f}" height="{h - 1}" rx="5.5" fill="none" stroke="#ff4500" stroke-opacity=".8"/>
</svg>
'''


def banner():
    T, fs, x, y = 15, 14, 96, 334
    cw, per = fs * .6, T / len(BANNER_LINES)
    lines = []
    for i, (cmd, out) in enumerate(BANNER_LINES):
        s, e = i * per, (i + 1) * per
        cx = x + 2 * cw
        typ, end = typed(f"b{i}", cx, y, cmd, s + .3, T, fs, "#ff8c61")
        rx, rw = cx + (len(cmd) + 2) * cw, text_w(out, fs)
        lines.append(
            f'<g>{show(T, s, e)}<text x="{x}" y="{y}" class="mono" font-size="{fs}" font-weight="700" fill="#ff4500">$</text>{typ}'
            f'<g>{show(T, end + .3, e)}<text x="{rx:.1f}" y="{y}" class="mono" font-size="{fs}" font-weight="600" fill="#fff1e8" fill-opacity=".85" '
            f'textLength="{rw:.1f}" lengthAdjust="spacingAndGlyphs">{html.escape(out)}</text>'
            f'<rect class="blink" x="{rx + rw + 6:.1f}" y="{y - 12}" width="8" height="15" fill="#ffd166"/></g></g>'
        )
    embers = [(140, 2, "#ff8c00", 7, 0), (260, 1.5, "#ffd166", 9, 2), (380, 2.5, "#ff4500", 8, 4), (500, 1.5, "#ff8c00", 10, 1),
              (610, 2, "#ffd166", 7.5, 3), (720, 2.5, "#ff4500", 9.5, 5), (830, 1.5, "#ff8c00", 8.5, .5), (940, 2, "#ffd166", 11, 2.5),
              (1040, 2.5, "#ff4500", 7, 4.5), (1160, 1.5, "#ff8c00", 9, 1.5), (70, 1.5, "#ffd166", 10, 6), (1230, 2, "#ff4500", 8, 3.5)]
    ember_svg = "".join(f'<circle class="ember" cx="{ex}" cy="398" r="{r}" fill="{c}" style="animation-duration:{d}s;animation-delay:{dl}s"/>'
                        for ex, r, c, d, dl in embers)
    chips = [("LOCAL-FIRST AI", 300, 150), ("VOICE", 464, 90), ("LLM TOOLING", 568, 130), ("AI SECURITY", 712, 130), ("DATA VIZ", 856, 110)]
    chip_svg = "".join(
        f'<g class="chip" style="animation-delay:{i * 90}ms"><rect class="wave" style="animation-delay:{1 + i * .15:.2f}s" x="{cx}" y="236" width="{w}" height="30" rx="15" '
        f'fill="#fff" fill-opacity=".055" stroke="#ff4500" stroke-opacity=".68"/><text x="{cx + w / 2:.0f}" y="256" text-anchor="middle">{t}</text></g>'
        for i, (t, cx, w) in enumerate(chips)
    )
    name = 'x="298" y="180" font-size="68" font-weight="900" textLength="760" lengthAdjust="spacingAndGlyphs"'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 400" width="1280" height="400" role="img" aria-labelledby="title desc">
  <title id="title">Rehaan Taherbhoy</title>
  <desc id="desc">B.Tech AI and Data Science. Local-first AI, voice, LLM tooling and the security around them.</desc>
  <style>
    .sans {{ font-family: {SANS}; }}
    .mono {{ font-family: {MONO}; }}
    .orb-a {{ animation: fa 9s ease-in-out infinite; }}
    .orb-b {{ animation: fb 11s ease-in-out infinite 1.1s; }}
    .orb-c {{ animation: fc 13s ease-in-out infinite .6s; }}
    .ring {{ animation: ring 8s ease-in-out infinite; }}
    .ring-b {{ animation: ring 10s ease-in-out infinite 1.6s; }}
    .cursor, .blink {{ animation: blink 1.1s step-end infinite; }}
    .chip {{ animation: chip .7s ease-out both; }}
    .wave {{ animation: wave 5s ease-in-out infinite; }}
    .ember {{ animation: rise linear infinite; }}
    .pulse {{ animation: pulse 2.6s ease-in-out infinite; }}
    .comet {{ animation: comet 10s linear infinite; }}
    .jit {{ animation: jit 7s step-end infinite; }}
    .g1 {{ opacity: 0; animation: g1 7s step-end infinite; }}
    .g2 {{ opacity: 0; animation: g2 7s step-end infinite; }}
    @keyframes fa {{ 0%,100% {{ transform: translate(0,0); opacity: .58; }} 50% {{ transform: translate(40px,-24px); opacity: .9; }} }}
    @keyframes fb {{ 0%,100% {{ transform: translate(0,0); opacity: .42; }} 50% {{ transform: translate(-36px,20px); opacity: .74; }} }}
    @keyframes fc {{ 0%,100% {{ transform: translate(0,0); opacity: .34; }} 50% {{ transform: translate(24px,-14px); opacity: .62; }} }}
    @keyframes ring {{ 0%,100% {{ opacity: .1; }} 50% {{ opacity: .32; }} }}
    @keyframes blink {{ 50% {{ opacity: 0; }} }}
    @keyframes chip {{ from {{ opacity: 0; transform: translateY(8px); }} to {{ opacity: 1; transform: translateY(0); }} }}
    @keyframes wave {{ 0%,14%,100% {{ stroke-opacity: .6; fill-opacity: .055; }} 7% {{ stroke-opacity: 1; fill-opacity: .18; }} }}
    @keyframes rise {{ 0% {{ transform: translateY(0); opacity: 0; }} 12% {{ opacity: .9; }} 100% {{ transform: translateY(-330px); opacity: 0; }} }}
    @keyframes pulse {{ 0%,100% {{ opacity: .35; }} 50% {{ opacity: 1; }} }}
    @keyframes comet {{ from {{ stroke-dashoffset: 0; }} to {{ stroke-dashoffset: -1000; }} }}
    @keyframes jit {{ 0%,90% {{ transform: none; }} 91% {{ transform: translate(3px,0); }} 92% {{ transform: translate(-2px,1px); }} 93% {{ transform: none; }} }}
    @keyframes g1 {{ 0%,90% {{ opacity: 0; transform: none; }} 91% {{ opacity: .8; transform: translate(-5px,1px); }} 92% {{ opacity: .6; transform: translate(4px,-2px); }} 93% {{ opacity: 0; transform: none; }} }}
    @keyframes g2 {{ 0%,90% {{ opacity: 0; transform: none; }} 91% {{ opacity: .7; transform: translate(5px,-1px); }} 92% {{ opacity: .5; transform: translate(-3px,2px); }} 93% {{ opacity: 0; transform: none; }} }}
    @media (prefers-reduced-motion: reduce) {{ .orb-a, .orb-b, .orb-c, .ring, .ring-b, .cursor, .blink, .chip, .wave, .ember, .pulse, .comet, .jit, .g1, .g2 {{ animation: none; }} .ember, .comet, .g1, .g2 {{ opacity: 0; }} }}
  </style>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#000000"/><stop offset="54%" stop-color="#280000"/><stop offset="100%" stop-color="#000000"/></linearGradient>
    {orb(0, "#ff4500", .72)}{orb(1, "#ff8c00", .5)}{orb(2, "#ffd166", .6)}{orb(3, "#cc0000", .72)}
    <linearGradient id="fire" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="#ff4500"/><stop offset="60%" stop-color="#ff8c00"/><stop offset="100%" stop-color="#ffd166"/></linearGradient>
    <linearGradient id="shine" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="#ff6b35" stop-opacity="0"/><stop offset="40%" stop-color="#ff4500" stop-opacity=".8"/><stop offset="100%" stop-color="#ff8c61" stop-opacity="0"/></linearGradient>
    <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="#ff6b35" stroke-opacity=".05"/></pattern>
    <filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="7"/></filter>
    <clipPath id="clip"><rect width="1280" height="400" rx="28"/></clipPath>
  </defs>
  <g clip-path="url(#clip)">
    <rect width="1280" height="400" fill="url(#bg)"/>
    <rect width="1280" height="400" fill="url(#grid)"/>
    <ellipse class="orb-a" cx="200" cy="60" rx="320" ry="150" fill="url(#o0)"/>
    <ellipse class="orb-b" cx="980" cy="70" rx="360" ry="140" fill="url(#o1)"/>
    <ellipse class="orb-c" cx="720" cy="380" rx="460" ry="110" fill="url(#o2)"/>
    <ellipse class="orb-b" cx="1240" cy="320" rx="260" ry="140" fill="url(#o3)"/>
    <circle class="ring" cx="1140" cy="200" r="28" fill="none" stroke="#ff6b35" stroke-opacity=".5"/>
    <circle class="ring-b" cx="1140" cy="200" r="48" fill="none" stroke="#ff6b35" stroke-opacity=".36"/>
    <circle class="ring" cx="1140" cy="200" r="72" fill="none" stroke="#ff6b35" stroke-opacity=".24"/>
    <g><circle cx="1188" cy="200" r="4" fill="#ff4500"/><animateTransform attributeName="transform" type="rotate" from="0 1140 200" to="360 1140 200" dur="9s" repeatCount="indefinite"/></g>
    <g><circle cx="1212" cy="200" r="3" fill="#ffd166"/><animateTransform attributeName="transform" type="rotate" from="360 1140 200" to="0 1140 200" dur="14s" repeatCount="indefinite"/></g>
    <g>{ember_svg}</g>
    <rect x="36" y="36" width="1208" height="328" rx="24" fill="#08080c" fill-opacity=".5" stroke="#ff4500" stroke-opacity=".55"/>
    {comet(36, 36, 1208, 328, 24, 10)}
    <rect x="96" y="104" width="160" height="160" rx="22" fill="#0c0303" stroke="#ff4500" stroke-width="3"/>
    <rect class="pulse" x="96" y="104" width="160" height="160" rx="22" fill="none" stroke="#ff4500" stroke-width="3" filter="url(#glow)"/>
    <path d="M130 152l36 32-36 32" fill="none" stroke="url(#fire)" stroke-width="14" stroke-linecap="square"/>
    <rect class="cursor" x="180" y="208" width="46" height="12" fill="#ffd166"/>
    <text x="300" y="104" class="sans" font-size="14" font-weight="800" letter-spacing="3" fill="#ff8c61">@REHAAN15790</text>
    <path d="M300 116 C420 92 560 92 680 118" fill="none" stroke="url(#shine)" stroke-width="2" stroke-linecap="round" opacity=".7"/>
    <text class="sans g1" {name} fill="#ff1e2d">REHAAN TAHERBHOY</text>
    <text class="sans g2" {name} fill="#ffd166">REHAAN TAHERBHOY</text>
    <text class="sans jit" {name}><tspan fill="#fff1e8">REHAAN</tspan><tspan fill="url(#fire)"> TAHERBHOY</tspan></text>
    <text x="302" y="216" class="sans" font-size="17" font-weight="600" fill="#ff8c61" textLength="640" lengthAdjust="spacing">B.TECH ARTIFICIAL INTELLIGENCE &amp; DATA SCIENCE · YEAR ONE</text>
    <g class="mono" font-size="13" font-weight="700" fill="#ff6b35">{chip_svg}</g>
    <path d="M96 300H1184" stroke="url(#shine)" stroke-width="1.5"/>
    {"".join(lines)}
    <text x="1184" y="334" text-anchor="end" class="mono" font-size="12" font-weight="600" fill="#ff8c61" fill-opacity=".55">github.com/{USER}</text>
  </g>
  <rect x=".75" y=".75" width="1278.5" height="398.5" rx="27.5" fill="none" stroke="#ff4500" stroke-opacity=".62" stroke-width="1.5"/>
</svg>
'''


def terminal_card():
    T, fs, lh, x0, y, t = 16, 13, 22, 50, 112, .5
    cw = fs * .6
    prompt = "rehaan@github ~ $"
    px = x0 + (len(prompt) + 1) * cw
    body = []

    def prompt_at(y, t):
        return (f'<g>{show(T, t)}<text x="{x0}" y="{y}" class="mono" font-size="{fs}" font-weight="700" textLength="{text_w(prompt, fs):.1f}" '
                f'lengthAdjust="spacingAndGlyphs"><tspan fill="#ff4500">rehaan@github</tspan><tspan fill="#ffd166"> ~ </tspan><tspan fill="#fff1e8">$</tspan></text></g>')

    for i, (cmd, rows) in enumerate(TERMINAL):
        body.append(prompt_at(y, t))
        typ, end = typed(f"t{i}", px, y, cmd, t + .15, T, fs, "#fff1e8")
        body.append(typ)
        t, y = end + .35, y + lh
        vx = x0 + 16 + (max(len(k) for k, _ in rows) + 3) * cw
        for k, v in rows:
            body.append(
                f'<g>{show(T, t)}<text x="{x0 + 16}" y="{y}" class="mono" font-size="{fs}" font-weight="700" fill="#ff8c61" '
                f'textLength="{text_w(k, fs):.1f}" lengthAdjust="spacingAndGlyphs">{html.escape(k)}</text>'
                f'<text x="{vx:.1f}" y="{y}" class="mono" font-size="{fs}" fill="#fff1e8" fill-opacity=".9" '
                f'textLength="{text_w(v, fs):.1f}" lengthAdjust="spacingAndGlyphs">{html.escape(v)}</text></g>'
            )
            t, y = t + .12, y + lh
        t += .6
    body.append(prompt_at(y, t))
    body.append(f'<g>{show(T, t)}<rect class="blink" x="{px:.1f}" y="{y - 11}" width="{cw:.1f}" height="14" fill="#ffd166"/></g>')
    head = (
        '<circle cx="50" cy="54" r="6" fill="#ff4500"/><circle cx="70" cy="54" r="6" fill="#ff8c00"/><circle cx="90" cy="54" r="6" fill="#ffd166"/>'
        f'<text x="{W / 2:.0f}" y="58" text-anchor="middle" class="mono" font-size="12" font-weight="600" fill="#ff8c61">rehaan@github: ~</text>'
        f'<path d="M26 78H{W - 26}" stroke="#ff4500" stroke-opacity=".35"/>'
    )
    return card(y + 44, "Terminal: whoami and focus", "", "".join(body), head=head)


def stack_card():
    body, y, n = [], 108, 0
    for group, tools in STACK:
        body.append(f'<text x="46" y="{y + 20}" class="mono" font-size="11" font-weight="800" letter-spacing="1.6" '
                    f'fill="#ff8c61">{html.escape(group.upper())}</text>')
        x = 190
        for name, ic in tools:
            tw = text_w(name, 12, .5)
            cw = 12 + 14 + 8 + tw + 14
            if x + cw > W - 46:
                x, y = 190, y + 40
            body.append(
                f'<g class="in" style="animation-delay:{n * 40}ms">'
                f'<rect class="wave" style="animation-delay:{1 + n * .12:.2f}s" x="{x}" y="{y}" width="{cw:.1f}" height="30" rx="15" '
                f'fill="#fff" fill-opacity=".05" stroke="#ff4500" stroke-opacity=".55"/>'
                f'{icon(ic, x + 12, y + 8, 14, "#ff6b35")}'
                f'<text x="{x + 34}" y="{y + 19.5}" class="mono" font-size="12" font-weight="700" letter-spacing=".5" fill="#fff1e8" '
                f'textLength="{tw:.1f}" lengthAdjust="spacingAndGlyphs">{html.escape(name)}</text></g>'
            )
            x, n = x + cw + 10, n + 1
        y += 48
    return card(y + 30, "Stack", "Tools I build with", "".join(body))


def render_static():
    return {
        "banner": banner(),
        "cards/terminal": terminal_card(),
        "cards/stack": stack_card(),
        "badges/linkedin": badge("LinkedIn", "Rehaan Taherbhoy", "linkedin", 30),
        "badges/github": badge("GitHub", USER, "github", 30),
        "badges/sih": badge("SIH 2026", "PS 26067"),
        "badges/open-app": badge("open", "the app"),
    }


def cell(x, y, level, extra=""):
    dim = ' fill-opacity=".07"' if level == 0 else ""
    return f'<rect{extra} x="{x:.1f}" y="{y}" width="11" height="11" rx="2.5" fill="{HEAT[level]}"{dim}/>'


def streaks(days):
    longest = run = 0
    for d in days:
        run = run + 1 if d["contributionCount"] else 0
        longest = max(longest, run)
    tail = days[:-1] if days and not days[-1]["contributionCount"] else days
    current = 0
    for d in reversed(tail):
        if not d["contributionCount"]:
            break
        current += 1
    return current, longest


def count_up(x, y, value, color, delay, frames=14, step=60):
    attrs = f'x="{x}" y="{y}" font-size="36" font-weight="900" fill="{color}"'
    ticks = "".join(f'<text class="blip" style="animation-delay:{delay + k * step}ms" {attrs}>{round(value * (1 - (1 - k / frames) ** 3)):,}</text>'
                    for k in range(frames))
    return ticks + f'<text style="animation:hide {delay + frames * step}ms linear" {attrs}>{value:,}</text>'


def stats_card(u, cal, current, longest):
    stars = sum(r["stargazerCount"] for r in u["repositories"]["nodes"])
    tiles = [
        ("Contributions", cal["totalContributions"], "last 12 months"),
        ("Current streak", current, f"best: {longest} days"),
        ("Stars", stars, "across my repos"),
        ("Repos", u["repositories"]["totalCount"], "public, not forks"),
    ]
    body = "".join(
        f'<g class="in" style="animation-delay:{i * 90}ms">'
        f'<rect class="wave" style="animation-delay:{1.5 + i * .2:.1f}s" x="{x}" y="108" width="180" height="100" rx="14" fill="#fff" fill-opacity=".05" stroke="#ff4500" stroke-opacity=".55"/>'
        f'<rect x="{x + 18}" y="108" width="40" height="3" rx="1.5" fill="{c}"/>'
        f'<text x="{x + 18}" y="136" font-size="11" font-weight="800" letter-spacing="1.6" fill="#ff8c61">{label.upper()}</text>'
        f'{count_up(x + 18, 178, value, c, 300 + i * 90)}'
        f'<text x="{x + 18}" y="196" font-size="11" fill="#ff8c61" fill-opacity=".75">{note}</text></g>'
        for i, ((label, value, note), c, x) in enumerate(zip(tiles, ACCENTS, range(46, W, 196)))
    )
    return card(252, "GitHub Stats", f"@{USER.lower()} · public activity, refreshed daily", body)


def languages_card(u):
    totals = {}
    for repo in u["repositories"]["nodes"]:
        for e in repo["languages"]["edges"]:
            n = e["node"]
            totals.setdefault(n["name"], [0, n["color"] or "#ff6b35"])[0] += e["size"]
    total = sum(v[0] for v in totals.values()) or 1
    top = sorted(totals.items(), key=lambda kv: -kv[1][0])[:6]
    rows = []
    for i, (name, (size, color)) in enumerate(top):
        y, pct = 130 + i * 34, size / total
        bw = max(490 * pct, 3)
        begin = 1.4 + i * .3
        rows.append(
            f'<g class="in" style="animation-delay:{i * 90}ms">'
            f'<circle cx="52" cy="{y - 5}" r="5" fill="{color}"><animate attributeName="r" values="5;6.5;5" dur="2.4s" begin="{i * .4:.1f}s" repeatCount="indefinite"/></circle>'
            f'<text x="66" y="{y}" font-size="14" font-weight="700" fill="#fff1e8">{html.escape(name)}</text>'
            f'<text x="300" y="{y}" text-anchor="end" class="mono" font-size="13" font-weight="700" fill="#ff8c61">{pct:.1%}</text>'
            f'<rect x="324" y="{y - 10}" width="490" height="8" rx="4" fill="#fff" fill-opacity=".07"/>'
            f'<clipPath id="b{i}"><rect x="324" y="{y - 10}" width="{bw:.1f}" height="8" rx="4"/></clipPath>'
            f'<rect class="grow" style="animation-delay:{i * 90}ms" x="324" y="{y - 10}" width="{bw:.1f}" height="8" rx="4" fill="url(#fire)"/>'
            f'<g clip-path="url(#b{i})"><rect x="264" y="{y - 10}" width="60" height="8" fill="url(#shine)" opacity="0">'
            f'<animateTransform attributeName="transform" type="translate" values="0 0;{bw + 60:.1f} 0;{bw + 60:.1f} 0" keyTimes="0;.4;1" '
            f'dur="3.2s" begin="{begin:.1f}s" repeatCount="indefinite"/><set attributeName="opacity" to="1" begin="{begin:.1f}s"/></rect></g></g>'
        )
    return card(150 + len(top) * 34, "Languages", "Share of code across my public repositories", "".join(rows))


def heatmap_card(cal, longest):
    weeks = cal["weeks"]
    x0, y0, step = (W - (len(weeks) * 14 - 3)) / 2, 124, 14
    gw = len(weeks) * step - 3
    months, last, last_x = [], None, -99
    cols = []
    for wi, w in enumerate(weeks):
        x = x0 + wi * step
        m = date.fromisoformat(w["contributionDays"][0]["date"]).strftime("%b")
        if m != last:
            label = f'<text x="{x:.1f}" y="114" font-size="10" font-weight="600" fill="#ff8c61" fill-opacity=".8">{m}</text>'
            months[-1:] = [label] if months and x - last_x < 30 else months[-1:] + [label]
            last, last_x = m, x
        cells = "".join(
            cell(x, y0 + d["weekday"] * step, lv,
                 f' class="tw" style="animation-delay:{(wi * 7 + d["weekday"] * 13) % 32 * 100}ms"' if lv >= 3 else "")
            for d in w["contributionDays"] for lv in [LEVEL[d["contributionLevel"]]]
        )
        cols.append(f'<g class="in" style="animation-delay:{wi * 12}ms">{cells}</g>')
    scan = (f'<clipPath id="grid"><rect x="{x0 - 2:.1f}" y="{y0 - 2}" width="{gw + 4:.1f}" height="{7 * step + 1}"/></clipPath>'
            f'<g clip-path="url(#grid)"><rect class="scan" x="{x0 - 90:.1f}" y="{y0 - 2}" width="90" height="{7 * step + 1}" fill="url(#scan)"/></g>')
    css = (f".scan {{ animation: scan 6s ease-in-out infinite 1.2s; }}"
           f"@keyframes scan {{ 0% {{ transform: translateX(0); }} 60%, 100% {{ transform: translateX({gw + 90:.0f}px); }} }}"
           f"@media (prefers-reduced-motion: reduce) {{ .scan {{ opacity: 0; }} }}")
    legend = (
        '<text x="704" y="64" text-anchor="end" font-size="10" fill="#ff8c61">Less</text>'
        + "".join(cell(710 + i * 14, 55, i) for i in range(5))
        + '<text x="784" y="64" font-size="10" fill="#ff8c61">More</text>'
    )
    sub = f"{cal['totalContributions']:,} contributions in the last year · longest streak {longest} days"
    return card(262, "Contributions", sub, "".join(months) + "".join(cols) + scan, legend, css=css)


def render(data):
    u = data["user"]
    cal = u["contributionsCollection"]["contributionCalendar"]
    days = [d for w in cal["weeks"] for d in w["contributionDays"]]
    current, longest = streaks(days)
    tag = ((data.get("release") or {}).get("latestRelease") or {}).get("tagName", "none")
    return {
        "cards/stats": stats_card(u, cal, current, longest),
        "cards/languages": languages_card(u),
        "cards/heatmap": heatmap_card(cal, longest),
        "badges/ultron-release": badge("release", tag, "github"),
    }


def fetch():
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        json.dumps({"query": QUERY, "variables": {"login": USER}}).encode(),
        {"Authorization": f"bearer {os.environ['GITHUB_TOKEN']}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        body = json.load(r)
    if body.get("errors"):
        raise SystemExit(body["errors"])
    return body["data"]


def main():
    files = render_static()
    if os.environ.get("GITHUB_TOKEN"):
        files |= render(fetch())
    else:
        print("GITHUB_TOKEN not set: drawing only the cards and badges that need no GitHub data")
    for name, svg in files.items():
        path = ASSETS / f"{name}.svg"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(svg, encoding="utf-8")
        print(f"wrote assets/{name}.svg")


if __name__ == "__main__":
    main()
