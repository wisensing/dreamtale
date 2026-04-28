# DreamTale — Development Status

## What's Built

Full MVP end-to-end implementation across 76 files. Backend uses FastAPI + Python, frontend uses React Native (Expo). LLM/TTS use mock stubs (swappable to real providers via config).

---

## Backend (FastAPI + Python) — 30 files

### Core
- `backend/app/config.py` — Pydantic settings from env vars
- `backend/app/database.py` — Async SQLAlchemy engine + session
- `backend/app/main.py` — FastAPI app with CORS, lifespan (auto-creates tables), all routers mounted

### Models (SQLAlchemy)
- `backend/app/models/user.py` — User with subscription_tier, credit_balance, COPPA consent
- `backend/app/models/kid.py` — Kid profile with nickname, age, interests, fears, languages
- `backend/app/models/story.py` — Story, StoryVersion, StoryTranslation, SharedStory
- `backend/app/models/chat.py` — ChatSession, ChatMessage
- `backend/app/models/credit.py` — CreditTransaction with purchase/usage/bonus/refund types
- `backend/app/models/bedtime.py` — BedtimeSession

### Schemas (Pydantic)
- `backend/app/schemas/auth.py`, `kid.py`, `story.py`, `chat.py`, `credit.py`, `bedtime.py`

### Routers (API Endpoints)
| Router | Prefix | Key Endpoints |
|--------|--------|---------------|
| auth | `/api/auth` | signup, login, me |
| kids | `/api/kids` | CRUD for kid profiles |
| stories | `/api/stories` | generate, modify, list, get, save, share, shared/{token}, delete, translate |
| chat | `/api/chat` | sessions CRUD, send message (auto-detects modification vs generation) |
| credits | `/api/credits` | balance, checkout (Stripe), webhook, transactions |
| bedtime | `/api/bedtime` | sessions, streaks, stats |
| tts | `/api/tts` | generate audio |

