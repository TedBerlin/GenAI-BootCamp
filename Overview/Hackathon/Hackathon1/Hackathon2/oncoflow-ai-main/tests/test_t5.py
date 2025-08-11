import unittest
from t5_pipeline.summarizer_core_t5 import Summarizer
import json

class TestT5Summarizer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.summarizer = Summarizer()
        with open("data/test.json", "r") as f:
            cls.test_data = json.load(f)
    
    def test_basic_summary(self):
        for example in self.test_data["documents"]:
            summary = self.summarizer.summarize_text(example["text"])
            self.assertTrue(len(summary) > 0, "Summary should not be empty")

if __name__ == "__main__":
    unittest.main()
