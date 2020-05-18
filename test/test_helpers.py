import unittest
import os

from helpers import helpers as hp

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
PICTURES_FILE = os.path.join(THIS_DIR, 'test_pictures.txt')
SUBMISSION_FILE = 'test_submission.txt'


class TestHelpers(unittest.TestCase):
    def test_tag_sets_score(self):
        """
        Test that we can calculate the score of two sets
        """
        # test case were 2 tags in common + 3 uniques for each set
        set1 = set(['aaa', 'bbb', 'ccc', 'ddd', 'eee'])
        set2 = set(['aaa', 'bbb', 'fff', 'ggg', 'hhh'])
        score = hp.tag_sets_score(set1, set2)
        self.assertEqual(score, 2)

        # test case where 2 tags in common, 2 unique for set 1, 1 unique for set 2
        set1 = set(['aaa', 'bbb', 'ccc', 'ddd'])
        set2 = set(['aaa', 'bbb', 'fff'])
        score = hp.tag_sets_score(set1, set2)
        self.assertEqual(score, 1)

        # test case where 0 tags in common
        set1 = set(['aaa', 'bbb', 'ccc', 'ddd'])
        set2 = set(['eee', 'fff', 'ggg'])
        score = hp.tag_sets_score(set1, set2)
        self.assertEqual(score, 0)

    def test_slide_score(self):
        """
        Test that we can calculate the score for a slide
        """
        pictures = hp.load_pictures_from_file(filename=PICTURES_FILE)
        slideshow = [1, 2, 3, 0]
        slide_index = 1
        score = hp.slide_score(pictures, slideshow, slide_index)
        self.assertEqual(score, 1)

    def test_slideshow_score(self):
        """
        Test that we can calculate the score for a slideshow as list
        """
        pictures = hp.load_pictures_from_file(filename=PICTURES_FILE)
        slideshow = [1, 2, 3, 0]
        score = hp.slideshow_score(pictures, slideshow)
        self.assertEqual(score, 3)

    def test_check_slideshow_integrity(self):
        """
        Test that slideshow is valid
        """
        pictures = hp.load_pictures_from_file(filename=PICTURES_FILE)
        non_valid_slideshow = [0, 1, 2, 3]
        valid_slideshow = [1, 2, 3, 0]

        self.assertFalse(
            hp.check_slideshow_integrity(pictures, non_valid_slideshow))
        self.assertTrue(hp.check_slideshow_integrity(pictures,
                                                     valid_slideshow))


if __name__ == '__main__':
    unittest.main()
