import random


def check_slideshow_integrity(pictures, slideshow):
    """
    Test that slideshow is valid:
    - two adjacent slides have at least 1 common tag
    - a slide can contain max 1 horizontal image
    - a slide can contain 1 or 2 vertical image(s)
    """
    slideshow_len = len(slideshow)
    used = []

    for i, slide in enumerate(slideshow):
        # two adjacent slides need at least 1 common tag. Last slide has score of 0 by design
        if i < slideshow_len - 1:
            assert slide_score(pictures, slideshow, i) >= 1

        # slide can contain 1 horizontal image or (1 or 2) vertical images
        # slide cannot contain image that's already been used
        if type(slide) is tuple:
            assert slide[0] not in used
            assert pictures[slide[0]][0] == 'V'
            used.append(slide[0])
            assert slide[1] not in used
            assert pictures[slide[1]][0] == 'V'
            used.append(slide[1])
        else:
            assert slide not in used
            assert pictures[slide][0] == 'H'
            used.append(slide)

    print(
        f'{len(used)}/{len(pictures)} images used for {len(slideshow)} slides')
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
        pic_1, pic_2 = slideshow[index]
        tags = set(pictures[pic_1][2:]).union(pictures[pic_2][2:])
    else:
        tags = set(pictures[slideshow[index]][2:])

    return tags


def pair_verticals(pictures, remaining, params):
    paired = []

    min_tags = params['min_tags']
    max_tags = params['max_tags']
    nb_candidates = params['nb_candidates']

    # try to pair all pictures
    while len(remaining) > 1:
        # current picture tags
        curr_tags = get_slide_tags(pictures, [remaining[0]], 0)

        # choose random nb_candidates pictures
        candidates = random.sample(remaining[1:], min(nb_candidates, len(remaining[1:])))

        # look for best candidates
        min_common = 1000
        pair_tags = 0
        best_candidate = None

        for cand in candidates:
            # get candidate tags
            cand_tags = get_slide_tags(pictures, [cand], 0)

            # calc # of common tags
            commons = len(curr_tags.intersection(cand_tags))

            # try to evenly distribute # tags in resulting pictures
            total_tags = len(cand_tags) + len(curr_tags) - commons

            if commons == 0 and total_tags >= min_tags and total_tags <= max_tags:
                best_candidate = cand
                break
            elif commons < min_common or (commons == min_common and total_tags > pair_tags):
                min_common = commons
                best_candidate = cand
                pair_tags = total_tags

        # pair current picture with best candidate
        if best_candidate is not None:
            pair = (remaining[0], cand)
            paired.append(pair)
            remaining.remove(cand)
            remaining.pop(0)

    return paired


def slide_score(pictures, slideshow, index):
    """
    Given a slide index, calculate score
    Slide N score is the tag_sets_score of tags from slide N and slide N+1
    """
    max_index = len(slideshow) - 1

    # if last slide in slideshow, score is 0 (no next slide)
    if index == max_index:
        return 0

    # if index out of slideshow, return 0
    if index < 0 or index > max_index:
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


def submission_score(pictures, filename):
    """ Calculate score of submission file """
    # read submission file
    with open(filename, 'r') as file:
        lines = file.readlines()

    # define slideshow
    nb_slides, slideshow = int(lines[0]), lines[1:]

    # convert slideshow to list
    slideshow_list = []

    for slide in slideshow:
        slide = slide.rstrip().split(' ')
        if len(slide) == 2:
            slide = tuple([int(slide[0]), int(slide[1])])
        else:
            slide = int(slide[0])

        slideshow_list.append(slide)

    # get score
    score = slideshow_score(pictures, slideshow_list)

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

        for slide in slideshow:
            if type(slide) is tuple:
                file.write(f'{slide[0]} {slide[1]}\n')
            else:
                file.write(f'{slide}\n')
