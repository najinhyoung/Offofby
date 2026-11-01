// 등급 산정 전까지는 자리만 표시한다. 등급이 생기면 grade prop으로 넘긴다.
export function GradeBadge({ grade }: { grade?: string | null }) {
  if (!grade) {
    return (
      <span
        className="inline-flex shrink-0 items-center rounded border border-dashed border-line px-2 py-0.5 text-xs text-muted"
        title="평판등급은 준비 중입니다"
      >
        등급 준비 중
      </span>
    );
  }
  return (
    <span className="inline-flex shrink-0 items-center rounded bg-accent px-2 py-0.5 text-xs font-bold text-white">
      {grade}
    </span>
  );
}
