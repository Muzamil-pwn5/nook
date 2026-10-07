import { useEffect, useRef, useState } from "react";
import { agentClient } from "./api/agentClient";
import "./index.css";

const HERO_VIDEO = "https://cdn.sceneai.art/Hero%20Section%20Video/50b4f304-cdca-4e12-8735-580d225834be.mp4";
const CHAT_VIDEO = "https://cdn.sceneai.art/Hero%20Section%20Video/1bcc8fa3-37f6-4c53-8591-0347e4c7f8ac.mp4";
const TRANSCRIPTION_VIDEO = "https://cdn.sceneai.art/Hero%20Section%20Video/736fd4a0-70ac-4f44-9633-55769ead6aca.mp4";

const faqItems = [
  ["Is my data safe?", "Yes. Your conversation is handled in a private session and the interface never exposes internal orchestration, provider details, or operational metadata."],
  ["Can Plety connect to my existing tools?", "The hosted agent is designed around controlled tools and provider-neutral reasoning. Ask the concierge what is available in the current workspace."],
  ["How does the AI chat work?", "Send a natural-language request in the chat card. The live agent reasons through the request, uses approved tools when needed, and returns a conversational answer."],
  ["Can I use Plety on mobile?", "Yes. The navigation, feature cards, chat composer, FAQ, and footer are responsive and designed for touch-first use."],
  ["Do I need to install anything?", "No. Plety runs in the browser and the hosted experience is ready to use without a local development setup."],
];

function FadeInUp({ children, className = "", delay = 0 }) {
  return <div className={`fade-up ${className}`} style={{ "--delay": `${delay}ms` }}>{children}</div>;
}

function Logo() {
  return <a className="plety-logo" href="#about" aria-label="Plety home"><svg viewBox="0 0 32 32" aria-hidden="true"><path d="M7 25V7h8.2a5.2 5.2 0 0 1 0 10.4H7M20 7v18M20 7h4.1a4 4 0 0 1 0 8H20" /></svg><span>Plety</span></a>;
}

function ArrowIcon() { return <svg viewBox="0 0 20 20" aria-hidden="true"><path d="M4 10h11M10 4l6 6-6 6" /></svg>; }
function PlusIcon() { return <span className="plus-icon" aria-hidden="true" />; }
function MicIcon() { return <svg viewBox="0 0 20 20" aria-hidden="true"><rect x="7" y="3" width="6" height="10" rx="3" /><path d="M4 10a6 6 0 0 0 12 0M10 16v2M7 18h6" /></svg>; }
function WaveIcon() { return <span className="wave-icon"><i /><i /><i /><i /><i /><i /><i /></span>; }

function Nav({ onGetStarted }) {
  const [scrolled, setScrolled] = useState(false);
  const [open, setOpen] = useState(false);
  useEffect(() => {
    const handle = () => setScrolled(window.scrollY > 20);
    handle(); window.addEventListener("scroll", handle, { passive: true });
    return () => window.removeEventListener("scroll", handle);
  }, []);
  const close = () => setOpen(false);
  const start = () => { close(); onGetStarted(); };
  return <>
    <header className={`plety-nav ${scrolled ? "is-scrolled" : ""}`}>
      <div className="nav-inner"><Logo /><nav className="nav-links" aria-label="Primary navigation"><a href="#about">About</a><a href="#features">Features</a><a href="#faq">FAQ</a><a href="#contact">Contact</a></nav><div className="nav-actions"><button className="nav-cta" onClick={start}>Get started <ArrowIcon /></button><button className={`hamburger ${open ? "is-open" : ""}`} onClick={() => setOpen((value) => !value)} aria-label={open ? "Close menu" : "Open menu"} aria-expanded={open}><span /><span /><span /></button></div></div>
    </header>
    {open && <div className="mobile-nav-menu"><a href="#about" onClick={close}>About</a><a href="#features" onClick={close}>Features</a><a href="#faq" onClick={close}>FAQ</a><a href="#contact" onClick={close}>Contact</a><button onClick={start}>Get started <ArrowIcon /></button></div>}
  </>;
}

