export function FullWidthHero({ title, subtitle, cta }: { title: string; subtitle?: string; cta?: { label: string; href: string } }) {
  return (
    <section className="w-full bg-[var(--accent)] text-white py-[var(--section-space)]">
      <div className="mx-auto max-w-6xl">
        <h1>{title}</h1>
        {subtitle && <p>{subtitle}</p>}
        {cta && <a href={cta.href}>{cta.label}</a>}
      </div>
    </section>
  );
}
