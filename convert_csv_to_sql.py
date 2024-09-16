import csv
import argparse
from datetime import datetime


def convert_to_sql(file_path):
    with open(file_path, newline='') as file:
        reader = csv.reader(file)
        _ = next(reader)

        with open("output.sql", "w") as output:
            output.write("-- SQL statements generated from CSV file\n")

            # Create table
            output.write("DROP TABLE IF EXISTS statement;\n")
            output.write(
                "CREATE TABLE statement (id integer, date text, doc_no text, description text, credit real);\n"
            )

            # Write rows
            id = 1
            for row in reader:
                date_obj = datetime.strptime(row[0], "%d/%m/%Y")
                formatted_date_str = date_obj.strftime("%Y-%m-%d")
                doc_no = row[1]
                descripttion = row[2]
                credit = row[3]
                output.write(
                    f"INSERT INTO statement VALUES ({id}, '{formatted_date_str}', '{doc_no}', '{descripttion}', {credit});\n"
                )
                id += 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", help="CSV file path")
    args = parser.parse_args()

    print("Writing records to output.sql")
    convert_to_sql(args.file_path)
    print("SQL writing complete.")


if __name__ == '__main__':
    main()
