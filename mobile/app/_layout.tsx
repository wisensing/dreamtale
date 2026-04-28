import React, { useEffect } from "react";
import { Stack } from "expo-router";
import { StatusBar } from "expo-status-bar";
import { ActivityIndicator, View } from "react-native";
import { Colors } from "../constants/colors";
import { useAuthStore } from "../stores/authStore";

export default function RootLayout() {
  const { isAuthenticated, isLoading, initialize } = useAuthStore();

  useEffect(() => {
    initialize();
  }, []);

  if (isLoading) {
    return (
      <View style={{ flex: 1, justifyContent: "center", alignItems: "center", backgroundColor: Colors.background }}>
        <ActivityIndicator size="large" color={Colors.primary} />
      </View>
    );
  }

  return (
    <>
      <StatusBar style="dark" />
      <Stack screenOptions={{ headerShown: false }}>
        <Stack.Screen name="index" />
        <Stack.Screen name="auth/login" />
        <Stack.Screen name="auth/signup" />
        <Stack.Screen name="onboarding/add-kid" />
        <Stack.Screen name="onboarding/interests" />
        <Stack.Screen name="onboarding/bedtime-goal" />
        <Stack.Screen name="(tabs)" />
        <Stack.Screen name="story/[id]" options={{ presentation: "modal" }} />
      </Stack>
    </>
  );
}
