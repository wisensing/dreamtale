# DreamTale - AI Bedtime Story App for Kids

## Context

Parents struggle with nightly bedtime routines — repeating the same stories, running out of ideas, and keeping kids engaged. Kids are far more interested when they hear their own name and familiar things in stories. This app solves both problems: it generates personalized, age-appropriate bedtime stories using AI, helping kids build healthy sleep routines while giving parents a break.

**Every story is an educational opportunity, not just entertainment.** Stories naturally weave in real-world lessons — how to call 911 in an emergency, basic math through counting adventures, learning to share with friends, understanding emotions, hygiene habits, stranger danger, and more. The educational content is embedded in the narrative so kids absorb it without feeling like they're being taught.

**Language skill development is a core pillar.** Stories can be generated in multiple languages (English, Spanish, Chinese, French, etc.) to support bilingual families or kids learning a new language. A single story can be told in the child's native language first, then replayed in a target language — turning bedtime into a natural language immersion experience. Vocabulary from each story is tracked and revisited across future stories to reinforce learning.

The key differentiators are:
- **Deep personalization** — the child's name, interests, and preferences are woven into every story
- **Education-first design** — every story teaches something valuable for the child's age
- **Multilingual storytelling** — one story, multiple languages, natural language learning

---

## App Name Suggestions

- **DreamTale** (recommended — evokes bedtime + storytelling)
- SleepyStory
- NightNest
- TaleTime
- StarStory

---

## Core Features (MVP)

### 1. User Onboarding
- Parent creates account (email or Google/Apple sign-in)
- Add child profile: **nickname**, **age** (2-10), **interests** (pick 3-5 from list + freeform), **fears to avoid** (optional, e.g., "spiders", "loud thunder")
- Set **bedtime goal** (e.g., 8:00 PM) for routine reminders
- Tutorial: generate first story together

### 2. Story Generation
- Parent enters **a few keywords** as today's topic (e.g., "dinosaurs, sharing", "rainy day, counting") — or leaves it blank for a **totally random** AI-chosen theme
- Keywords are flexible: can be a theme ("space"), a lesson ("learning to share"), a situation ("first day at school"), or just a mood ("cozy")
- AI generates a **~1 minute story** (~150-200 words, adjusted by age)
- Story is **personalized**: uses kid's name 2-3 times naturally, incorporates their interests
- Story is **educational**: every story teaches something — life skills (emergency calls, hygiene), academics (counting, colors, basic science), or social skills (sharing, empathy, kindness)
- **Multilingual support**: story can be generated in the kid's primary language, then regenerated in a second language for language learning — same story, different language
- Story has a **calm, peaceful ending** that encourages sleep
- Loading screen shows soothing animation (~10-15 seconds generation time)

### 3. Audio Playback (TTS)
- Every story auto-generates audio via text-to-speech
- Audio player: play/pause, speed control (0.8x for sleepy mode), sleep timer
- Background play supported (parent can close screen)
- Optional: ambient background sounds (rain, ocean, crickets)

### 4. Interactive Chat Interface (ChatGPT-style — Core UX)
The main interface is a **persistent chat**, always available — not a secondary feature. Designed like ChatGPT:

- **Chat area (center)**: ongoing conversation with the AI storyteller. User types keywords, asks for stories, requests modifications, all in one flow
- **Saved stories sidebar (left)**: list of saved/favorited stories for quick access and replay — similar to ChatGPT's conversation history sidebar
- The chat is **always active** — user can say "make the dragon friendly", "tell it again but in Spanish", "change the ending to be funnier", "now make a story about going to the dentist" at any point
- AI responds conversationally and regenerates or adjusts stories inline
- Modifications are **free** (no credit cost) — encourages engagement
- Exact layout to be finalized during UI design phase

### 5. Save & Organize Stories
- User can **save** any story they love from the chat (adds it to the sidebar)
- Saved stories are browsable, grouped by date or kid profile
- Quick replay (text + audio) from the sidebar
- Delete or archive old stories

### 6. Sleep Routine Features
- **Bedtime reminder** notification 15 min before target bedtime
- **Wind-down mode**: dark theme, reduced brightness, gentle animations auto-enabled in the evening
- **Bedtime streak tracker**: "5 nights in a row!" — builds habit
- **Sleepy meter**: stories get progressively calmer as the week goes on, adapting to patterns

---

## Additional Feature Ideas

