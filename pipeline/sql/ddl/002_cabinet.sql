-- 대통령·국무위원 스테이징 + cabinet 컬럼 추가 + 현재 뷰 갱신
-- 실행: python pipeline/python/apply_sql.py pipeline/sql/ddl/002_cabinet.sql --approve  (사용자 승인 필요)

-- 스테이징은 덮어쓰지 않고 날짜별로 쌓는다(append). MERGE가 "며칠 연속 같은 이름"을 판단하는 데 쓴다
CREATE TABLE IF NOT EXISTS `${project}.${dataset}.stg_cabinet` (
  position       STRING NOT NULL,   -- 위키 표의 직위명 그대로 (예: 경제부총리 겸 재정경제부 장관)
  rank_order     INT64,             -- 표 순서 = 정부조직법 순서
  name           STRING,            -- 공석이면 NULL
  start_date     DATE,              -- 취임일(표의 기간 시작). 유임 등은 NULL
  verified       BOOL,              -- 기관 누리집에서 이름 확인 여부
  source_urls    ARRAY<STRING>,
  snapshot_date  DATE NOT NULL
)
PARTITION BY snapshot_date;

ALTER TABLE `${project}.${dataset}.cabinet`
  ADD COLUMN IF NOT EXISTS start_date DATE,
  ADD COLUMN IF NOT EXISTS verified BOOL;

-- 공석을 NULL로 저장하기 위해 NOT NULL 해제
ALTER TABLE `${project}.${dataset}.cabinet`
  ALTER COLUMN name DROP NOT NULL;

CREATE OR REPLACE VIEW `${project}.${dataset}.v_current_cabinet` AS
SELECT position, rank_order, name, start_date, verified, valid_from
FROM `${project}.${dataset}.cabinet`
WHERE is_current;
