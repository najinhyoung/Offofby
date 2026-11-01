import { revalidatePath } from "next/cache";
import { NextRequest, NextResponse } from "next/server";

// 일일 파이프라인이 적재를 끝낸 뒤 호출: POST /api/revalidate  (Authorization: Bearer $REVALIDATE_SECRET)
export async function POST(req: NextRequest) {
  const secret = process.env.REVALIDATE_SECRET;
  if (!secret || req.headers.get("authorization") !== `Bearer ${secret}`) {
    return NextResponse.json({ ok: false }, { status: 401 });
  }
  revalidatePath("/", "layout");
  return NextResponse.json({ ok: true });
}
