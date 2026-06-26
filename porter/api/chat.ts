import Anthropic from "@anthropic-ai/sdk";

const SYSTEM_PROMPT = `당신은 대한민국 전국의 문화유산, 관광지, 맛집, 교통을 안내하는 AI 가이드입니다.

다음 분야에서 상세하고 친절하게 안내해 드립니다:
- 문화유산: 궁궐(경복궁·창덕궁 등), 사찰, 유네스코 세계유산, 역사 유적지
- 관광지: 자연명소, 국립공원, 해변, 섬, 테마파크, 도심 명소
- 맛집: 지역 향토 음식, 유명 맛집, 음식 문화 소개
- 교통: KTX, 지하철, 고속버스, 렌터카, 항공편 등 이동 수단

항상 한국어로 답변하세요. 정보는 구체적이고 실용적으로 제공하며, 운영시간·입장료·교통편 같은 실용 정보도 함께 안내해 주세요.`;

export default async function handler(req: any, res: any) {
  if (req.method !== "POST") {
    res.status(405).json({ error: "Method not allowed" });
    return;
  }

  const { messages } = req.body as {
    messages: Array<{ role: "user" | "assistant"; content: string }>;
  };

  if (!messages || !Array.isArray(messages)) {
    res.status(400).json({ error: "messages array required" });
    return;
  }

  const client = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });

  try {
    const response = await client.messages.create({
      model: "claude-opus-4-8",
      max_tokens: 1024,
      system: SYSTEM_PROMPT,
      messages,
    });

    const text =
      response.content[0].type === "text" ? response.content[0].text : "";
    res.status(200).json({ reply: text });
  } catch (err: any) {
    console.error("Claude API error:", err);
    res.status(500).json({ error: "AI 응답 오류가 발생했습니다." });
  }
}
