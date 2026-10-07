# Agentic storefront refinement plan

## Required outcomes

- Route every concierge message to the real backend agent instead of frontend keyword matching or hardcoded product replies.
- Preserve the existing provider-neutral LLM, tool registry, permission, and approval architecture; never expose deterministic mock answers to customers.
- Persist the agent conversation inside each API session so follow-up messages remain conversational.
- Keep tool calls, provider errors, approval metadata, and orchestration details out of the end-user chat transcript.
- Use natural final assistant responses from the configured Groq/Google provider, with an honest unavailable state when the hosted provider is not configured.
- Improve the homepage visual hierarchy with the existing product imagery in the collection while keeping the hero focused on the animated sculptural object and removing unnecessary hero photography.
- Rework the interface so it does not read as an AI-generated demo: use a dark, restrained editorial shell, custom stroke-based wordmark mark, human commerce copy, sticky navigation with scroll state, mobile navigation, scroll-reveal transitions, marquee masking, accordion FAQ, and a considered contact/footer finish.

## Implementation approach

- Extend `LLMAgentRunner.run` to accept an existing `AgentConversation` while preserving its current call signature for tests and other callers.
- Store the conversation object in `backend/app/api/agent.py` session state and update it after normal turns and approval resumes.
- Keep API responses compatible, but let the frontend render only the public `response` field and map non-public workflow states to friendly copy.
- Replace frontend local matching in `App.jsx` with one initialized `/agent/session` and `/agent/chat` calls for every user message.
- Reuse the existing Unsplash-backed product images from `demoData.js` in the collection; keep the hero image-free and focused on the animated sculptural object. Adapt the uploaded Plety brief's dark black/white system, smooth scrolling, masked marquee, mobile menu, reveal animation, FAQ accordion, and footer CTA without replacing the Morrow & Form brand or live-commerce behavior.
- Seed the backend agent catalog with fashion categories that match the storefront, including Shoes, Accessories, Dresses, Bags, Jewellery, Perfume, Sneakers, and Beauty.
- Validate with backend pytest, frontend lint/build, and the running FastAPI preview.

## Design direction

- **Movement:** dark editorial commerce / neo-modernist product journal, informed by the uploaded Plety brief but grounded in Morrow & Form.
- **Core principles:** quiet confidence, generous negative space, tactile imagery, and restrained motion; the interface should feel authored rather than generated.
- **Color philosophy:** near-black gives the collection room to breathe, warm white keeps it human, and acid lime acts as one ownable signal for availability, interaction, and live status.
- **Layout paradigm:** asymmetrical hero with copy anchored left and layered visual evidence right; editorial sections rather than centered card grids, with a split FAQ and an open footer CTA.
- **Signature elements:** a custom stroke-based M mark, thin mono labels, circular crosshair geometry, masked marquees, and collection image cards with index markers.
- **Interaction philosophy:** direct and calm; the concierge answers in plain language while implementation details remain invisible.
- **Animation:** preserve cursor parallax, use scroll progress, reveal-on-scroll, hover lift, button shimmer, a responsive sticky header, mobile menu reveal, masked marquee, and CSS-grid FAQ expansion; respect reduced-motion settings.
- **Typography:** Manrope for utility and headlines, Playfair Display italic for editorial emphasis, DM Mono for metadata and status—not decorative over-labeling.
- **Brand essence:** a considered AI-assisted collection for people who want useful recommendations without robotic shopping flows. Personality: considered, observant, quietly capable.
- **Brand voice:** “Things worth keeping close.” / “Let’s find the right direction.” Keep AI implementation language out of customer-facing copy; call the experience a personal edit.
- **Wordmark:** replace the old text-in-circle mark with a minimal geometric stroke M that can stand alone beside the Morrow & Form wordmark.
- **Signature color:** acid lime used as a precise live/status/action signal, not a fill-everything accent.

## Project structure

- `backend/app/llm/`: provider-neutral reasoning and conversation models.
- `backend/app/api/agent.py`: session lifecycle and public agent routes.
- `frontend/src/App.jsx`: storefront, concierge UI, and public response presentation.
- `frontend/src/data/demoData.js`: catalog presentation data and existing imagery.
- `frontend/src/index.css`: visual system, hero, card, drawer, and responsive behavior.
