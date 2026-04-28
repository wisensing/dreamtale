import React, { useEffect } from "react";
import { View, Text, FlatList, StyleSheet, TouchableOpacity } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { useRouter } from "expo-router";
import { Colors } from "../../constants/colors";
import { useStoryStore } from "../../stores/storyStore";
import { useKidStore } from "../../stores/kidStore";
import StoryCard from "../../components/StoryCard";
import { Story } from "../../types";

export default function StoriesScreen() {
  const { stories, fetchStories, saveStory } = useStoryStore();
  const { kids, activeKidId, fetchKids } = useKidStore();
  const router = useRouter();

  useEffect(() => {
    fetchKids();
  }, []);

  useEffect(() => {
    if (activeKidId) {
      fetchStories({ kid_id: activeKidId });
    }
  }, [activeKidId]);

  const handlePressStory = (story: Story) => {
    useStoryStore.getState().setCurrentStory(story);
    router.push(`/story/${story.id}`);
  };

  return (
    <SafeAreaView style={styles.container} edges={["top"]}>
      <View style={styles.header}>
        <Text style={styles.title}>My Stories</Text>
        {kids.find((k) => k.id === activeKidId) && (
          <Text style={styles.subtitle}>For {kids.find((k) => k.id === activeKidId)?.nickname}</Text>
        )}
      </View>

      <FlatList
        data={stories}
        keyExtractor={(item) => item.id}
        renderItem={({ item }) => (
          <StoryCard
            story={item}
            onPress={handlePressStory}
            onSave={(s) => saveStory(s.id, !s.is_saved)}
          />
        )}
        contentContainerStyle={styles.list}
        ListEmptyComponent={
          <View style={styles.empty}>
            <Text style={styles.emptyEmoji}>📖</Text>
            <Text style={styles.emptyTitle}>No stories yet</Text>
            <Text style={styles.emptySubtitle}>
              Go to the Chat tab and type some keywords to create your first story!
            </Text>
            <TouchableOpacity style={styles.ctaButton} onPress={() => router.push("/(tabs)/chat")}>
              <Text style={styles.ctaText}>Create a Story</Text>
            </TouchableOpacity>
          </View>
        }
      />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.background },
  header: {
    paddingHorizontal: 20,
    paddingTop: 16,
    paddingBottom: 8,
    backgroundColor: Colors.surface,
    borderBottomWidth: 1,
    borderBottomColor: Colors.border,
  },
  title: { fontSize: 24, fontWeight: "700", color: Colors.text },
  subtitle: { fontSize: 14, color: Colors.textSecondary, marginTop: 2 },
  list: { paddingHorizontal: 16, paddingTop: 16, paddingBottom: 40 },
  empty: { alignItems: "center", paddingVertical: 60, paddingHorizontal: 32 },
  emptyEmoji: { fontSize: 64, marginBottom: 12 },
  emptyTitle: { fontSize: 20, fontWeight: "700", color: Colors.text, marginBottom: 8 },
  emptySubtitle: { fontSize: 15, color: Colors.textSecondary, textAlign: "center", lineHeight: 22, marginBottom: 24 },
  ctaButton: {
    backgroundColor: Colors.primary,
    borderRadius: 12,
    paddingHorizontal: 24,
    paddingVertical: 12,
  },
  ctaText: { fontSize: 16, fontWeight: "600", color: Colors.textLight },
});
