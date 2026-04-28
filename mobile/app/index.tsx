import React from "react";
import { Redirect } from "expo-router";
import { useAuthStore } from "../stores/authStore";
import { useKidStore } from "../stores/kidStore";

export default function Index() {
  const { isAuthenticated } = useAuthStore();
  const { kids } = useKidStore();

  if (!isAuthenticated) {
    return <Redirect href="/auth/login" />;
  }

  if (kids.length === 0) {
    return <Redirect href="/onboarding/add-kid" />;
  }

  return <Redirect href="/(tabs)/chat" />;
}
