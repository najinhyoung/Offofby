import { MemberExplorer } from "@/components/MemberExplorer";
import { GradeBadge } from "@/components/GradeBadge";
import { getCabinet, getMembers, usingSampleData } from "@/lib/data";

export const revalidate = 86400; // 파이프라인이 /api/revalidate로 매일 갱신, 이건 안전망

export default async function Home() {
  const [cabinet, members] = await Promise.all([getCabinet(), getMembers()]);

  return (
    <div className="space-y-10">
      {usingSampleData && (
        <p role="note" className="rounded border border-dashed border-line bg-card px-3 py-2 text-sm text-muted">
          개발용 예시 데이터입니다. 실제 인물이 아닙니다.
        </p>
      )}

      <section aria-labelledby="cabinet-heading">
        <h2 id="cabinet-heading" className="mb-3 text-xl font-bold">
          대통령·국무위원
        </h2>
        {cabinet.length === 0 ? (
          <p className="rounded border border-dashed border-line px-3 py-6 text-center text-sm text-muted">
            대통령·국무위원 자동 수집은 준비 중입니다.
          </p>
        ) : (
          <p className="mb-3 text-xs text-muted">
            위키백과 「이재명 정부의 국무위원」을 매일 수집해 각 기관 누리집과 교차 확인합니다. ※는 누리집 확인이 아직 안 된 직위입니다.
          </p>
        )}
        <ul className="grid grid-cols-1 gap-2 sm:grid-cols-2 lg:grid-cols-3">
          {cabinet.map((c) => (
            <li key={c.position} className="flex items-center justify-between gap-3 rounded border border-line bg-card px-3 py-3">
              <span className="min-w-0">
                <span className="block truncate text-sm text-muted">{c.position}</span>
                {c.name === null ? (
                  <span className="font-medium text-muted">공석</span>
                ) : (
                  <span className="font-medium">
                    {c.name}
                    {!c.verified && (
                      <span className="ml-1 text-xs text-muted" title="기관 누리집에서 아직 확인되지 않았습니다">
                        ※
                      </span>
                    )}
                  </span>
                )}
                {c.start_date && <span className="block text-xs text-muted">{c.start_date} 취임</span>}
              </span>
              {c.name !== null && <GradeBadge />}
            </li>
          ))}
        </ul>
      </section>

      <MemberExplorer members={members} />
    </div>
  );
}
