import { Card } from "../components/Card";

// Composite section: full-width background, three identical Card children,
// one column below 768px, three columns from lg.
export function CardGrid({ cards }: { cards: React.ComponentProps<typeof Card>[] }) {
  return (
    <section className="w-full bg-slate-50 py-[var(--section-space)]">
      <div className="mx-auto grid max-w-6xl gap-6 md:grid-cols-2 lg:grid-cols-3">
        {cards.slice(0, 3).map((c) => <Card key={c.title} {...c} />)}
      </div>
    </section>
  );
}
