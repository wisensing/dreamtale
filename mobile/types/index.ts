export interface User {
  id: string;
  email: string;
  subscription_tier: "free" | "premium" | "family";
  credit_balance: number;
  coppa_consent: boolean;
  content_strictness: number;
  created_at: string;
}

export interface Kid {
  id: string;
  nickname: string;
  age: number;
  interests: string[];
  fears: string[];
  bedtime_goal: string | null;
  primary_language: string;
  learning_languages: string[];
  companion_name: string | null;
  created_at: string;
}

export interface Story {
  id: string;
  kid_id: string;
  text: string;
  audio_url: string | null;
  theme: string;
  educational_topic: string;
  story_style: string;
  language: string;
  keywords_used: string[];
  is_saved: boolean;
  play_count: number;
  safety_score: number;
  parent_rating: number | null;
  created_at: string;
}

export interface ChatSession {
  id: string;
  kid_id: string;
  title: string;
  created_at: string;
  updated_at: string;
}

export interface ChatMessage {
  id: string;
  chat_session_id: string;
  role: "user" | "assistant";
  content: string;
  story_id: string | null;
  created_at: string;
}

export interface ChatSessionDetail extends ChatSession {
  messages: ChatMessage[];
}

export interface CreditTransaction {
  id: string;
  amount: number;
  transaction_type: "purchase" | "usage" | "bonus" | "refund";
  description: string;
  created_at: string;
}

export interface SharedStory {
  story_text: string;
  story_audio_url: string | null;
  story_theme: string;
  story_language: string;
  kid_nickname: string;
  share_token: string;
}

export interface BedtimeStreak {
  current_streak: number;
  longest_streak: number;
  last_bedtime_date: string | null;
}

export interface BedtimeStats {
  total_sessions: number;
  avg_duration_minutes: number | null;
  stories_played: number;
  streak: BedtimeStreak;
  weekly_data: { date: string; bedtime: string; duration: number | null }[];
}
