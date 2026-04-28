import React, { useState } from "react";
import { View, Text, TouchableOpacity, StyleSheet } from "react-native";
import { useRouter } from "expo-router";
import { Colors } from "../../constants/colors";
import { useKidStore } from "../../stores/kidStore";

const TIME_OPTIONS = ["7:00 PM", "7:30 PM", "8:00 PM", "8:30 PM", "9:00 PM"];

export default function BedtimeGoalScreen() {
  const [selected, setSelected] = useState("8:00 PM");
  const router = useRouter();
  const { kids, updateKid } = useKidStore();

  const handleDone = async () => {
    const kid = kids[0];
    if (kid) {
      await updateKid(kid.id, { bedtime_goal: selected });
    }
    router.replace("/(tabs)/chat");
  };

  return (
    <View style={styles.container}>
      <View style={styles.content}>
        <Text style={styles.emoji}>🌙</Text>
        <Text style={styles.title}>Set a bedtime goal</Text>
        <Text style={styles.subtitle}>We'll send a gentle reminder each night</Text>

        <View style={styles.options}>
          {TIME_OPTIONS.map((time) => (
            <TouchableOpacity
              key={time}
              style={[styles.timeOption, selected === time && styles.timeOptionSelected]}
              onPress={() => setSelected(time)}
            >
              <Text style={[styles.timeText, selected === time && styles.timeTextSelected]}>
                {time}
              </Text>
            </TouchableOpacity>
          ))}
        </View>

        <TouchableOpacity style={styles.button} onPress={handleDone}>
          <Text style={styles.buttonText}>Start DreamTale!</Text>
        </TouchableOpacity>

        <TouchableOpacity onPress={() => router.replace("/(tabs)/chat")}>
          <Text style={styles.skipText}>Skip for now</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.background },
  content: { flex: 1, justifyContent: "center", paddingHorizontal: 32 },
  emoji: { fontSize: 64, textAlign: "center", marginBottom: 8 },
  title: { fontSize: 28, fontWeight: "700", color: Colors.text, textAlign: "center", marginBottom: 4 },
  subtitle: { fontSize: 16, color: Colors.textSecondary, textAlign: "center", marginBottom: 32 },
  options: { marginBottom: 32 },
  timeOption: {
    backgroundColor: Colors.surface,
    borderRadius: 12,
    paddingVertical: 14,
    paddingHorizontal: 20,
    marginBottom: 10,
    borderWidth: 2,
    borderColor: "transparent",
    alignItems: "center",
  },
  timeOptionSelected: { borderColor: Colors.primary, backgroundColor: Colors.chatBubble },
  timeText: { fontSize: 18, fontWeight: "600", color: Colors.text },
  timeTextSelected: { color: Colors.primary },
  button: {
    backgroundColor: Colors.primary,
    borderRadius: 12,
    paddingVertical: 14,
    alignItems: "center",
    marginBottom: 12,
  },
  buttonText: { fontSize: 16, fontWeight: "600", color: Colors.textLight },
  skipText: { fontSize: 14, color: Colors.textSecondary, textAlign: "center" },
});
