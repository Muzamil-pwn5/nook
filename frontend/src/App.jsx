import { useEffect, useMemo, useRef, useState } from "react";
import { agentClient } from "./api/agentClient";
import { CATEGORY_NAMES, DEMO_MESSAGES, DEMO_PRODUCTS } from "./data/demoData";
import { Icon } from "./components/Icons";
import "./index.css";

const categories = ["All pieces", ...CATEGORY_NAMES];
const faqItems = [
  ["Can I ask for a specific colour or size?", "Yes. Tell the concierge what you have in mind and it can narrow the collection by category, colour, size, price, and availability."],
  ["Is the collection available in real time?", "The concierge checks the connected catalogue before it recommends or prepares an order. It will never present a made-up availability as confirmed."],
  ["What happens when I add something to my bag?", "Your bag is a private shortlist for this visit. You can review it with the concierge before any order is prepared."],
  ["Do you keep my conversation?", "The conversation is held in a temporary session so the concierge can understand follow-up questions. Operational details stay behind the interface."],
  ["Can I speak to a person?", "The collection is designed to start with a useful first edit. If you need a human follow-up, use the contact links below."],
];

function money(value) {
  return new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 }).format(value);
}

function useReveal(key) {
  useEffect(() => {
    const items = document.querySelectorAll(".reveal");
    const observer = new IntersectionObserver((entries) => entries.forEach((entry) => entry.isIntersecting && entry.target.classList.add("is-visible")), { threshold: 0.12, rootMargin: "0px 0px -8% 0px" });
    items.forEach((item) => observer.observe(item));
    return () => observer.disconnect();
  }, [key]);
}

function Wordmark({ light = false }) {
  return <button className={`wordmark ${light ? "wordmark--light" : ""}`} onClick={() => window.scrollTo({ top: 0, behavior: "smooth" })} aria-label="Morrow & Form home">
    <svg className="wordmark__mark" viewBox="0 0 28 28" aria-hidden="true"><path d="M5 20V8l6 7 6-7v12M17 8l6 4v8" /></svg>
    <span>Morrow <em>&</em> Form</span>
  </button>;
}

function Header({ view, setView, bagCount, onConcierge }) {
  const [scrolled, setScrolled] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);
  useEffect(() => {
    const update = () => setScrolled(window.scrollY > 20);
    update();
    window.addEventListener("scroll", update, { passive: true });
    return () => window.removeEventListener("scroll", update);
  }, []);
  const go = (id) => { setMenuOpen(false); document.getElementById(id)?.scrollIntoView({ behavior: "smooth" }); };
  const home = () => { setMenuOpen(false); setView("home"); window.scrollTo({ top: 0, behavior: "smooth" }); };
  return <>
    <header className={`site-header ${scrolled ? "is-scrolled" : ""}`}>
      <Wordmark />
      <nav className="site-nav" aria-label="Primary navigation">
        <button className={view === "home" ? "is-active" : ""} onClick={home}>Index</button>
        <button className={view === "catalog" ? "is-active" : ""} onClick={() => { setView("catalog"); setMenuOpen(false); window.scrollTo({ top: 0, behavior: "smooth" }); }}>Objects</button>
        <button onClick={() => go("point-of-view")}>Point of view</button>
        <button onClick={() => go("faq")}>FAQ</button>
      </nav>
      <div className="header-actions">
        <button className="concierge-link" onClick={onConcierge}><span className="status-pip" /> Personal edit</button>
        <button className="bag-button" aria-label={`Open bag, ${bagCount} items`}><span>Bag</span><b>{String(bagCount).padStart(2, "0")}</b></button>
        <button className={`mobile-nav ${menuOpen ? "is-open" : ""}`} onClick={() => setMenuOpen((open) => !open)} aria-label={menuOpen ? "Close navigation" : "Open navigation"} aria-expanded={menuOpen}><span /><span /></button>
      </div>
    </header>
    {menuOpen && <div className="mobile-menu"><button onClick={home}>Index</button><button onClick={() => { setView("catalog"); setMenuOpen(false); window.scrollTo({ top: 0, behavior: "smooth" }); }}>Objects</button><button onClick={() => go("point-of-view")}>Point of view</button><button onClick={() => go("faq")}>FAQ</button><button className="mobile-menu__cta" onClick={() => { setMenuOpen(false); onConcierge(); }}>Open personal edit <span>↗</span></button></div>}
  </>;
}

function ProductVisual({ product, large = false }) {
  return <div className={`product-visual ${large ? "product-visual--large" : ""}`}><img src={product.image} alt={`${product.name} product photograph`} loading={large ? "eager" : "lazy"} /><span className="product-visual__index">{String(product.id).padStart(2, "0")}</span><span className="product-visual__veil" /></div>;
}

