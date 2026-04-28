import React from "react";
import { View, Text, TouchableOpacity, FlatList, StyleSheet, Modal } from "react-native";
import { Colors } from "../constants/colors";
import { Story, Kid } from "../types";
import StoryCard from "./StoryCard";

interface SidebarProps {
  visible: boolean;
  onClose: () => void;
  stories: Story[];
  kids: Kid[];
  activeKidId: string | null;
  onSelectKid: (id: string) => void;
  onSelectStory: (story: Story) => void;
}

export default function Sidebar({
  visible,
  onClose,
  stories,
  kids,
  activeKidId,
  onSelectKid,
  onSelectStory,
}: SidebarProps) {
  return (
    <Modal visible={visible} animationType="slide" presentationStyle="pageSheet" onRequestClose={onClose}>
      <View style={styles.container}>
        <View style={styles.header}>
          <Text style={styles.title}>Saved Stories</Text>
          <TouchableOpacity onPress={onClose}>
            <Text style={styles.closeButton}>Close</Text>
          </TouchableOpacity>
        </View>

        {kids.length > 1 && (
          <FlatList
            horizontal
            data={kids}
            keyExtractor={(item) => item.id}
            renderItem={({ item }) => (
              <TouchableOpacity
                style={[styles.kidChip, item.id === activeKidId && styles.kidChipActive]}
                onPress={() => onSelectKid(item.id)}
              >
                <Text style={[styles.kidChipText, item.id === activeKidId && styles.kidChipTextActive]}>
                  {item.nickname}
                </Text>
              </TouchableOpacity>
            )}
            style={styles.kidList}
            showsHorizontalScrollIndicator={false}
          />
        )}

        <FlatList
          data={stories}
          keyExtractor={(item) => item.id}
          renderItem={({ item }) => (
            <StoryCard story={item} onPress={(s) => { onSelectStory(s); onClose(); }} />
          )}
          ListEmptyComponent={
            <View style={styles.empty}>
              <Text style={styles.emptyText}>No saved stories yet</Text>
              <Text style={styles.emptySubtext}>Save stories from the chat to see them here</Text>
            </View>
          }
          contentContainerStyle={styles.list}
        />
      </View>
    </Modal>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.background,
  },
  header: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    paddingHorizontal: 16,
    paddingVertical: 16,
    borderBottomWidth: 1,
    borderBottomColor: Colors.border,
  },
  title: {
    fontSize: 20,
    fontWeight: "700",
    color: Colors.text,
  },
  closeButton: {
    fontSize: 16,
    color: Colors.primary,
    fontWeight: "600",
  },
  kidList: {
    paddingHorizontal: 16,
    paddingVertical: 12,
    maxHeight: 60,
  },
  kidChip: {
    backgroundColor: Colors.surface,
    borderRadius: 16,
    paddingHorizontal: 14,
    paddingVertical: 8,
    marginRight: 8,
    borderWidth: 1,
    borderColor: Colors.border,
  },
  kidChipActive: {
    backgroundColor: Colors.primary,
    borderColor: Colors.primary,
  },
  kidChipText: {
    fontSize: 13,
    color: Colors.text,
    fontWeight: "500",
  },
  kidChipTextActive: {
    color: Colors.textLight,
  },
  list: {
    paddingHorizontal: 16,
    paddingTop: 12,
    paddingBottom: 40,
  },
  empty: {
    alignItems: "center",
    paddingVertical: 40,
  },
  emptyText: {
    fontSize: 16,
    fontWeight: "600",
    color: Colors.textSecondary,
  },
  emptySubtext: {
    fontSize: 14,
    color: Colors.textSecondary,
    marginTop: 4,
  },
});
