import { serve } from "@hono/node-server";
import { Hono } from "hono";
import { cors } from "hono/cors";
import "dotenv/config";

const app = new Hono();
const SECRET_KEY = process.env.VITE_CLOUDFLARE_TURNSTILE_PRIVATE || "";
console.log("Using Turnstile secret key:", SECRET_KEY);
async function validateTurnstile(token: string): Promise<boolean> {
  const formData = new FormData();
  formData.append("secret", SECRET_KEY);
  formData.append("response", token);

  try {
    const response = await fetch(
      "https://challenges.cloudflare.com/turnstile/v0/siteverify",
      {
        method: "POST",
        body: formData,
      }
    );

    const result = await response.json();
    console.log("Turnstile verification response:", result);
    return result.success;
  } catch (error) {
    console.error("Turnstile validation error:", error);
    return false;
  }
}

app.use(cors());

app.post("/hello", async (c) => {
  const json = await c.req.json();

  if (!(await validateTurnstile(json.token))) {
    return c.json({ message: "Turnstile validation failed" }, 400);
  }

  return c.json({ message: `Hello, ${json.name}!` });
});

app.get("/", (c) => {
  return c.text("Hello Hono!");
});

serve(
  {
    fetch: app.fetch,
    port: 3000,
  },
  (info) => {
    console.log(`Server is running on http://localhost:${info.port}`);
  }
);
