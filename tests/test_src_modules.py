import unittest
import pandas as pd
from src.preprocess import clean_text, preprocess_dataframe
from src.skill_extractor import extract_skills

class TestPreprocess(unittest.TestCase):

    def test_clean_text(self):
        self.assertEqual(clean_text("Hello, World!"), "hello world")
        self.assertEqual(clean_text("ML/AI#2024"), "mlai2024")
        self.assertEqual(clean_text(""), "")
        self.assertEqual(clean_text(None), "")

    def test_preprocess_dataframe(self):
        df = pd.DataFrame({"description": ["Data Scientist with Python skills.", None]})
        result = preprocess_dataframe(df)
        self.assertIn("clean_description", result.columns)
        self.assertEqual(result.loc[0, "clean_description"], "data scientist with python skills")
        self.assertEqual(result.loc[1, "clean_description"], "")

class TestSkillExtractor(unittest.TestCase):

    def test_extract_skills(self):
        text = "Looking for someone skilled in Python, SQL, and machine learning."
        skills = extract_skills(text)
        expected_skills = set(["python", "sql", "machine learning"])
        self.assertTrue(expected_skills.issubset(set(skills)))

        # Test with None input
        self.assertEqual(extract_skills(None), [])

        # Test with unrelated text
        self.assertEqual(extract_skills("This role involves marketing and design."), [])

if __name__ == '__main__':
    unittest.main()
