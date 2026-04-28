import { create } from "zustand";
import { ChatSession, ChatMessage, ChatSessionDetail } from "../types";
import * as chatService from "../services/chat";

interface ChatState {
  sessions: ChatSession[];
  activeSession: ChatSessionDetail | null;
  messages: ChatMessage[];
  isSending: boolean;
  isLoading: boolean;

  fetchSessions: (kidId: string) => Promise<void>;
  createSession: (kidId: string, title?: string) => Promise<ChatSession>;
  loadSession: (sessionId: string) => Promise<void>;
  sendMessage: (content: string) => Promise<ChatMessage>;
  clearActiveSession: () => void;
}

export const useChatStore = create<ChatState>((set, get) => ({
  sessions: [],
  activeSession: null,
  messages: [],
  isSending: false,
  isLoading: false,

  fetchSessions: async (kidId) => {
    set({ isLoading: true });
    try {
      const sessions = await chatService.listChatSessions(kidId);
      set({ sessions, isLoading: false });
    } catch {
      set({ isLoading: false });
    }
  },

  createSession: async (kidId, title) => {
    const session = await chatService.createChatSession({
      kid_id: kidId,
      title: title || "New Chat",
    });
    set((state) => ({
      sessions: [session, ...state.sessions],
      activeSession: { ...session, messages: [] },
      messages: [],
    }));
    return session;
  },

  loadSession: async (sessionId) => {
    set({ isLoading: true });
    try {
      const detail = await chatService.getChatSession(sessionId);
      set({ activeSession: detail, messages: detail.messages, isLoading: false });
    } catch {
      set({ isLoading: false });
    }
  },

  sendMessage: async (content) => {
    const { activeSession } = get();
    if (!activeSession) throw new Error("No active session");

    set({ isSending: true });

    const userMessage: ChatMessage = {
      id: "temp-" + Date.now(),
      chat_session_id: activeSession.id,
      role: "user",
      content,
      story_id: null,
      created_at: new Date().toISOString(),
    };
    set((state) => ({ messages: [...state.messages, userMessage] }));

    try {
      const response = await chatService.sendMessage(activeSession.id, content);
      set((state) => ({
        messages: [...state.messages, response],
        isSending: false,
      }));
      return response;
    } catch {
      set({ isSending: false });
      throw new Error("Failed to send message");
    }
  },

  clearActiveSession: () => set({ activeSession: null, messages: [] }),
}));
