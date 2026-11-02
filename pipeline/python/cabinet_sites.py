"""대통령·국무위원 교차검증용 공식 누리집 URL.

키는 위키백과 직위명에 포함되는 기관명(부분 문자열). 값은 장관 이름이 적혀 있을 법한 페이지 목록으로,
하나라도 이름을 포함하면 '확인'으로 본다. 기관 개편·사이트 개편 시 여기만 고치면 된다.
"""

CABINET_SITES: dict[str, list[str]] = {
    "대통령": ["https://www.president.go.kr", "https://www.president.go.kr/greeting"],
    "국무총리": ["https://www.opm.go.kr"],
    "재정경제부": ["https://www.mofe.go.kr"],
    "과학기술정보통신부": ["https://www.msit.go.kr", "https://www.msit.go.kr/bbs/list.do?sCode=user&mId=99&mPid=74"],
    "교육부": ["https://www.moe.go.kr", "https://www.moe.go.kr/sub/infoRenewal.do?m=060101&s=moe"],
    "외교부": ["https://www.mofa.go.kr", "https://www.mofa.go.kr/www/wpge/m_3964/contents.do"],
    "통일부": ["https://www.unikorea.go.kr", "https://www.unikorea.go.kr/web/minister/contents/introduce_minister"],
    "법무부": ["https://www.moj.go.kr", "https://www.moj.go.kr/moj/190/subview.do"],
    "국방부": ["https://www.mnd.go.kr", "https://www.mnd.go.kr/mbshome/mbs/mnd/subview.jsp?id=mnd_010300000000"],
    "행정안전부": ["https://www.mois.go.kr", "https://www.mois.go.kr/frt/sub/a07/minister/screen.do"],
    "국가보훈부": ["https://www.mpva.go.kr", "https://www.mpva.go.kr/mpva/minister/greeting.do"],
    "문화체육관광부": ["https://www.mcst.go.kr", "https://www.mcst.go.kr/kor/s_about/minister/greeting.jsp"],
    "농림축산식품부": ["https://www.mafra.go.kr", "https://www.mafra.go.kr/home/5101/subview.do"],
    "산업통상부": ["https://www.motir.go.kr", "https://www.motir.go.kr/kor/43/greeting/talk"],
    "보건복지부": ["https://www.mohw.go.kr", "https://www.mohw.go.kr/menu.es?mid=a10702010100"],
    "기후에너지환경부": ["https://www.mcee.go.kr"],
    "고용노동부": ["https://www.moel.go.kr", "https://www.moel.go.kr/info/minister/greeting.do"],
    "성평등가족부": ["https://www.mogef.go.kr"],
    "국토교통부": ["https://www.molit.go.kr", "https://www.molit.go.kr/USR/WPGE0201/m_36511/DTL.jsp"],
    "해양수산부": ["https://www.mof.go.kr", "https://www.mof.go.kr/mi/org/minister.do"],
    "중소벤처기업부": ["https://www.mss.go.kr", "https://www.mss.go.kr/site/smba/03/10306010000002019110612.jsp"],
    "기획예산처": ["https://www.mpb.go.kr"],
}
