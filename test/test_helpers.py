import unittest
import os

from helpers import helpers as hp

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
PICTURES_FILE = os.path.join(THIS_DIR, 'test_pictures.txt')
SUBMISSION_FILE = os.path.join(THIS_DIR, 'test_submission.txt')


class TestHelpers(unittest.TestCase):
    def test_pair_verticals(self):
        pictures = [
            ['V', '4', 'aaa', 'bbb', 'ccc', 'ddd'],
            ['V', '3', 'aaa', 'bbb', 'ddd'],
            ['V', '4', 'aaa', 'bbb', 'ccc', 'eee'],
            ['V', '2', 'aaa', 'eee'],
            ['V', '6', 'aaa', 'eee', 'fff', 'bbb', 'ccc', 'ddd'],
        ]

        verticals = [i for i, pic in enumerate(pictures) if pic[0] == 'V']

        paired = hp.pair_verticals(pictures, verticals)
        used = []

        # check that each element is a tuple of 2 different integers
        for pair in paired:
            # check that each element is a tuple of size 2
            self.assertEqual(type(pair), tuple)
            self.assertEqual(len(pair), 2)
            # check that each element of tuple is an int
            self.assertEqual(type(pair[0]), int)
            self.assertEqual(type(pair[1]), int)
            # check that each picture in tuple are different
            self.assertFalse(pair[0] == pair[1])
            # check that each picture correspond to an index in pictures
            self.assertTrue(pair[0] < len(pictures))
            self.assertTrue(pair[1] < len(pictures))
            # check that pictures aren't used twice
            self.assertTrue(pair[0] not in used)
            self.assertTrue(pair[1] not in used)
            # add pictures to "used" set
            used.extend([pair[0], pair[1]])

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
        # slide with 1 horizontal image
        slideshow = [1, 2, 3, 0]
        score = hp.slide_score(pictures, slideshow, 1)
        self.assertEqual(score, 1)
        # slide with 2 vertical images
        slideshow = [(1, 2), 3, 0]
        score = hp.slide_score(pictures, slideshow, 0)
        self.assertEqual(score, 1)

    def test_slideshow_score(self):
        """
        Test that we can calculate the score for a slideshow as list
        """
        pictures = hp.load_pictures_from_file(filename=PICTURES_FILE)
        slideshow = [1, 2, 3, 0]
        score = hp.slideshow_score(pictures, slideshow)
        self.assertEqual(score, 3)

    def test_submission_score(self):
        pictures = hp.load_pictures_from_file(filename=PICTURES_FILE)
        nb_slides, score = hp.submission_score(pictures, SUBMISSION_FILE)
        self.assertEqual(nb_slides, 4)
        self.assertEqual(score, 3)

    def test_check_slideshow_integrity(self):
        """
        Test that slideshow is valid
        """
        pictures = hp.load_pictures_from_file(filename=PICTURES_FILE)
        # non valid: slide 0 and 1 have no tags in common
        with self.assertRaises(AssertionError):
            hp.check_slideshow_integrity(pictures, [0, 4, 3])
        # non valid: slide 0 and 1 contain only 1 V picture
        with self.assertRaises(AssertionError):
            hp.check_slideshow_integrity(pictures, [1, 2, 3, 0])
        # non valid: slide 2 and 3 contain same picture
        with self.assertRaises(AssertionError):
            hp.check_slideshow_integrity(pictures, [(1, 2), 3, 0, 3])
        # valid slideshow
        self.assertTrue(
            hp.check_slideshow_integrity(pictures, [4, (1, 2), 3, 0]))


if __name__ == '__main__':
    unittest.main()
