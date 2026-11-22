"""Summarize paired input/output timestamps in integer microseconds."""
import argparse
import csv
import statistics


def summarize(stream):
    rows = csv.DictReader(stream)
    if not {"input_us", "output_us"}.issubset(rows.fieldnames or []):
        raise ValueError("required CSV columns are input_us and output_us")
    delays = []
    for row in rows:
        try:
            start, end = int(row["input_us"]), int(row["output_us"])
        except (TypeError, ValueError):
            raise ValueError(f"line {rows.line_num}: expected integer timestamps") from None
        if start < 0 or end < start:
            raise ValueError(f"line {rows.line_num}: timestamps must satisfy 0 <= input <= output")
        delays.append(end - start)
    if not delays:
        raise ValueError("capture contains no samples")
    delays.sort()
    return len(delays), statistics.median(delays), delays[(95 * len(delays) - 1) // 100], delays[-1]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("capture", help="CSV file containing paired timestamps")
    args = parser.parse_args()
    try:
        with open(args.capture, newline="", encoding="utf-8-sig") as capture:
            count, median, p95, maximum = summarize(capture)
    except (OSError, ValueError, csv.Error) as error:
        parser.exit(1, f"{error}\n")
    print(f"Samples: {count}\nMedian: {median:g} us\nP95: {p95} us\nMaximum: {maximum} us")
