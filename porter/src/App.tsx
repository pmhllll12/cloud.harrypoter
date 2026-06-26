import { useState, useEffect, useCallback } from "react";
import "./App.css";
import MapPage from "./MapPage";
import StorePage from "./StorePage";
import TourInfoPage from "./TourInfoPage";
import TicketPage from "./TicketPage";
import BookingPage, { type Ticket } from "./BookingPage";
import SpotDetailPage, { type Spot } from "./SpotDetailPage";

type Page = "landing" | "map" | "store" | "tourinfo" | "ticket" | "booking" | "spotdetail";

type HistoryState = {
  page: Page;
  ticket?: Ticket;
  spot?: Spot;
};

export default function App() {
  const [page, setPage] = useState<Page>("landing");
  const [textVisible, setTextVisible] = useState(false);
  const [selectedTicket, setSelectedTicket] = useState<Ticket | null>(null);
  const [selectedSpot, setSelectedSpot] = useState<Spot | null>(null);

  // 초기 히스토리 상태 설정
  useEffect(() => {
    window.history.replaceState({ page: "landing" } as HistoryState, "");
  }, []);

  // 까치가 지나간 후 텍스트 등장
  useEffect(() => {
    const t = setTimeout(() => setTextVisible(true), 1800);
    return () => clearTimeout(t);
  }, []);

  // 브라우저 뒤로/앞으로 처리
  useEffect(() => {
    const handlePop = (e: PopStateEvent) => {
      window.scrollTo(0, 0);
      const state = e.state as HistoryState | null;
      if (!state) { setPage("landing"); return; }
      setPage(state.page);
      if (state.ticket) setSelectedTicket(state.ticket);
      if (state.spot) setSelectedSpot(state.spot);
    };
    window.addEventListener("popstate", handlePop);
    return () => window.removeEventListener("popstate", handlePop);
  }, []);

  // navigate: 히스토리에 쌓으면서 페이지 전환 + 스크롤 최상단
  const navigate = useCallback((newPage: Page) => {
    window.scrollTo(0, 0);
    window.history.pushState({ page: newPage } as HistoryState, "");
    setPage(newPage);
  }, []);

  const handleBook = useCallback((ticket: Ticket) => {
    window.scrollTo(0, 0);
    setSelectedTicket(ticket);
    window.history.pushState({ page: "booking", ticket } as HistoryState, "");
    setPage("booking");
  }, []);

  const handleViewSpot = useCallback((spot: Spot) => {
    window.scrollTo(0, 0);
    setSelectedSpot(spot);
    window.history.pushState({ page: "spotdetail", spot } as HistoryState, "");
    setPage("spotdetail");
  }, []);

  if (page === "map") return <MapPage onNavigate={navigate} />;
  if (page === "store") return <StorePage onNavigate={navigate} />;
  if (page === "tourinfo") return <TourInfoPage onNavigate={navigate} onViewSpot={handleViewSpot} />;
  if (page === "spotdetail" && selectedSpot) return <SpotDetailPage onNavigate={navigate} spot={selectedSpot} />;
  if (page === "ticket") return <TicketPage onNavigate={navigate} onBook={handleBook} />;
  if (page === "booking" && selectedTicket)
    return <BookingPage onNavigate={navigate} ticket={selectedTicket} allTickets={ALL_TICKETS} />;

  return (
    <section className={`landing ${!textVisible ? "landing--intro" : ""}`}>
      <nav className="navbar">
        <div className="nav-left">
          <div className="nav-brand">
            <div className="nav-logo-circle">
              <span className="nav-logo-text">A</span>
            </div>
            <span className="nav-brand-name">dapter4</span>
          </div>
          <div className="nav-links">
            <a onClick={() => navigate("tourinfo")} style={{ cursor: "pointer" }}>관광정보</a>
            <a onClick={() => navigate("map")} style={{ cursor: "pointer" }}>관광동선</a>
            <a onClick={() => navigate("store")} style={{ cursor: "pointer" }}>스토어</a>
            <a onClick={() => navigate("ticket")} style={{ cursor: "pointer" }}>티켓</a>
          </div>
        </div>
        <div className="nav-actions" />
      </nav>

      <div className="landing-visual" aria-hidden="true">
        <img className="palace-img" src="/palace.jpg" alt="" />
        <div className="palace-mask" />
      </div>

      {/* 까치 인트로 애니메이션 */}
      <div className="magpie-overlay" aria-hidden="true">
        <svg className="magpie-bird" viewBox="0 0 160 100" xmlns="http://www.w3.org/2000/svg">
          {/* 꼬리 */}
          <path d="M22 54 Q4 70 8 90 L26 58 Z" fill="#0d0d0d"/>
          <path d="M17 50 Q-2 64 3 84 L21 54 Z" fill="#1a1a1a"/>
          {/* 몸통 */}
          <ellipse cx="56" cy="54" rx="33" ry="17" fill="#111"/>
          {/* 흰 배 */}
          <ellipse cx="50" cy="59" rx="21" ry="12" fill="#f0f0f0"/>
          {/* 날개 + 흰 패치 (함께 퍼덕) */}
          <g className="magpie-wing-group">
            <path d="M38 46 Q60 16 94 34 Q70 44 44 53 Z" fill="#111"/>
            <path d="M43 48 Q63 21 89 36 Q67 44 48 52 Z" fill="#ddd"/>
          </g>
          {/* 머리 */}
          <ellipse cx="97" cy="40" rx="18" ry="16" fill="#111"/>
          {/* 부리 */}
          <path d="M114 39 L134 36 L114 44 Z" fill="#555"/>
          {/* 눈 */}
          <circle cx="102" cy="35" r="4.5" fill="#fff"/>
          <circle cx="103" cy="35" r="2.8" fill="#111"/>
          <circle cx="101" cy="34" r="1" fill="#fff"/>
        </svg>
      </div>

      <div className="landing-text">
        <h1 className="landing-title">
          대한민국 구석구석을<br />
          AI와 함께 탐험하세요
        </h1>
        <p className="landing-sub">
          서울부터 제주까지, AI가 전국의 자연과 문화유산을 생생하게 안내합니다
        </p>
      </div>
    </section>
  );
}

