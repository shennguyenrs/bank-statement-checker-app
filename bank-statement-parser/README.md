# Bank Statement Parser

This project is a command-line tool for parsing bank statements from different banks and outputting the results in CSV or SQLite format.

## Usage

```
python main.py <file_path> --bank-code <bank_code> [--output <output_format>]
```

### Arguments

1. `file_path`: Path to the PDF file containing the bank statement (required)

2. `--bank-code`: Bank code for the statement (required)

   - Choices: "bidv", "icb", "vcb"

3. `--output`: Output format (optional)
   - Choices: "csv", "sqlite", "both"
   - Default: "both"

## Examples

1. Parse a BIDV bank statement and output to both CSV and SQLite:

   ```
   python main.py statement.pdf --bank-code bidv
   ```

2. Parse an ICB bank statement and output only to CSV:

   ```
   python main.py statement.pdf --bank-code icb --output csv
   ```

3. Parse a VCB bank statement and output only to SQLite:
   ```
   python main.py statement.pdf --bank-code vcb --output sqlite
   ```

## Output

- CSV output will be saved as `<bank_code>_statement.csv`
- SQLite output will be saved as `<bank_code>.db`

## Requirements

- Python 3.8 or later
- Required libraries: (list the required libraries here)

## Installation

1. Clone this repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
