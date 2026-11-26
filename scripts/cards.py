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
@keyframes fa { 50%% { transform: translate(28px,-18px); opacity: .9; } }
@keyframes fb { 50%% { transform: translate(-24px,16px); opacity: .75; } }
@keyframes fc { 50%% { transform: translate(18px,-10px); opacity: .6; } }
@keyframes in { from { opacity: 0; transform: translateY(6px); } }
@keyframes grow { from { transform: scaleX(0); } }
@media (prefers-reduced-motion: reduce) { * { animation: none !important; } }
""" % (SANS, MONO)


def orb(i, color, peak):
    return (f'<radialGradient id="o{i}"><stop offset="0%" stop-color="{color}" stop-opacity="{peak}"/>'
            f'<stop offset="58%" stop-color="{color}" stop-opacity=".18"/>'
            f'<stop offset="100%" stop-color="{color}" stop-opacity="0"/></radialGradient>')


def card(h, title, sub, body, aside=""):
    t = html.escape(title)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}" role="img" aria-label="{t}">
<title>{t}</title>
<style>{CSS}</style>
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#000"/><stop offset="54%" stop-color="#280000"/><stop offset="100%" stop-color="#000"/></linearGradient>
<linearGradient id="fire" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="#ff4500"/><stop offset="60%" stop-color="#ff8c00"/><stop offset="100%" stop-color="#ffd166"/></linearGradient>
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
<text x="46" y="64" font-size="28" font-weight="800" fill="url(#fire)">{t}</text>
<text x="48" y="88" font-size="13" font-weight="600" letter-spacing="1.2" fill="#ff8c61">{html.escape(sub)}</text>
{aside}{body}
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{h - 1}" rx="19.5" fill="none" stroke="#ff4500" stroke-opacity=".62"/>
</svg>
'''


def text_w(s, size, spacing):
    return len(s) * (size * 0.6 + spacing) - spacing


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
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w:.0f}" height="{h}" viewBox="0 0 {w:.1f} {h}" role="img" aria-label="{alt}">
<title>{alt}</title>
<defs>
<linearGradient id="fire" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="#ff4500"/><stop offset="100%" stop-color="#ff8c00"/></linearGradient>
<clipPath id="c"><rect width="{w:.1f}" height="{h}" rx="6"/></clipPath>
</defs>
<g clip-path="url(#c)" font-family="{MONO}" font-size="{fs}" font-weight="700" letter-spacing="{ls}">
<rect width="{split:.1f}" height="{h}" fill="#0a0000"/>
<rect x="{split:.1f}" width="{w - split:.1f}" height="{h}" fill="url(#fire)"/>
{icon(icon_name, 10, (h - isz) / 2, isz, "#ff6b35") if icon_name else ""}
<text x="{lx}" y="{ty:.1f}" fill="#ff8c61" textLength="{lw:.1f}" lengthAdjust="spacingAndGlyphs">{html.escape(label.upper())}</text>
<text x="{split + 10:.1f}" y="{ty:.1f}" fill="#140300" textLength="{vw:.1f}" lengthAdjust="spacingAndGlyphs">{html.escape(value)}</text>
</g>
<rect x=".5" y=".5" width="{w - 1:.1f}" height="{h - 1}" rx="5.5" fill="none" stroke="#ff4500" stroke-opacity=".8"/>
</svg>
'''


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
                f'<rect x="{x}" y="{y}" width="{cw:.1f}" height="30" rx="15" fill="#fff" fill-opacity=".055" stroke="#ff4500" stroke-opacity=".6"/>'
                f'{icon(ic, x + 12, y + 8, 14, "#ff6b35")}'
                f'<text x="{x + 34}" y="{y + 19.5}" class="mono" font-size="12" font-weight="700" letter-spacing=".5" fill="#fff1e8" '
                f'textLength="{tw:.1f}" lengthAdjust="spacingAndGlyphs">{html.escape(name)}</text></g>'
            )
            x, n = x + cw + 10, n + 1
        y += 48
    return card(y + 30, "Stack", "Tools I build with", "".join(body))


def render_static():
    return {
        "cards/stack": stack_card(),
        "badges/linkedin": badge("LinkedIn", "Rehaan Taherbhoy", "linkedin", 30),
        "badges/github": badge("GitHub", USER, "github", 30),
        "badges/sih": badge("SIH 2026", "PS 26067"),
        "badges/open-app": badge("open", "the app"),
    }


def cell(x, y, level):
    dim = ' fill-opacity=".07"' if level == 0 else ""
    return f'<rect x="{x:.1f}" y="{y}" width="11" height="11" rx="2.5" fill="{HEAT[level]}"{dim}/>'


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
        f'<rect x="{x}" y="108" width="180" height="100" rx="14" fill="#fff" fill-opacity=".04" stroke="#ff4500" stroke-opacity=".45"/>'
        f'<rect x="{x + 18}" y="108" width="40" height="3" rx="1.5" fill="{c}"/>'
        f'<text x="{x + 18}" y="136" font-size="11" font-weight="800" letter-spacing="1.6" fill="#ff8c61">{label.upper()}</text>'
        f'<text x="{x + 18}" y="178" font-size="36" font-weight="900" fill="{c}">{value:,}</text>'
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
        rows.append(
            f'<g class="in" style="animation-delay:{i * 90}ms">'
            f'<circle cx="52" cy="{y - 5}" r="5" fill="{color}"/>'
            f'<text x="66" y="{y}" font-size="14" font-weight="700" fill="#fff1e8">{html.escape(name)}</text>'
            f'<text x="300" y="{y}" text-anchor="end" class="mono" font-size="13" font-weight="700" fill="#ff8c61">{pct:.1%}</text>'
            f'<rect x="324" y="{y - 10}" width="490" height="8" rx="4" fill="#fff" fill-opacity=".07"/>'
            f'<rect class="grow" style="animation-delay:{i * 90}ms" x="324" y="{y - 10}" width="{max(490 * pct, 3):.1f}" height="8" rx="4" fill="url(#fire)"/></g>'
        )
    return card(150 + len(top) * 34, "Languages", "Share of code across my public repositories", "".join(rows))


def heatmap_card(cal, longest):
    weeks = cal["weeks"]
    x0, y0, step = (W - (len(weeks) * 14 - 3)) / 2, 124, 14
    months, last, last_x = [], None, -99
    cols = []
    for wi, w in enumerate(weeks):
        x = x0 + wi * step
        m = date.fromisoformat(w["contributionDays"][0]["date"]).strftime("%b")
        if m != last:
            label = f'<text x="{x:.1f}" y="114" font-size="10" font-weight="600" fill="#ff8c61" fill-opacity=".8">{m}</text>'
            months[-1:] = [label] if months and x - last_x < 30 else months[-1:] + [label]
            last, last_x = m, x
        cells = "".join(cell(x, y0 + d["weekday"] * step, LEVEL[d["contributionLevel"]]) for d in w["contributionDays"])
        cols.append(f'<g class="in" style="animation-delay:{wi * 12}ms">{cells}</g>')
    legend = (
        '<text x="704" y="64" text-anchor="end" font-size="10" fill="#ff8c61">Less</text>'
        + "".join(cell(710 + i * 14, 55, i) for i in range(5))
        + '<text x="784" y="64" font-size="10" fill="#ff8c61">More</text>'
    )
    sub = f"{cal['totalContributions']:,} contributions in the last year · longest streak {longest} days"
    return card(262, "Contributions", sub, "".join(months) + "".join(cols), legend)


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
