# Nook agentic commerce workspace plan

## Product scope

Nook is an agentic commerce workspace, not a customer-service landing page. It combines a searchable product catalogue with AI agents that understand shopper intent, recommend products, prepare order actions, and surface operational signals.

## Required outcomes

- Keep the real product catalogue from `frontend/src/data/demoData.js` visible and searchable.
- Preserve product detail, wishlist, bag, checkout, filtering, category browsing, and responsive mobile navigation.
- Surface the live backend concierge through the assistant drawer using the existing agent session, conversation, tool, and approval APIs.
- Make order-creating actions approval-gated and explain unavailable AI-provider states honestly.
- Provide a home experience that explains agentic commerce: agents understand intent, take the next action, and learn from outcomes.
- Provide an AI dashboard showing conversations, AI-assisted revenue, resolution rate, inventory signals, agent performance, and recent workflows.
- Keep the app’s warm editorial product-marketplace visual language: paper canvas, sage intelligence cues, terracotta action cues, rounded product imagery, and compact commerce metadata.

## Implementation approach

- `frontend/src/App.jsx` owns the responsive shell, product catalogue, product interactions, assistant drawer, checkout flow, and dashboard view.
- `frontend/src/data/demoData.js` remains the source of demo product records and verified image URLs.
- `frontend/src/api/agentClient.js` remains the only frontend boundary for live agent sessions, chat, and approval resumes.
- `backend/app/api/agent.py` and the provider-neutral LLM/tool architecture remain intact.
- `frontend/src/index.css` contains the shared paper/sage/terracotta design tokens, marketplace layout, responsive behavior, assistant drawer, and dashboard styling.
- Vite accepts the public sandbox preview host through `server.allowedHosts`.

## Agent workspace direction

- The assistant is presented as an execution workspace, with live tool-event history, explicit approval pauses, and honest runtime states rather than a generic chat transcript.
- Voice input uses browser speech recognition when supported, while voice output is routed through the backend `/agent/speak` boundary so the ElevenLabs key never reaches the browser.
- ElevenLabs is optional at runtime: the transcript and agent workflow remain usable when audio is not configured.
- Canva is reserved for explicit creative assets or brand work; the application UI itself remains source-controlled in the repository and does not replicate Canva template internals.

## Design direction

- **Movement:** warm editorial commerce workspace with an operations-console layer.
- **Core principles:** product-first, useful, calm, and agent-aware.
- **Color philosophy:** bone paper and warm white keep the catalogue tactile; sage signals intelligence and health; terracotta marks human attention and next actions.
- **Layout paradigm:** fixed browse rail plus sticky search bar; home narrative above the catalogue; dashboard uses metric cards and workflow panels.
- **Signature elements:** rounded product imagery, compact catalogue metadata, the terracotta AI concierge signal, and agent workflow cards.
- **Brand essence:** Nook helps people and commerce teams make better decisions together with useful AI agents.

## Workspace split

- **Customer storefront:** a product-first shopping surface with a large demo catalogue, search and filters, product detail, wishlist, bag, checkout request flow, responsive navigation, and a customer concierge that accepts text and supported browser voice input.
- **Owner control room:** a separate workspace state in the same shell with revenue, products sold, active AI sessions, inventory health, category mix, order pipeline, live workflow events, pending approvals, and an owner operations agent entry point.
- **Shared execution model:** both agents use the same server-side session and tool boundary. Product discovery can stay conversational; order mutation remains approval-gated. If the backend is unavailable, the interface uses clearly labelled demo workspace data instead of claiming a live action occurred.
