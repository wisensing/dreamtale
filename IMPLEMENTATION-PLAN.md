# DreamTale MVP Implementation Plan

## Context
Greenfield implementation of the DreamTale AI bedtime story app — full MVP end-to-end. The repo contains only the product spec (`DreamTale-Plan.md`). We'll build a FastAPI backend + React Native (Expo) frontend with Supabase auth, Stripe payments, credit system, and COPPA flows. LLM/TTS use mock stubs for now (swappable later).

---

## Directory Structure

```
dreamtale/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                  # FastAPI app, CORS, lifespan
│   │   ├── config.py                # Settings from env vars
│   │   ├── database.py              # SQLAlchemy async engine + session
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py              # User model
│   │   │   ├── kid.py               # Kid model
│   │   │   ├── story.py             # Story, StoryTranslation, StoryVersion
│   │   │   ├── chat.py              # ChatSession, ChatMessage
│   │   │   ├── credit.py            # CreditTransaction
│   │   │   ├── bedtime.py           # BedtimeSession
│   │   │   └── shared.py            # SharedStory
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── kid.py
│   │   │   ├── story.py
│   │   │   ├── chat.py
│   │   │   ├── credit.py
│   │   │   └── bedtime.py
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py              # Auth endpoints (Supabase wrapper)
│   │   │   ├── kids.py              # CRUD for kid profiles
│   │   │   ├── stories.py           # Generate, list, save, share stories
│   │   │   ├── chat.py              # Chat session + message endpoints
│   │   │   ├── credits.py           # Credit balance, purchase, Stripe webhooks
│   │   │   ├── bedtime.py           # Bedtime sessions, streaks
│   │   │   └── tts.py               # TTS generation endpoint
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── story_engine.py      # Story generation pipeline
│   │   │   ├── prompt_builder.py    # Build prompts from kid config + keywords
│   │   │   ├── age_config.py        # Age-appropriate content settings
│   │   │   ├── diversity_tracker.py # Track recent themes, avoid repetition
│   │   │   ├── safety_filter.py     # Pre/post filter stubs
│   │   │   ├── llm_provider.py      # LLM abstraction (mock impl)
│   │   │   ├── tts_provider.py      # TTS abstraction (mock impl)
│   │   │   ├── credit_service.py    # Credit deduction, balance check
│   │   │   └── stripe_service.py    # Stripe checkout + webhook handling
│   │   ├── auth/
│   │   │   ├── __init__.py
│   │   │   └── supabase.py          # Supabase JWT verification middleware
│   │   └── workers/
│   │       ├── __init__.py
│   │       └── story_worker.py      # Celery task for async story gen
│   ├── alembic/
│   │   ├── env.py
│   │   └── versions/
│   │       └── 001_initial.py
│   ├── alembic.ini
│   ├── requirements.txt
│   └── Dockerfile
│
├── mobile/
│   ├── app/
│   │   ├── _layout.tsx              # Root layout with providers
│   │   ├── index.tsx                # Landing/auth check
│   │   ├── auth/
│   │   │   ├── login.tsx            # Sign in screen
│   │   │   └── signup.tsx           # Sign up screen
│   │   ├── onboarding/
│   │   │   ├── add-kid.tsx          # Add child profile
│   │   │   ├── interests.tsx        # Pick interests
│   │   │   └── bedtime-goal.tsx     # Set bedtime
│   │   ├── (tabs)/
│   │   │   ├── _layout.tsx          # Tab navigator
│   │   │   ├── chat.tsx             # Main chat interface
│   │   │   ├── stories.tsx          # Saved stories list
│   │   │   └── profile.tsx          # Kid profiles + settings
│   │   └── story/
│   │       └── [id].tsx             # Story detail + audio player
│   ├── components/
│   │   ├── ChatBubble.tsx
│   │   ├── ChatInput.tsx
│   │   ├── StoryCard.tsx
│   │   ├── AudioPlayer.tsx
│   │   ├── Sidebar.tsx
│   │   ├── StreakCounter.tsx
│   │   ├── CreditBadge.tsx
│   │   ├── AgeGate.tsx              # COPPA age verification for purchases
│   │   └── WindDownOverlay.tsx
│   ├── stores/
│   │   ├── authStore.ts
│   │   ├── chatStore.ts
│   │   ├── storyStore.ts
│   │   └── kidStore.ts
│   ├── services/
│   │   ├── api.ts                   # Axios instance + interceptors
│   │   ├── auth.ts                  # Supabase client
│   │   ├── stories.ts               # Story API calls
│   │   ├── chat.ts                  # Chat API calls
│   │   └── credits.ts               # Credit API calls
│   ├── constants/
│   │   ├── themes.ts                # Age-appropriate themes/interests
│   │   └── colors.ts
│   ├── types/
│   │   └── index.ts
│   ├── app.json
│   ├── package.json
│   └── tsconfig.json
│
├── DreamTale-Plan.md
└── docker-compose.yml               # Postgres + Redis for local dev
```

