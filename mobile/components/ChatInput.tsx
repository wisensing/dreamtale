import React, { useState } from "react";
import { View, TextInput, TouchableOpacity, StyleSheet, ActivityIndicator } from "react-native";
import { Colors } from "../constants/colors";

interface ChatInputProps {
  onSend: (message: string) => void;
  isLoading?: boolean;
  placeholder?: string;
}

export default function ChatInput({ onSend, isLoading, placeholder }: ChatInputProps) {
  const [text, setText] = useState("");

  const handleSend = () => {
    const trimmed = text.trim();
    if (!trimmed || isLoading) return;
    onSend(trimmed);
    setText("");
  };

  return (
    <View style={styles.container}>
      <TextInput
        style={styles.input}
        value={text}
        onChangeText={setText}
        placeholder={placeholder || "Type keywords or a message..."}
        placeholderTextColor={Colors.textSecondary}
        multiline
        maxLength={500}
        editable={!isLoading}
        onSubmitEditing={handleSend}
      />
      <TouchableOpacity
        style={[styles.sendButton, (!text.trim() || isLoading) && styles.sendButtonDisabled]}
        onPress={handleSend}
        disabled={!text.trim() || isLoading}
      >
        {isLoading ? (
          <ActivityIndicator size="small" color={Colors.textLight} />
        ) : (
          <Text style={styles.sendButtonText}>Send</Text>
        )}
      </TouchableOpacity>
    </View>
  );
}

import { Text } from "react-native";

const styles = StyleSheet.create({
  container: {
    flexDirection: "row",
    alignItems: "flex-end",
    paddingHorizontal: 16,
    paddingVertical: 12,
    backgroundColor: Colors.surface,
    borderTopWidth: 1,
    borderTopColor: Colors.border,
  },
  input: {
    flex: 1,
    minHeight: 40,
    maxHeight: 100,
    backgroundColor: Colors.background,
    borderRadius: 20,
    paddingHorizontal: 16,
    paddingVertical: 10,
    fontSize: 15,
    color: Colors.text,
  },
  sendButton: {
    marginLeft: 8,
    backgroundColor: Colors.primary,
    borderRadius: 20,
    paddingHorizontal: 16,
    paddingVertical: 10,
    minWidth: 60,
    alignItems: "center",
  },
  sendButtonDisabled: {
    backgroundColor: Colors.primaryLight,
  },
  sendButtonText: {
    color: Colors.textLight,
    fontWeight: "600",
    fontSize: 14,
  },
});
