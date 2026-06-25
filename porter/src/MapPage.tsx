import { useState, useRef, useEffect } from "react";
import { MapContainer, TileLayer, useMap } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import "./MapPage.css";

type Page = "landing" | "map" | "store" | "tourinfo" | "ticket" | "booking" | "spotdetail";
type Props = { onNavigate: (page: Page) => void };

type Festival = {
  name: string;
  period: string;
  location: string;
  desc: string;
};

type Spot = {
  tag: "추천" | "진행 중";
  title: string;
  region: string;
  guide: string;
  progress: number;
  category: string;
  year: number;
  theme: string;
  era: string;
  method: string;
  provider: string;
  overview: string;
  description: string;
  images: string[];
  festivals: Festival[];
};

type Message = { role: "user" | "ai"; text: string };

const SPOTS: Spot[] = [
  {
    tag: "추천",
    title: "속리산 국립공원",
    region: "보은",
    guide: "AI 관광 가이드",
    progress: 92,
    category: "국립공원",
    year: 2026,
    theme: "자연생태·산악",
    era: "현대",
    method: "현장탐방, 트레킹",
    provider: "국립공원공단",
    overview: "속리산 국립공원은 충청북도 보은군에 위치한 대한민국 제6호 국립공원입니다. 천왕봉(1,058m)을 주봉으로 비로봉, 길상봉 등 8개 봉우리로 이루어진 산으로 법주사, 세조길 등 다양한 역사·문화 자원을 품고 있습니다.",
    description: "속리산은 1970년 국립공원으로 지정되었으며, 우리나라에서 손꼽히는 명산으로 '속세를 벗어난 산'이라는 뜻을 지니고 있습니다. 화강암 암봉과 울창한 산림이 조화를 이루며, 봄에는 진달래와 철쭉, 가을에는 단풍이 절경을 이룹니다. 정이품송(천연기념물 제103호)을 비롯해 천연기념물과 명승지가 다수 포함되어 있으며, 연간 200만 명 이상의 탐방객이 방문하는 충청도 대표 관광지입니다.",
    images: [
      "/spot-songnisan-1.jpg",
      "/spot-songnisan-2.jpg",
      "/spot-songnisan-3.jpg",
    ],
    festivals: [
      {
        name: "속리산 철쭉제",
        period: "5월 초·중순",
        location: "충북 보은군 속리산면",
        desc: "속리산 천왕봉 일대에 피어나는 철쭉을 주제로 한 봄 축제. 등산 대회, 사생 대회, 지역 특산물 장터가 함께 열립니다.",
      },
      {
        name: "보은 대추 축제",
        period: "10월 초·중순",
        location: "충북 보은군 보은읍",
        desc: "보은 대추는 왕실 진상품으로 유명합니다. 대추 따기 체험, 다양한 대추 가공 식품 시식, 지역 문화 공연을 즐길 수 있습니다.",
      },
      {
        name: "속리산 단풍 축제",
        period: "10월 하순 ~ 11월 초",
        location: "충북 보은군 속리산면",
        desc: "천왕봉과 법주사 주변을 물들이는 단풍 절경을 감상하는 가을 축제. 야간 단풍 투어와 포토존이 인기입니다.",
      },
    ],
  },
  {
    tag: "추천",
    title: "법주사",
    region: "보은",
    guide: "AI 관광 가이드",
    progress: 85,
    category: "사적",
    year: 2026,
    theme: "불교문화·건축",
    era: "삼국시대",
    method: "고증, 원형",
    provider: "문화재청",
    overview: "법주사는 충청북도 보은군 속리산에 위치한 신라시대 고찰로, 553년(진흥왕 14)에 의신조사가 창건한 사찰입니다. 팔상전(국보 제55호)을 비롯해 대웅보전, 원통보전 등 다수의 국보·보물이 보존되어 있습니다.",
    description: "법주사는 '부처님의 법이 머무는 곳'이라는 뜻으로, 신라 진흥왕 14년(553년) 의신조사에 의해 창건되었습니다. 우리나라 유일의 목조 5층 탑인 팔상전(국보 제55호)이 있으며, 거대한 금동미륵대불(33m)로도 유명합니다. 경내에는 석련지(국보 제64호), 쌍사자석등(국보 제5호) 등 국보 3점과 다수의 보물이 보존되어 있어 한국 불교 문화의 정수를 만날 수 있습니다. 2018년 유네스코 세계유산 '산사, 한국의 산지승원' 7개소 중 하나로 등재되었습니다.",
    images: [
      "/spot-beopjusa-1.jpg",
      "/spot-beopjusa-2.jpg",
      "/spot-beopjusa-3.jpg",
    ],
    festivals: [
      {
        name: "법주사 연등 축제",
        period: "5월 (부처님 오신 날 전후)",
        location: "충북 보은군 법주사",
        desc: "경내를 가득 채우는 연등 행렬과 소원 연등 달기 행사. 야간에 수천 개의 연등이 켜지면 환상적인 분위기를 연출합니다.",
      },
      {
        name: "보은 속리산 문화제",
        period: "10월 중순",
        location: "충북 보은군 보은읍·속리산",
        desc: "지역 전통문화와 민속 공연, 향토 음식 체험이 어우러진 종합 문화 행사. 속리산 트레킹과 연계 운영됩니다.",
      },
      {
        name: "세계유산 산사 문화제",
        period: "연중 (계절별)",
        location: "전국 7개 산사 (법주사 포함)",
        desc: "유네스코 세계유산 등재 기념으로 열리는 산사 문화 체험 프로그램. 템플스테이, 불교 미술 전시, 명상 체험 등을 운영합니다.",
      },
    ],
  },
  {
    tag: "진행 중",
    title: "단양 패러글라이딩",
    region: "단양",
    guide: "AI 관광 가이드",
    progress: 60,
    category: "레저스포츠",
    year: 2026,
    theme: "레저·액티비티",
    era: "현대",
    method: "체험형",
    provider: "단양군청",
    overview: "단양 소백산 패러글라이딩은 소백산 국립공원을 배경으로 단양강(남한강)의 절경을 하늘에서 감상할 수 있는 레저 스포츠 체험입니다. 도담삼봉, 구담봉 등 단양 8경을 조망하며 비행하는 특별한 경험을 제공합니다.",
    description: "충청북도 단양군은 남한강과 소백산이 어우러진 천혜의 경관을 자랑합니다. 패러글라이딩 이륙장에서 도약하면 도담삼봉, 석문, 구담봉 등 단양 8경을 한눈에 조망할 수 있습니다. 전문 조종사와 함께 탑승하는 2인 탠덤 비행으로 누구나 안전하게 즐길 수 있으며, 약 10~20분간의 비행 코스를 운영합니다. 봄·가을이 최고 성수기이며, 맑은 날에는 소백산 능선과 굽이치는 단양강의 절경이 장관을 이룹니다.",
    images: [
      "/spot-danyang-1.jpg",
      "/spot-danyang-2.jpg",
      "/spot-danyang-3.jpg",
    ],
    festivals: [
      {
        name: "단양 소백산 철쭉제",
        period: "5월 중·하순",
        location: "충북 단양군 소백산 비로봉",
        desc: "소백산 비로봉 일대를 분홍빛으로 뒤덮는 철쭉 군락을 감상하는 봄 축제. 산신제, 가요제, 포토 경연 대회가 함께 열립니다.",
      },
      {
        name: "단양 마늘 축제",
        period: "6월 초·중순",
        location: "충북 단양군 단양읍",
        desc: "단양의 특산물 마늘을 주제로 한 특산물 축제. 마늘 떡메치기, 마늘 요리 경연, 마늘 테마 체험 부스가 운영됩니다.",
      },
      {
        name: "온달 문화 축제",
        period: "10월 초·중순",
        location: "충북 단양군 영춘면 온달산성",
        desc: "고구려 장수 온달과 평강공주 설화를 테마로 한 역사문화 축제. 마상 무예 공연, 온달관광지 투어, 남한강 뗏목 체험이 인기입니다.",
      },
    ],
  },
  {
    tag: "진행 중",
    title: "청주 고인쇄박물관",
    region: "청주",
    guide: "AI 관광 가이드",
    progress: 74,
    category: "박물관",
    year: 2026,
    theme: "역사·인쇄문화",
    era: "고려시대",
    method: "전시, 체험",
    provider: "청주시",
    overview: "청주 고인쇄박물관은 세계 최초의 금속활자본인 직지심체요절(1377년)이 인쇄된 청주 흥덕사지에 건립된 박물관입니다. 고인쇄 문화의 역사와 가치를 체계적으로 보존·전시하고 있습니다.",
    description: "청주 고인쇄박물관은 1992년 흥덕사지 발굴 이후 1992년 개관한 박물관으로, '직지심체요절'의 인쇄지인 흥덕사지(사적 제315호)에 위치합니다. 직지심체요절은 1377년 청주 흥덕사에서 금속활자로 인쇄된 세계 최고(最古)의 금속활자 인쇄물로 2001년 유네스코 세계기록유산에 등재되었습니다. 박물관에서는 금속활자 제작 과정, 목판·금속활자 인쇄 시연, 직접 인쇄를 체험하는 교육 프로그램을 운영합니다. 매년 9~10월에는 '직지코리아 국제페스티벌'이 개최됩니다.",
    images: [
      "/spot-cheongju-1.jpg",
      "/spot-cheongju-2.jpg",
      "/spot-cheongju-3.jpg",
    ],
    festivals: [
      {
        name: "직지코리아 국제 페스티벌",
        period: "9월 하순 ~ 10월 초",
        location: "충북 청주시 흥덕구 일원",
        desc: "세계 최초 금속활자본 직지를 기념하는 국제 행사. 활자 인쇄 체험, 국제 학술 심포지엄, 미디어아트 전시, 북 페어가 함께 열립니다.",
      },
      {
        name: "청주 공예 비엔날레",
        period: "격년제 (홀수년 9~10월)",
        location: "충북 청주시 문화제조창",
        desc: "세계 유일의 공예 전문 국제 비엔날레. 50여 개국 작가들의 현대 공예 작품과 전통 공예 재현 전시가 함께 진행됩니다.",
      },
      {
        name: "청주 가경 어울마당",
        period: "10월 중순",
        location: "충북 청주시 가경동 일원",
        desc: "시민 참여형 지역 문화 축제. 전통 놀이, 지역 예술가 공연, 향토 음식 마당이 열리며 가족 단위 방문객에게 인기입니다.",
      },
    ],
  },
];


