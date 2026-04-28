import { create } from "zustand";
import { User } from "../types";
import { getSession, signIn, signUp, signOut } from "../services/auth";
import api from "../services/api";

interface AuthState {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;

  initialize: () => Promise<void>;
  login: (email: string, password: string) => Promise<void>;
  signup: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  refreshUser: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isLoading: true,
  isAuthenticated: false,

  initialize: async () => {
    try {
      const session = await getSession();
      if (session) {
        const { data } = await api.get("/auth/me");
        set({ user: data, isAuthenticated: true, isLoading: false });
      } else {
        set({ user: null, isAuthenticated: false, isLoading: false });
      }
    } catch {
      set({ user: null, isAuthenticated: false, isLoading: false });
    }
  },

  login: async (email, password) => {
    await signIn(email, password);
    const { data } = await api.get("/auth/me");
    set({ user: data, isAuthenticated: true });
  },

  signup: async (email, password) => {
    await signUp(email, password);
    // After signup, we need to create user in our DB too
    // The backend auth/signup endpoint handles this
    set({ isAuthenticated: true });
  },

  logout: async () => {
    await signOut();
    set({ user: null, isAuthenticated: false });
  },

  refreshUser: async () => {
    try {
      const { data } = await api.get("/auth/me");
      set({ user: data });
    } catch {
      // ignore
    }
  },
}));
