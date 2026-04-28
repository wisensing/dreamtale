import api from "./api";
import { Story, SharedStory } from "../types";

export async function generateStory(params: {
  kid_id: string;
  keywords?: string;
  language?: string;
  story_style?: string;
}): Promise<Story> {
  const { data } = await api.post("/stories/generate", params);
  return data;
}

export async function modifyStory(
  storyId: string,
  modification: string,
  language?: string
): Promise<Story> {
  const { data } = await api.post(`/stories/${storyId}/modify`, { modification, language });
  return data;
}

export async function listStories(params?: {
  kid_id?: string;
  is_saved?: boolean;
  limit?: number;
  offset?: number;
}): Promise<Story[]> {
  const { data } = await api.get("/stories", { params });
  return data;
}

export async function getStory(storyId: string): Promise<Story> {
  const { data } = await api.get(`/stories/${storyId}`);
  return data;
}

export async function saveStory(storyId: string, isSaved: boolean): Promise<Story> {
  const { data } = await api.post(`/stories/${storyId}/save`, { is_saved: isSaved });
  return data;
}

export async function shareStory(storyId: string, isPublic = true): Promise<SharedStory> {
  const { data } = await api.post(`/stories/${storyId}/share`, { is_public: isPublic });
  return data;
}

export async function getSharedStory(token: string): Promise<SharedStory> {
  const { data } = await api.get(`/stories/shared/${token}`);
  return data;
}

export async function deleteStory(storyId: string): Promise<void> {
  await api.delete(`/stories/${storyId}`);
}

export async function translateStory(
  storyId: string,
  targetLanguage: string
): Promise<{ id: string; language: string; translated_text: string; audio_url: string | null }> {
  const { data } = await api.post(`/stories/${storyId}/translate`, {
    target_language: targetLanguage,
  });
  return data;
}