---

## Database Schema (SQLAlchemy Models)

### users
- id (UUID, PK), supabase_id (str, unique), email (str), subscription_tier (enum: free/premium/family), credit_balance (int, default 3), coppa_consent (bool), coppa_consent_date (datetime), content_strictness (int, 1-5, default 3), created_at, updated_at

### kids
- id (UUID, PK), user_id (FK users), nickname (str, encrypted), age (int, 2-10), interests (JSON array), fears (JSON array), bedtime_goal (time), primary_language (str, default "en"), learning_languages (JSON array), companion_name (str, optional), created_at, updated_at

### stories
- id (UUID, PK), kid_id (FK kids), chat_session_id (FK chat_sessions, nullable), text (text), audio_url (str, nullable), theme (str), educational_topic (str), story_style (str, default ""), language (str, default "en"), keywords_used (JSON), is_saved (bool, default false), play_count (int, default 0), safety_score (float, default 1.0), parent_rating (int, nullable), created_at

### story_versions
- id (UUID, PK), story_id (FK stories), text (text), audio_url (str, nullable), version_number (int), modification_prompt (str, nullable), created_at

### story_translations
- id (UUID, PK), story_id (FK stories), language (str), translated_text (text), audio_url (str, nullable), created_at

### shared_stories
- id (UUID, PK), story_id (FK stories), share_token (str, unique), is_public (bool, default false), view_count (int, default 0), created_at

### chat_sessions
- id (UUID, PK), kid_id (FK kids), title (str), created_at, updated_at

### chat_messages
- id (UUID, PK), chat_session_id (FK chat_sessions), role (enum: user/assistant), content (text), story_id (FK stories, nullable), created_at

### credit_transactions
- id (UUID, PK), user_id (FK users), amount (int), transaction_type (enum: purchase/usage/bonus/refund), description (str), stripe_payment_id (str, nullable), created_at

### bedtime_sessions
- id (UUID, PK), kid_id (FK kids), date (date), bedtime_actual (time), story_id (FK stories, nullable), duration_minutes (int, nullable), created_at

---

## API Endpoints

### Auth (`/api/auth`)
- POST `/api/auth/signup` — Create account (email + password via Supabase)
- POST `/api/auth/login` — Sign in
- POST `/api/auth/logout` — Sign out
- GET `/api/auth/me` — Get current user profile

### Kids (`/api/kids`)
- POST `/api/kids` — Create kid profile
- GET `/api/kids` — List user's kids
- GET `/api/kids/{id}` — Get kid profile
- PUT `/api/kids/{id}` — Update kid profile
- DELETE `/api/kids/{id}` — Delete kid profile

### Stories (`/api/stories`)
- POST `/api/stories/generate` — Generate a new story (deducts credit)
- POST `/api/stories/{id}/modify` — Modify a story via chat (free)
- GET `/api/stories` — List stories (filterable by kid_id, is_saved)
- GET `/api/stories/{id}` — Get story detail
- POST `/api/stories/{id}/save` — Save/unsave story
- POST `/api/stories/{id}/share` — Generate share link
- GET `/api/stories/shared/{token}` — View shared story (public, no auth)
- DELETE `/api/stories/{id}` — Delete story
- POST `/api/stories/{id}/translate` — Translate story to another language

### Chat (`/api/chat`)
- POST `/api/chat/sessions` — Create chat session
- GET `/api/chat/sessions` — List chat sessions for kid
- GET `/api/chat/sessions/{id}` — Get session with messages
- POST `/api/chat/sessions/{id}/messages` — Send message (generates story or modification)

### Credits (`/api/credits`)
- GET `/api/credits/balance` — Get current balance
- POST `/api/credits/checkout` — Create Stripe checkout session
- POST `/api/credits/webhook` — Stripe webhook handler
- GET `/api/credits/transactions` — Transaction history

### Bedtime (`/api/bedtime`)
- POST `/api/bedtime/sessions` — Record bedtime session
- GET `/api/bedtime/streaks/{kid_id}` — Get streak info
- GET `/api/bedtime/stats/{kid_id}` — Get weekly stats

### TTS (`/api/tts`)
- POST `/api/tts/generate` — Generate TTS audio for a story

---

## Frontend Screens & Components

