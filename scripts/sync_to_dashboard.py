"""
sync_to_dashboard.py

Syncs Lightning Network datasets from lightning-data to plebdashboard-ln (Option B data strategy).
Ensures plebdashboard-ln always has the latest parity with lightning-data without CORS overhead.
"""

import os
import shutil
import argparse
from pathlib import Path


def sync_data(source_dir: Path, target_dir: Path, dry_run: bool = False):
    print(f"Syncing from: {source_dir}")
    print(f"Syncing to:   {target_dir}")
    print("-" * 50)

    if not source_dir.exists():
        print(f"Error: Source directory {source_dir} does not exist.")
        return False

    if not target_dir.exists():
        print(f"Error: Target directory {target_dir} does not exist.")
        return False

    # 1. Sync root data files (parquets and JSONs)
    synced_count = 0
    for item in source_dir.iterdir():
        if item.is_file() and (item.suffix in ['.parquet', '.json']):
            dest = target_dir / item.name
            size_mb = item.stat().st_size / (1024 * 1024)
            print(f"[{'DRY-RUN' if dry_run else 'COPY'}] {item.name} ({size_mb:.2f} MB)")
            if not dry_run:
                shutil.copy2(item, dest)
            synced_count += 1

    # 2. Sync weekly_snapshots
    src_snapshots = source_dir / "weekly_snapshots"
    dest_snapshots = target_dir / "weekly_snapshots"
    if src_snapshots.exists():
        if not dry_run:
            dest_snapshots.mkdir(parents=True, exist_ok=True)
        for snap in src_snapshots.glob("*.json"):
            dest = dest_snapshots / snap.name
            print(f"[{'DRY-RUN' if dry_run else 'COPY'}] weekly_snapshots/{snap.name}")
            if not dry_run:
                shutil.copy2(snap, dest)
            synced_count += 1

    # 3. Sync graph directory
    src_graph = source_dir / "graph"
    dest_graph = target_dir / "graph"
    if src_graph.exists():
        if not dry_run:
            dest_graph.mkdir(parents=True, exist_ok=True)
        for graph_file in src_graph.glob("*.json"):
            dest = dest_graph / graph_file.name
            size_mb = graph_file.stat().st_size / (1024 * 1024)
            print(f"[{'DRY-RUN' if dry_run else 'COPY'}] graph/{graph_file.name} ({size_mb:.2f} MB)")
            if not dry_run:
                shutil.copy2(graph_file, dest)
            synced_count += 1

    print("-" * 50)
    print(f"Sync complete. Total files processed: {synced_count}")
    return True


def main():
    parser = argparse.ArgumentParser(description="Sync data from lightning-data to plebdashboard-ln")
    parser.add_argument("--dry-run", action="store_true", help="Simulate sync without writing files")
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parent
    source_data = repo_root / "data"

    # Default plebdashboard-ln location
    candidates = [
        repo_root.parent / "plebdashboard-ln" / "data",
        Path(r"C:\Users\14087\saurabh\dev\github\plebdashboard-ln\data")
    ]
    target_data = next((c for c in candidates if c.exists()), None)

    if not target_data:
        print("Error: Could not locate plebdashboard-ln/data directory.")
        return

    sync_data(source_data, target_data, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
