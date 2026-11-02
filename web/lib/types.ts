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

export type President = {
  name: string | null; // 공석(권한대행 체제 등)이면 null
  start_date: string | null; // 취임일 YYYY-MM-DD
  verified: boolean; // 대통령실 누리집에서 이름 확인됨
};
