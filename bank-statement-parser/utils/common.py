import sqlite3
import csv
from tqdm import tqdm


def write_to_sql(records, db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS statement")
    cursor.execute(
        """
                   CREATE TABLE statement
                     (date text, doc_no text, description text, credit real)
                   """
    )

    with tqdm(total=len(records), desc="Writing to database") as pbar:
        for record in records:
            cursor.execute(
                "INSERT INTO statement VALUES (?, ?, ?, ?)",
                (
                    record["date"],
                    record["doc_no"],
                    record["description"],
                    record["credit"],
                ),
            )
            pbar.update(1)

    conn.commit()
    conn.close()


def write_to_csv(records, filename):
    fieldnames = ["date", "doc_no", "description", "credit"]

    with open(filename, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for record in records:
            writer.writerow(record)

    print(f"CSV file '{filename}' has been created successfully.")
