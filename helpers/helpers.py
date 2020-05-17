import numpy as np


def check_slideshow_integrity(pictures, slideshow):
    """
    Test that slideshow is valid:
    - two adjacent slides have at least 1 common tag
    - TODO: a slide can contain max 1 horizontal image
    - TODO: a slide can contain 1 or 2 vertical image(s)
    """
    for i in range(len(slideshow) - 1):
        slide1 = slideshow[i]
        slide2 = slideshow[i + 1]
        if slide_score(pictures, slide1, slide2) < 1:
            print(f'Slides {i} and {i+1} cannot be adjacents')
            print(pictures[slide1])
            print(pictures[slide2])
            return False

    return True


def load_pictures_from_file(filename='d_pet_pictures.txt', nb_lines=-1):
    """ Load pictures from Kaggle file """
    with open(filename, 'r') as file:
        lines = file.readlines()
    return lines[1:] if nb_lines == -1 else lines[1:nb_lines + 1]


def slide_score(pictures, i, j):
    """ Given two picture indexes, calculate score """
    # get both images data
    n = pictures[i].rstrip().split(' ')[2:]
    n_1 = pictures[j].rstrip().split(' ')[2:]
    # return score
    return tag_sets_score(n, n_1)


def slideshow_score(pictures, slideshow):
    # initialize slideshow lenght, index and score
    lenght = len(slideshow)
    index = score = 0

    # calculate slideshow score
    while index + 1 < lenght:
        score += slide_score(pictures, slideshow[index], slideshow[index + 1])
        index += 1

    return score


def submission_score(filename):
    """ Calculate score of submission file """
    # load pictures
    pictures = load_pictures_from_file()
    # read submission file
    with open(filename, 'r') as file:
        lines = file.readlines()

    # define slideshow
    nb_slides, slideshow = int(lines[0]), lines[1:]

    # convert slideshow to list
    slideshow = [int(slide.rstrip()) for slide in slideshow]

    # get score
    score = slideshow_score(pictures, slideshow)

    return nb_slides, score


def tag_sets_score(a, b):
    """ Given two sets of tags, calculate score """
    # tags both in a and b
    intersection = set(a).intersection(b)
    # tags in a NOT in b
    a_unique = np.setdiff1d(a, b, assume_unique=True)
    # tags in b NOT in a
    b_unique = np.setdiff1d(b, a, assume_unique=True)
    # calculate score: min of intersection, a_unique and b_unique
    return min(len(intersection), len(a_unique), len(b_unique))


def write_submission(slideshow):
    """ Write slideshow to submission txt file """
    with open('submission.txt', 'w') as file:
        # number of images
        file.write(f'{len(slideshow)}\n')

        for pic in slideshow:
            file.write(f'{pic}\n')