const AI_RESPONSES: Record<string, string> = {
  default: "안녕하세요! 충북 관광 AI 가이드입니다. 여행 계획, 관광지 추천, 맛집 정보 등 무엇이든 물어보세요!",
};

function getAIResponse(input: string): string {
  if (input.includes("속리산") || input.includes("국립공원")) {
    return "속리산 국립공원은 충북 보은에 위치한 아름다운 명산입니다. 법주사, 세조길, 문장대 등 볼거리가 많아요. 봄 철쭉과 가을 단풍이 특히 아름답습니다!";
  }
  if (input.includes("법주사")) {
    return "법주사는 신라 시대에 창건된 유서 깊은 사찰입니다. 국보인 쌍사자석등과 팔상전이 있으며, 속리산 국립공원 내에 위치해 있어 함께 방문하기 좋습니다.";
  }
  if (input.includes("맛집") || input.includes("음식")) {
    return "충북의 대표 음식으로는 청주 순대국밥, 단양 마늘요리, 보은 대추 관련 음식이 있습니다. 지역 특산물을 활용한 맛집이 많으니 꼭 방문해 보세요!";
  }
  if (input.includes("추천") || input.includes("어디")) {
    return "충북 여행지로는 속리산 국립공원, 단양 8경, 청주 고인쇄박물관, 청남대를 추천드립니다. 계절에 따라 다양한 매력을 즐길 수 있어요!";
  }
  return "좋은 질문이에요! 충북에는 아름다운 자연과 역사 문화 명소가 가득합니다. 더 구체적인 장소나 활동에 대해 알고 싶으시면 말씀해 주세요.";
}

