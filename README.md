# Bank Statement Checker App

This repository contains a multi-component project designed to handle various tasks, including a frontend application built with Svelte, a backend API using Cloudflare Workers, and a command-line tool for parsing bank statements from different banks ([VCB](https://drive.google.com/file/d/18dIWiReYtJkyuQ_8vSBJWweGaD71rBpu/view?fbclid=IwY2xjawFXkbRleHRuA2FlbQIxMAABHau6qAglZ3RpcytJHPKW1AUsTzr5zOnvJ0rHcMIOXajRK9_GjJeEcEpkjw_aem_FJdahzQvhliCozn8Wi4h2Q), [ICB](https://drive.google.com/file/d/1ffkLOPymobFQjlklgpjabeHK7TX1ic3B/view?fbclid=IwY2xjawFXkZhleHRuA2FlbQIxMAABHd0xpXiuNyIuzchhIxoCEXEkJG5C4-iZQ7NmdqEpXzSc_h4N0nEVje9BBA_aem_1iI761WruIVOyiT4xYfypg), [BIDV](https://drive.google.com/file/d/15CcMvRMufl2v4_wtTD-qpL_lokjLo326/view?fbclid=IwY2xjawFXkVxleHRuA2FlbQIxMAABHau6qAglZ3RpcytJHPKW1AUsTzr5zOnvJ0rHcMIOXajRK9_GjJeEcEpkjw_aem_FJdahzQvhliCozn8Wi4h2Q)).

## Table of Contents

- [Frontend](#frontend)
- [Backend](#backend)
- [Bank Statement Parser](#bank-statement-parser)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Frontend

The frontend is a Svelte application that provides a user interface for interacting with the backend API. It includes features such as filtering and sorting bank statements records.

### Key Features

- Built with Svelte and Vite
- Tailwind CSS for styling
- Integration with Cloudflare Workers for backend API

For more details, refer to the [frontend README](frontend/README.md).

## Backend

The backend is built using Cloudflare Workers and Hono framework. It provides an API for managing bank statements, including filtering and sorting functionalities.

### Key Features

- Cloudflare Workers for serverless deployment
- Hono framework for routing and middleware
- SQLite database for storing bank statements

For more details, refer to the [backend README](backend/README.md).

## Bank Statement Parser

The bank statement parser is a command-line tool for parsing bank statements from different banks and outputting the results in CSV or SQLite format.

### Key Features

- Supports multiple banks: VCB, ICB, BIDV
- Outputs to CSV and SQLite formats
- Uses concurrent processing for faster parsing

For more details, refer to the [bank statement parser README](bank-statement-parser/README.md).

## Setup and Installation

### Prerequisites

- Bun
- Python 3.8 or later

### Installation

1. Clone the repository:

   ```bash
   git clone <repository_url>
   ```

2. Install dependencies for the frontend:

   ```bash
   cd frontend
   bun install
   ```

3. Copy `.env.example` to `.env` and update the values:

   ```bash
   cp .env.example .env
   ```

4. Install dependencies for the backend:

   ```bash
   cd backend
   bun install
   ```

5. Copy `.dev.vars.example` to `.dev.vars` and update the values:

   ```bash
   cp .dev.vars.example .dev.vars
   ```

6. Install dependencies for the bank statement parser:
   ```bash
   cd bank-statement-parser
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

7. Create `D1` table from parsed statements in `backend`:

   ```bash
   bunx wrangler d1 execute <db-name> --local file=<ouput-file-sql>
   ```

## Usage

### Frontend

To start the frontend development server:

```bash
cd frontend
bun run dev
```

### Backend

To start the backend development server:

```bash
cd backend
bun run dev
```

### Bank Statement Parser

To parse a bank statement:

```bash
cd bank-statement-parser
python main.py <file_path> --bank-code <bank_code> [--output <output_format>]
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License.
