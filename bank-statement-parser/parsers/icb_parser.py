import re
import fitz
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm

# Compile regex pattern at once
DATE_PATTERN = re.compile(r"(\d{,6} \d{2}/09/2024)")


def process_page(args):
    """Process a single page and return records"""
    pdf_path, page_num = args
    doc = fitz.open(pdf_path)
    records = parse_records(doc[page_num].find_tables()[0])
    doc.close()
    return records


def parse_records(table) -> list:
    """
    Parse page to a record
    """
    records = []

    for line in table.extract():
        record = {"date": "", "doc_no": "", "description": "", "credit": 0.0}
        if line[0].isdigit():
            record["doc_no"] = f"icb.{line[0]}"
            record["date"] = line[1].split("\n")[0]
            record["description"] = " ".join(line[2].split("\n"))

            # Remove minus for one record having negative value due to the table recognition
            if line[3][0] == "-":
                record["credit"] = float(line[3].split(" ")[1].replace(".", ""))
            elif line[3][-1] == "-":
                record["credit"] = float(line[3].split("\n")[0].replace(".", ""))
            else:
                record["credit"] = float(line[3].replace(".", ""))

            records.append(record)

    return records


def process_pdf(pdf_path, batch_size=100):
    """Process PDF in batches with progress bar"""
    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    doc.close()

    all_records = []

    with ProcessPoolExecutor() as executor:
        batches = range(0, total_pages, batch_size)
        with tqdm(total=total_pages, desc="Processing PDF") as pbar:
            for i in batches:
                batch_pages = range(i, min(i + batch_size, total_pages))
                batch_args = [(pdf_path, j) for j in batch_pages]
                batch_results = list(executor.map(process_page, batch_args))
                all_records.extend(
                    [item for sublist in batch_results for item in sublist]
                )
                pbar.update(len(batch_pages))

    return all_records
