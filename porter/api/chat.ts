// Vercel 함수는 Node ESM이라 상대 경로 import에 .js 확장자가 필요 (빌드 시 .ts가 .js로 바뀜)
import { DETAIL_DATA } from "../src/spotDetailData.js";

const SYSTEM_PROMPT = `당신은 대한민국 전국의 문화유산, 관광지, 맛집, 교통을 안내하는 AI 가이드입니다.

다음 분야에서 상세하고 친절하게 안내해 드립니다:
- 문화유산: 궁궐(경복궁·창덕궁 등), 사찰, 유네스코 세계유산, 역사 유적지
- 관광지: 자연명소, 국립공원, 해변, 섬, 테마파크, 도심 명소
- 맛집: 지역 향토 음식, 유명 맛집, 음식 문화 소개
- 교통: KTX, 지하철, 고속버스, 렌터카, 항공편 등 이동 수단

항상 한국어로 답변하세요. 정보는 구체적이고 실용적으로 제공하며, 운영시간·입장료·교통편 같은 실용 정보도 함께 안내해 주세요.

답변 형식:
- 채팅 화면은 마크다운을 표시하지 못합니다. **, #, 표(|), 코드 블록 없이 평문으로 쓰고, 목록은 "1." 또는 "-"로 시작하는 줄로만 나눠 주세요.
- 15줄 이내로 핵심만 간결하게 답하세요.
- 장소의 위치, 노선, 요금처럼 확실하지 않은 정보는 지어내지 말고 "방문 전 공식 안내를 확인해 주세요"라고 안내하세요.

근거 자료:
- 시스템 메시지 끝의 [사이트 자료]는 검수된 정보입니다. 관련 내용이 있으면 이 자료를 우선 사용하고, 일반 지식과 다르면 자료를 따르세요.
- 자료에 없는 연도, 인물, 문화재 지정 번호 같은 세부 사실은 확실할 때만 말하고, 확실하지 않으면 생략하세요.`;

// 이름에서 검색어 뽑기: 전체 이름 + 일반 명사가 아닌 2글자 이상 단어 (예: "성균관 문묘" → 성균관, 문묘)
const GENERIC = new Set(["국립공원", "해수욕장", "해변"]);
const SPOT_KEYWORDS = Object.keys(DETAIL_DATA).map((name) => ({
  name,
  keywords: [name, ...name.split(" ").filter((w) => w.length >= 2 && !GENERIC.has(w))],
}));

// 최근 사용자 질문에 나온 명소의 검수된 자료(소개·주소·운영시간·FAQ)만 골라 근거로 넣는다
// 전부 넣으면 Groq 무료 등급 분당 토큰 한도를 넘으므로 질문과 관련된 것만 (리뷰는 예시 데이터라 제외)
function siteContext(messages: Array<{ role: string; content: string }>): string {
  const recent = messages.filter((m) => m.role === "user").slice(-3).map((m) => m.content).join("\n");
  const hits = SPOT_KEYWORDS.filter((s) => s.keywords.some((k) => recent.includes(k))).slice(0, 2);
  if (hits.length === 0) {
    return `[사이트 자료] 이 사이트가 상세 정보를 보유한 명소: ${Object.keys(DETAIL_DATA).join(", ")}`;
  }
  return hits.map(({ name }) => {
    const d = DETAIL_DATA[name];
    const faq = d.faq.map((f) => `Q. ${f.q}\nA. ${f.a}`).join("\n");
    return `[사이트 자료: ${name}]\n소개: ${d.overview}\n주소: ${d.address}\n운영시간: ${d.hours}\n${faq}`;
  }).join("\n\n");
}

// Groq가 2026-08-16에 llama-3.3-70b-versatile을 엔터프라이즈 전용으로 바꿔 일반 키로는 404 → 권장 대체 모델
// GROQ_MODEL 환경변수로 바꿀 수 있다
const MODEL = process.env.GROQ_MODEL || "openai/gpt-oss-120b";

export default async function handler(req: any, res: any) {
  if (req.method !== "POST") {
    res.status(405).json({ error: "Method not allowed" });
    return;
  }

  const { messages } = req.body as {
    messages: Array<{ role: "user" | "assistant"; content: string }>;
  };

  if (!messages || !Array.isArray(messages) || messages.length === 0) {
    res.status(400).json({ error: "messages array required" });
    return;
  }

  const apiKey = process.env.GROQ_API_KEY ?? "";
  if (!apiKey) {
    res.status(500).json({ error: "GROQ_API_KEY 환경변수가 없습니다" });
    return;
  }

  try {
    const response = await fetch("https://api.groq.com/openai/v1/chat/completions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${apiKey}`,
      },
      body: JSON.stringify({
        model: MODEL,
        messages: [
          { role: "system", content: `${SYSTEM_PROMPT}\n\n${siteContext(messages)}` },
          ...messages.map((m) => ({ role: m.role, content: m.content })),
        ],
        // gpt-oss는 추론 모델: 추론은 중간, 응답에서는 빼고(최종 답만 content로), 추론 토큰을 감안해 출력 한도를 넉넉히
        reasoning_effort: "medium",
        include_reasoning: false,
        max_completion_tokens: 2048,
        temperature: 0.7,
      }),
    });

    if (!response.ok) {
      const errText = await response.text();
      console.error("Groq error:", response.status, errText);
      // 자세한 오류는 서버 로그에만 (방문자 화면에 제공자 응답이나 키 정보를 보이지 않는다)
      res.status(502).json({ error: "AI 응답을 받지 못했습니다. 잠시 뒤 다시 시도해 주세요." });
      return;
    }

    const data = await response.json() as {
      choices: Array<{ message: { content: string } }>;
    };
    const text = data.choices[0]?.message?.content ?? "";
    res.status(200).json({ reply: text });
  } catch (err: any) {
    console.error("Chat error:", err?.message);
    res.status(500).json({ error: err?.message ?? "AI 응답 오류가 발생했습니다." });
  }
}
