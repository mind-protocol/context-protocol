/** DOCS: docs/api/sse/OBJECTIVES_SSE_API.md */
export const runtime = "nodejs";
export const dynamic = "force-dynamic";

import { spawn } from "child_process";

const encoder = new TextEncoder();

const formatEvent = (event: string, data: unknown) =>
  `event: ${event}\ndata: ${JSON.stringify(data)}\n\n`;

interface PhysicsIndicator {
  name: string;
  status: string;
  message: string;
  details: Record<string, unknown>;
}

interface PhysicsHealth {
  overall: string;
  indicators: PhysicsIndicator[];
  graph_name: string;
  checked_at: number;
}

interface HealthPayload {
  ts: number;
  playthrough_id: string;
  place_id: string;
  status: { state: string; score: number; notes: string[] };
  runner: { speed: string; tick: number; last_interrupt: unknown };
  counters: { query_write_attempts: number; dmz_violation_attempts: number; async_epoch_mismatch: number };
  attention: { sink_set_size: { p50: number; p95: number }; focus_reconfig_rate_per_min: number; plateau_seconds: number };
  pressure: { contradiction: number; top_edges: unknown[] };
  physics?: PhysicsHealth;
}

async function fetchConnectomeHealth(): Promise<HealthPayload> {
  return new Promise((resolve) => {
    const proc = spawn("python3", ["-c", `
import json, sys
sys.path.insert(0, '.')
from engine.health import get_current_health
print(json.dumps(get_current_health()))
`]);
    let stdout = "";
    proc.stdout.on("data", (d) => { stdout += d.toString(); });
    proc.on("close", (code) => {
      if (code === 0 && stdout.trim()) {
        try { resolve(JSON.parse(stdout.trim())); return; } catch {}
      }
      // Fallback if service not available
      resolve({
        ts: Date.now(),
        playthrough_id: "",
        place_id: "",
        status: { state: "UNKNOWN", score: 0, notes: ["Health service initializing..."] },
        runner: { speed: "pause", tick: 0, last_interrupt: null },
        counters: { query_write_attempts: 0, dmz_violation_attempts: 0, async_epoch_mismatch: 0 },
        attention: { sink_set_size: { p50: 0, p95: 0 }, focus_reconfig_rate_per_min: 0, plateau_seconds: 0 },
        pressure: { contradiction: 0, top_edges: [] },
      });
    });
    setTimeout(() => { proc.kill(); }, 5000);
  });
}

export async function GET() {
  let heartbeat: NodeJS.Timeout | null = null;
  let healthPoller: NodeJS.Timeout | null = null;

  const stream = new ReadableStream({
    async start(controller) {
      controller.enqueue(encoder.encode(":ok\n\n"));

      // Initial health fetch
      const health = await fetchConnectomeHealth();
      controller.enqueue(encoder.encode(formatEvent("connectome_health", health)));

      // Poll health every 5 seconds
      healthPoller = setInterval(async () => {
        try {
          const health = await fetchConnectomeHealth();
          controller.enqueue(encoder.encode(formatEvent("connectome_health", health)));
        } catch {
          // Ignore polling errors
        }
      }, 5000);

      // Heartbeat every 15 seconds
      heartbeat = setInterval(() => {
        controller.enqueue(encoder.encode(formatEvent("ping", { t: Date.now() })));
      }, 15000);
    },
    cancel() {
      if (heartbeat) clearInterval(heartbeat);
      if (healthPoller) clearInterval(healthPoller);
    },
  });

  return new Response(stream, {
    headers: {
      "Content-Type": "text/event-stream",
      "Cache-Control": "no-cache, no-transform",
      Connection: "keep-alive",
    },
  });
}