### Services (Business Logic)
- `backend/app/services/llm_provider.py` — Abstract `BaseLLMProvider` with `MockLLMProvider` (10+ story templates per age group, personalized with child's name/interests), `OpenAILLMProvider`, `OpenRouterLLMProvider`. Provider selected by `LLM_PROVIDER` env var.
- `backend/app/services/tts_provider.py` — Abstract `BaseTTSProvider` with `MockTTSProvider`, `GoogleTTSProvider`, `ElevenLabsTTSProvider`. Provider selected by `TTS_PROVIDER` env var.
- `backend/app/services/story_engine.py` — Full pipeline: generate_story (pre-filter → build prompt → LLM → post-filter → tone check → TTS → save), modify_story (free, saves version), translate_story
- `backend/app/services/prompt_builder.py` — Builds system/user prompts from child config, age, keywords, fears, recent themes
- `backend/app/services/age_config.py` — Age-appropriate content: 2-3 (100 words, counting/emotions), 4-5 (150 words, sharing/safety), 6-7 (200 words, emergency/science), 8-10 (250 words, critical thinking)
- `backend/app/services/diversity_tracker.py` — Tracks recent themes/topics to avoid repetition
- `backend/app/services/safety_filter.py` — Pre-filter (blocked keywords), post-filter (inappropriate content + excitement check), tone check (must end calmly)
- `backend/app/services/credit_service.py` — 3 free stories, 1 credit per generation, modifications free, InsufficientCreditsError
- `backend/app/services/stripe_service.py` — Checkout session creation, webhook signature verification

### Auth
- `backend/app/auth/supabase.py` — JWT verification middleware (`get_current_user`, `get_optional_user`)

### Infrastructure
- `backend/requirements.txt` — FastAPI, SQLAlchemy, asyncpg, Supabase, Stripe, Celery, Redis, Alembic, OpenAI
- `backend/Dockerfile` — Python 3.12-slim, uvicorn
- `docker-compose.yml` — Postgres 16 + Redis 7 + backend service
- `backend/.env.example` — All env vars documented

---

## Frontend (React Native / Expo) — 42 files

### Screens
| Screen | Path | Description |
|--------|------|-------------|
| Root | `app/index.tsx` | Auth gate → redirects to login/onboarding/tabs |
| Login | `app/auth/login.tsx` | Email/password sign in |
| Signup | `app/auth/signup.tsx` | Email/password + COPPA consent checkbox |
| Add Kid | `app/onboarding/add-kid.tsx` | Nickname + age (2-10) with age descriptions |
| Interests | `app/onboarding/interests.tsx` | Pick 3-5 from 18 interests (emoji grid) |
| Bedtime Goal | `app/onboarding/bedtime-goal.tsx` | Pick bedtime from 5 time options |
| Chat | `app/(tabs)/chat.tsx` | ChatGPT-style main interface — message list, input bar, sidebar for saved stories |
| Stories | `app/(tabs)/stories.tsx` | All stories list with save/share actions |
| Profile | `app/(tabs)/profile.tsx` | Kid profiles, bedtime streak, buy credits, subscriptions, sign out |
| Story Detail | `app/story/[id].tsx` | Full story text, audio player, save/share, keywords |

### Components
| Component | Description |
|-----------|-------------|
| ChatBubble | User/assistant message bubbles with story badge |
| ChatInput | Text input + send button with loading state |
| StoryCard | Story preview card with theme, language badge, save button |
| AudioPlayer | Play/pause, speed control (0.8x/1.0x/1.2x), time display |
| Sidebar | Modal with saved stories list, kid profile filter chips |
| StreakCounter | Night count with moon emoji |
| CreditBadge | Balance display with tier label |
| AgeGate | Math problem verification (COPPA — blocks kids from purchases) |
| WindDownOverlay | Dark overlay for wind-down mode |

### State Management (Zustand)
- `stores/authStore.ts` — User state, login/signup/logout/initialize
- `stores/kidStore.ts` — Kids list, active kid selection, CRUD
- `stores/chatStore.ts` — Chat sessions, messages, send message with optimistic UI
- `stores/storyStore.ts` — Stories list, generate/modify/save/delete

### API Services (Axios)
- `services/api.ts` — Axios instance with auth token interceptor
- `services/auth.ts` — Supabase client (signup/signin/signout, SecureStore persistence)
- `services/stories.ts` — All story endpoints
- `services/chat.ts` — Chat session + message endpoints
- `services/credits.ts` — Balance, checkout, transactions

### Constants
- `constants/colors.ts` — Full palette (primary #6C5CE7, dark mode colors, shadows)
- `constants/themes.ts` — 18 interests, 7 languages, 5 story styles, 4 credit packs, 2 subscription plans

### Types
- `types/index.ts` — User, Kid, Story, ChatSession, ChatMessage, CreditTransaction, SharedStory, BedtimeStats

---

## How to Run

### Backend
```bash
docker-compose up              # Starts Postgres + Redis + backend
# Or manually:
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload  # http://localhost:8000/docs for Swagger
```

### Frontend
```bash
cd mobile
npm install
npx expo start                 # iOS/Android/Web
```

### Environment
Copy `backend/.env.example` to `backend/.env` and fill in:
- `SUPABASE_URL`, `SUPABASE_KEY`, `SUPABASE_JWT_SECRET` — for auth
- `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET` — for payments
- `LLM_PROVIDER=mock` (default), `TTS_PROVIDER=mock` (default) — no API keys needed for dev

---

## What's Next

1. **Wire up real LLM** — Set `LLM_PROVIDER=openai` + `OPENAI_API_KEY` in .env (or openrouter/vllm)
2. **Wire up real TTS** — Set `TTS_PROVIDER=google` or `elevenlabs` + corresponding API key
3. **Supabase setup** — Create project at supabase.com, add URL + anon key + JWT secret
4. **Stripe setup** — Create products/prices, add keys to .env
5. **Test the full flow** — Sign up → add kid → generate story → modify → save → share → buy credits
6. **Push notifications** — Bedtime reminders (expo-notifications)
7. **Wind-down mode** — Auto dark theme in evening based on bedtime goal
8. **Offline support** — expo-sqlite for caching stories
9. **Parent dashboard** — Weekly report with stats from bedtime_sessions
10. **Voice cloning** — Implement Coqui XTTS v2 or ElevenLabs voice cloning
