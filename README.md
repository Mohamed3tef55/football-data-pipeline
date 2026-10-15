# Mini Football Data Pipeline (ETL)

A lightweight Data Engineering pipeline built with Python and SQLite, demonstrating fundamental ETL processes and Git workflows.

## Features
- **Extract:** Ingests raw football player statistics from a CSV file.
- **Transform:** Cleans whitespace, drops invalid rows, handles missing numeric values, and formats data types.
- **Load:** Creates an SQLite table using SQL and upserts the clean data.

## Tech Stack
- Python 3
- SQLite3
- Git & GitHub

## How to Run
```bash
python src/pipeline.py
