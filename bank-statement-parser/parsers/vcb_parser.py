import re
import fitz
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm

# Compile regex patterns once
DATE_PATTERN = re.compile(r"(\d{2}/09/2024)")
DOC_NO_PATTERN = re.compile(r"(\d{4}\.\d{4})")
POSTAL_PATTERN = re.compile(r"(Postal)")


def process_page(args):
    """Process a single page and return records"""
    pdf_path, page_num = args
    doc = fitz.open(pdf_path)
    page = doc[page_num]
    lines = page.get_text().split("\n")
    records = []
    date_pos = [i for i, line in enumerate(lines) if DATE_PATTERN.match(line)]

    for i in range(len(date_pos) - 1):
        records.append(parse_records(lines, date_pos[i], date_pos[i + 1]))

    if date_pos:
        records.append(parse_records(lines, date_pos[-1], len(lines)))

    doc.close()
    return records


def parse_records(lines, current_date_pos, next_date_pos):
    """Parse lines to a record"""
    record = {"date": "", "doc_no": "", "description": "", "credit": 0.0}

    for line in lines[current_date_pos:next_date_pos]:
        if not record["date"]:
            date_match = DATE_PATTERN.match(line)
            if date_match:
                record["date"] = date_match.group(1)
                continue

        if not record["doc_no"]:
            doc_no_match = DOC_NO_PATTERN.match(line)
            if doc_no_match:
                record["doc_no"] = f"vcb.{doc_no_match.group(1)}"
                continue

        record["description"] += " " + line

    description_parts = record["description"].strip().split()
    if description_parts:
        record["credit"] = float(description_parts[0].replace(".", ""))
        record["description"] = " ".join(description_parts[1:])

        postal_index = next(
            (
                i
                for i, word in enumerate(description_parts)
                if POSTAL_PATTERN.match(word)
            ),
            None,
        )
        if postal_index:
            record["description"] = " ".join(description_parts[1:postal_index])

    return record


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
