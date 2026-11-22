import unittest
from io import StringIO
from pathlib import Path

from latency import summarize


class CaptureTests(unittest.TestCase):
    def test_sample(self):
        with Path(__file__).with_name("sample.csv").open() as stream:
            self.assertEqual(summarize(stream), (4, 130, 180, 180))

    def test_nearest_rank(self):
        records = "".join(f"0,{i}\n" for i in range(1, 21))
        self.assertEqual(summarize(StringIO("input_us,output_us\n" + records)),
                         (20, 10.5, 19, 20))

    def test_duplicate_timestamp_columns(self):
        for field in ("input_us", "output_us"):
            capture = StringIO(f"input_us,output_us,{field}\n0,10,90\n")
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, field):
                summarize(capture)

    def test_invalid_captures(self):
        for capture in ["bad_header\n", "input_us,output_us\n",
                        "input_us,output_us\n3,2\n", "input_us,output_us\nx,5\n"]:
            with self.subTest(capture=capture), self.assertRaises(ValueError):
                summarize(StringIO(capture))
