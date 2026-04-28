import React from "react";
import { View, Text, StyleSheet } from "react-native";
import { Colors } from "../constants/colors";

interface CreditBadgeProps {
  balance: number;
  tier: string;
}

export default function CreditBadge({ balance, tier }: CreditBadgeProps) {
  const isUnlimited = tier === "premium" || tier === "family";

  return (
    <View style={styles.container}>
      <Text style={styles.emoji}>✨</Text>
      <Text style={styles.balance}>
        {isUnlimited ? "∞" : balance}
      </Text>
      <Text style={styles.label}>
        {isUnlimited ? tier : "credits"}
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: Colors.surface,
    borderRadius: 20,
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderWidth: 1,
    borderColor: Colors.primaryLight,
  },
  emoji: {
    fontSize: 14,
    marginRight: 4,
  },
  balance: {
    fontSize: 14,
    fontWeight: "700",
    color: Colors.primary,
  },
  label: {
    fontSize: 11,
    color: Colors.textSecondary,
    marginLeft: 4,
  },
});