function ProductCard({ product, index, onSelect, onAdd }) {
  return <article className="product-card reveal" style={{ "--delay": `${(index % 4) * 80}ms` }}>
    <button className="product-card__image" onClick={() => onSelect(product)} aria-label={`View ${product.name}`}><ProductVisual product={product} /><span className="card-hover">View piece <Icon name="arrow" size={14} /></span></button>
    <div className="product-card__meta"><div><span className="product-card__category">{product.category} / {product.material}</span><h3>{product.name}</h3></div><strong>{money(product.price)}</strong></div>
    <div className="product-card__foot"><span>{product.color} · {product.sizes?.join(" / ")}</span><button onClick={() => onAdd(product)} aria-label={`Add ${product.name} to bag`}><Icon name="plus" size={15} /></button></div>
  </article>;
}

function Concierge({ open, onClose, messages, input, setInput, onSend, busy, connection }) {
  if (!open) return null;
  return <div className="concierge-drawer" role="dialog" aria-modal="true" aria-label="Morrow personal edit">
    <div className="drawer__veil" onClick={onClose} />
    <aside className="drawer__panel">
      <div className="drawer__head"><div><span className="kicker">MORROW / PERSONAL EDIT</span><h2>A second opinion.</h2></div><button className="drawer-close" onClick={onClose} aria-label="Close concierge">×</button></div>
      <p className="drawer__intro">Tell us what you are looking for. The edit can search the collection, check availability, and prepare a considered order for your approval.</p>
      <div className="drawer__status"><span className="status-pip" /> {connection === "live" ? "Available now" : connection === "offline" ? "Temporarily unavailable" : "Finding the collection"}</div>
      <div className="drawer__messages">{messages.map((message) => <div key={message.id} className={`drawer-message drawer-message--${message.role}`}><span>{message.role === "assistant" ? "M" : "You"}</span><p>{message.text}</p></div>)}{busy && <div className="drawer-message drawer-message--assistant"><span>M</span><p className="typing"><i /><i /><i /></p></div>}</div>
      <div className="drawer__suggestions"><button onClick={() => setInput("Find me something for a long day")}>For a long day</button><button onClick={() => setInput("Show me something under $300")}>Under $300</button></div>
      <form className="drawer__composer" onSubmit={(event) => { event.preventDefault(); onSend(); }}><input value={input} onChange={(event) => setInput(event.target.value)} placeholder="Ask about the collection…" aria-label="Ask the personal edit" /><button disabled={!input.trim() || busy} aria-label="Send"><Icon name="arrow" size={16} /></button></form>
    </aside>
  </div>;
}

function ProductModal({ product, onClose, onAdd }) {
  if (!product) return null;
  return <div className="product-modal" role="dialog" aria-modal="true" aria-label={product.name}><div className="modal__veil" onClick={onClose} /><div className="modal__panel"><button className="drawer-close" onClick={onClose} aria-label="Close product">×</button><div className="modal__visual"><ProductVisual product={product} large /></div><div className="modal__copy"><span className="kicker">OBJECT {String(product.id).padStart(2, "0")} / {product.category}</span><h2>{product.name}</h2><p className="modal__tagline">{product.tagline}</p><p>{product.description}</p><dl><div><dt>Material</dt><dd>{product.material}</dd></div><div><dt>Availability</dt><dd>{product.stock_quantity > 5 ? "In the studio" : "Few remaining"}</dd></div><div><dt>Edition</dt><dd>{product.edition}</dd></div><div><dt>Colour</dt><dd>{product.colors?.join(" / ")}</dd></div><div><dt>Sizes</dt><dd>{product.sizes?.join(" / ")}</dd></div></dl><div className="modal__buy"><strong>{money(product.price)}</strong><button className="button button--dark" onClick={() => { onAdd(product); onClose(); }}>Add to bag <Icon name="arrow" size={15} /></button></div></div></div></div>;
}

