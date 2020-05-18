def check_slideshow_integrity(pictures, slideshow):
    """
    Test that slideshow is valid:
    - two adjacent slides have at least 1 common tag
    - TODO: a slide can contain max 1 horizontal image
    - TODO: a slide can contain 1 or 2 vertical image(s)
    """
    for i in range(len(slideshow) - 1):
        if slide_score(pictures, slideshow, i) < 1:
            return False

    return True


def load_pictures_from_file(filename='d_pet_pictures.txt', nb_lines=-1):
    """ Load pictures from Kaggle file """
    with open(filename, 'r') as file:
        lines = file.readlines()

    pictures = lines[1:] if nb_lines == -1 else lines[1:nb_lines + 1]

    return [picture.rstrip().split(' ') for picture in pictures]


def get_slide_tags(pictures, slideshow, index):
    tags = []

    if type(slideshow[index]) is tuple:
        pic_1, pic_2 = slideshow
        tags = pictures[pic_1][2:] + pictures[pic_2][2:]
    else:
        tags = pictures[slideshow[index]][2:]

    return set(tags)


def slide_score(pictures, slideshow, index):
    """
    Given a slide index, calculate score
    Slide N score is the tag_sets_score of tags from slide N and slide N+1
    """
    # if last slide in slideshow, score is 0 (no next slide)
    if slideshow[index] == slideshow[-1]:
        return 0

    # get tags for slide
    tags_n = get_slide_tags(pictures, slideshow, index)

    # get tags for next slide
    tags_n1 = get_slide_tags(pictures, slideshow, index + 1)

    # return score
    return tag_sets_score(tags_n, tags_n1)


def slideshow_score(pictures, slideshow):
    # initialize slideshow lenght, index and score
    lenght = len(slideshow)
    index = score = 0

    # calculate slideshow score
    while index + 1 < lenght:
        score += slide_score(pictures, slideshow, index)
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
    intersection = len(a.intersection(b))
    # calculate score: min of intersection, a_unique and b_unique
    return min(intersection, len(a) - intersection, len(b) - intersection)


def write_submission(slideshow):
    """ Write slideshow to submission txt file """
    with open('submission.txt', 'w') as file:
        # number of images
        file.write(f'{len(slideshow)}\n')

        for pic in slideshow:
            file.write(f'{pic}\n')
