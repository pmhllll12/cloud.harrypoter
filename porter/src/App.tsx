import { useState } from "react";
import "./App.css";
import MapPage from "./MapPage";
import StorePage from "./StorePage";

type Page = "landing" | "map" | "store";

export default function App() {
  const [page, setPage] = useState<Page>("landing");

  if (page === "map") return <MapPage onNavigate={setPage} />;
  if (page === "store") return <StorePage onNavigate={setPage} />;

  return (
    <section className="landing">
      <nav className="navbar">
        <div className="nav-left">
          <div className="nav-brand">
            <div className="nav-logo-circle">
              <span className="nav-logo-text">A</span>
            </div>
            <span className="nav-brand-name">dapter4</span>
          </div>
          <div className="nav-links">
            <a href="#">관광정보</a>
            <a href="#">관광동선</a>
            <a onClick={() => setPage("map")} style={{ cursor: "pointer" }}>지도</a>
            <a onClick={() => setPage("store")} style={{ cursor: "pointer" }}>스토어</a>
            <a href="#">티켓</a>
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
          충북 관광을<br />
          AI와 함께 탐험하세요
        </h1>
        <p className="landing-sub">
          청주부터 단양까지, AI가 충북의 자연과 문화유산을 생생하게 안내합니다
        </p>
        <a href="#" className="landing-cta">충북 AI</a>
      </div>
    </section>
  );
}
