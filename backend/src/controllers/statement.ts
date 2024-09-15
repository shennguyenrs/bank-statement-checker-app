import { asc, desc, like } from "drizzle-orm";
import { drizzle } from "drizzle-orm/d1";
import { Hono } from "hono";

import { statement } from "../db/schema";
import type { Env } from "../index";

const router = new Hono<{ Bindings: Env }>();

router.get("/", async (c) => {
  let { name, page, size, sort } = c.req.query();

  // Validate page, size, sort
  if (!page || isNaN(Number(page))) {
    page = "1";
  }

  if (!size || isNaN(Number(size))) {
    size = "10";
  }

  if (!sort || (sort !== "asc" && sort !== "desc")) {
    sort = "asc";
  }

  const pageNum = Number(page);
  const sizeNum = Number(size);

  const db = drizzle(c.env.DB);
  const rows = await db
    .select()
    .from(statement)
    .where(
      name?.trim().length > 0
        ? like(statement.description, `%${name.trim()}%`)
        : undefined,
    )
    .limit(sizeNum)
    .offset((pageNum - 1) * sizeNum)
    .orderBy(sort === "asc" ? asc(statement.id) : desc(statement.id));

  return c.json({
    rows,
  });
});

export default router;
