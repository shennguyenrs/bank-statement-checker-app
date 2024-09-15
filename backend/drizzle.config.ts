import { defineConfig } from "drizzle-kit";

export default defineConfig({
  schema: "./src/db/",
  dialect: "sqlite",
  dbCredentials: {
    url: process.env.LOCAL_DB_PATH as string,
  },
});
