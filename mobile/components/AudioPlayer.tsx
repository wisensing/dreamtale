import React, { useState, useRef, useEffect } from "react";
import { View, Text, TouchableOpacity, StyleSheet, Slider } from "react-native";
import { Audio } from "expo-av";
import { Colors } from "../constants/colors";

interface AudioPlayerProps {
  audioUrl: string | null;
  title?: string;
}

const SPEED_OPTIONS = [0.8, 1.0, 1.2];

export default function AudioPlayer({ audioUrl, title }: AudioPlayerProps) {
  const [isPlaying, setIsPlaying] = useState(false);
  const [speedIndex, setSpeedIndex] = useState(1);
  const [duration, setDuration] = useState(0);
  const [position, setPosition] = useState(0);
  const soundRef = useRef<Audio.Sound | null>(null);

  useEffect(() => {
    return () => {
      if (soundRef.current) {
        soundRef.current.unloadAsync();
      }
    };
  }, []);

  const loadSound = async () => {
    if (!audioUrl) return;
    const { sound } = await Audio.Sound.createAsync({ uri: audioUrl });
    soundRef.current = sound;
    sound.setOnPlaybackStatusUpdate((status) => {
      if (status.isLoaded) {
        setPosition(status.positionMillis / 1000);
        setDuration(status.durationMillis / 1000);
        if (status.didJustFinish) {
          setIsPlaying(false);
          setPosition(0);
        }
      }
    });
  };

  const togglePlay = async () => {
    if (!soundRef.current) {
      await loadSound();
    }
    if (isPlaying) {
      await soundRef.current?.pauseAsync();
      setIsPlaying(false);
    } else {
      await soundRef.current?.playAsync();
      setIsPlaying(true);
    }
  };

  const cycleSpeed = () => {
    const next = (speedIndex + 1) % SPEED_OPTIONS.length;
    setSpeedIndex(next);
    if (soundRef.current) {
      soundRef.current.setRateAsync(SPEED_OPTIONS[next], true);
    }
  };

  const formatTime = (seconds: number) => {
    const m = Math.floor(seconds / 60);
    const s = Math.floor(seconds % 60);
    return `${m}:${s.toString().padStart(2, "0")}`;
  };

  return (
    <View style={styles.container}>
      <View style={styles.row}>
        <TouchableOpacity style={styles.playButton} onPress={togglePlay}>
          <Text style={styles.playIcon}>{isPlaying ? "⏸" : "▶"}</Text>
        </TouchableOpacity>
        <View style={styles.info}>
          {title && <Text style={styles.title} numberOfLines={1}>{title}</Text>}
          <Text style={styles.time}>
            {formatTime(position)} / {formatTime(duration)}
          </Text>
        </View>
        <TouchableOpacity style={styles.speedButton} onPress={cycleSpeed}>
          <Text style={styles.speedText}>{SPEED_OPTIONS[speedIndex]}x</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: Colors.surface,
    borderRadius: 12,
    padding: 12,
    ...{ shadowColor: "#000", shadowOffset: { width: 0, height: 2 }, shadowOpacity: 0.1, shadowRadius: 4, elevation: 3 },
  },
  row: {
    flexDirection: "row",
    alignItems: "center",
  },
  playButton: {
    width: 44,
    height: 44,
    borderRadius: 22,
    backgroundColor: Colors.primary,
    justifyContent: "center",
    alignItems: "center",
  },
  playIcon: {
    color: Colors.textLight,
    fontSize: 18,
  },
  info: {
    flex: 1,
    marginLeft: 12,
  },
  title: {
    fontSize: 14,
    fontWeight: "600",
    color: Colors.text,
  },
  time: {
    fontSize: 12,
    color: Colors.textSecondary,
    marginTop: 2,
  },
  speedButton: {
    backgroundColor: Colors.background,
    borderRadius: 8,
    paddingHorizontal: 10,
    paddingVertical: 6,
  },
  speedText: {
    fontSize: 12,
    fontWeight: "600",
    color: Colors.primary,
  },
});
