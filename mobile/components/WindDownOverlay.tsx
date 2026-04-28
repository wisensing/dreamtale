import React from "react";
import { View, StyleSheet } from "react-native";
import { Colors } from "../constants/colors";

interface WindDownOverlayProps {
  active: boolean;
}

export default function WindDownOverlay({ active }: WindDownOverlayProps) {
  if (!active) return null;

  return <View style={styles.overlay} pointerEvents="none" />;
}

const styles = StyleSheet.create({
  overlay: {
    ...StyleSheet.absoluteFillObject,
    backgroundColor: "rgba(26, 26, 46, 0.15)",
  },
});
