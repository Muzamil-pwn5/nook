import { useEffect, useMemo, useRef, useState } from "react";
import { agentClient } from "./api/agentClient";
import { CATEGORY_NAMES, DEMO_MESSAGES, DEMO_PRODUCTS } from "./data/demoData";
import { Icon } from "./components/Icons";
import "./index.css";

const categories = ["All pieces", ...CATEGORY_NAMES];

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

function Wordmark() {
  return <button className="wordmark" onClick={() => window.scrollTo({ top: 0, behavior: "smooth" })} aria-label="Morrow & Form home"><span className="wordmark__mark">M</span><span>Morrow <em>&</em> Form</span></button>;
}

function Header({ view, setView, bagCount, onConcierge }) {
  return <header className="site-header">
    <Wordmark />
    <nav className="site-nav" aria-label="Primary navigation">
      <button className={view === "home" ? "is-active" : ""} onClick={() => { setView("home"); window.scrollTo({ top: 0, behavior: "smooth" }); }}>Index</button>
      <button className={view === "catalog" ? "is-active" : ""} onClick={() => { setView("catalog"); window.scrollTo({ top: 0, behavior: "smooth" }); }}>Objects</button>
      <button onClick={() => document.getElementById("point-of-view")?.scrollIntoView({ behavior: "smooth" })}>Point of view</button>
    </nav>
    <div className="header-actions">
      <button className="concierge-link" onClick={onConcierge}><span className="status-pip" /> Concierge</button>
      <button className="bag-button" aria-label={`Open bag, ${bagCount} items`}><span>Bag</span><b>{String(bagCount).padStart(2, "0")}</b></button>
      <button className="mobile-nav" aria-label="Open navigation"><Icon name="menu" size={19} /></button>
    </div>
  </header>;
}

function ProductVisual({ product, large = false }) {
  return <div className={`product-visual ${large ? "product-visual--large" : ""}`}><img src={product.image} alt={`${product.name} product photograph`} loading={large ? "eager" : "lazy"} /><span className="product-visual__index">{String(product.id).padStart(2, "0")}</span></div>;
}

function ProductCard({ product, index, onSelect, onAdd }) {
  return <article className="product-card reveal" style={{ "--delay": `${(index % 4) * 80}ms` }}>
    <button className="product-card__image" onClick={() => onSelect(product)} aria-label={`View ${product.name}`}><ProductVisual product={product} /><span className="card-hover">View object <Icon name="arrow" size={14} /></span></button>
    <div className="product-card__meta"><div><span className="product-card__category">{product.category} / {product.material}</span><h3>{product.name}</h3></div><strong>{money(product.price)}</strong></div>
    <div className="product-card__foot"><span>{product.color} · {product.sizes?.join(" / ")}</span><button onClick={() => onAdd(product)} aria-label={`Add ${product.name} to bag`}><Icon name="plus" size={15} /></button></div>
  </article>;
}

