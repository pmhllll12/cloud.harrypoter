import { useState } from "react";
import "./TourInfoPage.css";
import type { Spot } from "./SpotDetailPage";
import ChatModal from "./ChatModal";

type Page = "landing" | "map" | "store" | "tourinfo" | "ticket" | "booking" | "spotdetail";
type Props = { onNavigate: (page: Page) => void; onViewSpot: (spot: Spot) => void };

const SPOTS = [
  {
    name: "속리산 국립공원",
    region: "충북 보은",
    category: "자연",
    desc: "해발 1,058m의 장엄한 봉우리와 울창한 원시림. 법주사, 세조길 등 자연과 역사가 공존하는 대표 명소.",
    img: "https://upload.wikimedia.org/wikipedia/commons/4/4f/Songnisan.jpg",
  },
  {
    name: "성균관 문묘",
    region: "서울 종로",
    category: "역사문화",
    desc: "고려 말 창건된 조선 최고의 유교 교육 기관. 공자를 모신 대성전과 명륜당이 600년 역사를 간직하고 있는 유네스코 세계유산.",
    img: "https://images.unsplash.com/photo-1575034176396-66241b37d3d2?w=800&h=600&fit=crop&crop=center&q=80",
  },
  {
    name: "경복궁",
    region: "서울 종로",
    category: "역사문화",
    desc: "조선 왕조의 정궁. 근정전, 경회루 등 웅장한 전각들이 북악산을 배경으로 펼쳐지는 한국 대표 궁궐.",
    img: "https://images.unsplash.com/photo-1638964663550-e2123ac8900b?w=900&h=500&fit=crop&crop=center&q=80",
  },
  {
    name: "해운대 해수욕장",
    region: "부산 해운대",
    category: "자연",
    desc: "국내 최대 규모의 해수욕장. 에메랄드빛 바다와 도심 스카이라인이 어우러지는 부산의 상징.",
    img: "https://images.unsplash.com/photo-1700277842839-2ef54f815f47?w=800&h=450&fit=crop&crop=center&q=80",
  },
  {
    name: "불국사",
    region: "경북 경주",
    category: "역사문화",
    desc: "신라 불교 예술의 정수. 다보탑·석가탑을 품은 유네스코 세계유산으로 천년 고도 경주의 대표 사찰.",
    img: "https://images.unsplash.com/photo-1684134549350-be5fd0d8feaa?w=600&q=80&fit=crop",
  },
  {
    name: "경포대 해변",
    region: "강원 강릉",
    category: "힐링",
    desc: "동해안 최대 석호 경포호와 맞닿은 백사장. 솔숲 너머로 펼쳐지는 일출이 일품인 힐링 명소.",
    img: "https://images.unsplash.com/photo-1542086094-a61c1ab7c4b8?w=800&h=450&fit=crop&crop=center&q=80",
  },
];

const CATEGORIES = ["전체", "자연", "역사문화", "힐링"];

export default function TourInfoPage({ onNavigate, onViewSpot }: Props) {
  const [chatOpen, setChatOpen] = useState(false);
  return (
    <div className="tourinfo-page">
      <nav className="ti-nav">
        <div className="ti-nav-left">
          <div className="ti-nav-brand" onClick={() => onNavigate("landing")}>
            <div className="nav-logo-circle"><span className="nav-logo-text">A</span></div>
            <span className="nav-brand-name">dapter4</span>
          </div>
          <div className="ti-nav-links">
            <a className="active">관광정보</a>
            <a onClick={() => onNavigate("map")}>관광동선</a>
            <a onClick={() => onNavigate("store")}>스토어</a>
            <a onClick={() => onNavigate("ticket")}>티켓</a>
          </div>
        </div>
        <div className="ti-nav-setting">설정</div>
      </nav>

      {/* Hero */}
      <section className="ti-hero">
        <img
          src="https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1400&q=80&fit=crop"
          alt="한국 관광"
        />
        <div className="ti-hero-overlay">
          <span className="ti-hero-tag">관광정보</span>
          <h1>자연과 역사가 숨쉬는<br />대한민국</h1>
          <p>서울부터 제주까지, 전국의 숨겨진 보석 같은 명소를 AI와 함께 탐험하세요</p>
        </div>
      </section>

      {/* Category Filter */}
      <section className="ti-filter">
        {CATEGORIES.map((c) => (
          <button key={c} className={`ti-filter-btn ${c === "전체" ? "active" : ""}`}>{c}</button>
        ))}
      </section>

      {/* Spots Grid */}
      <section className="ti-spots">
        <div className="ti-spots-header">
          <h2>지역 추천 명소</h2>
          <span className="ti-spots-count">{SPOTS.length}곳</span>
        </div>
        <div className="ti-grid">
          {SPOTS.map((s) => (
            <div className="ti-card" key={s.name}>
              {s.name === "법주사" && (
                <div className="ti-event-badge">
                  <span className="ti-event-badge-label">· EVENT ·</span>
                  <span className="ti-event-badge-pct">50%</span>
                  <span className="ti-event-badge-off">OFF</span>
                </div>
              )}
              <div className="ti-card-img">
                <img src={s.img} alt={s.name} />
                <span className="ti-card-category">{s.category}</span>
              </div>
              <div className="ti-card-body">
                <div className="ti-card-region">{s.region}</div>
                <h3 className="ti-card-name">{s.name}</h3>
                <p className="ti-card-desc">{s.desc}</p>
                <button className="ti-card-btn" onClick={() => onViewSpot(s)}>AI 가이드 보기</button>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* AI Banner */}
      <section className="ti-ai-banner">
        <div className="ti-ai-content">
          <h2>AI와 함께하는 스마트 관광</h2>
          <p>원하는 명소에 대해 궁금한 점을 AI에게 물어보세요.<br />역사, 교통, 맛집까지 실시간으로 안내해드립니다.</p>
          <button className="ti-ai-btn" onClick={() => setChatOpen(true)}>AI와 대화하기</button>
        </div>
      </section>

      <ChatModal open={chatOpen} onClose={() => setChatOpen(false)} />
    </div>
  );
}
