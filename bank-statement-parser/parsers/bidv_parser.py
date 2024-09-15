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
    tables = doc[page_num].find_tables()
    records = []

    if len(tables.tables) > 0:
        for table in tables.tables:
            records.extend(parse_records(table))

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
            record["doc_no"] = f"bidv.{line[0]}"
            record["date"] = line[1].split(" ")[0]
            record["description"] = " ".join(line[3].split("\n"))
            record["credit"] = float(line[2].replace(".", ""))
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
