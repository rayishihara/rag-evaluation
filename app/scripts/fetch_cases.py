import argparse
import html
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://www.courtlistener.com/api/rest/v4"
TEXT_FIELDS = ["html_with_citations", "html", "html_lawbox", "html_columbia", "xml_harvard", "plain_text"]


def get(url: str, token: str) -> dict:
    req = urllib.request.Request(url, headers={"Authorization": f"Token {token}"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.load(resp)


def search(query: str, court: str, limit: int, token: str) -> list[dict]:
    params = urllib.parse.urlencode({"type": "o", "q": query, "court": court, "order_by": "score desc"})
    url = f"{API}/search/?{params}"
    hits: list[dict] = []
    while url and len(hits) < limit:
        page = get(url, token)
        hits.extend(page["results"])
        url = page.get("next")
    return hits[:limit]


def opinion_html(opinion_id: int, token: str) -> tuple[str, str]:
    op = get(f"{API}/opinions/{opinion_id}/?fields=type,{','.join(TEXT_FIELDS)}", token)
    for field in TEXT_FIELDS:
        text = op.get(field)
        if text:
            # Wrap plain text so the file stays valid HTML
            body = f"<pre>{html.escape(text)}</pre>" if field == "plain_text" else text
            return op.get("type", ""), body
    return op.get("type", ""), ""


def slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")[:80]


def main() -> int:
    parser = argparse.ArgumentParser(description="Download CourtListener opinions as HTML files for ingest.py.")
    parser.add_argument("out_dir", type=Path, help="Directory to write one HTML file per case")
    parser.add_argument("--query", default="breach of contract", help="CourtListener search query")
    parser.add_argument("--court", default="delch", help="CourtListener court ID (default: Delaware Chancery)")
    parser.add_argument("--limit", type=int, default=100, help="Maximum number of cases")
    args = parser.parse_args()

    token = os.environ.get("COURTLISTENER_TOKEN")
    if not token:
        print("COURTLISTENER_TOKEN is not set", file=sys.stderr)
        return 1
    out_dir: Path = args.out_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    hits = search(args.query, args.court, args.limit, token)
    print(f"Found {len(hits)} cases")
    for hit in hits:
        path = out_dir / f"{hit['cluster_id']}-{slugify(hit['caseName'])}.html"
        if path.exists():
            print(f"{path.name}: skipped (exists)")
            continue
        # Sort by type code so lead opinions come before concurrences and dissents
        opinions = sorted(opinion_html(op["id"], token) for op in hit["opinions"])
        sections = "\n".join(f"<h2>{html.escape(t)}</h2>\n{body}" for t, body in opinions if body)
        if not sections:
            print(f"{path.name}: skipped (no text)")
            continue
        header = (
            f"<h1>{html.escape(hit['caseName'])}</h1>\n"
            f"<p>{html.escape(hit['court'])} · Filed {html.escape(hit.get('dateFiled') or '')}"
            f" · {html.escape('; '.join(hit.get('citation') or []))}</p>"
        )
        path.write_text(f"<!doctype html>\n<html><body>\n{header}\n{sections}\n</body></html>\n", encoding="utf-8")
        print(f"{path.name}: written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
