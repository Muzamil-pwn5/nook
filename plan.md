# Nook furniture marketplace dashboard plan

## Required outcomes

- Route every concierge message to the real backend agent instead of frontend keyword matching or hardcoded product replies.
- Preserve the existing provider-neutral LLM, tool registry, permission, and approval architecture; never expose deterministic mock answers to customers.
- Persist the agent conversation inside each API session so follow-up messages remain conversational.
- Keep tool calls, provider errors, approval metadata, and orchestration details out of the end-user chat transcript.
- Use natural final assistant responses from the configured Groq/Google provider, with an honest unavailable state when the hosted provider is not configured.
- Replace the prior AI/SaaS landing pages with a real responsive furniture e-commerce dashboard inspired by the supplied Dribbble Furniture Marketplace shot: warm neutral canvas, product-first hierarchy, immersive furniture photography, room browsing, collection filters, wishlist, bag, product details, mobile bottom navigation, and a secondary style assistant.
- Keep the existing live agent backend intact and surface its real conversation through the style assistant; do not show implementation details or mock AI responses.

## Implementation approach

- Extend `LLMAgentRunner.run` to accept an existing `AgentConversation` while preserving its current call signature for tests and other callers.
- Store the conversation object in `backend/app/api/agent.py` session state and update it after normal turns and approval resumes.
- Keep API responses compatible, but let the frontend render only the public `response` field and map non-public workflow states to friendly copy.
- Use a responsive React storefront in `frontend/src/App.jsx` with a fixed desktop sidebar, sticky search topbar, warm editorial welcome hero, room cards, furniture product grid, filters/search, functional product modal, cart drawer, wishlist state, assistant drawer, and mobile bottom navigation.
- Use curated furniture photography from Unsplash with rounded image cards, warm sage/terracotta accents, compact commerce metadata, and responsive touch-friendly controls.
- Validate with backend pytest, frontend lint/build, and the running FastAPI preview.

## Design direction

- **Movement:** minimal furniture marketplace / warm editorial product catalog.
- **Core principles:** product-first, calm, tactile, and immediately shoppable.
- **Color philosophy:** bone paper and warm white make photography feel at home; sage communicates calm and terracotta provides a human purchase/assistant signal.
- **Layout paradigm:** app-like desktop shell with sidebar + sticky toolbar, then a full-width feature card, room discovery, and a dense catalog grid.
- **Signature elements:** rounded furniture photography, sage feature panel, compact product badges, floating quick-view affordances, and a terracotta assistant signal.
- **Interaction philosophy:** browsing should feel effortless: filter, search, save, inspect, add to bag, and ask for help without leaving the collection.
- **Animation:** image scale on hover, quick-view reveal, drawer/modal transitions, smooth anchor scrolling, horizontal room scroller on mobile, and reduced-motion support.
- **Typography:** DM Sans for the commerce interface with Playfair Display italic used sparingly for editorial warmth.
- **Brand essence:** Nook is considered furniture for everyday rituals. Personality: warm, observant, quietly useful.
- **Brand voice:** “Make room for better living.” / “Furniture with a point of view, chosen for the way you actually live.”
- **Wordmark:** a compact rounded lowercase n mark beside the Nook wordmark.
- **Signature color:** sage green for the seasonal edit, with terracotta for saved/helpful actions.

## Project structure

- `backend/app/llm/`: provider-neutral reasoning and conversation models.
- `backend/app/api/agent.py`: session lifecycle and public agent routes.
- `frontend/src/App.jsx`: storefront, concierge UI, and public response presentation.
- `frontend/src/data/demoData.js`: catalog presentation data and existing imagery.
- `frontend/src/index.css`: visual system, hero, card, drawer, and responsive behavior.
