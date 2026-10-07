# Plety exact landing page plan

## Required outcomes

- Route every concierge message to the real backend agent instead of frontend keyword matching or hardcoded product replies.
- Preserve the existing provider-neutral LLM, tool registry, permission, and approval architecture; never expose deterministic mock answers to customers.
- Persist the agent conversation inside each API session so follow-up messages remain conversational.
- Keep tool calls, provider errors, approval metadata, and orchestration details out of the end-user chat transcript.
- Use natural final assistant responses from the configured Groq/Google provider, with an honest unavailable state when the hosted provider is not configured.
- Replace the old Morrow & Form commerce shell with the uploaded Plety landing page specification: pure black background, white typography, transparent-to-blurred sticky navigation, exact hero copy, hero video, API badge, dual CTA, masked trusted-by marquee, two video-backed feature mockups, FAQ accordion, and video-backed footer CTA.
- Keep the existing live agent backend intact and wire its real conversation into the Plety “Ask anything…” chat mockup; no customer-facing mock responses.

## Implementation approach

- Extend `LLMAgentRunner.run` to accept an existing `AgentConversation` while preserving its current call signature for tests and other callers.
- Store the conversation object in `backend/app/api/agent.py` session state and update it after normal turns and approval resumes.
- Keep API responses compatible, but let the frontend render only the public `response` field and map non-public workflow states to friendly copy.
- Use a single React landing page in `frontend/src/App.jsx` with a FadeInUp wrapper, exact anchor sections (`about`, `features`, `faq`, `contact`), responsive navigation, real chat composer, FAQ grid-row animation, and exact footer credit layout.
- Use the supplied SceneAI video URLs for the hero, AI chat mockup, AI transcription mockup, and footer background; use only CSS/SVG for the Plety logo and trusted-brand marks.
- Validate with backend pytest, frontend lint/build, and the running FastAPI preview.

## Design direction

- **Movement:** sleek dark SaaS landing page / modern product launch.
- **Core principles:** exact hierarchy, generous negative space, high-contrast typography, and restrained glassmorphism.
- **Color philosophy:** pure black and white form the canvas; gray supports reading; yellow/green badges provide semantic feature accents without muddying the system.
- **Layout paradigm:** centered hero followed by alternating two-column feature rows, a constrained FAQ, and a four-column footer.
- **Signature elements:** stroke-based Plety logo, masked brand marquee, rounded video mockups, pill CTAs, and plus-to-close FAQ controls.
- **Interaction philosophy:** fast, clear, responsive; nav links scroll to anchors, mobile menu closes after selection, the chat card talks to the real agent, and feature buttons return users to chat.
- **Animation:** 1000ms FadeInUp reveal from translate-y-10/opacity-0, 30-second marquee, smooth scrolling, sticky-nav blur after 20px, FAQ grid-template-rows transition, and reduced-motion support.
- **Typography:** DM Sans/Manrope for UI and headings, Playfair Display italic for the word “decisions.” and footer “everything?”.
- **Brand essence:** Plety is the intelligence layer for clear decisions. Personality: clear, capable, fast.
- **Brand voice:** “The intelligence layer for clear decisions.” / “Speed, scale, and smarts — deployed.”
- **Wordmark:** custom geometric stroke-based P mark beside the Plety wordmark.
- **Signature color:** white interaction surfaces with restrained yellow/green feature accents.

## Project structure

- `backend/app/llm/`: provider-neutral reasoning and conversation models.
- `backend/app/api/agent.py`: session lifecycle and public agent routes.
- `frontend/src/App.jsx`: storefront, concierge UI, and public response presentation.
- `frontend/src/data/demoData.js`: catalog presentation data and existing imagery.
- `frontend/src/index.css`: visual system, hero, card, drawer, and responsive behavior.
