// 선거구명 첫 토큰으로 시도를 뽑는다. 예: "서울 종로구" → "서울", "세종특별자치시갑" → "세종"
export function regionOf(district: string): string {
  if (district === "비례대표") return "비례대표";
  if (district.startsWith("세종")) return "세종";
  return district.split(" ")[0];
}