function Hero({ onExplore, onConcierge }) {
  const art = useRef(null);
  const move = (event) => { const rect = art.current?.getBoundingClientRect(); if (!rect) return; const x = ((event.clientX - rect.left) / rect.width - .5) * 2; const y = ((event.clientY - rect.top) / rect.height - .5) * 2; art.current.style.setProperty("--mx", `${x * 8}deg`); art.current.style.setProperty("--my", `${y * -8}deg`); art.current.style.setProperty("--px", `${x * 18}px`); art.current.style.setProperty("--py", `${y * 18}px`); };
  const leave = () => { if (!art.current) return; ["--mx", "--my", "--px", "--py"].forEach((name, index) => art.current.style.setProperty(name, ["0deg", "0deg", "0px", "0px"][index])); };
  return <section className="hero" onMouseMove={move} onMouseLeave={leave}>
    <div className="hero__grid" aria-hidden="true" /><div className="hero__copy"><span className="hero__badge"><span className="status-pip" /> Live collection / 2026</span><h1>Things worth<br /><i>keeping close.</i></h1><p>A quieter way to find what fits. Clothing, fragrance, and small objects chosen for the life around them.</p><div className="hero__actions"><button className="button button--light" onClick={onExplore}>Browse the edit <Icon name="arrow" size={15} /></button><button className="link-button" onClick={onConcierge}>Ask for a direction <span>↗</span></button></div></div>
    <div className="hero__stage" ref={art}><div className="hero__halo" /><img src="/hero-object.svg" alt="Abstract sculptural object from the Morrow and Form collection" className="hero__object" /><span className="hero__note hero__note--top">A study in<br />useful beauty</span><span className="hero__note hero__note--bottom">Move through<br />the collection</span><span className="hero__crosshair" /></div>
    <div className="hero__foot"><span>Scroll to wander</span><span className="scroll-line" /><span>01 / 04</span></div>
  </section>;
}

function IntroSection() {
  return <section id="point-of-view" className="statement reveal"><div className="statement__label"><span className="kicker">POINT OF VIEW</span><span className="statement__line" /></div><p>We believe the things around us should do more than perform. They should <em>change the temperature of a room,</em> make a ritual feel deliberate, and earn their place over time.</p></section>;
}

function FAQSection() {
  const [open, setOpen] = useState(0);
  return <section id="faq" className="faq-section"><div className="faq-heading reveal"><span className="kicker">THE SHORT ANSWER</span><h2>Good to know.</h2></div><div className="faq-list reveal">{faqItems.map(([question, answer], index) => <div className={`faq-item ${open === index ? "is-open" : ""}`} key={question}><button onClick={() => setOpen(open === index ? -1 : index)} aria-expanded={open === index}><span>{question}</span><i /></button><div className="faq-answer"><p>{answer}</p></div></div>)}</div></section>;
}

function Footer({ onConcierge }) {
  return <footer id="contact" className="site-footer"><div className="footer__cta reveal"><span className="kicker">WHEN YOU NEED A STARTING POINT</span><h2>Let’s find the<br /><i>right direction.</i></h2><button className="button button--light" onClick={onConcierge}>Open the personal edit <Icon name="arrow" size={15} /></button></div><div className="footer__grid"><div><Wordmark light /><p>Considered things for an intentional life.</p></div><div><span className="footer__label">Explore</span><a href="#point-of-view">Point of view</a><a href="#objects">The collection</a><a href="#faq">FAQ</a></div><div><span className="footer__label">Connect</span><a href="mailto:hello@morrowandform.com">Email</a><a href="#contact">Instagram</a><a href="#contact">Journal</a></div><div><span className="footer__label">A note</span><p>Useful, not noisy.<br />Always a little considered.</p></div></div><div className="footer__bottom"><span>© 2026 Morrow & Form</span><span>Made for the things that stay.</span></div></footer>;
}

