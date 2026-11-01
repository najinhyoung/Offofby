@echo off
REM Actions 쓰기용 서비스계정에 BigQuery 권한 부여 (1회)
call gcloud.cmd projects add-iam-policy-binding offofby --member=serviceAccount:offofby-writer@offofby.iam.gserviceaccount.com --role=roles/bigquery.dataEditor --condition=None --format=none
call gcloud.cmd projects add-iam-policy-binding offofby --member=serviceAccount:offofby-writer@offofby.iam.gserviceaccount.com --role=roles/bigquery.jobUser --condition=None --format=none
echo.
echo 완료. 부여된 역할:
call gcloud.cmd projects get-iam-policy offofby --flatten=bindings[].members --filter=bindings.members:offofby-writer --format=value(bindings.role)