### Engagement & Retention
- **Famous book series style**: stories can be generated "in the style of" beloved children's series — **Pete the Cat** (cool, relaxed tone), **Curious George** (exploration & curiosity), **The Very Hungry Caterpillar** (repetitive structure, counting), **Goodnight Moon** (calm, rhythmic). These high-quality narrative styles are familiar to kids and parents, making AI stories feel premium and trustworthy. (Note: use style/tone inspiration, not copyrighted characters — e.g., "a cool, laid-back cat who always stays positive" rather than "Pete the Cat")
- **Recurring companion character**: a friendly character (e.g., a stuffed bear named Luna) that appears across stories, growing with the kid — creates attachment and continuity
- **Choose-your-own-adventure mode** (ages 6+): mid-story choices ("Should Mia explore the cave or follow the river?") — makes stories interactive
- **Story of the day**: daily push notification with a themed teaser ("Tonight: a rainy day adventure for Emma!")
- **Seasonal/holiday stories**: auto-themed for Christmas, Halloween, birthdays, first day of school, etc.
- **Vocabulary builder**: new words from stories collected in a "Word Garden" — kids can review and learn them, especially useful for multilingual stories
- **Story stickers/badges**: earn collectible stickers for milestones (10 stories, tried a new theme, 7-day streak, first story in a new language)

### Social Sharing
- **Share to social media**: generate a shareable link for any saved story
- Link opens a **public story page** with audio player + full text transcript — no account needed to view
- Beautiful, branded share cards for Instagram/WeChat/WhatsApp/Facebook (auto-generated preview image with story title + kid-friendly illustration)
- Parents can share "Tonight's bedtime story for Emma" — great for grandparents, friends, and social media engagement
- Optional: make stories private (default) or shareable (parent chooses per story)
- Shared stories act as **organic marketing** — friends see the app in action

### Family Features
- **Multiple kid profiles** (up to 5 per family)
- **Parent dashboard**: weekly report — stories told, educational themes covered, bedtime consistency, engagement patterns
- **Story series**: multi-part stories that continue across nights ("Part 2 of The Moon Garden")
- **Family story time**: collaborative mode where parent and kid build a story together through the chat

