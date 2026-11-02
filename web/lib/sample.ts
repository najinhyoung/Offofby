import type { CabinetPost, Member } from "./types";

// 로컬 개발용 가짜 데이터. 실존 인물·정당이 아님.
const districts = [
  "서울 종로구", "서울 강남구갑", "부산 해운대구갑", "대구 수성구을", "인천 연수구갑",
  "광주 북구갑", "대전 유성구을", "울산 남구갑", "세종특별자치시갑", "경기 수원시갑",
  "경기 성남시분당구을", "강원 춘천시철원군화천군양구군갑", "충북 청주시상당구", "충남 천안시갑",
  "전북 전주시갑", "전남 목포시", "경북 포항시북구", "경남 창원시성산구", "제주 제주시갑",
];
const parties = ["가나당", "다라당", "마바당", "무소속"];

export const sampleMembers: Member[] = Array.from({ length: 30 }, (_, i) => {
  const proportional = i >= districts.length;
  return {
    member_code: `SAMPLE${String(i + 1).padStart(3, "0")}`,
    name: `예시의원${String(i + 1).padStart(2, "0")}`,
    name_hanja: null,
    party: parties[i % parties.length],
    district: proportional ? "비례대표" : districts[i],
    election_type: proportional ? "비례대표" : "지역구",
    reelection: ["초선", "재선", "3선"][i % 3],
    units: "제22대",
    committees: ["법제사법위원회", "기획재정위원회", "교육위원회"][i % 3],
    tel: null,
    email: null,
    homepage: null,
  };
});

export const sampleCabinet: CabinetPost[] = [
  "대통령", "국무총리", "기획재정부장관", "교육부장관", "과학기술정보통신부장관", "외교부장관",
  "통일부장관", "법무부장관", "국방부장관", "행정안전부장관",
].map((position, i) => ({
  position,
  rank_order: i,
  name: i === 7 ? null : `예시인물${String(i + 1).padStart(2, "0")}`,
  start_date: i === 7 ? null : "2025-07-01",
  verified: i % 3 !== 0,
}));
