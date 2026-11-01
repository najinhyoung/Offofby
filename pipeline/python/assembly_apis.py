"""열린국회정보 OpenAPI 엔드포인트 모음. ASSEMBLY_API_KEY 하나로 모두 호출한다.

현재는 인적사항만 수집하고, 나머지는 2단계 이후 필요 시 사용.
"""
ASSEMBLY_APIS = {
    # 국회의원 인적사항 (1단계에서 사용 중)
    "members": "https://open.assembly.go.kr/portal/openapi/nwvrqwxyaytdsfvhu",
    # 국회의원 발의법률안
    "bills": "https://open.assembly.go.kr/portal/openapi/nzmimeepazxkubdpn",
    # 국회의원 상임위활동
    "committee_activity": "https://open.assembly.go.kr/portal/openapi/nuvypcdgahexhvrjt",
    # 국회의원 정책자료실
    "policy_materials": "https://open.assembly.go.kr/portal/openapi/npggiwnfaihlruyso",
}
