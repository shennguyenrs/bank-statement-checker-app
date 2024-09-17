import { asc, count, desc, like } from "drizzle-orm";
import { drizzle } from "drizzle-orm/d1";
import { Hono } from "hono";

import { statement } from "../db/schema";
import type { Env } from "../index";

const router = new Hono<{ Bindings: Env }>();

router.get("/", async (c) => {
  let { description, page, pageSize, sort, sortBy } = c.req.query();

  // Validate page, size, sort
  if (!page || isNaN(Number(page))) {
    page = "1";
  }

  if (!pageSize || isNaN(Number(pageSize))) {
    pageSize = "10";
  }

  const pageNum = Number(page);
  const sizeNum = Number(pageSize);
  const orderBy = getSortBy({ sort, sortBy, sqlCols: statement });

  const db = drizzle(c.env.DB);
  const rows = await db
    .select()
    .from(statement)
    .where(
      description?.trim().length > 0
        ? like(statement.description, `%${description.trim()}%`)
        : undefined,
    )
    .limit(sizeNum)
    .offset((pageNum - 1) * sizeNum)
    .orderBy(orderBy);

  const countRows = await db
    .select({
      value: count(),
    })
    .from(statement)
    .where(
      description?.trim().length > 0
        ? like(statement.description, `%${description.trim()}%`)
        : undefined,
    );

  return c.json({
    rows,
    currentPage: pageNum,
    pageSize: sizeNum,
    totalPages: Math.ceil(countRows[0].value / sizeNum),
    sort,
    sortBy,
  });
});

function getSortBy({
  sort,
  sortBy,
  sqlCols,
}: {
  sort: string;
  sortBy: string;
  sqlCols: typeof statement;
}) {
  if (!sort || (sort !== "asc" && sort !== "desc")) {
    sort = "asc";
  }

  if (sortBy !== "date" && sortBy !== "credit") {
    sortBy = "id";
  }

  if (sortBy === "id") {
    if (sort === "asc") {
      return asc(sqlCols.id);
    } else {
      return desc(sqlCols.id);
    }
  } else if (sortBy === "date") {
    if (sort === "asc") {
      return asc(sqlCols.date);
    } else {
      return desc(sqlCols.date);
    }
  } else if (sortBy === "credit") {
    if (sort === "asc") {
      return asc(sqlCols.credit);
    } else {
      return desc(sqlCols.credit);
    }
  }

  return asc(sqlCols.id);
}

export default router;
