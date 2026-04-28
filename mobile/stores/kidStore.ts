import { create } from "zustand";
import { Kid } from "../types";
import api from "../services/api";

interface KidState {
  kids: Kid[];
  activeKidId: string | null;
  isLoading: boolean;

  fetchKids: () => Promise<void>;
  addKid: (kid: Partial<Kid>) => Promise<Kid>;
  updateKid: (id: string, updates: Partial<Kid>) => Promise<void>;
  deleteKid: (id: string) => Promise<void>;
  setActiveKid: (id: string) => void;
  getActiveKid: () => Kid | undefined;
}

export const useKidStore = create<KidState>((set, get) => ({
  kids: [],
  activeKidId: null,
  isLoading: false,

  fetchKids: async () => {
    set({ isLoading: true });
    try {
      const { data } = await api.get("/kids");
      const kids = data as Kid[];
      set({ kids, activeKidId: kids[0]?.id || null, isLoading: false });
    } catch {
      set({ isLoading: false });
    }
  },

  addKid: async (kidData) => {
    const { data } = await api.post("/kids", kidData);
    const kid = data as Kid;
    set((state) => ({
      kids: [...state.kids, kid],
      activeKidId: state.activeKidId || kid.id,
    }));
    return kid;
  },

  updateKid: async (id, updates) => {
    const { data } = await api.put(`/kids/${id}`, updates);
    set((state) => ({
      kids: state.kids.map((k) => (k.id === id ? (data as Kid) : k)),
    }));
  },

  deleteKid: async (id) => {
    await api.delete(`/kids/${id}`);
    set((state) => ({
      kids: state.kids.filter((k) => k.id !== id),
      activeKidId: state.activeKidId === id ? state.kids[0]?.id || null : state.activeKidId,
    }));
  },

  setActiveKid: (id) => set({ activeKidId: id }),

  getActiveKid: () => {
    const { kids, activeKidId } = get();
    return kids.find((k) => k.id === activeKidId);
  },
}));
