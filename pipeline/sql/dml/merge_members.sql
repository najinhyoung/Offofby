-- stg_assembly(오늘 스냅샷) → members(SCD2)
-- 1) 바뀌었거나 사라진 현재 행을 닫는다  2) 새로 생겼거나 바뀐 행을 연다
-- 실행: python pipeline/apply_sql.py pipeline/sql/dml/merge_members.sql --approve  (사용자 승인 필요)

DECLARE snap DATE DEFAULT (SELECT MAX(snapshot_date) FROM `${project}.${dataset}.stg_assembly`);

-- 스냅샷이 비정상적으로 작으면(API 장애 등) 전원 퇴임 처리되지 않도록 중단
IF (SELECT COUNT(*) FROM `${project}.${dataset}.stg_assembly` WHERE snapshot_date = snap) < 250 THEN
  RAISE USING MESSAGE = 'stg_assembly 행 수가 250 미만이라 적재를 중단합니다.';
END IF;

CREATE TEMP TABLE src AS
SELECT
  * EXCEPT (snapshot_date),
  TO_HEX(MD5(TO_JSON_STRING(STRUCT(name, name_hanja, party, district, election_type,
                                   reelection, units, committees, tel, email, homepage)))) AS row_hash
FROM `${project}.${dataset}.stg_assembly`
WHERE snapshot_date = snap;

BEGIN TRANSACTION;

UPDATE `${project}.${dataset}.members` m
SET valid_to = DATE_SUB(snap, INTERVAL 1 DAY), is_current = FALSE
WHERE m.is_current
  AND NOT EXISTS (SELECT 1 FROM src s WHERE s.member_code = m.member_code AND s.row_hash = m.row_hash);

INSERT INTO `${project}.${dataset}.members`
SELECT s.*, snap AS valid_from, CAST(NULL AS DATE) AS valid_to, TRUE AS is_current
FROM src s
WHERE NOT EXISTS (
  SELECT 1 FROM `${project}.${dataset}.members` m
  WHERE m.is_current AND m.member_code = s.member_code AND m.row_hash = s.row_hash
);

COMMIT TRANSACTION;
