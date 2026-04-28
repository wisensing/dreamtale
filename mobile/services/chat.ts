import api from "./api";
import { ChatSession, ChatSessionDetail, ChatMessage } from "../types";

export async function createChatSession(params: {
  kid_id: string;
  title?: string;
}): Promise<ChatSession> {
  const { data } = await api.post("/chat/sessions", params);
  return data;
}

export async function listChatSessions(kidId: string): Promise<ChatSession[]> {
  const { data } = await api.get("/chat/sessions", { params: { kid_id: kidId } });
  return data;
}

export async function getChatSession(sessionId: string): Promise<ChatSessionDetail> {
  const { data } = await api.get(`/chat/sessions/${sessionId}`);
  return data;
}

export async function sendMessage(
  sessionId: string,
  content: string
): Promise<ChatMessage> {
  const { data } = await api.post(`/chat/sessions/${sessionId}/messages`, { content });
  return data;
}
