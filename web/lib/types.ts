export type Member = {
  member_code: string;
  name: string;
  name_hanja: string | null;
  party: string;
  district: string;
  election_type: string; // 지역구 | 비례대표
  reelection: string | null;
  units: string | null;
  committees: string | null;
  tel: string | null;
  email: string | null;
  homepage: string | null;
};

export type CabinetPost = {
  position: string;
  rank_order: number;
  name: string | null; // 공석이면 null
  start_date: string | null; // 취임일 YYYY-MM-DD
  verified: boolean; // 기관 누리집에서 이름 확인됨
};
