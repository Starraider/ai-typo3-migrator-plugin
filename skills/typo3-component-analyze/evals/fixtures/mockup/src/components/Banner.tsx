// Full-width promo banner; background image is remote and may be unreachable.
export function Banner({ headline }: { headline: string }) {
  return (
    <section className="w-full bg-[url('https://cdn.example.invalid/banner-bg.jpg')] py-[var(--section-space)]">
      <h2>{headline}</h2>
      <img src="/assets/missing-badge.svg" alt="" />
    </section>
  );
}