### Premium / Differentiators
- **Parent voice cloning**: record 2-3 minutes of your voice → stories narrated in your voice (huge differentiator — kids hear mom/dad even when they're not there)
- **AI illustrations**: each story gets 1-2 simple, dreamy illustrations
- **Offline story packs**: pre-generate 5 stories for trips/airplane mode
- **Smart home integration**: connect to Philips Hue to auto-dim lights when story starts
- **Lullaby mode**: after story ends, transition into gentle background sounds or lullaby music for continued sleep support

---

## Monetization Strategy

### Free Tier
- **3 stories total** (lifetime) — enough to experience personalization magic
- Basic TTS voice
- Single kid profile
- Non-intrusive banner ads (COPPA compliant, contextual only — no behavioral targeting)

### Credit System (Pay-as-you-go)
| Pack | Price | Per Story |
|------|-------|-----------|
| 10 credits | $4.99 | $0.50 |
| 25 credits | $9.99 | $0.40 |
| 50 credits | $14.99 | $0.30 |
| 100 credits | $24.99 | $0.25 |

- 1 credit = 1 story
- Story modifications = free
- Story with illustration = 2 credits
- Bonus credits: referral (+5), app review (+3), weekly active (+1)

### Subscription (Better Value)
| Plan | Price | Includes |
|------|-------|----------|
| Premium | $9.99/mo | Unlimited stories, premium voices, 5 kid profiles, illustrations, no ads, parent dashboard |
| Family | $14.99/mo | All premium + voice cloning, 10 profiles, offline packs, sharing |

### Ad Strategy (COPPA Compliant)
- Contextual ads only (parenting/family products) — **no behavioral targeting for kids under 13**
- Banner ads between stories, never during playback
- No video interruptions
- Use Google AdMob with "child-directed" setting enabled

---

## Tech Stack

### Frontend: React Native (Expo)
- Cross-platform: iOS, Android, Web from one codebase
- Key libraries: `expo-av` (audio), `zustand` (state), `react-query` (API), `expo-sqlite` (offline cache)

### Backend: Python FastAPI
- Async-first for concurrent story generation
- Celery + Redis for async job queue (story generation is ~10-15s)
- PostgreSQL (Supabase) for data + auth
- Cloudflare R2 for audio file storage

### Self-Deployed LLM

**Recommended model: Qwen2.5-14B-Instruct**
- Excellent creative writing quality and instruction following
- Fits on a single RTX 4090 (24GB) with 4-bit quantization
- ~10-15 tokens/sec → ~15s for a 200-word story
- Apache 2.0 license (commercial use OK)
- Served via **vLLM** (fast inference with automatic batching)

**Hardware options:**
| Setup | GPU | Cost/month | Throughput |
|-------|-----|-----------|------------|
| MVP | 1x RTX 4090 (RunPod) | ~$300 | 2-3 concurrent |
| Growth | 1x A100 40GB | ~$600 | 4-5 concurrent |
| Scale | 2x A100 40GB | ~$1,200 | 8-10 concurrent |

**Fallback chain** (if self-hosted goes down):
1. OpenRouter API (Qwen 72B)
2. OpenAI GPT-4o-mini
3. Pre-written template stories (personalized by string replacement)

### Text-to-Speech

**Primary: Coqui XTTS v2** (self-hosted, free, supports voice cloning)
**Fallback: Google Cloud TTS** (reliable, cheap)
**Premium: ElevenLabs** (best quality, for subscribers)

---

## Architecture Overview

```
React Native App (iOS/Android/Web)
        │
        │ REST + WebSocket (story streaming)
        ▼
   FastAPI Backend (Railway/Render)
        │
   ┌────┼────────────────┐
   │    │                 │
   ▼    ▼                 ▼
Supabase  Redis         PostgreSQL
 (Auth)   (Queue/Cache)  (Data)
            │
      ┌─────┼─────┐
      ▼           ▼
  LLM Worker   TTS Worker
  (vLLM on     (Coqui XTTS
   RunPod)      or API)
                  │
                  ▼
            Cloudflare R2
            (Audio Storage)
```

---

## Key Backend Design

### Prompt Engineering (core of story quality)

```python
SYSTEM_PROMPT = """You are a gentle children's storyteller for bedtime.

RULES:
- Exactly {target_words} words (±10%)
- Age-appropriate for {age} years old
- Use child's name "{child_name}" naturally, 2-3 times
- Calm, soothing tone — ending must encourage sleep
- EDUCATIONAL GOAL: Naturally teach about {educational_theme} through the story
  (e.g., if "emergency calls" — show the character learning when to call 911)
- Language: {language} (if bilingual mode, keep vocabulary accessible for learners)
- Story style inspiration: {story_style} (e.g., "calm and repetitive like Goodnight Moon")
- AVOID: {fears_to_avoid}
- AVOID recent themes: {recent_themes}

Parent's keywords for today: {keywords}  ← use these as the story's topic/theme
If no keywords provided, choose a creative theme from: {theme} | {setting}

Lesson: {lesson}
"""
```

### Age-Appropriate Content Config

| Age | Words | Vocabulary | Themes | Educational Focus |
|-----|-------|-----------|--------|-------------------|
| 2-3 | 100 | Simple, repetitive | Animals, colors, family | Counting, emotions, routines, hygiene (brushing teeth, washing hands) |
| 4-5 | 150 | Basic + new words | Friendship, nature | Sharing, kindness, basic safety (don't talk to strangers, hold hands crossing street), seasons, weather |
| 6-7 | 200 | Elementary | Courage, discovery, teamwork | Emergency skills (calling 911), basic math in stories, recycling, empathy, simple science |
| 8-10 | 250 | Intermediate | Mystery, space, history | Critical thinking, problem-solving, money basics, geography, history, science concepts |

### Multilingual Story Config
- Stories can be generated in: **English, Spanish, Chinese (Simplified), French, German, Japanese, Korean** (expandable)
- **Language learning mode**: same story generated in 2 languages — native first, then target language
- Vocabulary difficulty adjusted: simpler words in the target language for beginners
- TTS voice matched to language (native-sounding voices per language)
- **Vocabulary tracker**: words introduced in target language are saved and revisited in future stories

### Story Diversity System
- Track last 10 stories per kid across 4 dimensions: **theme, characters, setting, educational topic**
- Exclude recently used values when generating next story
- Rotate educational topics cyclically (cover all before repeating)
- Use **pgvector** embeddings to detect similarity and prevent "same but different" stories

### Content Safety (Multi-Layer)
1. **Pre-filter**: block inappropriate user prompts
2. **Post-filter**: validate generated story with safety model (Llama Guard)
3. **Tone check**: ensure story is calm enough for bedtime (reject overly exciting content)
4. **Human review queue**: flag low-confidence stories for manual review
5. **Parent report**: thumbs-down → feedback loop for improvement

---

## Database Schema (Key Tables)

- **users**: parent account, subscription tier, credit balance, COPPA consent
- **kids**: nickname (encrypted), age, interests, fears, bedtime goal, content strictness level, **primary_language**, **learning_languages[]**
- **stories**: text, audio_url, theme, educational_topic, safety_score, **is_saved** (user explicitly saved), play_count, completion_rate, rating, **language**, **keywords_used**, **story_style**
- **story_translations**: story_id, language, translated_text, audio_url — same story in different languages
- **story_versions**: modifications linked to original story (from chat interactions)
- **shared_stories**: story_id, share_token, share_url, is_public, created_at, view_count — powers social sharing links
- **chat_sessions**: conversation history per kid (ChatGPT-style chat persistence)
- **credit_transactions**: full audit trail of credits (purchases, usage, bonuses)
- **bedtime_sessions**: date, time, duration, story played — powers parent dashboard
- **educational_topics_covered**: tracks which topics each kid has learned about
- **vocabulary_learned**: kid_id, word, language, first_seen_story_id, times_reinforced — tracks language learning progress
- **story_embeddings**: pgvector for similarity detection

---

## Safety & Compliance (COPPA)

This is critical — the app targets children under 13.

- **Parental consent** required before any data collection (verified via credit card or ID)
- **No behavioral advertising** — only contextual ads
- **Minimal data collection**: only nickname + age + interests (no full name, no photos, no location)
- **Kid data encrypted** at rest
- **Parental controls**: view all stories, delete data, block themes, set content strictness (1-5)
- **Data retention**: auto-delete after 1 year of inactivity, parent can delete anytime
- **Age gate**: math problem or password for in-app purchases (kids can't buy accidentally)
- **Legal review** before launch

---

## Implementation Roadmap

### Phase 1: MVP (8-10 weeks)
| Week | Focus |
|------|-------|
| 1-2 | Infrastructure setup: Supabase, FastAPI skeleton, deploy Qwen on RunPod, DB schema, React Native shell |
| 3-4 | Core story engine: prompt engineering, context builder, diversity tracker, safety filter, TTS integration |
| 5-6 | App screens: onboarding, story generation, playback, history/favorites |
| 7-8 | Monetization: credit system, Stripe/RevenueCat, ads, COPPA consent flows |
| 9-10 | Beta test with 50 families, iterate, security audit, soft launch |

### Phase 2: Growth (months 2-4)
- Interactive chat/modification
- Multiple kid profiles
- Premium subscription
- Better TTS (Coqui XTTS)
- Offline mode
- Parent dashboard v2

### Phase 3: Differentiation (months 5+)
- Parent voice cloning
- AI illustrations
- Story series/continuations
- Smart home integration
- Multi-language support
- Fine-tuned model on user ratings

---

## Verification Plan

1. **Story quality**: Generate 50 test stories across all age groups, manually evaluate for quality, age-appropriateness, personalization, length accuracy, and educational content
2. **Keyword input**: Test with various keyword combinations, test blank input (random mode), verify stories reflect the given keywords
3. **Educational content**: Verify each age group's stories actually teach the intended lessons (not just mention them)
4. **Multilingual**: Generate same story in 3+ languages, verify TTS works in each, verify vocabulary tracking
5. **Chat interface**: Test full conversation flow — generate → modify → modify again → save → access from sidebar
6. **Social sharing**: Generate share link, open in incognito browser, verify audio plays and transcript displays without login
7. **Safety**: Run adversarial prompts through the system, verify all are caught by safety filters
8. **Audio**: Verify TTS output sounds natural and calm in all supported languages, test playback on iOS and Android
9. **Credits**: Test full purchase flow (Stripe test mode), verify credit deduction and balance tracking
10. **COPPA**: Review all data flows with checklist, ensure no PII leaks to third parties or shared story pages
11. **Performance**: Load test story generation — verify <20s p95 latency under 10 concurrent users
12. **Fallback**: Kill LLM server, verify fallback chain activates and stories still generate
13. **E2E**: Full flow — sign up → add kid → generate 3 free stories (with keywords + random) → chat to modify → save favorite → share to social → buy credits → generate multilingual story