function Concierge({ open, onClose, messages, input, setInput, onSend, busy, connection }) {
  if (!open) return null;
  return <div className="concierge-drawer" role="dialog" aria-modal="true" aria-label="Morrow concierge">
    <div className="drawer__veil" onClick={onClose} />
    <aside className="drawer__panel">
      <div className="drawer__head"><div><span className="kicker">MORROW CONCIERGE</span><h2>A second opinion.</h2></div><button className="drawer-close" onClick={onClose} aria-label="Close concierge">×</button></div>
      <p className="drawer__intro">Tell us what you are looking for. The concierge can search the collection, check availability, and prepare a considered order for your approval.</p>
      <div className="drawer__status"><span className="status-pip" /> {connection === "live" ? "Live AI concierge" : connection === "offline" ? "Concierge unavailable" : "Connecting to concierge"}</div>
      <div className="drawer__messages">{messages.map((message) => <div key={message.id} className={`drawer-message drawer-message--${message.role}`}><span>{message.role === "assistant" ? "M&F" : "You"}</span><p>{message.text}</p></div>)}{busy && <div className="drawer-message drawer-message--assistant"><span>M&F</span><p className="typing"><i /><i /><i /></p></div>}</div>
      <div className="drawer__suggestions"><button onClick={() => setInput("Find me a quiet object for my desk")}>For my desk</button><button onClick={() => setInput("Show me something under $300")}>Under $300</button></div>
      <form className="drawer__composer" onSubmit={(event) => { event.preventDefault(); onSend(); }}><input value={input} onChange={(event) => setInput(event.target.value)} placeholder="Ask the collection…" aria-label="Ask the concierge" /><button disabled={!input.trim() || busy} aria-label="Send"><Icon name="arrow" size={16} /></button></form>
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
  const leave = () => { if (!art.current) return; art.current.style.setProperty("--mx", "0deg"); art.current.style.setProperty("--my", "0deg"); art.current.style.setProperty("--px", "0px"); art.current.style.setProperty("--py", "0px"); };
  return <section className="hero" onMouseMove={move} onMouseLeave={leave}>
    <div className="hero__copy"><span className="kicker hero__kicker">THE COLLECTION / 01—26</span><h1>Objects that<br /><i>hold attention.</i></h1><p>A considered collection of tools for living, working, listening and looking. Selected for their quiet insistence.</p><div className="hero__actions"><button className="button button--dark" onClick={onExplore}>Enter the collection <Icon name="arrow" size={15} /></button><button className="link-button" onClick={onConcierge}>Ask the concierge <span>↗</span></button></div></div>
    <div className="hero__stage" ref={art}><div className="hero__halo" /><img src="/hero-object.svg" alt="Abstract sculptural object from the Morrow and Form collection" className="hero__object" /><span className="hero__note hero__note--top">A study in<br />useful beauty</span><span className="hero__note hero__note--bottom">Move your cursor<br />over the object</span><span className="hero__crosshair" /></div>
    <div className="hero__foot"><span>Scroll to wander</span><span className="scroll-line" /><span>01 / 04</span></div>
  </section>;
}

