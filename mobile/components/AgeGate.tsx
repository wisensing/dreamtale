import React, { useState } from "react";
import { View, Text, TextInput, TouchableOpacity, StyleSheet, Modal } from "react-native";
import { Colors } from "../constants/colors";

interface AgeGateProps {
  visible: boolean;
  onVerified: () => void;
  onCancel: () => void;
}

export default function AgeGate({ visible, onVerified, onCancel }: AgeGateProps) {
  const [a, setA] = useState(0);
  const [b, setB] = useState(0);
  const [answer, setAnswer] = useState("");
  const [error, setError] = useState(false);

  React.useEffect(() => {
    if (visible) {
      setA(Math.floor(Math.random() * 10) + 1);
      setB(Math.floor(Math.random() * 10) + 1);
      setAnswer("");
      setError(false);
    }
  }, [visible]);

  const verify = () => {
    if (parseInt(answer, 10) === a + b) {
      onVerified();
    } else {
      setError(true);
    }
  };

  return (
    <Modal visible={visible} animationType="fade" transparent>
      <View style={styles.overlay}>
        <View style={styles.card}>
          <Text style={styles.title}>Parent Verification</Text>
          <Text style={styles.description}>
            Please solve this math problem to continue. This helps ensure a parent is making this purchase.
          </Text>
          <Text style={styles.problem}>
            {a} + {b} = ?
          </Text>
          <TextInput
            style={[styles.input, error && styles.inputError]}
            value={answer}
            onChangeText={(v) => { setAnswer(v); setError(false); }}
            keyboardType="number-pad"
            placeholder="Your answer"
            placeholderTextColor={Colors.textSecondary}
            autoFocus
          />
          {error && <Text style={styles.errorText}>Incorrect answer. Please try again.</Text>}
          <View style={styles.buttons}>
            <TouchableOpacity style={styles.cancelButton} onPress={onCancel}>
              <Text style={styles.cancelText}>Cancel</Text>
            </TouchableOpacity>
            <TouchableOpacity style={styles.verifyButton} onPress={verify}>
              <Text style={styles.verifyText}>Verify</Text>
            </TouchableOpacity>
          </View>
        </View>
      </View>
    </Modal>
  );
}

const styles = StyleSheet.create({
  overlay: {
    flex: 1,
    backgroundColor: "rgba(0,0,0,0.5)",
    justifyContent: "center",
    alignItems: "center",
    padding: 24,
  },
  card: {
    backgroundColor: Colors.surface,
    borderRadius: 16,
    padding: 24,
    width: "100%",
    maxWidth: 400,
  },
  title: {
    fontSize: 20,
    fontWeight: "700",
    color: Colors.text,
    marginBottom: 8,
  },
  description: {
    fontSize: 14,
    color: Colors.textSecondary,
    lineHeight: 20,
    marginBottom: 16,
  },
  problem: {
    fontSize: 32,
    fontWeight: "700",
    color: Colors.primary,
    textAlign: "center",
    marginBottom: 16,
  },
  input: {
    backgroundColor: Colors.background,
    borderRadius: 12,
    paddingHorizontal: 16,
    paddingVertical: 12,
    fontSize: 18,
    color: Colors.text,
    textAlign: "center",
    borderWidth: 1,
    borderColor: Colors.border,
    marginBottom: 8,
  },
  inputError: {
    borderColor: Colors.danger,
  },
  errorText: {
    color: Colors.danger,
    fontSize: 13,
    marginBottom: 8,
  },
  buttons: {
    flexDirection: "row",
    justifyContent: "space-between",
    marginTop: 8,
  },
  cancelButton: {
    flex: 1,
    paddingVertical: 12,
    borderRadius: 12,
    backgroundColor: Colors.background,
    alignItems: "center",
    marginRight: 8,
  },
  cancelText: {
    fontSize: 16,
    fontWeight: "600",
    color: Colors.textSecondary,
  },
  verifyButton: {
    flex: 1,
    paddingVertical: 12,
    borderRadius: 12,
    backgroundColor: Colors.primary,
    alignItems: "center",
  },
  verifyText: {
    fontSize: 16,
    fontWeight: "600",
    color: Colors.textLight,
  },
});