### Navigation Flow
1. **Auth Stack**: Login → Signup
2. **Onboarding Stack**: AddKid → Interests → BedtimeGoal
3. **Main Tabs**: Chat | Stories | Profile
4. **Modals**: Story Detail (with audio player), Age Gate (for purchases)

### Key Component Design
- **Chat Interface**: ChatGPT-style — message list + input bar, story cards appear inline as assistant messages
- **Sidebar**: Swipeable drawer with saved stories list, filterable by kid
- **AudioPlayer**: Mini player bar at bottom, full player in story detail, controls for play/pause/speed/sleep timer
- **StoryCard**: Compact card showing title/preview, language badge, play button

---

## Implementation Order

### Phase A: Backend Foundation (files 1-20)
1. `backend/app/config.py` — Environment settings
2. `backend/app/database.py` — Async SQLAlchemy setup
3. `backend/app/models/` — All SQLAlchemy models
4. `backend/app/schemas/` — Pydantic schemas
5. `backend/app/auth/supabase.py` — JWT verification
6. `backend/app/services/llm_provider.py` — Mock LLM
7. `backend/app/services/tts_provider.py` — Mock TTS
8. `backend/app/services/age_config.py` — Age-based content settings
9. `backend/app/services/prompt_builder.py` — Prompt construction
10. `backend/app/services/diversity_tracker.py` — Theme diversity
11. `backend/app/services/safety_filter.py` — Safety stubs
12. `backend/app/services/story_engine.py` — Full pipeline
13. `backend/app/services/credit_service.py` — Credit logic
14. `backend/app/services/stripe_service.py` — Stripe integration
15. `backend/app/routers/` — All API routers
16. `backend/app/main.py` — App assembly
17. `backend/requirements.txt`
18. `backend/Dockerfile`
19. `docker-compose.yml` — Postgres + Redis
20. `backend/alembic/` — Initial migration

### Phase B: Frontend Foundation (files 21-45)
21. `mobile/package.json` — Dependencies
22. `mobile/tsconfig.json`
23. `mobile/app.json` — Expo config
24. `mobile/constants/` — Themes, colors
25. `mobile/types/index.ts` — TypeScript types
26. `mobile/services/api.ts` — API client
27. `mobile/services/auth.ts` — Supabase client
28. `mobile/services/stories.ts` — Story API
29. `mobile/services/chat.ts` — Chat API
30. `mobile/services/credits.ts` — Credit API
31. `mobile/stores/` — Zustand stores
32. `mobile/components/` — All components
33. `mobile/app/_layout.tsx` — Root layout
34. `mobile/app/auth/login.tsx`
35. `mobile/app/auth/signup.tsx`
36. `mobile/app/onboarding/` — Onboarding screens
37. `mobile/app/(tabs)/_layout.tsx`
38. `mobile/app/(tabs)/chat.tsx`
39. `mobile/app/(tabs)/stories.tsx`
40. `mobile/app/(tabs)/profile.tsx`
41. `mobile/app/story/[id].tsx`

---

## Key Architectural Decisions

1. **LLM/TTS via provider abstraction**: `BaseLLMProvider` / `BaseTTSProvider` abstract classes with `MockLLMProvider` and `MockTTSProvider` implementations. Swap to real providers by changing config.

2. **Mock story generation**: The mock LLM will use string templates with the child's name, age, interests, and keywords to produce varied stories. It will have a pool of 10+ story templates per age group that get personalized.

3. **Auth flow**: Supabase handles signup/login/JWT. Backend verifies JWTs via middleware. Frontend uses `@supabase/supabase-js`.

4. **Credit system**: 3 free stories on signup. Each story generation costs 1 credit. Modifications are free. Stripe checkout for credit packs.

5. **Chat architecture**: Chat messages are persisted. When user sends a message with keywords, it triggers story generation. "Modify" messages modify the last story. All context sent to LLM includes chat history.

6. **COPPA**: Parental consent on signup, encrypted kid nicknames, age gate (math problem) before purchase screens, no behavioral ads, content strictness setting.

---

## Verification

1. **Backend**: Run `docker-compose up` to start Postgres + Redis, then `uvicorn app.main:app --reload`. Test all endpoints via Swagger UI at `/docs`.
2. **Frontend**: Run `npx expo start`. Test on iOS simulator / Android emulator / web.
3. **E2E flow**: Sign up → add kid → generate story (verify credit deducted) → modify story (verify free) → save story → view in sidebar → share → open share link → check credit balance.
4. **COPPA**: Verify age gate appears before purchase, consent is recorded, kid data is encrypted in DB.