function BrandLogo({ name }) {
  return <span className="brand-logo"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 18V6l5 6 5-6v12M14 6l6 4v8" /></svg>{name}</span>;
}

function Marquee() {
  const logos = ["Springfield", "Orbitc", "Cloud", "Amster", "Nexus"];
  return <section className="trust-strip"><p>Trusted by teams building what comes next</p><div className="marquee-window"><div className="brand-marquee">{[...logos, ...logos, ...logos, ...logos].map((logo, index) => <BrandLogo key={`${logo}-${index}`} name={logo} />)}</div></div></section>;
}

function ChatMockup({ messages, input, setInput, onSend, busy, onMic }) {
  return <div className="feature-mockup chat-mockup"><video className="mockup-video" autoPlay muted loop playsInline src={CHAT_VIDEO} /><div className="video-shade" /><div className="floating-chat-card"><div className="chat-card-top"><span className="live-dot" /> Plety chat <span className="card-status">Live</span></div><div className="chat-chips"><span>Create image</span><span>Summarize</span><span>Analyze</span></div><div className="chat-history">{messages.map((message) => <div className={`mini-message mini-message--${message.role}`} key={message.id}>{message.text}</div>)}{busy && <div className="mini-message mini-message--assistant typing"><i /><i /><i /></div>}</div><form className="chat-composer" onSubmit={(event) => { event.preventDefault(); onSend(); }}><input value={input} onChange={(event) => setInput(event.target.value)} placeholder="Ask anything…" aria-label="Ask Plety anything" /><button type="button" onClick={onMic} className="icon-button" aria-label="Use microphone"><MicIcon /></button><button className="send-button" disabled={!input.trim() || busy} aria-label="Send"><ArrowIcon /></button></form></div></div>;
}

function TranscriptionMockup() {
  return <div className="feature-mockup transcription-mockup"><video className="mockup-video" autoPlay muted loop playsInline src={TRANSCRIPTION_VIDEO} /><div className="video-shade" /><div className="floating-transcript-card"><div className="transcript-top"><button className="play-button" aria-label="Play transcription"><span /></button><div><strong>11:06 AM – Chris</strong><small>Team sync / 32 min</small></div><span className="transcript-more">•••</span></div><div className="transcript-wave"><WaveIcon /><span>02:48</span></div><p>We need to make the next decision clear, then give the team room to move.</p><span className="transcript-cursor" /></div></div>;
}

function FeatureCopy({ badge, title, children, onGetStarted, tone = "yellow" }) {
  return <div className="feature-copy"><span className={`feature-badge feature-badge--${tone}`}>✦ {badge}</span><h2>{title}</h2><p>{children}</p><button className="text-cta" onClick={onGetStarted}>Get started <ArrowIcon /></button></div>;
}

function FAQ() {
  const [open, setOpen] = useState(-1);
  return <section id="faq" className="faq-section"><FadeInUp><h2>We’ve got answers</h2></FadeInUp><FadeInUp delay={80}><div className="faq-box">{faqItems.map(([question, answer], index) => <div className={`faq-row ${open === index ? "is-open" : ""}`} key={question}><button onClick={() => setOpen(open === index ? -1 : index)} aria-expanded={open === index}><span>{question}</span><PlusIcon /></button><div className="faq-answer"><div><p>{answer}</p></div></div></div>)}</div></FadeInUp></section>;
}

function Footer({ onGetStarted }) {
  return <footer id="contact" className="plety-footer"><video className="footer-video" autoPlay muted loop playsInline src={HERO_VIDEO} /><div className="footer-shade" /><div className="footer-inner"><FadeInUp><div className="footer-cta"><h2>Ready to automate <em>everything?</em></h2><div className="footer-buttons"><button className="button button--white" onClick={onGetStarted}>Get started <ArrowIcon /></button><a className="button button--dark" href="#features">Learn more <ArrowIcon /></a></div></div></FadeInUp><div className="footer-links"><div className="footer-brand"><Logo /><p>Speed, scale, and smarts — deployed.</p></div><div><span>Product</span><a href="#about">About</a><a href="#features">Pricing</a><a href="#features">Changelog</a><a href="#contact">Contact</a></div><div><span>Legal</span><a href="#contact">Terms of service</a><a href="#contact">Privacy policy</a><a href="#contact">404</a></div><div><span>Connect</span><a href="#contact">Instagram</a><a href="#contact">YouTube</a><a href="#contact">LinkedIn</a><a href="#contact">Twitter / X</a></div></div><div className="footer-bottom"><span>© 2026 Plety. All rights reserved</span><i>•</i><span>by <b>Re-text</b></span><i>•</i><span>Made in <b>Gemini</b></span></div></div></footer>;
}

