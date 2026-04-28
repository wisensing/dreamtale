import React from "react";
import { View, Text, StyleSheet } from "react-native";
import { Colors } from "../constants/colors";

interface StreakCounterProps {
  streak: number;
}

export default function StreakCounter({ streak }: StreakCounterProps) {
  return (
    <View style={styles.container}>
      <Text style={styles.emoji}>🌙</Text>
      <Text style={styles.count}>{streak}</Text>
      <Text style={styles.label}>{streak === 1 ? "night" : "nights"}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    alignItems: "center",
    backgroundColor: Colors.background,
    borderRadius: 16,
    padding: 12,
    minWidth: 80,
  },
  emoji: {
    fontSize: 24,
  },
  count: {
    fontSize: 28,
    fontWeight: "700",
    color: Colors.primary,
  },
  label: {
    fontSize: 12,
    color: Colors.textSecondary,
  },
});
