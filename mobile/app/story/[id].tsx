import React, { useEffect } from "react";
import { View, Text, ScrollView, TouchableOpacity, StyleSheet, Share, Alert } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { useLocalSearchParams, useRouter } from "expo-router";
import { Colors } from "../../constants/colors";
import { useStoryStore } from "../../stores/storyStore";
import AudioPlayer from "../../components/AudioPlayer";

export default function StoryDetailScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const router = useRouter();
  const { currentStory, saveStory, shareStory, setCurrentStory } = useStoryStore();

  useEffect(() => {
    return () => {
      setCurrentStory(null);
    };
  }, []);

  if (!currentStory) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.empty}>
          <Text style={styles.emptyText}>Story not found</Text>
          <TouchableOpacity onPress={() => router.back()}>
            <Text style={styles.backLink}>Go back</Text>
          </TouchableOpacity>
        </View>
      </SafeAreaView>
    );
  }

  const story = currentStory;

  const handleShare = async () => {
    try {
      const shared = await shareStory(story.id);
      await Share.share({
        message: `Read this bedtime story: ${shared.story_text.slice(0, 100)}...`,
        url: `https://dreamtale.app/s/${shared.share_token}`,
      });
    } catch {
      Alert.alert("Error", "Could not share story");
    }
  };

  return (
    <SafeAreaView style={styles.container} edges={["top"]}>
      {/* Header */}
      <View style={styles.header}>
        <TouchableOpacity onPress={() => router.back()}>
          <Text style={styles.closeButton}>Close</Text>
        </TouchableOpacity>
        <View style={styles.headerActions}>
          <TouchableOpacity onPress={() => saveStory(story.id, !story.is_saved)}>
            <Text style={styles.saveButton}>{story.is_saved ? "Saved" : "Save"}</Text>
          </TouchableOpacity>
          <TouchableOpacity onPress={handleShare} style={{ marginLeft: 16 }}>
            <Text style={styles.shareButton}>Share</Text>
          </TouchableOpacity>
        </View>
      </View>

      <ScrollView style={styles.content} contentContainerStyle={styles.scrollContent}>
        {/* Story meta */}
        <View style={styles.meta}>
          <Text style={styles.theme}>{story.theme || "Story"}</Text>
          <Text style={styles.topic}>{story.educational_topic}</Text>
          {story.language !== "en" && (
            <View style={styles.languageBadge}>
              <Text style={styles.languageText}>{story.language.toUpperCase()}</Text>
            </View>
          )}
        </View>

        {/* Story text */}
        <Text style={styles.storyText}>{story.text}</Text>

        {/* Audio player */}
        <View style={styles.playerSection}>
          <AudioPlayer audioUrl={story.audio_url} title={story.theme} />
        </View>

        {/* Keywords */}
        {story.keywords_used.length > 0 && (
          <View style={styles.keywordsSection}>
            <Text style={styles.keywordsLabel}>Keywords</Text>
            <View style={styles.keywordsRow}>
              {story.keywords_used.map((kw, i) => (
                <View key={i} style={styles.keywordChip}>
                  <Text style={styles.keywordText}>{kw}</Text>
                </View>
              ))}
            </View>
          </View>
        )}
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.background },
  header: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    paddingHorizontal: 16,
    paddingVertical: 12,
    backgroundColor: Colors.surface,
    borderBottomWidth: 1,
    borderBottomColor: Colors.border,
  },
  closeButton: { fontSize: 16, color: Colors.primary, fontWeight: "600" },
  headerActions: { flexDirection: "row", alignItems: "center" },
  saveButton: { fontSize: 16, color: Colors.primary, fontWeight: "600" },
  shareButton: { fontSize: 16, color: Colors.secondary, fontWeight: "600" },
  content: { flex: 1 },
  scrollContent: { paddingHorizontal: 20, paddingVertical: 16, paddingBottom: 40 },
  meta: { marginBottom: 16 },
  theme: { fontSize: 24, fontWeight: "700", color: Colors.text, marginBottom: 4 },
  topic: { fontSize: 14, color: Colors.primary, fontWeight: "500" },
  languageBadge: {
    alignSelf: "flex-start",
    backgroundColor: Colors.primaryLight,
    borderRadius: 8,
    paddingHorizontal: 8,
    paddingVertical: 2,
    marginTop: 6,
  },
  languageText: { fontSize: 11, fontWeight: "700", color: Colors.primaryDark },
  storyText: {
    fontSize: 17,
    lineHeight: 28,
    color: Colors.text,
    marginBottom: 24,
  },
  playerSection: { marginBottom: 24 },
  keywordsSection: { marginBottom: 16 },
  keywordsLabel: { fontSize: 13, fontWeight: "600", color: Colors.textSecondary, marginBottom: 8 },
  keywordsRow: { flexDirection: "row", flexWrap: "wrap", gap: 6 },
  keywordChip: {
    backgroundColor: Colors.chatBubble,
    borderRadius: 8,
    paddingHorizontal: 10,
    paddingVertical: 4,
  },
  keywordText: { fontSize: 13, color: Colors.primary },
  empty: { flex: 1, justifyContent: "center", alignItems: "center" },
  emptyText: { fontSize: 16, color: Colors.textSecondary, marginBottom: 12 },
  backLink: { fontSize: 16, color: Colors.primary, fontWeight: "600" },
});
