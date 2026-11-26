import html
import json
import os
import urllib.request
from datetime import date
from pathlib import Path

USER = os.environ.get("GH_USER", "Rehaan15790")
OUT = Path(__file__).resolve().parent.parent / "assets" / "cards"
W = 860
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Consolas,'Liberation Mono',Menlo,monospace"
HEAT = ["#ffffff", "#5c1a08", "#a32800", "#ff4500", "#ffb000"]
LEVEL = {"NONE": 0, "FIRST_QUARTILE": 1, "SECOND_QUARTILE": 2, "THIRD_QUARTILE": 3, "FOURTH_QUARTILE": 4}
ACCENTS = ["#ff4500", "#ff8c00", "#ffd166", "#ff6b35"]

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


def render(u):
    cal = u["contributionsCollection"]["contributionCalendar"]
    days = [d for w in cal["weeks"] for d in w["contributionDays"]]
    current, longest = streaks(days)
    return {
        "stats": stats_card(u, cal, current, longest),
        "languages": languages_card(u),
        "heatmap": heatmap_card(cal, longest),
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
    return body["data"]["user"]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, svg in render(fetch()).items():
        (OUT / f"{name}.svg").write_text(svg, encoding="utf-8")
        print(f"wrote assets/cards/{name}.svg")


if __name__ == "__main__":
    main()
