import { useEffect, useRef, useState } from "react";
import lottie from "lottie-web";
import "./SplashScreen.css";

interface Props {
  onDone: () => void;
}

const END_FRAME = 240; // 4초 (60fps)

export default function SplashScreen({ onDone }: Props) {
  const ref = useRef<HTMLDivElement>(null);
  const [fading, setFading] = useState(false);

  useEffect(() => {
    if (!ref.current) return;

    const anim = lottie.loadAnimation({
      container: ref.current,
      renderer: "svg",
      loop: false,
      autoplay: false,
      path: "/lottie-preview.json",
    });

    anim.addEventListener("DOMLoaded", () => {
      anim.playSegments([0, END_FRAME], true);
    });

    anim.addEventListener("complete", () => {
      setFading(true);
      // 페이드아웃 후 palace-img 줌아웃과 글자 등장
      setTimeout(onDone, 800);
    });

    return () => anim.destroy();
  }, [onDone]);

  return (
    <div className={`splash-overlay ${fading ? "splash-overlay--out" : ""}`}>
      <div ref={ref} className="splash-lottie-player" />
    </div>
  );
}
