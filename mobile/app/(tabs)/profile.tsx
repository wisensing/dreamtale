import React, { useEffect, useState } from "react";
import {
  View,
  Text,
  FlatList,
  TouchableOpacity,
  StyleSheet,
  Alert,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { useRouter } from "expo-router";
import { Colors } from "../../constants/colors";
import { CREDIT_PACKS, SUBSCRIPTION_PLANS } from "../../constants/themes";
import { useKidStore } from "../../stores/kidStore";
import { useAuthStore } from "../../stores/authStore";
import StreakCounter from "../../components/StreakCounter";
import CreditBadge from "../../components/CreditBadge";
import AgeGate from "../../components/AgeGate";
import { Kid } from "../../types";

export default function ProfileScreen() {
  const { kids, activeKidId, fetchKids, addKid, setActiveKid, deleteKid } = useKidStore();
  const { user, logout, refreshUser } = useAuthStore();
  const [ageGateVisible, setAgeGateVisible] = useState(false);
  const [selectedPack, setSelectedPack] = useState<string | null>(null);
  const router = useRouter();

  useEffect(() => {
    fetchKids();
    refreshUser();
  }, []);

  const handlePurchase = (packId: string) => {
    setSelectedPack(packId);
    setAgeGateVisible(true);
  };

  const handleAgeVerified = async () => {
    setAgeGateVisible(false);
    if (selectedPack) {
      try {
        const { createCheckout } = await import("../../services/credits");
        const result = await createCheckout(selectedPack);
        // In a real app, open the checkout URL in a browser
        Alert.alert("Redirecting to checkout", result.checkout_url);
      } catch {
        Alert.alert("Error", "Could not start checkout");
      }
    }
  };

  const handleLogout = async () => {
    await logout();
    router.replace("/auth/login");
  };

  const activeKid = kids.find((k) => k.id === activeKidId);

  return (
    <SafeAreaView style={styles.container} edges={["top"]}>
      <FlatList
        data={kids}
        keyExtractor={(item) => item.id}
        ListHeaderComponent={
          <View>
            {/* User info */}
            <View style={styles.section}>
              <Text style={styles.sectionTitle}>Account</Text>
              {user && (
                <View style={styles.userInfo}>
                  <Text style={styles.userEmail}>{user.email}</Text>
                  <CreditBadge balance={user.credit_balance} tier={user.subscription_tier} />
                </View>
              )}
            </View>

            {/* Bedtime streak */}
            {activeKid && (
              <View style={styles.section}>
                <Text style={styles.sectionTitle}>Bedtime Streak</Text>
                <View style={styles.streakRow}>
                  <StreakCounter streak={0} />
                  <Text style={styles.streakLabel}>for {activeKid.nickname}</Text>
                </View>
              </View>
            )}

            {/* Kids */}
            <View style={styles.section}>
              <View style={styles.sectionHeader}>
                <Text style={styles.sectionTitle}>Kids</Text>
                <TouchableOpacity onPress={() => router.push("/onboarding/add-kid")}>
                  <Text style={styles.addButton}>+ Add</Text>
                </TouchableOpacity>
              </View>
            </View>
          </View>
        }
        renderItem={({ item }) => (
          <TouchableOpacity
            style={[styles.kidCard, item.id === activeKidId && styles.kidCardActive]}
            onPress={() => setActiveKid(item.id)}
          >
            <View style={styles.kidInfo}>
              <Text style={styles.kidName}>{item.nickname}</Text>
              <Text style={styles.kidAge}>Age {item.age}</Text>
              {item.interests.length > 0 && (
                <Text style={styles.kidInterests}>{item.interests.join(", ")}</Text>
              )}
            </View>
            {item.id === activeKidId && <Text style={styles.activeBadge}>Active</Text>}
          </TouchableOpacity>
        )}
        ListFooterComponent={
          <View>
            {/* Credits */}
            <View style={styles.section}>
              <Text style={styles.sectionTitle}>Buy Credits</Text>
              {CREDIT_PACKS.map((pack) => (
                <TouchableOpacity
                  key={pack.id}
                  style={styles.creditPack}
                  onPress={() => handlePurchase(pack.id)}
                >
                  <View>
                    <Text style={styles.creditAmount}>{pack.credits} credits</Text>
                    <Text style={styles.creditPer}>{pack.perStory}/story</Text>
                  </View>
                  <Text style={styles.creditPrice}>{pack.price}</Text>
                </TouchableOpacity>
              ))}
            </View>

            {/* Subscription */}
            <View style={styles.section}>
              <Text style={styles.sectionTitle}>Subscriptions</Text>
              {SUBSCRIPTION_PLANS.map((plan) => (
                <View key={plan.id} style={styles.planCard}>
                  <View style={styles.planHeader}>
                    <Text style={styles.planName}>{plan.name}</Text>
                    <Text style={styles.planPrice}>{plan.price}</Text>
                  </View>
                  {plan.features.map((f, i) => (
                    <Text key={i} style={styles.planFeature}>  {f}</Text>
                  ))}
                  <TouchableOpacity
                    style={styles.planButton}
                    onPress={() => handlePurchase(plan.id)}
                  >
                    <Text style={styles.planButtonText}>Subscribe</Text>
                  </TouchableOpacity>
                </View>
              ))}
            </View>

            {/* Logout */}
            <TouchableOpacity style={styles.logoutButton} onPress={handleLogout}>
              <Text style={styles.logoutText}>Sign Out</Text>
            </TouchableOpacity>
          </View>
        }
        contentContainerStyle={styles.list}
      />

      <AgeGate
        visible={ageGateVisible}
        onVerified={handleAgeVerified}
        onCancel={() => setAgeGateVisible(false)}
      />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.background },
  list: { paddingHorizontal: 16, paddingBottom: 40 },
  section: { marginTop: 24 },
  sectionHeader: { flexDirection: "row", justifyContent: "space-between", alignItems: "center" },
  sectionTitle: { fontSize: 18, fontWeight: "700", color: Colors.text, marginBottom: 12 },
  userInfo: { flexDirection: "row", justifyContent: "space-between", alignItems: "center" },
  userEmail: { fontSize: 15, color: Colors.textSecondary },
  streakRow: { flexDirection: "row", alignItems: "center", gap: 12 },
  streakLabel: { fontSize: 15, color: Colors.textSecondary },
  addButton: { fontSize: 15, color: Colors.primary, fontWeight: "600" },
  kidCard: {
    backgroundColor: Colors.surface,
    borderRadius: 12,
    padding: 16,
    marginBottom: 8,
    borderWidth: 2,
    borderColor: "transparent",
  },
  kidCardActive: { borderColor: Colors.primary },
  kidInfo: { flex: 1 },
  kidName: { fontSize: 16, fontWeight: "600", color: Colors.text },
  kidAge: { fontSize: 13, color: Colors.textSecondary, marginTop: 2 },
  kidInterests: { fontSize: 12, color: Colors.primary, marginTop: 4 },
  activeBadge: { fontSize: 12, fontWeight: "600", color: Colors.primary, position: "absolute", top: 12, right: 12 },
  creditPack: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    backgroundColor: Colors.surface,
    borderRadius: 12,
    padding: 16,
    marginBottom: 8,
  },
  creditAmount: { fontSize: 16, fontWeight: "600", color: Colors.text },
  creditPer: { fontSize: 13, color: Colors.textSecondary, marginTop: 2 },
  creditPrice: { fontSize: 18, fontWeight: "700", color: Colors.primary },
  planCard: {
    backgroundColor: Colors.surface,
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
  },
  planHeader: { flexDirection: "row", justifyContent: "space-between", alignItems: "center", marginBottom: 8 },
  planName: { fontSize: 18, fontWeight: "700", color: Colors.text },
  planPrice: { fontSize: 18, fontWeight: "700", color: Colors.primary },
  planFeature: { fontSize: 14, color: Colors.textSecondary, paddingVertical: 2 },
  planButton: {
    backgroundColor: Colors.primary,
    borderRadius: 10,
    paddingVertical: 10,
    alignItems: "center",
    marginTop: 12,
  },
  planButtonText: { fontSize: 14, fontWeight: "600", color: Colors.textLight },
  logoutButton: { marginTop: 24, paddingVertical: 14, alignItems: "center" },
  logoutText: { fontSize: 16, color: Colors.danger, fontWeight: "600" },
});