function App() {
  const [view, setView] = useState("home");
  const [products] = useState(DEMO_PRODUCTS);
  const [filter, setFilter] = useState("All pieces");
  const [query, setQuery] = useState("");
  const [selected, setSelected] = useState(null);
  const [bag, setBag] = useState([]);
  const [conciergeOpen, setConciergeOpen] = useState(false);
  const [messages, setMessages] = useState(DEMO_MESSAGES);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const [connection, setConnection] = useState("demo");
  const [sessionId, setSessionId] = useState(null);
  const [scrollProgress, setScrollProgress] = useState(0);
  useReveal(`${view}-${products.length}`);
  useEffect(() => {
    let frame = 0;
    const updateProgress = () => { cancelAnimationFrame(frame); frame = requestAnimationFrame(() => { const max = document.documentElement.scrollHeight - window.innerHeight; setScrollProgress(max > 0 ? (window.scrollY / max) * 100 : 0); }); };
    updateProgress(); window.addEventListener("scroll", updateProgress, { passive: true }); window.addEventListener("resize", updateProgress);
    return () => { cancelAnimationFrame(frame); window.removeEventListener("scroll", updateProgress); window.removeEventListener("resize", updateProgress); };
  }, []);
  useEffect(() => {
    let active = true;
    Promise.all([agentClient.health(), agentClient.createSession()]).then(([, session]) => { if (!active) return; setSessionId(session.session_id); setConnection("live"); }).catch(() => { if (active) setConnection("offline"); });
    return () => { active = false; };
  }, []);
  const filtered = useMemo(() => products.filter((product) => { const haystack = `${product.name} ${product.category} ${product.color} ${product.material} ${product.sizes?.join(" ")}`.toLowerCase(); return (filter === "All pieces" || product.category === filter) && (!query.trim() || haystack.includes(query.toLowerCase().trim())); }), [filter, products, query]);
  const featuredProducts = useMemo(() => ["Dresses", "Shoes", "Perfume", "Bags"].map((category) => products.find((product) => product.category === category)).filter(Boolean), [products]);
  const addToBag = (product) => setBag((items) => [...items, product]);
  const explore = () => { setView("catalog"); setTimeout(() => document.getElementById("objects")?.scrollIntoView({ behavior: "smooth" }), 50); };
  const sendMessage = async () => {
    const text = input.trim(); if (!text || busy) return; setInput(""); setMessages((items) => [...items, { id: `user-${Date.now()}`, role: "user", text, time: "now" }]); setBusy(true);
    try {
      if (!sessionId) throw new Error("The personal edit is still connecting.");
      const result = await agentClient.chat(sessionId, text); setConnection(result?.agent === "llm" ? "live" : "offline");
      const responseText = result?.response && result?.type !== "provider_unavailable" ? result.response : result?.type === "provider_unavailable" ? "The personal edit is unavailable right now. Please try again in a moment." : result?.type === "approval_required" ? "I’ve prepared that request and kept the operational details private. If you’d like me to continue, say so and I’ll take the next step." : "I’m still considering the best direction. Tell me a little more about what you need.";
      setMessages((items) => [...items, { id: `assistant-${Date.now()}`, role: "assistant", text: responseText, time: "now" }]);
    } catch { setMessages((items) => [...items, { id: `assistant-${Date.now()}`, role: "assistant", text: "I’m having trouble reaching the personal edit right now. Please try again in a moment.", time: "now" }]); } finally { setBusy(false); }
  };
  return <div className="storefront"><div className="scroll-progress" style={{ "--progress": `${scrollProgress}%` }} /><Header view={view} setView={setView} bagCount={bag.length} onConcierge={() => setConciergeOpen(true)} />
    {view === "home" ? <main><Hero onExplore={explore} onConcierge={() => setConciergeOpen(true)} /><IntroSection /><section id="objects" className="featured-section"><div className="section-heading reveal"><div><span className="kicker">THE EDIT / FOUR PIECES</span><h2>Wear the good<br /><i>often.</i></h2></div><button className="link-button" onClick={() => setView("catalog")}>See the full edit <span>↗</span></button></div><div className="featured-grid">{featuredProducts.map((product, index) => <ProductCard key={product.id} product={product} index={index} onSelect={setSelected} onAdd={addToBag} />)}</div></section><section className="marquee-section" aria-label="Collection principles"><div className="marquee"><span>USEFUL BEAUTY</span><i>✦</i><span>QUIET INSISTENCE</span><i>✦</i><span>OBJECTS WITH INTENT</span><i>✦</i><span>USEFUL BEAUTY</span><i>✦</i><span>QUIET INSISTENCE</span><i>✦</i></div></section><section className="concierge-banner reveal"><div><span className="kicker">A LITTLE HELP, WHEN NEEDED</span><h2>Not sure where<br />to begin?</h2></div><div><p>Describe the mood, the room, or the ritual. The personal edit will make the first move.</p><button className="button button--dark" onClick={() => setConciergeOpen(true)}>Start a conversation <Icon name="arrow" size={15} /></button></div></section><FAQSection /></main> : <main className="catalog-page"><section className="catalog-hero"><span className="kicker">THE COMPLETE COLLECTION / {products.length} PIECES</span><h1>Find your<br /><i>everyday extraordinary.</i></h1><p>Clothing, fragrance and considered accessories chosen for the way they move with you and live in the room.</p></section><section id="objects" className="catalog-list"><div className="filter-row"><label className="catalog-search"><Icon name="search" size={14} /><input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search colour, size, category…" aria-label="Search catalogue" /></label>{categories.map((category) => <button key={category} className={filter === category ? "is-active" : ""} onClick={() => setFilter(category)}>{category}</button>)}<span className="filter-count">{filtered.length} objects</span></div><div className="catalog-grid">{filtered.map((product, index) => <ProductCard key={product.id} product={product} index={index} onSelect={setSelected} onAdd={addToBag} />)}</div></section></main>}
    <Footer onConcierge={() => setConciergeOpen(true)} /><Concierge open={conciergeOpen} onClose={() => setConciergeOpen(false)} messages={messages} input={input} setInput={setInput} onSend={sendMessage} busy={busy} connection={connection} /><ProductModal product={selected} onClose={() => setSelected(null)} onAdd={addToBag} />
    {bag.length > 0 && <div className="bag-toast"><span><b>{bag.length}</b> piece{bag.length > 1 ? "s" : ""} in your bag</span><button onClick={() => setConciergeOpen(true)}>Review with personal edit <Icon name="arrow" size={14} /></button></div>}
  </div>;
}

export default App;
