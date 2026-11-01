"""열린국회정보 OpenAPI에서 현직 국회의원 인적사항을 받아 일일 스냅샷(jsonl)으로 저장한다.

사용: python pipeline/collect_assembly.py [--dry-run]
환경변수: ASSEMBLY_API_KEY
"""
import argparse
import datetime as dt
import json
import os
import pathlib
import sys
import urllib.parse
import urllib.request

ENDPOINT = "https://open.assembly.go.kr/portal/openapi/nwvrqwxyaytdsfvhu"  # 국회의원 인적사항
PAGE_SIZE = 100
OUT_DIR = pathlib.Path(__file__).parent / "out"

FIELDS = {
    "MONA_CD": "member_code",
    "HG_NM": "name",
    "HJ_NM": "name_hanja",
    "POLY_NM": "party",
    "ORIG_NM": "district",
    "ELECT_GBN_NM": "election_type",  # 지역구 / 비례대표
    "REELE_GBN_NM": "reelection",
    "UNITS": "units",
    "CMITS": "committees",
    "TEL_NO": "tel",
    "E_MAIL": "email",
    "HOMEPAGE": "homepage",
}


def fetch_page(key: str, page: int) -> list[dict]:
    query = urllib.parse.urlencode({"KEY": key, "Type": "json", "pIndex": page, "pSize": PAGE_SIZE})
    with urllib.request.urlopen(f"{ENDPOINT}?{query}", timeout=30) as resp:
        body = json.load(resp)
    if "nwvrqwxyaytdsfvhu" not in body:
        # 데이터 끝이면 INFO-200, 그 외는 오류
        result = body.get("RESULT", {})
        if result.get("CODE") == "INFO-200":
            return []
        raise RuntimeError(f"API 오류: {result}")
    return body["nwvrqwxyaytdsfvhu"][1]["row"]


def collect(key: str) -> list[dict]:
    rows, page = [], 1
    while True:
        batch = fetch_page(key, page)
        rows.extend({dst: r.get(src) for src, dst in FIELDS.items()} for r in batch)
        if len(batch) < PAGE_SIZE:
            return rows
        page += 1


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="저장하지 않고 요약만 출력")
    args = parser.parse_args()

    key = os.environ.get("ASSEMBLY_API_KEY")
    if not key:
        sys.exit("ASSEMBLY_API_KEY 환경변수가 필요합니다.")

    rows = collect(key)
    snapshot_date = dt.date.today().isoformat()
    district = sum(1 for r in rows if r["election_type"] == "지역구")
    print(f"{snapshot_date}: 의원 {len(rows)}명 (지역구 {district}, 비례 {len(rows) - district})")

    if args.dry_run:
        return
    OUT_DIR.mkdir(exist_ok=True)
    out = OUT_DIR / f"assembly_{snapshot_date.replace('-', '')}.jsonl"
    with out.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps({**r, "snapshot_date": snapshot_date}, ensure_ascii=False) + "\n")
    print(f"저장: {out}")


if __name__ == "__main__":
    main()
