"""수집 스냅샷(jsonl)을 BigQuery 스테이징 테이블에 적재한다(기존 내용 덮어씀).

사용: python pipeline/python/load_snapshot.py <jsonl 파일> --table stg_assembly [--approve]
--approve 없이 실행하면 행 수와 대상 테이블만 보여주고 적재하지 않는다.
환경변수: GCP_PROJECT, BQ_DATASET(기본 offofby), BQ_LOCATION(기본 asia-northeast3)
"""
import argparse
import os
import pathlib
import sys

from google.cloud import bigquery


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("jsonl_file", type=pathlib.Path)
    parser.add_argument("--table", required=True, help="대상 스테이징 테이블명 (예: stg_assembly)")
    parser.add_argument("--approve", action="store_true", help="실제로 적재")
    args = parser.parse_args()

    project = os.environ.get("GCP_PROJECT")
    dataset = os.environ.get("BQ_DATASET", "offofby")
    location = os.environ.get("BQ_LOCATION", "asia-northeast3")
    if not project:
        sys.exit("GCP_PROJECT 환경변수가 필요합니다.")

    n_rows = sum(1 for line in args.jsonl_file.open(encoding="utf-8") if line.strip())
    table_id = f"{project}.{dataset}.{args.table}"
    print(f"{args.jsonl_file} ({n_rows}행) → {table_id} (WRITE_TRUNCATE)")

    if not args.approve:
        print("확인만 했습니다. 적재하려면 --approve")
        return
    client = bigquery.Client(project=project, location=location)
    config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    )
    with args.jsonl_file.open("rb") as f:
        job = client.load_table_from_file(f, table_id, job_config=config)
    job.result()
    print(f"완료: {client.get_table(table_id).num_rows}행 적재")


if __name__ == "__main__":
    main()