function KoreaMask() {
  const map = useMap();

  useEffect(() => {
    let maskLayer: L.GeoJSON | undefined;

    fetch("/korea-outline.json")
      .then((r) => r.json())
      .then((data) => {
        const feature = data.features[0];
        // shapely unary_union 결과: MultiPolygon (진짜 외곽선, 내부 경계 없음)
        // 각 폴리곤의 외곽 링을 구멍으로 사용
        const koreaPolygons: number[][][][] = feature.geometry.type === "MultiPolygon"
          ? feature.geometry.coordinates
          : [feature.geometry.coordinates];

        const maskGeoJSON = {
          type: "Feature",
          geometry: {
            type: "Polygon",
            coordinates: [
              // 세계 외곽 링
              [[-180, -90], [180, -90], [180, 90], [-180, 90], [-180, -90]],
              // 한국 각 섬/본토의 외곽 링을 구멍으로
              ...koreaPolygons.map((poly) => poly[0]),
            ],
          },
          properties: {},
        };

        maskLayer = L.geoJSON(maskGeoJSON as any, {
          style: {
            fillColor: "#555555",
            fillOpacity: 0.97,
            color: "transparent",
            weight: 0,
            fillRule: "evenodd",
          } as any,
        }).addTo(map);
      });

    return () => {
      if (maskLayer) map.removeLayer(maskLayer);
    };
  }, [map]);

  return null;
}

