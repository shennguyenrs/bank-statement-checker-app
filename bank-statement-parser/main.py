import argparse
from parsers import bidv_parser, icb_parser, vcb_parser
from utils.common import write_to_sql, write_to_csv


def main():
    parser = argparse.ArgumentParser(description="Parse bank statements")
    parser.add_argument("file_path", help="Path to the PDF file")
    parser.add_argument(
        "--bank-code", choices=["bidv", "icb", "vcb"], required=True, help="Bank code"
    )
    parser.add_argument(
        "--output",
        choices=["csv", "sqlite", "both"],
        default="both",
        help="Output format (default: both)",
    )
    args = parser.parse_args()

    print(f"Starting PDF processing for {args.bank_code.upper()}...")

    if args.bank_code == "bidv":
        records = bidv_parser.process_pdf(args.file_path)
    elif args.bank_code == "icb":
        records = icb_parser.process_pdf(args.file_path)
    elif args.bank_code == "vcb":
        records = vcb_parser.process_pdf(args.file_path)

    print(f"PDF processing complete. Total records: {len(records)}")

    if args.output in ["sqlite", "both"]:
        print("Writing records to database...")
        write_to_sql(records, f"{args.bank_code}.db")
        print("Database writing complete.")

    if args.output in ["csv", "both"]:
        print("Writing records to CSV...")
        write_to_csv(records, f"{args.bank_code}_statement.csv")
        print("CSV writing complete.")


if __name__ == "__main__":
    main()
