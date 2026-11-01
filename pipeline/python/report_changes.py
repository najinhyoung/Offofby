"""오늘 MERGE로 생긴 변경(신규·변경·퇴임)을 요약해 출력한다. 변경이 없으면 아무것도 출력하지 않는다.

사용: python pipeline/python/report_changes.py [--date YYYY-MM-DD]
GitHub Actions에서 출력이 있으면 Issue를 만든다. 읽기만 하며 DB를 바꾸지 않는다.
환경변수: GCP_PROJECT, BQ_DATASET(기본 offofby), BQ_LOCATION(기본 asia-northeast3)
"""
import argparse
import datetime as dt
import os
import sys

from google.cloud import bigquery

SQL = """
WITH opened AS (
  SELECT member_code, name, party, district FROM `{t}` WHERE valid_from = @d
),
closed AS (
  SELECT member_code, name, party, district FROM `{t}` WHERE valid_to = DATE_SUB(@d, INTERVAL 1 DAY)
)
SELECT
  COALESCE(o.member_code, c.member_code) AS member_code,
  COALESCE(o.name, c.name) AS name,
  CASE WHEN c.member_code IS NULL THEN '신규'
       WHEN o.member_code IS NULL THEN '퇴임'
       ELSE '변경' END AS kind,
  c.party AS old_party, o.party AS new_party,
  c.district AS old_district, o.district AS new_district
FROM opened o FULL OUTER JOIN closed c USING (member_code)
ORDER BY kind, name
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    kst_today = dt.datetime.now(dt.timezone(dt.timedelta(hours=9))).date().isoformat()
    parser.add_argument("--date", default=kst_today)
    args = parser.parse_args()

    project = os.environ.get("GCP_PROJECT")
    dataset = os.environ.get("BQ_DATASET", "offofby")
    location = os.environ.get("BQ_LOCATION", "asia-northeast3")
    if not project:
        sys.exit("GCP_PROJECT 환경변수가 필요합니다.")

    client = bigquery.Client(project=project, location=location)
    table = f"{project}.{dataset}.members"
    # 첫 적재일(전원 신규)은 보고하지 않는다
    first = list(client.query(f"SELECT MIN(valid_from) d FROM `{table}`").result())[0].d
    if first is None or first.isoformat() == args.date:
        return

    job = client.query(
        SQL.format(t=table),
        job_config=bigquery.QueryJobConfig(
            query_parameters=[bigquery.ScalarQueryParameter("d", "DATE", args.date)]
        ),
    )
    rows = list(job.result())
    if not rows:
        return
    print(f"## {args.date} 국회의원 변경 {len(rows)}건\n")
    print("| 구분 | 이름 | 정당 | 선거구 |\n|---|---|---|---|")
    for r in rows:
        party = r.new_party if r.kind == "신규" else (r.old_party if r.kind == "퇴임" else f"{r.old_party} → {r.new_party}")
        district = r.new_district if r.kind == "신규" else (r.old_district if r.kind == "퇴임" else f"{r.old_district} → {r.new_district}")
        print(f"| {r.kind} | {r.name} | {party} | {district} |")


if __name__ == "__main__":
    main()