const ALL_TICKETS: Ticket[] = [
  {
    name: "단양 패러글라이딩 체험",
    region: "충북 단양",
    category: "액티비티",
    price: 80000,
    duration: "약 2시간",
    rating: 4.9,
    reviews: 312,
    img: "https://images.unsplash.com/photo-1601024445121-e5b82f020549?w=600&q=80&fit=crop",
    badge: "인기",
  },
  {
    name: "속리산 가이드 트레킹",
    region: "충북 보은",
    category: "자연탐방",
    price: 35000,
    duration: "약 5시간",
    rating: 4.8,
    reviews: 187,
    img: "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=600&q=80&fit=crop",
    badge: "추천",
  },
  {
    name: "법주사 문화유산 해설 투어",
    region: "충북 보은",
    category: "문화유산",
    price: 15000,
    duration: "약 2시간",
    rating: 4.7,
    reviews: 243,
    img: "https://images.unsplash.com/photo-1548115184-bc6544d06a58?w=600&q=80&fit=crop",
    badge: "",
  },
  {
    name: "청주 한과 만들기 체험",
    region: "충북 청주",
    category: "음식체험",
    price: 25000,
    duration: "약 1.5시간",
    rating: 4.6,
    reviews: 98,
    img: "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=600&q=80&fit=crop",
    badge: "",
  },
  {
    name: "충주호 유람선 투어",
    region: "충북 충주",
    category: "자연탐방",
    price: 18000,
    duration: "약 1시간",
    rating: 4.5,
    reviews: 156,
    img: "https://images.unsplash.com/photo-1488590528505-98d2b5aba04b?w=600&q=80&fit=crop&auto=format",
    badge: "",
  },
  {
    name: "괴산 산막이옛길 트레킹",
    region: "충북 괴산",
    category: "자연탐방",
    price: 20000,
    duration: "약 3시간",
    rating: 4.8,
    reviews: 201,
    img: "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=600&q=80&fit=crop",
    badge: "추천",
  },
];
