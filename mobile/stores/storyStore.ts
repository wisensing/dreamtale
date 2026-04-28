import { create } from "zustand";
import { Story } from "../types";
import * as storyService from "../services/stories";

interface StoryState {
  stories: Story[];
  savedStories: Story[];
  currentStory: Story | null;
  isGenerating: boolean;
  isLoading: boolean;

  fetchStories: (params?: { kid_id?: string; is_saved?: boolean }) => Promise<void>;
  fetchSavedStories: (kidId?: string) => Promise<void>;
  generateStory: (params: {
    kid_id: string;
    keywords?: string;
    language?: string;
    story_style?: string;
  }) => Promise<Story>;
  modifyStory: (storyId: string, modification: string, language?: string) => Promise<Story>;
  saveStory: (storyId: string, isSaved: boolean) => Promise<void>;
  deleteStory: (storyId: string) => Promise<void>;
  setCurrentStory: (story: Story | null) => void;
}

export const useStoryStore = create<StoryState>((set, get) => ({
  stories: [],
  savedStories: [],
  currentStory: null,
  isGenerating: false,
  isLoading: false,

  fetchStories: async (params) => {
    set({ isLoading: true });
    try {
      const stories = await storyService.listStories(params);
      set({ stories, isLoading: false });
    } catch {
      set({ isLoading: false });
    }
  },

  fetchSavedStories: async (kidId) => {
    try {
      const stories = await storyService.listStories({ kid_id: kidId, is_saved: true });
      set({ savedStories: stories });
    } catch {
      // ignore
    }
  },

  generateStory: async (params) => {
    set({ isGenerating: true });
    try {
      const story = await storyService.generateStory(params);
      set((state) => ({
        stories: [story, ...state.stories],
        currentStory: story,
        isGenerating: false,
      }));
      return story;
    } catch {
      set({ isGenerating: false });
      throw new Error("Failed to generate story");
    }
  },

  modifyStory: async (storyId, modification, language) => {
    set({ isGenerating: true });
    try {
      const story = await storyService.modifyStory(storyId, modification, language);
      set((state) => ({
        stories: state.stories.map((s) => (s.id === storyId ? story : s)),
        currentStory: story,
        isGenerating: false,
      }));
      return story;
    } catch {
      set({ isGenerating: false });
      throw new Error("Failed to modify story");
    }
  },

  saveStory: async (storyId, isSaved) => {
    const story = await storyService.saveStory(storyId, isSaved);
    set((state) => ({
      stories: state.stories.map((s) => (s.id === storyId ? story : s)),
      savedStories: isSaved
        ? [...state.savedStories, story]
        : state.savedStories.filter((s) => s.id !== storyId),
      currentStory: state.currentStory?.id === storyId ? story : state.currentStory,
    }));
  },

  deleteStory: async (storyId) => {
    await storyService.deleteStory(storyId);
    set((state) => ({
      stories: state.stories.filter((s) => s.id !== storyId),
      savedStories: state.savedStories.filter((s) => s.id !== storyId),
      currentStory: state.currentStory?.id === storyId ? null : state.currentStory,
    }));
  },

  setCurrentStory: (story) => set({ currentStory: story }),
}));
