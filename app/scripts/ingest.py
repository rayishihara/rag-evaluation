import argparse
import os
import sys
from pathlib import Path

import snowflake.connector

PROCESS_DOCS_SQL = Path(__file__).resolve().parent.parent / "backend" / "sql" / "process_docs.sql"


def connect() -> snowflake.connector.SnowflakeConnection:
    role = os.environ["SNOWFLAKE_ROLE"]
    if role.upper() == "RAG_APP_ROLE":
        print("WARNING: SNOWFLAKE_ROLE is RAG_APP_ROLE, which cannot write; use RAG_INGEST_ROLE", file=sys.stderr)
    # Pass the PAT in place of a password when set
    secret = os.environ.get("SNOWFLAKE_PAT") or os.environ["SNOWFLAKE_PASSWORD"]
    return snowflake.connector.connect(
        account=os.environ["SNOWFLAKE_ACCOUNT"],
        user=os.environ["SNOWFLAKE_USER"],
        password=secret,
        role=role,
        warehouse=os.environ["SNOWFLAKE_WAREHOUSE"],
        database=os.environ["SNOWFLAKE_DATABASE"],
        schema=os.environ["SNOWFLAKE_SCHEMA"],
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Upload PDF/HTML documents to Snowflake and chunk them for Cortex Search.")
    parser.add_argument("pdf_dir", type=Path, help="Local directory containing PDF or HTML files (non-recursive)")
    args = parser.parse_args()

    pdf_dir: Path = args.pdf_dir.resolve()
    if not pdf_dir.is_dir():
        print(f"Not a directory: {pdf_dir}", file=sys.stderr)
        return 1
    pdfs = sorted(p for p in pdf_dir.iterdir() if p.is_file() and p.suffix.lower() in {".pdf", ".html", ".htm"})
    if not pdfs:
        print(f"No PDF or HTML files found in {pdf_dir}", file=sys.stderr)
        return 1

    conn = None
    try:
        conn = connect()
        cur = conn.cursor()
        for pdf in pdfs:
            # Quote the path so spaces and Windows paths survive
            file_uri = "file://" + pdf.as_posix().replace("'", "\\'")
            cur.execute(f"PUT '{file_uri}' @raw_docs_stage AUTO_COMPRESS = FALSE OVERWRITE = TRUE")
            status = cur.fetchone()[6]
            print(f"{pdf.name}: {status}")

        cur.execute("ALTER STAGE raw_docs_stage REFRESH")
        cur.execute(PROCESS_DOCS_SQL.read_text())
        print(f"Inserted {cur.rowcount} chunk rows")
        cur.execute("ALTER CORTEX SEARCH SERVICE docs_search_service REFRESH")
        print("Search service refresh triggered")
        return 0
    except Exception as exc:
        print(f"Ingestion failed: {exc}", file=sys.stderr)
        return 1
    finally:
        if conn is not None:
            conn.close()


if __name__ == "__main__":
    sys.exit(main())
