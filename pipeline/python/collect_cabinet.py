"""대통령·국무위원 현황을 수집해 일일 스냅샷(jsonl)으로 저장한다.

1차 소스: 한국어 위키백과 「이재명 정부의 국무위원」 표(MediaWiki API, wikitext 파싱)
2차 소스: 각 기관 공식 누리집(cabinet_sites.py)에 그 이름이 실려 있는지 확인 → verified
공석은 name=NULL로 남긴다(화면에서 공석 표시). 이름이 바뀌었는데 verified가 아니면
MERGE(merge_cabinet.sql)가 며칠간 같은 값이 유지될 때까지 반영을 보류한다.

사용: python pipeline/python/collect_cabinet.py [--dry-run] [--skip-verify]
"""
import argparse
import concurrent.futures as cf
import datetime as dt
import json
import pathlib
import re
import sys
import urllib.parse
import urllib.request

from cabinet_sites import CABINET_SITES

WIKI_API = "https://ko.wikipedia.org/w/api.php"
WIKI_PAGE = "이재명 정부의 국무위원"
UA = {"User-Agent": "offofby-collector (+https://offofby.vercel.app)"}
OUT_DIR = pathlib.Path(__file__).parents[1] / "out"
MIN_ROWS = 15  # 대통령·총리 + 부처 19곳이 정상. 이보다 적으면 표 구조가 바뀐 것


def fetch_wikitext() -> str:
    query = urllib.parse.urlencode({"action": "parse", "page": WIKI_PAGE, "prop": "wikitext",
                                    "format": "json", "formatversion": 2})
    req = urllib.request.Request(f"{WIKI_API}?{query}", headers=UA)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)["parse"]["wikitext"]


def strip_links(text: str) -> str:
    # [[문서|표시]] → 표시, [[문서]] → 문서, '''강조''' 제거
    text = re.sub(r"\[\[(?:[^|\]]*\|)?([^\]]+)\]\]", r"\1", text)
    return text.replace("'''", "").strip()


def parse_period(text: str) -> str | None:
    m = re.search(r"(\d{4})년\s*(\d{1,2})월\s*(\d{1,2})일", text)
    return f"{m[1]}-{int(m[2]):02d}-{int(m[3]):02d}" if m else None


def parse_table(wikitext: str) -> list[dict]:
    start = wikitext.find('{| class="wikitable')
    end = wikitext.find("\n|}", start)
    if start < 0 or end < 0:
        raise RuntimeError("위키 문서에서 국무위원 표를 찾지 못했습니다.")
    rows = []
    for block in wikitext[start:end].split("|-")[1:]:
        lines = [l.strip() for l in block.strip().split("\n") if l.strip()]
        head = next((l for l in lines if l.startswith("!")), None)
        cells = [l[1:].strip() for l in lines if l.startswith("|")]
        if not head or not cells:
            continue
        position = re.sub(r"\s*\((의장|부의장)\)\s*", "", strip_links(head[1:]))
        name = strip_links(cells[0])
        name = None if name in ("", "공석") else name  # 공석은 NULL
        period = cells[2] if len(cells) > 2 else ""
        rows.append({"position": position, "rank_order": len(rows) + 1, "name": name,
                     "start_date": parse_period(period)})
    return rows


def page_mentions(url: str, name: str) -> bool:
    try:
        req = urllib.request.Request(url, headers={**UA, "User-Agent": "Mozilla/5.0 " + UA["User-Agent"]})
        with urllib.request.urlopen(req, timeout=20) as resp:
            return name in resp.read().decode("utf-8", "ignore")
    except Exception as e:  # noqa: BLE001 - 누리집 장애는 '미확인'일 뿐 수집 실패가 아니다
        print(f"  확인 실패 {url}: {type(e).__name__}", file=sys.stderr)
        return False


def verify(row: dict) -> dict:
    sites = next((urls for org, urls in CABINET_SITES.items() if org in row["position"]), [])
    hit = None
    if row["name"]:
        hit = next((u for u in sites if page_mentions(u, row["name"])), None)
    return {**row, "verified": hit is not None,
            "source_urls": [f"https://ko.wikipedia.org/wiki/{urllib.parse.quote(WIKI_PAGE)}"] + ([hit] if hit else [])}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="저장하지 않고 표만 출력")
    parser.add_argument("--skip-verify", action="store_true", help="누리집 교차검증 생략(전부 미확인)")
    args = parser.parse_args()

    rows = parse_table(fetch_wikitext())
    if len(rows) < MIN_ROWS:
        sys.exit(f"표에서 {len(rows)}행만 읽혀 중단합니다(기대 {MIN_ROWS}+). 표 구조 변경 여부 확인 필요")

    if args.skip_verify:
        rows = [verify_skip(r) for r in rows]
    else:
        with cf.ThreadPoolExecutor(8) as ex:
            rows = list(ex.map(verify, rows))

    snapshot_date = dt.datetime.now(dt.timezone(dt.timedelta(hours=9))).date().isoformat()
    n_ok = sum(r["verified"] for r in rows)
    print(f"{snapshot_date}: 국무위원 {len(rows)}명 (누리집 확인 {n_ok}, 공석 {sum(r['name'] is None for r in rows)})")
    for r in rows:
        print(f"  {'✓' if r['verified'] else '·'} {r['rank_order']:2d} {r['position']}: {r['name'] or '(공석)'}")

    if args.dry_run:
        return
    OUT_DIR.mkdir(exist_ok=True)
    out = OUT_DIR / f"cabinet_{snapshot_date.replace('-', '')}.jsonl"
    with out.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps({**r, "snapshot_date": snapshot_date}, ensure_ascii=False) + "\n")
    print(f"저장: {out}")


def verify_skip(row: dict) -> dict:
    return {**row, "verified": False,
            "source_urls": [f"https://ko.wikipedia.org/wiki/{urllib.parse.quote(WIKI_PAGE)}"]}


if __name__ == "__main__":
    main()
