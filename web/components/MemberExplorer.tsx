"use client";

import Link from "next/link";
import { useMemo, useState } from "react";
import type { Member } from "@/lib/types";
import { regionOf } from "@/lib/region";
import { GradeBadge } from "./GradeBadge";

const ALL = "전체";

export function MemberExplorer({ members }: { members: Member[] }) {
  const [q, setQ] = useState("");
  const [region, setRegion] = useState(ALL);
  const [party, setParty] = useState(ALL);
  const [type, setType] = useState("지역구");

  // 시도는 가나다순, 비례대표는 맨 뒤
  const regions = useMemo(() => {
    const set = new Set(members.map((m) => regionOf(m.district)));
    const sorted = [...set].filter((r) => r !== "비례대표").sort((a, b) => a.localeCompare(b, "ko"));
    return [ALL, ...sorted, ...(set.has("비례대표") ? ["비례대표"] : [])];
  }, [members]);
  const parties = useMemo(
    () => [ALL, ...[...new Set(members.map((m) => m.party))].sort((a, b) => a.localeCompare(b, "ko"))],
    [members],
  );

  const filtered = members.filter(
    (m) =>
      (type === ALL || m.election_type === type) &&
      (region === ALL || regionOf(m.district) === region) &&
      (party === ALL || m.party === party) &&
      (!q || m.name.includes(q) || m.district.includes(q)),
  );

  const select = "rounded border border-line bg-background px-2 py-2 text-sm";

  return (
    <section aria-labelledby="members-heading">
      <h2 id="members-heading" className="mb-3 text-xl font-bold">
        국회의원
      </h2>
      <div className="mb-4 grid grid-cols-2 gap-2 sm:grid-cols-4">
        <input
          type="search"
          placeholder="이름·지역구 검색"
          aria-label="이름 또는 지역구 검색"
          value={q}
          onChange={(e) => setQ(e.target.value.trim())}
          className={`${select} col-span-2 sm:col-span-1`}
        />
        <select aria-label="선출 구분" value={type} onChange={(e) => setType(e.target.value)} className={select}>
          {[ALL, "지역구", "비례대표"].map((v) => (
            <option key={v}>{v}</option>
          ))}
        </select>
        <select aria-label="시도" value={region} onChange={(e) => setRegion(e.target.value)} className={select}>
          {regions.map((v) => (
            <option key={v}>{v}</option>
          ))}
        </select>
        <select aria-label="정당" value={party} onChange={(e) => setParty(e.target.value)} className={select}>
          {parties.map((v) => (
            <option key={v}>{v}</option>
          ))}
        </select>
      </div>
      <p className="mb-2 text-sm text-muted" aria-live="polite">
        {filtered.length}명
      </p>
      <ul className="divide-y divide-line rounded border border-line">
        {filtered.map((m) => (
          <li key={m.member_code}>
            <Link
              href={`/members/${m.member_code}`}
              className="flex items-center justify-between gap-3 px-3 py-3 hover:bg-card"
            >
              <span className="min-w-0">
                <span className="font-medium">{m.name}</span>
                <span className="ml-2 text-sm text-muted">{m.party}</span>
                <span className="block truncate text-sm text-muted">{m.district}</span>
              </span>
              <GradeBadge />
            </Link>
          </li>
        ))}
        {filtered.length === 0 && <li className="px-3 py-6 text-center text-sm text-muted">결과가 없습니다.</li>}
      </ul>
    </section>
  );
}
