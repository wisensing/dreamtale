import React, { useEffect, useState, useRef } from "react";
import {
  View,
  Text,
  FlatList,
  StyleSheet,
  TouchableOpacity,
  ActivityIndicator,
  KeyboardAvoidingView,
  Platform,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { Colors } from "../../constants/colors";
import { useChatStore } from "../../stores/chatStore";
import { useKidStore } from "../../stores/kidStore";
import { useAuthStore } from "../../stores/authStore";
import ChatBubble from "../../components/ChatBubble";
import ChatInput from "../../components/ChatInput";
import CreditBadge from "../../components/CreditBadge";
import Sidebar from "../../components/Sidebar";
import { useStoryStore } from "../../stores/storyStore";

export default function ChatScreen() {
  const { kids, activeKidId, fetchKids } = useKidStore();
  const { user, refreshUser } = useAuthStore();
  const {
    activeSession, messages, isSending, sessions,
    createSession, sendMessage, loadSession, fetchSessions,
  } = useChatStore();
  const { savedStories, fetchSavedStories, saveStory } = useStoryStore();
  const [sidebarVisible, setSidebarVisible] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);
  const flatListRef = useRef<FlatList>(null);

  useEffect(() => {
    fetchKids();
  }, []);

  useEffect(() => {
    if (activeKidId) {
      fetchSessions(activeKidId);
      fetchSavedStories(activeKidId);
      if (!activeSession) {
        createSession(activeKidId, "New Chat");
      }
    }
  }, [activeKidId]);

  useEffect(() => {
    // Scroll to bottom on new messages
    if (messages.length > 0) {
      setTimeout(() => flatListRef.current?.scrollToEnd({ animated: true }), 100);
    }
  }, [messages.length]);

  const handleSend = async (content: string) => {
    if (!activeSession) return;
    try {
      await sendMessage(content);
      await refreshUser();
    } catch (e: any) {
      // Error handled in store
    }
  };

  const kid = kids.find((k) => k.id === activeKidId);

  return (
    <SafeAreaView style={styles.container} edges={["top"]}>
      <KeyboardAvoidingView
        style={styles.container}
        behavior={Platform.OS === "ios" ? "padding" : undefined}
        keyboardVerticalOffset={0}
      >
        {/* Header */}
        <View style={styles.header}>
          <TouchableOpacity onPress={() => setSidebarVisible(true)}>
            <Text style={styles.sidebarButton}>📖</Text>
          </TouchableOpacity>
          <View style={styles.headerCenter}>
            <Text style={styles.headerTitle}>DreamTale</Text>
            {kid && <Text style={styles.headerSubtitle}>Stories for {kid.nickname}</Text>}
          </View>
          {user && <CreditBadge balance={user.credit_balance} tier={user.subscription_tier} />}
        </View>

        {/* Messages */}
        <FlatList
          ref={flatListRef}
          data={messages}
          keyExtractor={(item) => item.id}
          renderItem={({ item }) => <ChatBubble message={item} />}
          contentContainerStyle={styles.messageList}
          ListEmptyComponent={
            <View style={styles.empty}>
              <Text style={styles.emptyEmoji}>🌙</Text>
              <Text style={styles.emptyTitle}>Tell me what to dream about!</Text>
              <Text style={styles.emptySubtitle}>
                Type keywords like "dinosaurs, sharing" or just say "surprise me"
              </Text>
            </View>
          }
        />

        {/* Loading indicator for story generation */}
        {isSending && (
          <View style={styles.generating}>
            <ActivityIndicator size="small" color={Colors.primary} />
            <Text style={styles.generatingText}>Creating a story...</Text>
          </View>
        )}

        {/* Input */}
        <ChatInput onSend={handleSend} isLoading={isSending} />

        {/* Sidebar */}
        <Sidebar
          visible={sidebarVisible}
          onClose={() => setSidebarVisible(false)}
          stories={savedStories}
          kids={kids}
          activeKidId={activeKidId}
          onSelectKid={(id) => useKidStore.getState().setActiveKid(id)}
          onSelectStory={() => {}}
        />
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.background },
  header: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    paddingHorizontal: 16,
    paddingVertical: 12,
    backgroundColor: Colors.surface,
    borderBottomWidth: 1,
    borderBottomColor: Colors.border,
  },
  sidebarButton: { fontSize: 24, padding: 4 },
  headerCenter: { flex: 1, alignItems: "center" },
  headerTitle: { fontSize: 18, fontWeight: "700", color: Colors.text },
  headerSubtitle: { fontSize: 13, color: Colors.textSecondary },
  messageList: { paddingHorizontal: 8, paddingVertical: 12, flexGrow: 1 },
  empty: { flex: 1, justifyContent: "center", alignItems: "center", paddingHorizontal: 40, paddingVertical: 80 },
  emptyEmoji: { fontSize: 64, marginBottom: 12 },
  emptyTitle: { fontSize: 20, fontWeight: "700", color: Colors.text, marginBottom: 8, textAlign: "center" },
  emptySubtitle: { fontSize: 15, color: Colors.textSecondary, textAlign: "center", lineHeight: 22 },
  generating: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    paddingVertical: 8,
    backgroundColor: Colors.chatBubble,
  },
  generatingText: { marginLeft: 8, fontSize: 14, color: Colors.primary, fontWeight: "500" },
});
