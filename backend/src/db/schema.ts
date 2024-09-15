import { sqliteTable, integer, text, real } from "drizzle-orm/sqlite-core";

export const statement = sqliteTable("statement", {
  id: integer("id").primaryKey({ autoIncrement: true }),
  date: text("date"),
  docNo: text("doc_no"),
  description: text("description"),
  credit: real("credit"),
});
