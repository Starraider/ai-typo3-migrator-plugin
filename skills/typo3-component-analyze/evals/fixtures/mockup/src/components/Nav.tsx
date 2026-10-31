import { useState } from "react";
import { pages } from "../data/pages"; // site hierarchy: 4 top-level pages, 2 levels

export function Nav() {
  const [open, setOpen] = useState(false);
  const active = window.location.pathname;
  return (
    <header className="sticky top-0">
      <a href="/"><img src="/logo.svg" alt="Acme" /></a>
      <button className="lg:hidden" aria-expanded={open} onClick={() => setOpen(!open)}>Menu</button>
      <nav className={open ? "block" : "hidden lg:flex"} aria-label="Main">
        {pages.map((p) => (
          <div key={p.path} aria-current={active === p.path ? "page" : undefined}>
            <a href={p.path}>{p.title}</a>
            {p.children?.map((c) => <a key={c.path} href={c.path}>{c.title}</a>)}
          </div>
        ))}
      </nav>
    </header>
  );
}
