import sqlite3
import csv
from tqdm import tqdm


def write_to_sql(records, db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS statement")
    cursor.execute("""
                   CREATE TABLE statement
                   (id integer, date text, doc_no text, description text, credit real)
                   """)

    total_records = len(records)
    with tqdm(total=total_records, desc="Writing to database") as pbar:
        for i in range(total_records):
            record = records[i]
            cursor.execute(
                "INSERT INTO statement VALUES (?, ?, ?, ?, ?)",
                (
                    i + 1,
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
        with tqdm(total=len(records), desc="Writing to CSV file") as pbar:
            for record in records:
                writer.writerow(record)
                pbar.update(1)

    print(f"CSV file '{filename}' has been created successfully.")
