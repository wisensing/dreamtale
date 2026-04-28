import React, { useState } from "react";
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  Alert,
  KeyboardAvoidingView,
  Platform,
} from "react-native";
import { useRouter } from "expo-router";
import { Colors } from "../../constants/colors";
import { useAuthStore } from "../../stores/authStore";

export default function SignupScreen() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [coppaConsent, setCoppaConsent] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();
  const { signup } = useAuthStore();

  const handleSignup = async () => {
    if (!email || !password) {
      Alert.alert("Missing fields", "Please enter your email and password.");
      return;
    }
    if (password.length < 8) {
      Alert.alert("Weak password", "Password must be at least 8 characters.");
      return;
    }
    if (!coppaConsent) {
      Alert.alert("Consent required", "Please provide parental consent to continue.");
      return;
    }
    setIsLoading(true);
    try {
      await signup(email, password);
      router.replace("/onboarding/add-kid");
    } catch (e: any) {
      Alert.alert("Signup failed", e.message || "Could not create account");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === "ios" ? "padding" : "height"}
    >
      <View style={styles.content}>
        <Text style={styles.emoji}>✨</Text>
        <Text style={styles.title}>Create Account</Text>
        <Text style={styles.subtitle}>Join DreamTale for free bedtime stories</Text>

        <TextInput
          style={styles.input}
          value={email}
          onChangeText={setEmail}
          placeholder="Email"
          placeholderTextColor={Colors.textSecondary}
          keyboardType="email-address"
          autoCapitalize="none"
          autoCorrect={false}
        />
        <TextInput
          style={styles.input}
          value={password}
          onChangeText={setPassword}
          placeholder="Password (8+ characters)"
          placeholderTextColor={Colors.textSecondary}
          secureTextEntry
        />

        <TouchableOpacity style={styles.consentRow} onPress={() => setCoppaConsent(!coppaConsent)}>
          <View style={[styles.checkbox, coppaConsent && styles.checkboxChecked]}>
            {coppaConsent && <Text style={styles.checkmark}>✓</Text>}
          </View>
          <Text style={styles.consentText}>
            I am a parent/guardian and consent to data collection for my child under COPPA guidelines.
          </Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={[styles.button, (!coppaConsent || isLoading) && styles.buttonDisabled]}
          onPress={handleSignup}
          disabled={!coppaConsent || isLoading}
        >
          <Text style={styles.buttonText}>{isLoading ? "Creating account..." : "Create Account"}</Text>
        </TouchableOpacity>

        <TouchableOpacity onPress={() => router.back()}>
          <Text style={styles.linkText}>
            Already have an account? <Text style={styles.link}>Sign In</Text>
          </Text>
        </TouchableOpacity>
      </View>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.background },
  content: { flex: 1, justifyContent: "center", paddingHorizontal: 32 },
  emoji: { fontSize: 64, textAlign: "center", marginBottom: 8 },
  title: { fontSize: 32, fontWeight: "700", color: Colors.text, textAlign: "center", marginBottom: 4 },
  subtitle: { fontSize: 16, color: Colors.textSecondary, textAlign: "center", marginBottom: 40 },
  input: {
    backgroundColor: Colors.surface,
    borderRadius: 12,
    paddingHorizontal: 16,
    paddingVertical: 14,
    fontSize: 16,
    color: Colors.text,
    marginBottom: 12,
    borderWidth: 1,
    borderColor: Colors.border,
  },
  consentRow: { flexDirection: "row", alignItems: "flex-start", marginBottom: 20, marginTop: 8 },
  checkbox: {
    width: 22,
    height: 22,
    borderRadius: 6,
    borderWidth: 2,
    borderColor: Colors.border,
    marginRight: 10,
    marginTop: 1,
    justifyContent: "center",
    alignItems: "center",
  },
  checkboxChecked: { backgroundColor: Colors.primary, borderColor: Colors.primary },
  checkmark: { color: Colors.textLight, fontSize: 14, fontWeight: "700" },
  consentText: { flex: 1, fontSize: 13, color: Colors.textSecondary, lineHeight: 18 },
  button: {
    backgroundColor: Colors.primary,
    borderRadius: 12,
    paddingVertical: 14,
    alignItems: "center",
    marginBottom: 16,
  },
  buttonDisabled: { backgroundColor: Colors.primaryLight },
  buttonText: { fontSize: 16, fontWeight: "600", color: Colors.textLight },
  linkText: { fontSize: 14, color: Colors.textSecondary, textAlign: "center" },
  link: { color: Colors.primary, fontWeight: "600" },
});
