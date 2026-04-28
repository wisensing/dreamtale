import React, { useState } from "react";
import { View, Text, TextInput, TouchableOpacity, StyleSheet, Alert } from "react-native";
import { useRouter } from "expo-router";
import { Colors } from "../../constants/colors";
import { useKidStore } from "../../stores/kidStore";

export default function AddKidScreen() {
  const [nickname, setNickname] = useState("");
  const [age, setAge] = useState("");
  const router = useRouter();
  const { addKid } = useKidStore();

  const handleNext = async () => {
    if (!nickname.trim()) {
      Alert.alert("Missing name", "Please enter your child's nickname.");
      return;
    }
    const ageNum = parseInt(age, 10);
    if (isNaN(ageNum) || ageNum < 2 || ageNum > 10) {
      Alert.alert("Invalid age", "Please enter an age between 2 and 10.");
      return;
    }

    await addKid({ nickname: nickname.trim(), age: ageNum, interests: [], fears: [] });
    router.push({ pathname: "/onboarding/interests", params: { nickname: nickname.trim() } });
  };

  return (
    <View style={styles.container}>
      <View style={styles.content}>
        <Text style={styles.emoji}>🧸</Text>
        <Text style={styles.title}>Tell us about your child</Text>
        <Text style={styles.subtitle}>We'll personalize every story for them</Text>

        <Text style={styles.label}>Nickname</Text>
        <TextInput
          style={styles.input}
          value={nickname}
          onChangeText={setNickname}
          placeholder="e.g., Emma, Leo"
          placeholderTextColor={Colors.textSecondary}
          autoCapitalize="words"
          maxLength={50}
        />

        <Text style={styles.label}>Age</Text>
        <TextInput
          style={styles.input}
          value={age}
          onChangeText={setAge}
          placeholder="2-10"
          placeholderTextColor={Colors.textSecondary}
          keyboardType="number-pad"
          maxLength={2}
        />

        <View style={styles.ageHint}>
          <Text style={styles.ageHintText}>
            {age && parseInt(age, 10) >= 2 && parseInt(age, 10) <= 10
              ? getAgeDescription(parseInt(age, 10))
              : "Stories adapt to your child's age"}
          </Text>
        </View>

        <TouchableOpacity style={styles.button} onPress={handleNext}>
          <Text style={styles.buttonText}>Next</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

function getAgeDescription(age: number): string {
  if (age <= 3) return "Simple, repetitive stories with counting and colors";
  if (age <= 5) return "Stories about friendship, sharing, and basic safety";
  if (age <= 7) return "Adventures with teamwork, empathy, and science";
  return "Mysteries, critical thinking, and problem-solving";
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.background },
  content: { flex: 1, justifyContent: "center", paddingHorizontal: 32 },
  emoji: { fontSize: 64, textAlign: "center", marginBottom: 8 },
  title: { fontSize: 28, fontWeight: "700", color: Colors.text, textAlign: "center", marginBottom: 4 },
  subtitle: { fontSize: 16, color: Colors.textSecondary, textAlign: "center", marginBottom: 32 },
  label: { fontSize: 14, fontWeight: "600", color: Colors.text, marginBottom: 6, marginLeft: 4 },
  input: {
    backgroundColor: Colors.surface,
    borderRadius: 12,
    paddingHorizontal: 16,
    paddingVertical: 14,
    fontSize: 16,
    color: Colors.text,
    marginBottom: 16,
    borderWidth: 1,
    borderColor: Colors.border,
  },
  ageHint: { marginBottom: 24, paddingHorizontal: 4 },
  ageHintText: { fontSize: 13, color: Colors.primary, fontStyle: "italic" },
  button: {
    backgroundColor: Colors.primary,
    borderRadius: 12,
    paddingVertical: 14,
    alignItems: "center",
  },
  buttonText: { fontSize: 16, fontWeight: "600", color: Colors.textLight },
});
