#!/usr/bin/env python3
"""
pe4.py — Pair Exercise #4 (Fall 2025)

A. Sequentially download Wikipedia page references for topics related to a query.
B. Concurrently do the same using ThreadPoolExecutor.map.

Requirements:
- pip install wikipedia

Notes:
- Uses auto_suggest=False per instructions when fetching pages.
- Writes one "<Page Title>.txt" file per topic with references (one per line).
- Prints elapsed time for sequential and concurrent runs separately.
"""

from __future__ import annotations

import argparse
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Iterable, List, Optional, Tuple

try:
    import wikipedia  # type: ignore
    from wikipedia.exceptions import DisambiguationError, PageError  # type: ignore
except Exception as e:  # pragma: no cover
    print(
        "This script requires the 'wikipedia' package. Install it with:\n"
        "    pip install wikipedia\n\n"
        f"Import error details: {e}",
        file=sys.stderr,
    )
    sys.exit(1)


def _slugify_filename(title: str) -> str:
    """
    Sanitize a Wikipedia page title for safe filesystem use.
    Preserves spaces; strips chars that are invalid on common filesystems.
    """
    # Remove characters forbidden on Windows / common FS: \ / : * ? " < > |
    cleaned = re.sub(r'[\\/*?:"<>|]', " ", title)
    # Collapse repeated whitespace
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    # Safety: limit very long filenames
    return cleaned[:200] if len(cleaned) > 200 else cleaned


def _write_references_file(title: str, references: Iterable[str]) -> Path:
    """
    Write references to a UTF-8 .txt file named after the (sanitized) page title.
    Each reference goes on its own line.
    Returns the created file path.
    """
    safe_title = _slugify_filename(title)
    out_path = Path(f"{safe_title}.txt")
    with out_path.open("w", encoding="utf-8") as f:
        for ref in references:
            f.write(f"{str(ref)}\n")
    return out_path


def _fetch_page(topic: str):
    """
    Retrieve a wikipedia page object for the topic, prioritizing auto_suggest=False as required.
    If the topic is a disambiguation, try the first viable option (best-effort).
    """
    try:
        return wikipedia.page(topic, auto_suggest=False)
    except DisambiguationError as e:
        # Try a few disambiguation options deterministically
        for opt in e.options[:5]:
            try:
                return wikipedia.page(opt, auto_suggest=False)
            except Exception:
                continue
        raise
    except PageError:
        # Fallback: allow wikipedia to auto-suggest if the exact page wasn't found
        return wikipedia.page(topic, auto_suggest=True)


def wiki_dl_and_save(topic: str) -> Tuple[str, int, Optional[Path]]:
    """
    Download a single topic's references and save to "<title>.txt".
    Returns (page_title, num_references, path_or_None).
    """
    page = _fetch_page(topic)
    title = page.title
    references = list(page.references)  # typically a list[str]
    path = _write_references_file(title, references)
    return (title, len(references), path)


def run_sequential(topics: List[str]) -> float:
    """
    Iterate topics and write reference files one-by-one.
    Returns elapsed time in seconds.
    """
    t0 = time.perf_counter()
    for t in topics:
        try:
            title, n, path = wiki_dl_and_save(t)
            print(f"[SEQ] Saved {n:>3} refs for: {title}  ->  {path.name}")
        except Exception as e:
            print(f"[SEQ] Skipped '{t}': {e}", file=sys.stderr)
    t1 = time.perf_counter()
    elapsed = t1 - t0
    print(f"[SEQ] Completed {len(topics)} topic(s) in {elapsed:.2f}s")
    return elapsed


def run_concurrent(topics: List[str], workers: int = 8) -> float:
    """
    Execute wiki_dl_and_save for each topic concurrently with ThreadPoolExecutor.map.
    Returns elapsed time in seconds.
    """
    t0 = time.perf_counter()
    # To keep .map robust, wrap the call to handle exceptions per-topic and continue.
    def _safe(topic: str) -> Optional[Tuple[str, int, Optional[Path]]]:
        try:
            return wiki_dl_and_save(topic)
        except Exception as e:
            print(f"[CONC] Skipped '{topic}': {e}", file=sys.stderr)
            return None

    with ThreadPoolExecutor(max_workers=workers) as ex:
        for result in ex.map(_safe, topics):
            if result is None:
                continue
            title, n, path = result
            print(f"[CONC] Saved {n:>3} refs for: {title}  ->  {path.name}")
    t1 = time.perf_counter()
    elapsed = t1 - t0
    print(f"[CONC] Completed {len(topics)} topic(s) in {elapsed:.2f}s")
    return elapsed


def _search_topics(query: str, max_topics: Optional[int]) -> List[str]:
    topics = wikipedia.search(query)
    if max_topics is not None:
        topics = topics[:max_topics]
    return topics


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Pair Exercise 4: Wikipedia references downloader")
    parser.add_argument("--query", default="generative artificial intelligence", help="Search query (default: %(default)s)")
    parser.add_argument("--max-topics", type=int, default=None, help="Limit number of topics from search")
    parser.add_argument("--workers", type=int, default=8, help="Number of threads for concurrent run (default: %(default)s)")
    args = parser.parse_args(argv)

    # For both sections A and B we search based on the query
    topics = _search_topics(args.query, args.max_topics)
    print(f"Found {len(topics)} topic(s) for query: {args.query!r}")
    if not topics:
        return 0

    print("\n=== Section A: Sequential download ===")
    seq_time = run_sequential(topics)

    print("\n=== Section B: Concurrent download ===")
    conc_time = run_concurrent(topics, workers=args.workers)

    print("\n=== Summary ===")
    print(f"Sequential time: {seq_time:.2f}s")
    print(f"Concurrent time: {conc_time:.2f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