function IntroSection() {
  return <section id="point-of-view" className="statement reveal"><div className="statement__label"><span className="kicker">POINT OF VIEW</span><span className="statement__line" /></div><p>We believe the things around us should do more than perform. They should <em>change the temperature of a room,</em> make a ritual feel deliberate, and earn their place over time.</p></section>;
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
    const updateProgress = () => {
      cancelAnimationFrame(frame);
      frame = requestAnimationFrame(() => {
        const max = document.documentElement.scrollHeight - window.innerHeight;
        setScrollProgress(max > 0 ? (window.scrollY / max) * 100 : 0);
      });
    };
    updateProgress();
    window.addEventListener("scroll", updateProgress, { passive: true });
    window.addEventListener("resize", updateProgress);
    return () => { cancelAnimationFrame(frame); window.removeEventListener("scroll", updateProgress); window.removeEventListener("resize", updateProgress); };
  }, []);

  useEffect(() => {
    let active = true;
    Promise.all([agentClient.health(), agentClient.createSession()])
      .then(([, session]) => {
        if (!active) return;
        setSessionId(session.session_id);
        setConnection("live");
      })
      .catch(() => {
        if (active) setConnection("offline");
      });
    return () => { active = false; };
  }, []);
  const filtered = useMemo(() => products.filter((product) => { const haystack = `${product.name} ${product.category} ${product.color} ${product.material} ${product.sizes?.join(" ")}`.toLowerCase(); return (filter === "All pieces" || product.category === filter) && (!query.trim() || haystack.includes(query.toLowerCase().trim())); }), [filter, products, query]);
  const featuredProducts = useMemo(() => ["Dresses", "Shoes", "Perfume", "Bags"].map((category) => products.find((product) => product.category === category)).filter(Boolean), [products]);
  const addToBag = (product) => setBag((items) => [...items, product]);
  const explore = () => { setView("catalog"); setTimeout(() => document.getElementById("objects")?.scrollIntoView({ behavior: "smooth" }), 50); };
  const sendMessage = async () => {
    const text = input.trim();
    if (!text || busy) return;
    setInput("");
    setMessages((items) => [...items, { id: `user-${Date.now()}`, role: "user", text, time: "now" }]);
    setBusy(true);
    try {
      if (!sessionId) throw new Error("The concierge is still connecting.");
      const result = await agentClient.chat(sessionId, text);
      setConnection(result?.agent === "llm" ? "live" : "offline");
      const responseText = result?.response
        && result?.type !== "provider_unavailable"
        ? result.response
        : result?.type === "provider_unavailable"
          ? "The concierge is offline until a live AI provider is connected."
          : result?.type === "approval_required"
          ? "I’ve prepared that request and kept the operational details private. If you’d like me to continue, say so and I’ll take the next step."
          : "I’m still considering the best direction. Tell me a little more about what you need.";
      setMessages((items) => [...items, { id: `assistant-${Date.now()}`, role: "assistant", text: responseText, time: "now" }]);
    } catch {
      setMessages((items) => [...items, { id: `assistant-${Date.now()}`, role: "assistant", text: "I’m having trouble reaching the concierge right now. Please try again in a moment.", time: "now" }]);
    } finally {
      setBusy(false);
    }
  };
  return <div className="storefront"><div className="scroll-progress" style={{ "--progress": `${scrollProgress}%` }} /><Header view={view} setView={setView} bagCount={bag.length} onConcierge={() => setConciergeOpen(true)} />
    {view === "home" ? <main><Hero onExplore={explore} onConcierge={() => setConciergeOpen(true)} /><IntroSection /><section id="objects" className="featured-section"><div className="section-heading reveal"><div><span className="kicker">THE EDIT / 04 PIECES</span><h2>Wear the good<br /><i>often.</i></h2></div><button className="link-button" onClick={() => setView("catalog")}>See all objects <span>↗</span></button></div><div className="featured-grid">{featuredProducts.map((product, index) => <ProductCard key={product.id} product={product} index={index} onSelect={setSelected} onAdd={addToBag} />)}</div></section><section className="marquee-section" aria-hidden="true"><div className="marquee"><span>USEFUL BEAUTY</span><i>✦</i><span>QUIET INSISTENCE</span><i>✦</i><span>OBJECTS WITH INTENT</span><i>✦</i><span>USEFUL BEAUTY</span><i>✦</i></div></section><section className="concierge-banner reveal"><div><span className="kicker">A LITTLE HELP, WHEN NEEDED</span><h2>Not sure where<br />to begin?</h2></div><div><p>Describe the mood, the room, or the ritual. Our concierge will make the first edit.</p><button className="button button--dark" onClick={() => setConciergeOpen(true)}>Start a conversation <Icon name="arrow" size={15} /></button></div></section></main> : <main className="catalog-page"><section className="catalog-hero"><span className="kicker">THE COMPLETE COLLECTION / {products.length} PIECES</span><h1>Find your<br /><i>everyday extraordinary.</i></h1><p>Clothing, fragrance and considered accessories chosen for the way they move with you and live in the room.</p></section><section id="objects" className="catalog-list"><div className="filter-row"><label className="catalog-search"><Icon name="search" size={14} /><input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search colour, size, category…" aria-label="Search catalogue" /></label>{categories.map((category) => <button key={category} className={filter === category ? "is-active" : ""} onClick={() => setFilter(category)}>{category}</button>)}<span className="filter-count">{filtered.length} objects</span></div><div className="catalog-grid">{filtered.map((product, index) => <ProductCard key={product.id} product={product} index={index} onSelect={setSelected} onAdd={addToBag} />)}</div></section></main>}
    <footer className="site-footer"><Wordmark /><span>Objects for a more intentional life.</span><span>© 2026 Morrow & Form</span></footer>
    <Concierge open={conciergeOpen} onClose={() => setConciergeOpen(false)} messages={messages} input={input} setInput={setInput} onSend={sendMessage} busy={busy} connection={connection} />
    <ProductModal product={selected} onClose={() => setSelected(null)} onAdd={addToBag} />
    {bag.length > 0 && <div className="bag-toast"><span><b>{bag.length}</b> piece{bag.length > 1 ? "s" : ""} in your bag</span><button onClick={() => setConciergeOpen(true)}>Review with concierge <Icon name="arrow" size={14} /></button></div>}
  </div>;
}

export default App;
