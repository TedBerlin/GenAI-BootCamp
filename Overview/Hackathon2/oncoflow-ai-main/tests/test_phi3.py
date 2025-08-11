import unittest
from phi3_ollama.summarizer_core_phi3 import Summarizer
import json

class TestPhi3Summarizer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.summarizer = Summarizer()
        with open("data/test.json", "r") as f:
            cls.test_data = json.load(f)
    
    def test_basic_summary(self):
        for example in self.test_data["documents"]:
            summary = self.summarizer.summarize_text(example["text"])
            self.assertTrue(len(summary) > 0, "Summary should not be empty")

    def test_guidance_prompt(self):
        prompt = "Focus on key findings."
        for example in self.test_data["documents"]:
            summary = self.summarizer.summarize_text(example["text"], guidance=prompt)
            self.assertTrue(len(summary) > 0)

if __name__ == "__main__":
    unittest.main()
