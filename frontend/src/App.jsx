import { useState } from "react";
import "./index.css";

const navItems = ["Platform", "Products", "Solutions", "Resources", "Pricing"];
const customerLogos = ["SIEMENS", "GitHub", "Uber", "box", "vimeo", "LUSH", "TESCO", "Discord"];

function Arrow({ direction = "right" }) {
  return <span className={`arrow arrow-${direction}`} aria-hidden="true">→</span>;
}

function ZendeskMark({ light = false }) {
  return <span className={`zendesk-mark ${light ? "is-light" : ""}`} aria-hidden="true"><i /><b /><em /></span>;
}

function App() {
  const [bannerVisible, setBannerVisible] = useState(true);
  const [menuOpen, setMenuOpen] = useState(false);
  const [email, setEmail] = useState("");
  const [submitted, setSubmitted] = useState(false);
  const [chatOpen, setChatOpen] = useState(false);

  const submitEmail = (event) => {
    event.preventDefault();
    if (email.trim()) setSubmitted(true);
  };

  return (
    <div className="site-shell">
      {bannerVisible && <div className="summit-banner"><div><strong>AI Summit 2026</strong><span>Join 30,000+ service leaders online at AI Summit 2026 to learn how to turn AI ambition into real results.</span><a href="#form">Register now</a></div><button className="banner-close" onClick={() => setBannerVisible(false)} aria-label="Close announcement">×</button></div>}

      <header className="site-header">
        <a className="wordmark" href="#top" aria-label="Zendesk home"><ZendeskMark /><span>zendesk</span></a>
        <nav className={`main-nav ${menuOpen ? "is-open" : ""}`} aria-label="Primary navigation">
          {navItems.map((item) => <a href={`#${item.toLowerCase()}`} key={item}>{item}<span className="chevron">⌄</span></a>)}
        </nav>
        <div className="header-tools"><div className="utility-links"><a href="#signin">♙&nbsp; Sign in</a><a href="#contact">⌕&nbsp; Contact us</a><a href="#language">◎&nbsp; Language</a></div><div className="header-buttons"><a className="button button-lime button-small" href="#form">Try for free</a><a className="button button-outline button-small" href="#demo">View demo</a></div></div>
        <button className="menu-toggle" onClick={() => setMenuOpen((open) => !open)} aria-label="Toggle navigation"><span /><span /><span /></button>
      </header>

      <main id="top">
        <section className="hero-section" id="platform">
          <div className="hero-image" />
          <div className="hero-overlay" />
          <div className="hero-content"><p className="eyebrow eyebrow-light">AI-POWERED CUSTOMER SERVICE PLATFORM</p><h1>Automate up to 80%<br />of interactions with<br />Zendesk AI agents.</h1><p className="hero-copy">Built to improve with every resolution. Proven across 4.8B+ resolutions.</p><p className="trial-note"><span>●</span><strong>14-day free trial.</strong> No credit card required.</p><form className="hero-form" id="form" onSubmit={submitEmail}>{submitted ? <div className="form-success">Thanks — we’ll be in touch.</div> : <><input aria-label="Work email" type="email" required value={email} onChange={(event) => setEmail(event.target.value)} placeholder="Enter work email" /><button className="button button-lime" type="submit">Try for free</button></>}</form></div><button className="pause-button" aria-label="Pause hero animation">Ⅱ</button>
        </section>

        <section className="logo-strip" aria-label="Customers"><p>22,000+ SERVICE TEAMS TRUST ZENDESK AI</p><div>{customerLogos.map((logo) => <span className={`customer-logo logo-${logo.toLowerCase()}`} key={logo}>{logo}</span>)}</div></section>

        <section className="signal-section" id="solutions"><p className="eyebrow">ZENDESK AI</p><h2>AI that gets <span>smarter</span> with every resolution.</h2><p className="section-copy">Achieve up to 80% automation with AI Agents that continuously learn from every interaction, handle<br className="desktop-only" /> more complex workflows, and deliver better outcomes.</p><a className="button button-lime" href="#form">Explore the platform</a><div className="signal-stack"><div className="signal-line" /><article><strong>Every conversation<br />becomes a learning signal</strong></article><article className="signal-highlight"><strong>Zendesk AI turns signals into improvement</strong></article><article><strong>Faster resolutions. Stronger<br />loyalty. Better outcomes.</strong></article></div></section>

        <section className="metrics-section"><p>Trillions of data points turned into billions of successful<br className="desktop-only" /> outcomes.</p><div className="metrics"><div><strong>22K<span>+</span></strong><small>AI customers</small></div><div><strong>830M</strong><small>AI interactions</small></div><div><strong>4.8B</strong><small>Resolutions delivered</small></div></div></section>

        <section className="agents-section" id="products"><div className="agents-copy"><p className="eyebrow">ZENDESK + FORETHOUGHT <mark>NEW</mark></p><h2>Standalone AI agents for any platform</h2><p>Deploy self-improving AI Agents in Zendesk or your existing service platform. Every resolution helps improve performance over time, without requiring you to switch your service stack.</p><div className="button-row"><a className="button button-lime" href="#demo">Request Forethought demo</a><a className="button button-outline" href="#learn">Learn more</a></div></div><div className="brand-card"><div><ZendeskMark light /><span>zendesk</span></div><i /><div className="forethought-logo"><b>ℱ</b><span>Forethought</span></div></div></section>

        <section className="partnership-section"><div className="warriors-badge">◉<small>Official Partner of the<br /><b>Golden State Warriors</b></small></div><div className="partnership-copy">Zendesk’s partnership with the Golden State Warriors, Valkyries, and Chase Center is helping reshape the fan experience.</div><a className="button button-lime" href="#learn">Find out how</a></section>

        <section className="bottom-cta" id="resources"><h2>Designed for AI-first customer service</h2><p>Give every team the intelligence to make service feel effortless.</p><a className="button button-lime" href="#form">See what’s possible <Arrow /></a></section>
      </main>

      <button className={`chat-button ${chatOpen ? "is-open" : ""}`} onClick={() => setChatOpen((open) => !open)} aria-label="Open chat"><span>{chatOpen ? "×" : "•••"}</span></button>{chatOpen && <div className="chat-panel"><strong>How can we help?</strong><p>Talk to a Zendesk expert about AI-powered customer service.</p><a className="button button-lime" href="#contact" onClick={() => setChatOpen(false)}>Contact us</a></div>}
    </div>
  );
}

export default App;
