# Input latency analyzer

A command-line tool for reviewing response times from embedded input experiments. Use it to compare the timestamp of a sensor event with the timestamp of its corresponding output.

## Try the sample

Run `python latency.py sample.csv` with Python 3. The synthetic capture has four samples, a median of 130 microseconds, and a nearest-rank 95th percentile of 180 microseconds.

For your own experiment, record one event pair per CSV row using the columns `input_us` and `output_us`. Use integer microseconds from the same clock and account for timer rollover before exporting.

Run `python -m unittest -v` to check the example, percentile calculation, and invalid-input handling.
