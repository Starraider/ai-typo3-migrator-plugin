import { useEffect, useState } from "react";

export function Carousel({ slides }: { slides: { src: string; caption: string }[] }) {
  const [i, setI] = useState(0);
  // Auto-advance exists, but it is unclear whether it stops on hover/focus
  // and whether the last slide loops to the first.
  useEffect(() => {
    const t = setInterval(() => setI((n) => Math.min(n + 1, slides.length - 1)), 5000);
    return () => clearInterval(t);
  }, [slides.length]);
  return (
    <section aria-roledescription="carousel">
      <img src={slides[i].src} alt="" />
      <p>{slides[i].caption}</p>
      <button onClick={() => setI(i - 1)}>Prev</button>
      <button onClick={() => setI(i + 1)}>Next</button>
    </section>
  );
}