function FestivalPopup({
  festival,
  onClose,
}: {
  festival: Festival;
  onClose: () => void;
}) {
  return (
    <div className="festival-popup-overlay" onClick={onClose}>
      <div className="festival-popup" onClick={(e) => e.stopPropagation()}>
        <button className="festival-popup-close" onClick={onClose}>✕</button>
        <div className="festival-popup-period">{festival.period}</div>
        <h3 className="festival-popup-name">{festival.name}</h3>
        <p className="festival-popup-location">📍 {festival.location}</p>
        <p className="festival-popup-desc">{festival.desc}</p>
      </div>
    </div>
  );
}

function TouristDetail({
  spot,
  onClose,
}: {
  spot: Spot;
  onClose: () => void;
}) {
  const [imgIdx, setImgIdx] = useState(0);
  const [imgError, setImgError] = useState<Record<number, boolean>>({});
  const [activeFestival, setActiveFestival] = useState<Festival | null>(null);

  const prev = () => setImgIdx((i) => (i - 1 + spot.images.length) % spot.images.length);
  const next = () => setImgIdx((i) => (i + 1) % spot.images.length);

  return (
    <div className="detail-overlay" onClick={onClose}>
      <div className="detail-modal" onClick={(e) => e.stopPropagation()}>
        <button className="detail-close" onClick={onClose}>✕</button>

        {/* Left: image carousel */}
        <div className="detail-image-col">
          <div className="detail-image-wrap">
            {imgError[imgIdx] ? (
              <div className="detail-image-fallback">
                <span>{spot.title}</span>
              </div>
            ) : (
              <img
                src={spot.images[imgIdx]}
                alt={spot.title}
                onError={() => setImgError((e) => ({ ...e, [imgIdx]: true }))}
              />
            )}
          </div>
          <div className="detail-image-nav">
            <button onClick={prev} disabled={spot.images.length <= 1}>‹</button>
            <span>{imgIdx + 1} / {spot.images.length}</span>
            <button onClick={next} disabled={spot.images.length <= 1}>›</button>
          </div>
        </div>

        {/* Right: info */}
        <div className="detail-info-col">
          <div className="detail-info-top">
            <span className={`detail-badge detail-badge--${spot.tag === "추천" ? "active" : "progress"}`}>
              {spot.category}
            </span>
            <span className="detail-year">제작년도 {spot.year}</span>
          </div>

          <h2 className="detail-title">{spot.title}</h2>

          <table className="detail-table">
            <tbody>
              <tr>
                <th>테마</th>
                <td>{spot.theme}</td>
                <th>시대</th>
                <td>{spot.era}</td>
              </tr>
              <tr>
                <th>제작방식</th>
                <td>{spot.method}</td>
                <th>제공기관</th>
                <td>{spot.provider}</td>
              </tr>
              <tr>
                <th>제작개요</th>
                <td colSpan={3}>{spot.overview}</td>
              </tr>
            </tbody>
          </table>

          <p className="detail-desc">{spot.description}</p>

          {/* Nearby events section */}
          <div className="detail-festival">
            <div className="detail-festival-header">
              <span className="detail-festival-icon">🗓️</span>
              <span className="detail-festival-title">주변 행사</span>
            </div>
            <div className="detail-festival-grid">
              {spot.festivals.map((f) => (
                <div
                  className="festival-card"
                  key={f.name}
                  onClick={() => setActiveFestival(f)}
                >
                  <div className="festival-card-top">
                    <span className="festival-name">{f.name}</span>
                    <span className="festival-period">{f.period}</span>
                  </div>
                  <span className="festival-location">📍 {f.location}</span>
                  <p className="festival-desc">{f.desc}</p>
                  <span className="festival-more">자세히 보기 →</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {activeFestival && (
        <FestivalPopup
          festival={activeFestival}
          onClose={() => setActiveFestival(null)}
        />
      )}
    </div>
  );
}

export default function MapPage({ onNavigate }: Props) {
  const [selectedSpot, setSelectedSpot] = useState<Spot | null>(null);
  const [aiMode, setAiMode] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    { role: "ai", text: AI_RESPONSES.default },
  ]);
  const [input, setInput] = useState("");
  const chatEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = () => {
    const trimmed = input.trim();
    if (!trimmed) return;
    const userMsg: Message = { role: "user", text: trimmed };
    const aiMsg: Message = { role: "ai", text: getAIResponse(trimmed) };
    setMessages((prev) => [...prev, userMsg, aiMsg]);
    setInput("");
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") sendMessage();
  };

  return (
    <div className="map-page">
      {/* Navbar */}
      <nav className="map-nav">
        <div className="map-nav-left">
          <div className="map-nav-brand" onClick={() => onNavigate("landing")}>
            <div className="nav-logo-circle">
              <span className="nav-logo-text">A</span>
            </div>
            <span className="nav-brand-name">dapter4</span>
          </div>
          <div className="map-nav-links">
            <a onClick={() => onNavigate("tourinfo")}>관광정보</a>
            <a className="active">관광동선</a>
            <a onClick={() => onNavigate("store")}>스토어</a>
            <a onClick={() => onNavigate("ticket")}>티켓</a>
          </div>
        </div>
        <div className="map-nav-right">
          <div className="map-nav-setting">설정</div>
        </div>
      </nav>

      {/* Hero */}
      <div className="map-hero">
        <img src="/palace.jpg" alt="한국 관광" />
      </div>

      {/* Body */}
      <div className="map-body">
        {/* Left stats */}
        <div className="map-stats">
          <div className="stat-card">
            <div className="stat-card-header">
              <span className="stat-card-title">이번 주 방문객</span>
              <span className="stat-card-menu">···</span>
            </div>
            <div className="stat-num">2,840</div>
            <div className="stat-sub">
              <span className="stat-up">↑ 340명</span>&nbsp;지난주보다 많음
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-card-header">
              <span className="stat-card-title">진행 중인 행사</span>
              <span className="stat-card-menu">···</span>
            </div>
            <div className="stat-num">8</div>
            <div className="stat-sub">
              <span className="stat-up">↑ 2개</span>&nbsp;지난주보다 많음
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-card-header">
              <span className="stat-card-title">등록 관광지</span>
              <span className="stat-card-menu">···</span>
            </div>
            <div className="stat-num">156</div>
            <div className="stat-sub">
              <span>→</span>&nbsp;지난주와 동일
            </div>
          </div>
        </div>

        {/* Center: map with overlaid AI chat */}
        <div className="map-center">
          {aiMode ? (
            <div className="ai-chat-panel">
              <div className="ai-chat-character">
                <img src="/ai-character-male.png" alt="AI 가이드" />
              </div>
              <div className="ai-chat-area">
                <div className="ai-chat-messages">
                  {messages.map((msg, i) => (
                    <div key={i} className={`ai-msg ai-msg--${msg.role}`}>
                      {msg.role === "ai" && (
                        <div className="ai-msg-avatar">AI</div>
                      )}
                      <div className="ai-msg-bubble">{msg.text}</div>
                    </div>
                  ))}
                  <div ref={chatEndRef} />
                </div>
                <div className="ai-chat-input-row">
                  <input
                    className="ai-chat-input"
                    placeholder="관광지, 맛집, 일정 등 무엇이든 물어보세요..."
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={handleKeyDown}
                  />
                  <button className="ai-chat-send" onClick={sendMessage}>
                    전송
                  </button>
                </div>
              </div>
            </div>
          ) : (
            <>
              <div className="map-search-row">
                <span className="map-search-label">관광지 검색</span>
                <input className="map-search-input" placeholder="검색..." />
                <button className="map-filter-btn">필터</button>
              </div>
              <div className="map-container">
                <button
                  className="map-ai-btn"
                  onClick={() => setAiMode(true)}
                >
                  AI 검색
                </button>
                <MapContainer
                  center={[35.0, 127.8]}
                  zoom={7}
                  minZoom={7}
                  maxZoom={13}
                  maxBounds={[[32.0, 123.5], [39.8, 132.8]]}
                  maxBoundsViscosity={1.0}
                  style={{ width: "100%", height: "100%" }}
                  zoomControl={true}
                >
                  <TileLayer
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
                  />
                  <KoreaMask />
                </MapContainer>
              </div>
            </>
          )}
        </div>

        {/* Right: spot cards */}
        <div className="map-sidebar">
          {SPOTS.map((s) => (
            <div
              className="spot-card"
              key={s.title}
              onClick={() => setSelectedSpot(s)}
            >
              <div className={`spot-tag spot-tag--${s.tag === "추천" ? "active" : "progress"}`}>
                {s.tag}
              </div>
              <h3>{s.title}</h3>
              <div className="spot-meta">
                <span>2026</span>
                <div className="spot-meta-dot" />
                <span>{s.region}</span>
              </div>
              <div className="spot-guide">
                <div className="spot-guide-avatar">🗺️</div>
                <div className="spot-guide-info">
                  <span className="spot-guide-role">관광 가이드</span>
                  <span className="spot-guide-name">{s.guide}</span>
                </div>
              </div>
              <div className="spot-progress-row">
                <div className="spot-bar">
                  <div className="spot-bar-fill" style={{ width: `${s.progress}%` }} />
                </div>
                <span className="spot-pct">{s.progress}%</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Detail modal */}
      {selectedSpot && (
        <TouristDetail spot={selectedSpot} onClose={() => setSelectedSpot(null)} />
      )}
    </div>
  );
}
