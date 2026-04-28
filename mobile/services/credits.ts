import api from "./api";
import { CreditTransaction } from "../types";

export async function getCreditBalance(): Promise<{ balance: number; subscription_tier: string }> {
  const { data } = await api.get("/credits/balance");
  return data;
}

export async function createCheckout(pack: string): Promise<{ checkout_url: string; session_id: string }> {
  const { data } = await api.post("/credits/checkout", { pack });
  return data;
}

export async function listTransactions(): Promise<CreditTransaction[]> {
  const { data } = await api.get("/credits/transactions");
  return data;
}
