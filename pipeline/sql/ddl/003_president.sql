-- 대상 범위를 선출직(대통령·국회의원)으로 한정: cabinet → president 교체
-- cabinet 22행 중 position='대통령' 1행만 president로 옮기고, cabinet·stg_cabinet·v_current_cabinet은 삭제한다.
-- 실행: python pipeline/python/apply_sql.py pipeline/sql/ddl/003_president.sql --approve  (사용자 승인 필요)

CREATE TABLE IF NOT EXISTS `${project}.${dataset}.president` (
  position       STRING NOT NULL,   -- 항상 '대통령' (장래 권한대행 등 구분 여지)
  name           STRING,            -- 공석이면 NULL
  start_date     DATE,              -- 취임일
  verified       BOOL,              -- 대통령실 누리집에서 이름 확인 여부
  source_urls    ARRAY<STRING>,
  valid_from     DATE NOT NULL,
  valid_to       DATE,
  is_current     BOOL NOT NULL
)
CLUSTER BY is_current;

INSERT INTO `${project}.${dataset}.president`
  (position, name, start_date, verified, source_urls, valid_from, valid_to, is_current)
SELECT position, name, start_date, verified, source_urls, valid_from, valid_to, is_current
FROM `${project}.${dataset}.cabinet`
WHERE position = '대통령';

CREATE TABLE IF NOT EXISTS `${project}.${dataset}.stg_president` (
  position       STRING NOT NULL,
  name           STRING,
  start_date     DATE,
  verified       BOOL,
  source_urls    ARRAY<STRING>,
  snapshot_date  DATE NOT NULL
)
PARTITION BY snapshot_date;

CREATE OR REPLACE VIEW `${project}.${dataset}.v_current_president` AS
SELECT position, name, start_date, verified, valid_from
FROM `${project}.${dataset}.president`
WHERE is_current;

DROP VIEW IF EXISTS `${project}.${dataset}.v_current_cabinet`;
DROP TABLE IF EXISTS `${project}.${dataset}.cabinet`;
DROP TABLE IF EXISTS `${project}.${dataset}.stg_cabinet`;
