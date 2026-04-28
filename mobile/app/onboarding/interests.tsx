import React, { useState } from "react";
import { View, Text, TouchableOpacity, FlatList, StyleSheet } from "react-native";
import { useRouter, useLocalSearchParams } from "expo-router";
import { Colors } from "../../constants/colors";
import { INTERESTS } from "../../constants/themes";
import { useKidStore } from "../../stores/kidStore";

export default function InterestsScreen() {
  const [selected, setSelected] = useState<Set<string>>(new Set());
  const router = useRouter();
  const { nickname } = useLocalSearchParams<{ nickname?: string }>();
  const { kids, updateKid } = useKidStore();

  const toggleInterest = (id: string) => {
    const next = new Set(selected);
    if (next.has(id)) next.delete(id);
    else if (next.size < 5) next.add(id);
    setSelected(next);
  };

  const handleNext = async () => {
    const kid = kids[0];
    if (kid) {
      await updateKid(kid.id, { interests: Array.from(selected) });
    }
    router.push("/onboarding/bedtime-goal");
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.emoji}>🎨</Text>
        <Text style={styles.title}>What does {nickname || "your child"} like?</Text>
        <Text style={styles.subtitle}>Pick 3-5 interests ({selected.size}/5 selected)</Text>
      </View>

      <FlatList
        data={INTERESTS}
        keyExtractor={(item) => item.id}
        numColumns={2}
        renderItem={({ item }) => {
          const isSelected = selected.has(item.id);
          return (
            <TouchableOpacity
              style={[styles.chip, isSelected && styles.chipSelected]}
              onPress={() => toggleInterest(item.id)}
              activeOpacity={0.7}
            >
              <Text style={styles.chipEmoji}>{item.emoji}</Text>
              <Text style={[styles.chipLabel, isSelected && styles.chipLabelSelected]}>
                {item.label}
              </Text>
            </TouchableOpacity>
          );
        }}
        contentContainerStyle={styles.list}
        columnWrapperStyle={styles.row}
      />

      <View style={styles.footer}>
        <TouchableOpacity
          style={[styles.button, selected.size < 3 && styles.buttonDisabled]}
          onPress={handleNext}
          disabled={selected.size < 3}
        >
          <Text style={styles.buttonText}>
            {selected.size < 3 ? `Pick at least ${3 - selected.size} more` : "Next"}
          </Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.background },
  header: { paddingHorizontal: 24, paddingTop: 60, paddingBottom: 20, alignItems: "center" },
  emoji: { fontSize: 48, marginBottom: 8 },
  title: { fontSize: 24, fontWeight: "700", color: Colors.text, textAlign: "center", marginBottom: 4 },
  subtitle: { fontSize: 15, color: Colors.textSecondary },
  list: { paddingHorizontal: 16, paddingBottom: 100 },
  row: { justifyContent: "space-between", marginBottom: 10 },
  chip: {
    flex: 1,
    backgroundColor: Colors.surface,
    borderRadius: 12,
    paddingVertical: 14,
    paddingHorizontal: 12,
    alignItems: "center",
    borderWidth: 2,
    borderColor: "transparent",
    marginHorizontal: 4,
  },
  chipSelected: { borderColor: Colors.primary, backgroundColor: Colors.chatBubble },
  chipEmoji: { fontSize: 28, marginBottom: 4 },
  chipLabel: { fontSize: 13, color: Colors.text, fontWeight: "500" },
  chipLabelSelected: { color: Colors.primary, fontWeight: "600" },
  footer: { position: "absolute", bottom: 0, left: 0, right: 0, padding: 24, backgroundColor: Colors.background },
  button: {
    backgroundColor: Colors.primary,
    borderRadius: 12,
    paddingVertical: 14,
    alignItems: "center",
  },
  buttonDisabled: { backgroundColor: Colors.primaryLight },
  buttonText: { fontSize: 16, fontWeight: "600", color: Colors.textLight },
});
