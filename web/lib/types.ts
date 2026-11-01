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
  name: string;
};
