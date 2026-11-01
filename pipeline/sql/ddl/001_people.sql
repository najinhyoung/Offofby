-- 인물 테이블(SCD2 이력) + 일일 스테이징 + 화면용 현재 뷰
-- 실행: python pipeline/python/apply_sql.py pipeline/sql/ddl/001_people.sql --approve  (사용자 승인 필요)

CREATE SCHEMA IF NOT EXISTS `${project}.${dataset}`
OPTIONS (location = 'asia-northeast3');

-- 수집 스냅샷을 그대로 올리는 스테이징(매 실행 시 덮어씀)
CREATE TABLE IF NOT EXISTS `${project}.${dataset}.stg_assembly` (
  member_code    STRING NOT NULL,
  name           STRING,
  name_hanja     STRING,
  party          STRING,
  district       STRING,
  election_type  STRING,
  reelection     STRING,
  units          STRING,
  committees     STRING,
  tel            STRING,
  email          STRING,
  homepage       STRING,
  snapshot_date  DATE NOT NULL
);

-- 국회의원 이력(SCD2): 값이 바뀌면 이전 행을 닫고 새 행을 연다
CREATE TABLE IF NOT EXISTS `${project}.${dataset}.members` (
  member_code    STRING NOT NULL,
  name           STRING,
  name_hanja     STRING,
  party          STRING,
  district       STRING,
  election_type  STRING,
  reelection     STRING,
  units          STRING,
  committees     STRING,
  tel            STRING,
  email          STRING,
  homepage       STRING,
  row_hash       STRING NOT NULL,
  valid_from     DATE NOT NULL,
  valid_to       DATE,
  is_current     BOOL NOT NULL
)
CLUSTER BY is_current, member_code;

-- 대통령·국무위원 이력(SCD2). 두 소스 교차검증 결과만 들어옴
CREATE TABLE IF NOT EXISTS `${project}.${dataset}.cabinet` (
  position       STRING NOT NULL,  -- 예: 대통령, 기획재정부장관
  rank_order     INT64,            -- 정부조직법상 순서(화면 정렬용)
  name           STRING NOT NULL,
  source_urls    ARRAY<STRING>,
  valid_from     DATE NOT NULL,
  valid_to       DATE,
  is_current     BOOL NOT NULL
)
CLUSTER BY is_current, position;

CREATE OR REPLACE VIEW `${project}.${dataset}.v_current_members` AS
SELECT * EXCEPT (row_hash, valid_to, is_current)
FROM `${project}.${dataset}.members`
WHERE is_current;

CREATE OR REPLACE VIEW `${project}.${dataset}.v_current_cabinet` AS
SELECT position, rank_order, name, valid_from
FROM `${project}.${dataset}.cabinet`
WHERE is_current;
