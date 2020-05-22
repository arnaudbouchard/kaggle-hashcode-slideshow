from helpers import helpers as hp
import random
import time
import os

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
PICTURES_FILE = os.path.join(THIS_DIR, 'd_pet_pictures.txt')
SUBMISSION_FILE = 'submission.txt'


def main():
    # define our parameters
    first_picture_nb_tags = 10
    pairing_candidates = 1000
    nb_candidates = 200
    nb_lignes = -1  # for when testing on subset of pictures
    acceptable_score = 6

    # start timing
    start = time.perf_counter()

    # Read our input
    pictures = hp.load_pictures_from_file(filename=PICTURES_FILE,
                                          nb_lines=nb_lignes)

    print(f'{len(pictures)} pictures loaded')

    # separate H and V pictures
    horizontals = [i for i, pic in enumerate(pictures) if pic[0] == 'H']
    verticals = [i for i, pic in enumerate(pictures) if pic[0] == 'V']

    print('H/V splitted')

    # pair vertical pictures
    verticals = hp.pair_verticals(pictures, verticals, pairing_candidates)

    # assemble H and V pictures
    remaining = horizontals + verticals
    print('Picture set built')

    # shuffle pictures
    # TODO:

    # delete horizontals & verticals
    del horizontals, verticals

    # intialize slideshow
    slideshow = []

    # look for our first picture with min first_picture_nb_tags tags
    for pic in remaining:
        # get tags (use get_slide_tags with "fake" slideshow of 1 picture)
        tags = hp.get_slide_tags(pictures, [pic], 0)

        if len(tags) <= first_picture_nb_tags:
            slideshow.append(pic)
            remaining.remove(pic)
            break

    # intialize a "tried" set
    tried = set()

    # try to assign all pictures / tuple of pictures
    while len(remaining) > 0 and tried != set(remaining):
        # choose random nb_candidates pictures
        candidates = random.sample(remaining, min(nb_candidates,
                                                  len(remaining)))

        # look for best candidates
        max_score = 0
        best_candidate = None

        for cand in candidates:
            # get score if candidate was to be added at end of slideshow
            score = hp.slide_score(pictures, slideshow + [cand], -2)

            if score >= acceptable_score:
                best_candidate = cand
                break
            elif score == 0:
                tried.add(cand)
                remaining.remove(cand)
            elif score > max_score:
                max_score = score
                best_candidate = cand

        # append best candidate to slideshow, if any, then remove from remaining pictures
        if best_candidate is not None:
            slideshow.append(best_candidate)
            remaining.remove(best_candidate)
            # reinitialize tried pictures
            remaining.extend(tried)
            if len(remaining) % 1000 == 0:
                print(f'Elapsed time: {time.perf_counter() - start} seconds')
                print(f'Remaining: {len(remaining)}')
            tried = set()

    # print results
    print(f'Built slideshow in: {time.perf_counter() - start} seconds')
    print(
        f'Slideshow integrity: {hp.check_slideshow_integrity(pictures, slideshow)}'
    )
    print(f'Slideshow score: {hp.slideshow_score(pictures, slideshow)}')
    print(f'Total runtime: {time.perf_counter() - start} seconds')
    print('Writing slideshow...')
    hp.write_submission(slideshow)


if __name__ == '__main__':
    main()
