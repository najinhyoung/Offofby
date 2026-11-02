-- stg_cabinet(오늘 스냅샷) → cabinet(SCD2)
-- 이름이 바뀐 직위는 (a) 기관 누리집에서 확인됐거나 (b) 최근 5일 중 3일 이상 같은 이름이 수집됐을 때만 반영한다.
-- 그 전까지는 기존 행을 유지(보류)하고, 보류 건은 report_changes.py가 Issue에 적는다.
-- 실행: python pipeline/python/apply_sql.py pipeline/sql/dml/merge_cabinet.sql --approve  (사용자 승인 필요)

DECLARE snap DATE DEFAULT (SELECT MAX(snapshot_date) FROM `${project}.${dataset}.stg_cabinet`);

IF (SELECT COUNT(*) FROM `${project}.${dataset}.stg_cabinet` WHERE snapshot_date = snap) < 15 THEN
  RAISE USING MESSAGE = 'stg_cabinet 행 수가 15 미만이라 적재를 중단합니다.';
END IF;

CREATE TEMP TABLE src AS
SELECT
  s.position, s.rank_order, s.name, s.start_date, s.verified, s.source_urls,
  (
    c.position IS NULL            -- 새 직위
    OR c.name IS NOT DISTINCT FROM s.name  -- 이름 그대로(순서·취임일만 바뀐 경우 포함). 공석(NULL)끼리도 같음
    OR s.verified                 -- 누리집 확인됨
    OR (SELECT COUNT(DISTINCT h.snapshot_date)
        FROM `${project}.${dataset}.stg_cabinet` h
        WHERE h.position = s.position AND h.name IS NOT DISTINCT FROM s.name
          AND h.snapshot_date BETWEEN DATE_SUB(snap, INTERVAL 4 DAY) AND snap) >= 3
  ) AS accepted
FROM `${project}.${dataset}.stg_cabinet` s
LEFT JOIN `${project}.${dataset}.cabinet` c
  ON c.is_current AND c.position = s.position
WHERE s.snapshot_date = snap;

BEGIN TRANSACTION;

-- 1) 닫기: 사라진 직위, 또는 수용된 변경이 있는 직위의 현재 행. 보류 중인 직위는 건드리지 않는다
UPDATE `${project}.${dataset}.cabinet` c
SET valid_to = DATE_SUB(snap, INTERVAL 1 DAY), is_current = FALSE
WHERE c.is_current
  AND NOT EXISTS (SELECT 1 FROM src s WHERE s.position = c.position AND NOT s.accepted)
  AND NOT EXISTS (
    SELECT 1 FROM src s
    WHERE s.position = c.position AND s.accepted
      AND s.name IS NOT DISTINCT FROM c.name
      AND COALESCE(s.rank_order, -1) = COALESCE(c.rank_order, -1)
      AND COALESCE(s.start_date, DATE '1900-01-01') = COALESCE(c.start_date, DATE '1900-01-01')
  );

-- 2) 열기: 수용된 행 중 현재 동일 행이 없는 것
INSERT INTO `${project}.${dataset}.cabinet`
  (position, rank_order, name, source_urls, valid_from, valid_to, is_current, start_date, verified)
SELECT s.position, s.rank_order, s.name, s.source_urls, snap, NULL, TRUE, s.start_date, s.verified
FROM src s
WHERE s.accepted
  AND NOT EXISTS (
    SELECT 1 FROM `${project}.${dataset}.cabinet` c
    WHERE c.is_current AND c.position = s.position
  );

-- 3) 누리집 확인이 나중에 된 경우 현재 행에 반영(이력을 새로 열지 않음)
UPDATE `${project}.${dataset}.cabinet` c
SET verified = TRUE, source_urls = s.source_urls
FROM src s
WHERE c.is_current AND c.position = s.position AND c.name IS NOT DISTINCT FROM s.name
  AND s.verified AND NOT COALESCE(c.verified, FALSE);

COMMIT TRANSACTION;