function App() {
  const chatRef = useRef(null);
  const [sessionId, setSessionId] = useState(null);
  const [messages, setMessages] = useState([{ id: "welcome", role: "assistant", text: "Tell me what you’re working through." }]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const [connection, setConnection] = useState("connecting");
  useEffect(() => { let active = true; Promise.all([agentClient.health(), agentClient.createSession()]).then(([, session]) => { if (!active) return; setSessionId(session.session_id); setConnection("live"); }).catch(() => active && setConnection("offline")); return () => { active = false; }; }, []);
  const scrollToChat = () => { document.getElementById("features")?.scrollIntoView({ behavior: "smooth" }); setTimeout(() => chatRef.current?.focus(), 600); };
  const sendMessage = async () => {
    const text = input.trim(); if (!text || busy) return; setInput(""); setMessages((items) => [...items, { id: `user-${Date.now()}`, role: "user", text }]); setBusy(true);
    try { if (!sessionId) throw new Error("Not connected"); const result = await agentClient.chat(sessionId, text); setConnection(result?.agent === "llm" ? "live" : "offline"); const response = result?.response || "I’m ready when you are. Tell me a little more."; setMessages((items) => [...items, { id: `assistant-${Date.now()}`, role: "assistant", text: response }]); } catch { setMessages((items) => [...items, { id: `assistant-${Date.now()}`, role: "assistant", text: "I’m having trouble reaching Plety right now. Please try again." }]); } finally { setBusy(false); }
  };
  return <div className="plety-app"><Nav onGetStarted={scrollToChat} /><main><section id="about" className="plety-hero"><video className="hero-video" autoPlay muted loop playsInline src={HERO_VIDEO} /><div className="hero-overlay" /><FadeInUp className="hero-content"><span className="hero-badge">✦ Announcing API 2.0</span><h1>The intelligence layer<br />for clear <em>decisions.</em></h1><p>Our platform integrates seamlessly into your stack to deliver real-time understanding, not just predictions.</p><div className="hero-buttons"><button className="button button--white" onClick={scrollToChat}>Get started <ArrowIcon /></button><a className="button button--dark" href="#features">Learn more <ArrowIcon /></a></div></FadeInUp><div className="hero-bottom"><span>Scroll to explore</span><span className="hero-line" /><span className={`connection-label connection-label--${connection}`}><i /> {connection === "live" ? "Live system" : connection === "offline" ? "Offline" : "Connecting"}</span></div></section><Marquee /><section id="features" className="features-section"><div className="feature-row"><FadeInUp className="feature-copy-wrap"><FeatureCopy badge="AI chat" title="Where speed meets intelligent conversation." onGetStarted={scrollToChat}>A conversational AI assistant that understands your questions, provides intelligent answers, and helps you get things done fast — from casual chats to complex tasks.</FeatureCopy></FadeInUp><FadeInUp delay={100}><ChatMockup messages={messages} input={input} setInput={setInput} onSend={sendMessage} busy={busy} onMic={() => setInput((value) => value || "Can you help me think through ")} /></FadeInUp></div><div className="feature-row feature-row--reverse"><FadeInUp><TranscriptionMockup /></FadeInUp><FadeInUp delay={100} className="feature-copy-wrap"><FeatureCopy badge="AI transcription" tone="green" title="Turn speech into text with speed and precision." onGetStarted={scrollToChat}>Automatically convert speech into accurate, editable text in real time. Perfect for meetings, interviews, voice notes, and more, powered by advanced speech recognition technology.</FeatureCopy></FadeInUp></div></section><FAQ /></main><Footer onGetStarted={scrollToChat} /></div>;
}

export default App;
