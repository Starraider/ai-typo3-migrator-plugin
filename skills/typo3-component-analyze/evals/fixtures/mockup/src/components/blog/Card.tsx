// A second, unrelated "Card" (blog teaser) used on /blog.
export function Card({ title, date }: { title: string; date: string }) {
  return (
    <article className="teaser">
      <time dateTime={date}>{date}</time>
      <h3>{title}</h3>
    </article>
  );
}
