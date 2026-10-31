type Props = {
  layout?: "vertical" | "horizontal" | "featured";
  title: string;
  image: { src: string; alt?: string };
  badge?: string;
  text?: string;
  actions?: { label: string; href: string }[]; // up to 3
};

export function Card({ layout = "vertical", title, image, badge, text, actions = [] }: Props) {
  // horizontal places the image beside the text from md (768px) upward
  const dir = layout === "horizontal" ? "flex-col md:flex-row" : "flex-col";
  return (
    <article className={`card card--${layout} flex ${dir} rounded-[var(--radius-card)] hover:shadow-lg`}>
      <img src={image.src} alt={image.alt ?? ""} className="aspect-video object-cover" />
      <div className="p-6">
        {badge && <span className="badge">{badge}</span>}
        <h3>{title}</h3>
        {text && <p>{text}</p>}
        <div className="flex gap-2">
          {actions.slice(0, 3).map((a) => (
            <a key={a.href} href={a.href} className="focus-visible:ring-2">{a.label}</a>
          ))}
        </div>
      </div>
    </article>
  );
}
