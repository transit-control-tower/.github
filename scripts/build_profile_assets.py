"""
transit-control-tower 조직 프로필 SVG 생성기

사용법 (저장소 루트에서):
    python scripts/build_profile_assets.py

profile/assets/ 아래에 다크·라이트 SVG를 모두 다시 만듭니다.
진행 상태(ROADMAP)나 문구를 바꾼 뒤 다시 실행하면 됩니다.

글자는 선택한 글꼴의 윤곽선(path)으로 변환해 넣습니다. 보는 사람 PC에 글꼴이 없어도 똑같이 보입니다.
필요 패키지:  pip install uharfbuzz fonttools
글꼴은 FONT_FAMILY로 고르고, 첫 실행 때 공식 저장소에서 scripts/fonts/ 로 받아 둡니다.
패키지나 글꼴이 없으면 예전처럼 시스템 글꼴 <text>로 만듭니다.
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "profile" / "assets"

# 메인 배너(banner-dark/light.png)에서 추출한 색
GREEN = "#00A84D"   # 지하철 · 실시간 관측
BLUE = "#3D5BAB"    # 버스 · 근거 검색
PINK = "#E5336F"    # 잠실 · 혼잡 예측 · 현재 위치

THEMES = {
    "dark": dict(bg="#1E2733", ink="#F3F5F7", muted="#9AA3AF", faint="#3A4454",
                 station="#1E2733", ring="#F3F5F7", train="#FFFFFF"),
    "light": dict(bg="#F2F4F3", ink="#202833", muted="#626B78", faint="#D3D8DD",
                  station="#FFFFFF", ring="#202833", train="#FFFFFF"),
}

FONT = ("Pretendard, 'Pretendard Variable', 'Apple SD Gothic Neo', 'Malgun Gothic', "
        "'Noto Sans KR', 'Noto Sans CJK KR', system-ui, sans-serif")


def svg(w, h, t, body, title, extra_style="", radius=0):
    style = f"""
    text {{ font-family: {FONT}; }}
    .b {{ font-weight: 700; }}
    .xb {{ font-weight: 800; letter-spacing: -0.02em; }}
    """
    if extra_style:
        style += extra_style
    clip_defs = (f'<defs><clipPath id="banner-clip"><rect width="{w}" height="{h}" '
                 f'rx="{radius}"/></clipPath></defs>\n') if radius else ""
    clip_open = '<g clip-path="url(#banner-clip)">\n' if radius else ""
    clip_close = '</g>\n' if radius else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title)}">\n'
            f'<title>{escape(title)}</title>\n<style>{style}</style>\n'
            f'{glyph_defs()}{clip_defs}{clip_open}<rect width="{w}" height="{h}" fill="{t["bg"]}"/>\n'
            f'{body}\n{clip_close}</svg>\n')


# ---------------------------------------------------------------- 글자 → 윤곽선
FONT_DIR = Path(__file__).resolve().parent / "fonts"

# 쓸 글꼴: 아래 FAMILIES의 키 중 하나 (모두 무료·상업 이용 가능한 오픈 라이선스)
FONT_FAMILY = "WantedSans"

FAMILIES = {
    "Pretendard": ("https://github.com/orioncactus/pretendard/raw/v1.3.9/"
                   "packages/pretendard/dist/public/static/Pretendard-{w}.otf",
                   {"": "Regular", "b": "Bold", "xb": "ExtraBold"}),
    "SUIT": ("https://raw.githubusercontent.com/sun-typeface/SUIT/55118d981336d8fce005eb62888c12c0568ef7b0/"
             "fonts/static/otf/SUIT-{w}.otf",
             {"": "Regular", "b": "Bold", "xb": "ExtraBold"}),
    "WantedSans": ("https://raw.githubusercontent.com/wanteddev/wanted-sans/02c9b822349c188ada95f9e2d90c2ed18f853235/"
                   "packages/wanted-sans/fonts/otf/WantedSans-{w}.otf",
                   {"": "Regular", "b": "Bold", "xb": "ExtraBold"}),
    "SpoqaHanSansNeo": ("https://raw.githubusercontent.com/spoqa/spoqa-han-sans/6473330babd9f8e486114f1d9a7e7166e2028c51/"
                        "Original/SpoqaHanSansNeo/SpoqaHanSansNeo-{w}.otf",
                        {"": "Regular", "b": "Bold", "xb": "Bold"}),
}
TRACKING = {"xb": -0.02}  # em 단위 자간
_FONTS = {}
_GLYPHS = {}  # 현재 SVG 한 장에서 쓴 글리프: id -> path d


def _font(weight):
    fam = FONT_FAMILY
    key = (fam, weight)
    if key in _FONTS:
        return _FONTS[key]
    _FONTS[key] = None
    try:
        import uharfbuzz as hb
        from fontTools.ttLib import TTFont
    except ImportError:
        return None
    url = FAMILIES[fam][0]
    path = FONT_DIR / f"{fam}-{weight}.otf"
    if not path.exists():
        try:
            import urllib.request
            FONT_DIR.mkdir(parents=True, exist_ok=True)
            urllib.request.urlretrieve(url.format(w=weight), path)
        except Exception as e:  # 오프라인이면 시스템 글꼴로 대체
            print(f"[warn] {fam}-{weight} 다운로드 실패, 시스템 글꼴 사용: {e}")
            return None
    data = path.read_bytes()
    tt = TTFont(path)
    _FONTS[key] = dict(hb=hb.Font(hb.Face(data)), gs=tt.getGlyphSet(), order=tt.getGlyphOrder(),
                       upem=tt["head"].unitsPerEm)
    return _FONTS[key]


def _shape(s, f, track_units):
    import uharfbuzz as hb
    buf = hb.Buffer()
    buf.add_str(s)
    buf.guess_segment_properties()
    hb.shape(f["hb"], buf, {"kern": True, "liga": True})
    out, pen_x = [], 0
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        out.append((info.codepoint, pen_x + pos.x_offset, pos.y_offset))
        pen_x += pos.x_advance + track_units
    return out, pen_x - track_units


def _glyph_id(weight, gid, f):
    key = f"g{weight[0]}{weight[-1]}{gid}"
    if key not in _GLYPHS:
        from fontTools.pens.svgPathPen import SVGPathPen
        from fontTools.pens.transformPen import TransformPen
        pen = SVGPathPen(f["gs"], ntos=lambda v: ("%.0f" % v))
        f["gs"][f["order"][gid]].draw(TransformPen(pen, (1, 0, 0, -1, 0, 0)))
        _GLYPHS[key] = pen.getCommands()
    return key


def glyph_defs():
    """svg()가 호출: 이번 SVG에서 쓴 글리프 정의를 꺼내고 초기화."""
    if not _GLYPHS:
        return ""
    d = "".join(f'<path id="{k}" d="{v}"/>' for k, v in _GLYPHS.items() if v)
    _GLYPHS.clear()
    return f"<defs>{d}</defs>\n"


def text(x, y, s, size, fill, anchor="start", cls="", extra=""):
    weight = FAMILIES[FONT_FAMILY][1].get(cls, "Regular")
    f = _font(weight)
    if f is None:
        c = f' class="{cls}"' if cls else ""
        return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" '
                f'text-anchor="{anchor}"{c}{extra}>{escape(s)}</text>')
    track = TRACKING.get(cls, 0) * f["upem"]
    glyphs, width = _shape(s, f, track)
    k = size / f["upem"]
    shift = {"start": 0, "middle": -width * k / 2, "end": -width * k}[anchor]
    uses = "".join(f'<use href="#{_glyph_id(weight, gid, f)}" x="{gx:.0f}"'
                   + (f' y="{-gy:.0f}"' if gy else "") + "/>"
                   for gid, gx, gy in glyphs if _GLYPHS.get(_glyph_id(weight, gid, f)))
    return (f'<g fill="{fill}"{extra}><g transform="translate({x + shift:.2f} {y}) scale({k:.5f})">'
            f'{uses}</g></g>')


def est(s, size):
    """글자 폭(px). 선택한 글꼴 Bold 기준 실측, 글꼴이 없으면 근사값."""
    f = _font("Bold")
    if f is not None:
        return _shape(s, f, 0)[1] * size / f["upem"]
    w = 0
    for ch in s:
        if "\uac00" <= ch <= "\ud7a3":
            w += 0.95
        elif ch == " ":
            w += 0.28
        elif ch in "·.,:-()#/":
            w += 0.32
        elif ch.isupper():
            w += 0.64
        else:
            w += 0.55
    return w * size


def station(x, y, t, r=12, sw=5):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{t["station"]}" stroke="{t["ring"]}" stroke-width="{sw}"/>'


def hub(x, y, t, r=26):
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{t["station"]}" stroke="{t["ring"]}" stroke-width="6"/>'
            f'<circle cx="{x}" cy="{y}" r="{r * 0.3:.1f}" fill="{t["ring"]}"/>')


def train(path_d, dur, begin, color="#FFFFFF"):
    return (f'<g class="train"><rect x="-13" y="-5" width="26" height="10" rx="5" fill="{color}" opacity="0.95">'
            f'</rect><animateMotion dur="{dur}s" begin="{begin}s" repeatCount="indefinite" rotate="auto" '
            f'path="{path_d}"/></g>')


def hero_vehicle(accent, bus=False):
    """축소된 프로필에서도 창문과 차체가 구분되는 차량."""
    cars = [(-32, 64)] if bus else [(-46, 29), (-15, 29), (16, 29)]
    body = []
    for x, w in cars:
        body.append(f'<rect x="{x}" y="-12" width="{w}" height="24" rx="5" '
                    f'fill="#FFFFFF" stroke="{accent}" stroke-width="1.5"/>')
        body.append(f'<rect x="{x + 3}" y="6" width="{w - 6}" height="2" rx="1" fill="{accent}"/>')
        for wx in range(x + 4, x + w - 6, 8):
            body.append(f'<rect x="{wx}" y="-7" width="6" height="7" rx="1" fill="#1E2733"/>')
    if bus:
        for x in (-22, 22):
            body.append(f'<circle cx="{x}" cy="12" r="3" fill="#1E2733"/>')
    return "".join(body)


def hero_train(path_d, dur, begin, accent, parked, bus=False):
    """이동 차량과 모션 줄이기용 정차 차량을 각각 그린다."""
    vehicle = hero_vehicle(accent, bus)
    x, y, angle = parked
    return (f'<g class="train">{vehicle}'
            f'<animateMotion dur="{dur}s" begin="{begin}s" repeatCount="indefinite" rotate="{0 if bus else "auto"}" '
            f'path="{path_d}"/>'
            f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.05;0.95;1" '
            f'dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/></g>'
            f'<g class="train-parked" transform="translate({x} {y}) rotate({angle})">{vehicle}</g>')


def flow_background(width, height, theme):
    """두 주기 길이의 곡선을 이동해 반복 경계가 이어지는 배경을 만든다."""
    layers = [(354, 36, GREEN, 0.13, 18, False),
              (371, 36, BLUE, 0.22, 24, True),
              (391, 24, PINK, 0.09, 30, False)]
    moving, still = [], []
    for y, amplitude, color, opacity, duration, reverse in layers:
        d = f"M 0 {y}"
        for start in (0, width):
            d += (f" C {start + width / 6:.2f} {y - amplitude}"
                  f" {start + width / 3:.2f} {y - amplitude} {start + width / 2:.2f} {y}"
                  f" C {start + 2 * width / 3:.2f} {y + amplitude}"
                  f" {start + 5 * width / 6:.2f} {y + amplitude} {start + width} {y}")
        d += f" L {2 * width} {height + 30} L 0 {height + 30} Z"
        opacity *= 0.75 if theme == "light" else 1
        shape = f'<path d="{d}" fill="{color}" opacity="{opacity:.3f}"/>'
        values = f"{-width} 0;0 0" if reverse else f"0 0;{-width} 0"
        moving.append(f'<g>{shape}<animateTransform attributeName="transform" type="translate" '
                      f'values="{values}" dur="{duration}s" repeatCount="indefinite"/></g>')
        still.append(shape)
    return (f'<g class="flow">{"".join(moving)}</g>'
            f'<g class="flow-still">{"".join(still)}</g>')


# ---------------------------------------------------------------- hero
def hero(t, name):
    W, H = 1280, 400
    b = [flow_background(W, H, name)]
    # 오른쪽 노선 모티프 (조직 아바타와 같은 구도)
    b.append(f'''<defs>
  <linearGradient id="fade" x1="0" x2="1" y1="0" y2="0">
    <stop offset="0.6" stop-color="#fff" stop-opacity="0"/>
    <stop offset="0.74" stop-color="#fff" stop-opacity="1"/>
  </linearGradient>
  <mask id="m"><rect width="{W}" height="{H}" fill="url(#fade)"/></mask>
</defs>''')
    green = "M 700 196 H 1300"
    blue = "M 700 316 H 1300"
    pink = "M 1192 -20 V 84 L 1080 196 L 976 300 V 420"
    b.append(f'<g mask="url(#m)" fill="none" stroke-linecap="butt" stroke-linejoin="round">'
             f'<path d="{green}" stroke="{GREEN}" stroke-width="34"/>'
             f'<path d="{blue}" stroke="{BLUE}" stroke-width="34"/>'
             f'<path d="{pink}" stroke="{PINK}" stroke-width="34"/></g>')
    b.append(hero_train("M 900 196 H 1340", 8, -1, GREEN, (1160, 196, 0)))
    b.append(hero_train("M 1340 316 H 900", 10, -4, BLUE, (1130, 316, 0), bus=True))
    b.append(hero_train("M 1192 -50 V 84 L 1080 196 L 976 300 V 450", 11, -3, PINK,
                        (1162, 114, 135)))
    b.append(station(976, 316, t, r=15, sw=6))
    b.append(station(1232, 196, t, r=15, sw=6))
    b.append(station(1232, 316, t, r=15, sw=6))
    b.append(hub(1080, 196, t, r=30))
    b.append(text(1108, 248, "잠실종합운동장", 17, PINK, cls="b"))

    # 왼쪽 글
    x = 72
    b.append(f'<rect x="{x}" y="84" width="6" height="22" rx="3" fill="{PINK}"/>')
    b.append(text(x + 18, 101, "관제탑5팀", 18, t["muted"], cls="b"))
    b.append(text(x - 3, 170, "Transit Control Tower", 56, t["ink"], cls="xb"))
    b.append(text(x, 220, "교통 데이터로 도시의 흐름을 읽고, 운영 판단을 돕습니다.", 22, t["ink"]))
    b.append(text(x, 252, "잠실종합운동장 권역의 버스·지하철·행사·기상 데이터를 연결합니다.", 16, t["muted"]))

    chips = [(GREEN, "관측", "실시간 승하차 범위"), (PINK, "예측", "현재·60분·120분 혼잡 위험"),
             (BLUE, "근거", "운영 매뉴얼·대응 사례")]
    cx, cy = x, 316
    for color, k, v in chips:
        b.append(f'<circle cx="{cx + 7}" cy="{cy - 5}" r="7" fill="{color}"/>')
        b.append(text(cx + 22, cy, k, 15, t["ink"], cls="b"))
        kw = est(k, 15)
        b.append(text(cx + 30 + kw, cy, v, 14, t["muted"]))
        cx += 30 + kw + est(v, 14) + 24
    motion_style = """
    .train-parked, .flow-still { display: none; }
    """
    return svg(W, H, t, "\n".join(b), "Transit Control Tower — 관제탑5팀", motion_style, radius=28)


# ---------------------------------------------------------------- route map
def route(t, name):
    W, H = 1280, 600
    GY, PY, BY = 160, 310, 460
    HX = 1150  # 대시보드
    b = []
    b.append(text(48, 52, "시스템 노선도", 18, t["ink"], cls="b"))
    b.append(text(W - 48, 52, "최종 MVP 설계·시연 기준 흐름", 14, t["muted"], anchor="end"))

    gpath = f"M 152 {GY} H 1000 L {HX} {PY}"
    ppath = f"M 152 {PY} H {HX}"
    bpath = f"M 152 {BY} H 1000 L {HX} {PY}"
    for d, c in [(gpath, GREEN), (bpath, BLUE), (ppath, PINK)]:
        b.append(f'<path d="{d}" fill="none" stroke="{c}" stroke-width="16" stroke-linejoin="round"/>')

    # 노선 이름표
    for y, c, label in [(GY, GREEN, "실시간 관측"), (PY, PINK, "혼잡 예측"), (BY, BLUE, "근거 검색")]:
        b.append(f'<rect x="32" y="{y - 19}" width="128" height="38" rx="19" fill="{c}"/>')
        b.append(text(96, y + 6, label, 16, "#FFFFFF", anchor="middle", cls="b"))

    b.append(train(gpath, 12, 0))
    b.append(train(ppath, 10, -4))
    b.append(train(bpath, 13, -7))

    def label(x, y, name, sub, above):
        if above:
            return text(x, y - 46, name, 17, t["ink"], "middle", "b") + text(x, y - 26, sub, 13, t["muted"], "middle")
        return text(x, y + 44, name, 17, t["ink"], "middle", "b") + text(x, y + 64, sub, 13, t["muted"], "middle")

    # 환승 통로: SA ↔ Inference, PostgreSQL ↔ Azure ML
    for x, note in [(700, "예측 입력"), (920, "결과 저장")]:
        b.append(f'<rect x="{x - 17}" y="{GY - 17}" width="34" height="{PY - GY + 34}" rx="17" '
                 f'fill="{t["station"]}" stroke="{t["ring"]}" stroke-width="5"/>')
        b.append(text(x + 30, (GY + PY) // 2 + 5, note, 13, t["muted"]))

    for x, n, s in [(230, "도시데이터", "OA-21285"), (385, "Azure Functions", "5분 수집"),
                    (540, "Event Hubs", "스트림 수신"), (700, "Stream Analytics", "관측 집계"),
                    (920, "PostgreSQL", "관측·예측 저장")]:
        if x not in (700, 920):
            b.append(station(x, GY, t))
        b.append(label(x, GY, n, s, True))
    for x, n, s in [(385, "날씨·행사·공휴일", "영향 요인"), (700, "Inference Function", "추론 실행"),
                    (920, "Azure ML", "혼잡 점수 산출")]:
        if x not in (700, 920):
            b.append(station(x, PY, t))
        b.append(label(x, PY, n, s, False))
    for x, n, s in [(385, "운영 매뉴얼·사례", "공식 문서"), (700, "Azure AI Search", "문서 검색"),
                    (920, "RAG API", "근거 제시")]:
        b.append(station(x, BY, t))
        b.append(label(x, BY, n, s, False))

    b.append(hub(HX, PY, t, r=28))
    b.append(text(HX + 44, PY - 4, "대시보드", 18, t["ink"], cls="b"))
    b.append(text(HX + 44, PY + 16, "Next.js", 13, t["muted"]))

    b.append(f'<rect x="48" y="{H - 52}" width="14" height="26" rx="7" fill="{t["station"]}" '
             f'stroke="{t["ring"]}" stroke-width="3"/>')
    b.append(text(74, H - 33, "환승 통로: 한 흐름의 데이터가 다른 흐름으로 넘어가는 지점", 13, t["muted"]))
    b.append(text(W - 48, H - 33, "행사·공휴일 기준 데이터는 실시간 승하차 스트림과 구분해 관리합니다.",
                  13, t["muted"], anchor="end"))
    return svg(W, H, t, "\n".join(b),
               "시스템 노선도: 실시간 관측, 혼잡 예측, 근거 검색 세 흐름이 운영 웹 대시보드로 모입니다.")


# ---------------------------------------------------------------- roadmap
# state: done(구현) / now(진행 중) / next(예정) — 상태가 바뀌면 여기만 고치고 다시 실행
ROADMAP = [
    ("MVP 기준 수립", "서비스·데이터·모델 기준", "done"),
    ("수집·전처리", "PR #7", "done"),
    ("ML 재구성", "PR #2 · 오프라인 검증", "done"),
    ("추론 파이프라인", "PR #1 · PostgreSQL", "done"),
    ("운영 웹 대시보드", "Next.js · TypeScript", "now"),
    ("통합 검증", "클라우드 종단 간 연동", "next"),
]
ROADMAP_AS_OF = "2026년 10월 기준"


def roadmap(t, name):
    W, H = 1280, 300
    Y = 150
    xs = [130 + i * 204 for i in range(len(ROADMAP))]
    b = [text(48, 48, "개발 운행 현황", 18, t["ink"], cls="b"),
         text(W - 48, 48, ROADMAP_AS_OF, 14, t["muted"], anchor="end")]
    now_i = next((i for i, r in enumerate(ROADMAP) if r[2] == "now"), None)
    last_done = max([i for i, r in enumerate(ROADMAP) if r[2] == "done"], default=0)
    solid_end = xs[now_i] if now_i is not None else xs[last_done]
    b.append(f'<path d="M 70 {Y} H {solid_end}" stroke="{GREEN}" stroke-width="14"/>')
    b.append(f'<path d="M {solid_end} {Y} H {W - 70}" stroke="{t["faint"]}" stroke-width="14" '
             f'stroke-dasharray="18 12"/>')
    if now_i is not None:
        b.append(train(f"M 70 {Y} H {solid_end}", 6, 0))
    for i, (x, (n, s, st)) in enumerate(zip(xs, ROADMAP)):
        if st == "now":
            b.append(f'<rect x="{x - 10}" y="{Y - 62}" width="20" height="96" rx="10" fill="{PINK}"/>')
            b.append(hub(x, Y, t, r=24))
            b.append(text(x, Y - 76, "지금 여기", 15, PINK, "middle", "b"))
        elif st == "done":
            b.append(station(x, Y, t, r=13))
        else:
            b.append(f'<circle cx="{x}" cy="{Y}" r="13" fill="{t["bg"]}" stroke="{t["muted"]}" '
                     f'stroke-width="4" stroke-dasharray="5 4"/>')
        ink = t["ink"] if st != "next" else t["muted"]
        b.append(text(x, Y + 62, n, 17, ink, "middle", "b"))
        b.append(text(x, Y + 84, s, 13, t["muted"], "middle"))
        b.append(text(x, Y - 34 if st != "now" else Y - 98, f"{i + 1:02d}", 13, t["muted"], "middle", "b")
                 if st != "now" else "")
    lx = 48
    for kind, lab in [("done", "구현"), ("now", "진행 중"), ("next", "예정")]:
        if kind == "done":
            b.append(station(lx + 8, H - 34, t, r=7, sw=3))
        elif kind == "now":
            b.append(f'<circle cx="{lx + 8}" cy="{H - 34}" r="8" fill="{PINK}"/>')
        else:
            b.append(f'<circle cx="{lx + 8}" cy="{H - 34}" r="7" fill="none" stroke="{t["muted"]}" '
                     f'stroke-width="2.5" stroke-dasharray="3 3"/>')
        b.append(text(lx + 24, H - 29, lab, 13, t["muted"]))
        lx += 24 + est(lab, 13) + 28
    return svg(W, H, t, "\n".join(b), "개발 운행 현황: " + ", ".join(f"{n}({s})" for n, s, _ in ROADMAP))


# ---------------------------------------------------------------- stack
STACK = [
    (GREEN, "데이터 흐름", [("Azure Functions", "수집 실행"), ("Azure Event Hubs", "스트림 수신"),
                          ("Azure Stream Analytics", "5분 관측 집계"), ("PostgreSQL", "관측·예측 저장")]),
    (PINK, "예측 모델", [("Python", "수집·전처리·학습"), ("Azure Machine Learning", "모델 추론"),
                       ("SQL", "스키마·질의")]),
    (BLUE, "근거·운영 웹", [("Azure AI Search", "운영 문서 검색"), ("Next.js", "운영 웹 서비스"),
                         ("TypeScript", "대시보드 개발")]),
]


def stack(t, name):
    W, H = 1280, 384
    b = [text(48, 48, "기술 스택", 18, t["ink"], cls="b"),
         text(W - 48, 48, "노선별로 맡은 역할", 14, t["muted"], anchor="end")]
    for ci, (color, title, items) in enumerate(STACK):
        x = 72 + ci * 408
        b.append(f'<rect x="{x - 24}" y="76" width="{est(title, 16) + 40}" height="34" rx="17" fill="{color}"/>')
        b.append(text(x - 4, 99, title, 16, "#FFFFFF", cls="b"))
        y0, step = 150, 60
        y1 = y0 + step * (len(items) - 1)
        b.append(f'<path d="M {x} 110 V {y1}" stroke="{color}" stroke-width="12" stroke-linecap="round"/>')
        for i, (n, s) in enumerate(items):
            y = y0 + i * step
            b.append(station(x, y, t, r=10, sw=4))
            b.append(text(x + 28, y + 5, n, 17, t["ink"], cls="b"))
            b.append(text(x + 28, y + 25, s, 13, t["muted"]))
    return svg(W, H, t, "\n".join(b), "기술 스택: " + "; ".join(
        f"{title} — " + ", ".join(n for n, _ in items) for _, title, items in STACK))


# ---------------------------------------------------------------- footer
def footer(t, name):
    W, H = 1280, 150
    cy = 75
    TX = 470
    b = []
    for c, y0 in [(GREEN, cy - 36), (PINK, cy), (BLUE, cy + 36)]:
        if y0 == cy:
            d = f"M 0 {cy} H {TX}"
        else:
            d = f"M 0 {y0} H {TX - 110} L {TX - 110 + abs(y0 - cy)} {cy} H {TX}"
        b.append(f'<path d="{d}" fill="none" stroke="{c}" stroke-width="10" stroke-linejoin="round"/>')
    b.append(hub(TX, cy, t, r=24))
    b.append(text(TX + 50, cy - 6, "검증 가능한 데이터와 예측으로,", 21, t["ink"], cls="b"))
    b.append(text(TX + 50, cy + 24, "사람 중심의 교통 운영을 지원합니다.", 21, t["ink"], cls="b"))
    return svg(W, H, t, "\n".join(b), "검증 가능한 데이터와 예측으로, 사람 중심의 교통 운영을 지원합니다.")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for fn, f in [("hero", hero), ("route-map", route), ("roadmap", roadmap), ("stack", stack),
                  ("footer", footer)]:
        for name, t in THEMES.items():
            (OUT / f"{fn}-{name}.svg").write_text(f(t, name), encoding="utf-8")
            print("wrote", OUT / f"{fn}-{name}.svg")


if __name__ == "__main__":
    main()
