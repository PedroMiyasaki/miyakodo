export const MATERIAL_BUTTON_LABEL = "Quero o material";
export const FOLLOWED_BUTTON_LABEL = "Já segui";
export const GATE_BUTTON_TEXT = "Toque no botão para receber o material.";
export const FOLLOWER_UNKNOWN_TEXT = "Não consegui confirmar se você segue a conta. Toque em Já segui para eu verificar de novo.";
export const DEFAULT_RECHECK_MS = 4000;
export const MAX_RECHECK_MS = 8000;

export type GateStep = "material" | "followed";
export type GatePayload = { ruleId: number; commentId: string; step: GateStep };
export type FollowerDecision = "follower" | "not_follower" | "unknown";

const GATE_PAYLOAD = /^GATE:v1:(\d{1,10}):([A-Za-z0-9_-]{1,64}):(material|followed)$/;

export function recheckDelayMs(value: string | undefined): number {
  if (value == null || value.trim() === "") return DEFAULT_RECHECK_MS;
  const parsed = Number(value);
  if (!Number.isFinite(parsed) || parsed <= 0) return 0;
  return Math.min(Math.floor(parsed), MAX_RECHECK_MS);
}

export function gatePayload(ruleId: number, commentId: string, step: GateStep): string {
  return `GATE:v1:${ruleId}:${commentId}:${step}`;
}

export function parseGatePayload(payload: string | null | undefined): GatePayload | null {
  const match = GATE_PAYLOAD.exec(payload ?? "");
  if (!match) return null;
  return { ruleId: Number(match[1]), commentId: match[2], step: match[3] as GateStep };
}

export function postbackButtonMessage(text: string, title: string, payload: string): Record<string, unknown> {
  return {
    attachment: {
      type: "template",
      payload: {
        template_type: "button",
        text,
        buttons: [{ type: "postback", title, payload }]
      }
    }
  };
}

/** A stored username: key is the comment author when the webhook had no numeric id. */
export function sameRecipient(stored: string, senderId: string): boolean {
  return stored === senderId || stored.startsWith("username:");
}

/**
 * Never deny on the first negative lookup. Instagram can lag right after a follow,
 * so a miss waits and checks once more. A failed recheck does not count as "not following".
 */
export async function decideFollower(
  check: () => Promise<boolean | null>,
  wait: () => Promise<void>
): Promise<FollowerDecision> {
  const first = await check();
  if (first === true) return "follower";
  await wait();
  const second = await check();
  if (second === true) return "follower";
  if (second === false) return "not_follower";
  return "unknown";
}
