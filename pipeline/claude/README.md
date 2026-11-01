# pipeline/claude — Claude API를 호출하는 운영 스크립트

LLM(Claude API)으로 처리하는 단계만 여기에 둔다. 일반 Python 처리(수집·적재·스코어링)는 `pipeline/python/`.

예정:
- `sentiment.py` — 뉴스 기사×인물 긍부정 평가 배치 (2단계)

규칙: Message Batches API + 프롬프트 캐싱 사용, 일일 호출 상한(`SENTIMENT_DAILY_LIMIT`) 준수.
