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
        model: "llama-3.3-70b-versatile",
        messages: [
          { role: "system", content: SYSTEM_PROMPT },
          ...messages.map((m) => ({ role: m.role, content: m.content })),
        ],
        max_tokens: 1024,
        temperature: 0.7,
      }),
    });

    if (!response.ok) {
      const errText = await response.text();
      console.error("Groq error:", response.status, errText);
      res.status(500).json({ error: `Groq ${response.status}: ${errText} (key prefix: ${apiKey.slice(0,6)}, len: ${apiKey.length})` });
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
