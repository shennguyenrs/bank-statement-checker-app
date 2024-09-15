import { WorkersKVStore } from "@hono-rate-limiter/cloudflare";
import { Hono } from "hono";
import { rateLimiter } from "hono-rate-limiter";
import { bearerAuth } from "hono/bearer-auth";
import { cors } from "hono/cors";

import statement from "./controllers/statement";

export interface Env {
  DB: D1Database;
  KV: KVNamespace;
  TOKEN: string;
}

// App
const app = new Hono<{ Bindings: Env }>();
app.use("*", cors({ origin: "*", allowMethods: ["GET"] }));
app.use((c, next) =>
  rateLimiter<{ Bindings: Env }>({
    windowMs: 15 * 60 * 1000, // 15 minutes
    limit: 100, // limit each IP to 100 requests per windowMs
    standardHeaders: "draft-6",
    keyGenerator: (c) => c.req.header("cf-connecting-ip") ?? "",
    store: new WorkersKVStore({ namespace: c.env.KV }),
  })(c, next),
);
app.use("*", bearerAuth({ verifyToken: (token, c) => token === c.env.TOKEN }));

app.route("/api/v1/statements", statement);

export default app;
