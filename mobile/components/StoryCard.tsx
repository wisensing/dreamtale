import React from "react";
import { View, Text, TouchableOpacity, StyleSheet } from "react-native";
import { Colors, Shadows } from "../constants/colors";
import { Story } from "../types";

interface StoryCardProps {
  story: Story;
  onPress: (story: Story) => void;
  onSave?: (story: Story) => void;
}

export default function StoryCard({ story, onPress, onSave }: StoryCardProps) {
  const preview = story.text.length > 80 ? story.text.slice(0, 80) + "..." : story.text;

  return (
    <TouchableOpacity style={styles.card} onPress={() => onPress(story)} activeOpacity={0.7}>
      <View style={styles.content}>
        <View style={styles.header}>
          <Text style={styles.theme}>{story.theme || "Story"}</Text>
          {story.language !== "en" && (
            <View style={styles.languageBadge}>
              <Text style={styles.languageText}>{story.language.toUpperCase()}</Text>
            </View>
          )}
        </View>
        <Text style={styles.preview}>{preview}</Text>
        <View style={styles.footer}>
          <Text style={styles.meta}>
            {story.educational_topic} | Played {story.play_count}x
          </Text>
          {onSave && (
            <TouchableOpacity onPress={() => onSave(story)} hitSlop={{ top: 10, bottom: 10, left: 10, right: 10 }}>
              <Text style={styles.saveButton}>{story.is_saved ? "Saved" : "Save"}</Text>
            </TouchableOpacity>
          )}
        </View>
      </View>
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: Colors.surface,
    borderRadius: 12,
    marginBottom: 12,
    ...Shadows.small,
  },
  content: {
    padding: 16,
  },
  header: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 8,
  },
  theme: {
    fontSize: 16,
    fontWeight: "600",
    color: Colors.text,
    flex: 1,
  },
  languageBadge: {
    backgroundColor: Colors.primaryLight,
    borderRadius: 8,
    paddingHorizontal: 8,
    paddingVertical: 2,
  },
  languageText: {
    fontSize: 11,
    fontWeight: "700",
    color: Colors.primaryDark,
  },
  preview: {
    fontSize: 14,
    color: Colors.textSecondary,
    lineHeight: 20,
    marginBottom: 8,
  },
  footer: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
  },
  meta: {
    fontSize: 12,
    color: Colors.textSecondary,
  },
  saveButton: {
    fontSize: 13,
    fontWeight: "600",
    color: Colors.primary,
  },
});
