import { useState } from "react";
import "./App.css";
import MapPage from "./MapPage";
import StorePage from "./StorePage";
import TourInfoPage from "./TourInfoPage";
import TicketPage from "./TicketPage";
import SplashScreen from "./SplashScreen";

type Page = "landing" | "map" | "store" | "tourinfo" | "ticket";

export default function App() {
  const [page, setPage] = useState<Page>("landing");
  const [introPlaying, setIntroPlaying] = useState(false);

  if (page === "map") return <MapPage onNavigate={setPage} />;
  if (page === "store") return <StorePage onNavigate={setPage} />;
  if (page === "tourinfo") return <TourInfoPage onNavigate={setPage} />;
  if (page === "ticket") return <TicketPage onNavigate={setPage} />;

  return (
    <section className={`landing ${introPlaying ? "landing--intro" : ""}`}>
      <nav className="navbar">
        <div className="nav-left">
          <div className="nav-brand">
            <div className="nav-logo-circle">
              <span className="nav-logo-text">A</span>
            </div>
            <span className="nav-brand-name">dapter4</span>
          </div>
          <div className="nav-links">
            <a onClick={() => setPage("map")} style={{ cursor: "pointer" }}>관광동선</a>
            <a onClick={() => setPage("store")} style={{ cursor: "pointer" }}>스토어</a>
            <a onClick={() => setPage("ticket")} style={{ cursor: "pointer" }}>티켓</a>
          </div>
        </div>
        <div className="nav-actions" />
      </nav>

      <div className="landing-visual" aria-hidden="true">
        <img className="palace-img" src="/palace.jpg" alt="" />
        <div className="palace-mask" />
      </div>

      <div className="landing-text">
        <h1 className="landing-title">
          대한민국 구석구석을<br />
          AI와 함께 탐험하세요
        </h1>
        <p className="landing-sub">
          서울부터 제주까지, AI가 전국의 자연과 문화유산을 생생하게 안내합니다
        </p>
        <a href="#" className="landing-cta">AI와 대화하기</a>
      </div>

      {introPlaying && (
        <SplashScreen onDone={() => setIntroPlaying(false)} />
      )}
    </section>
  );
}
