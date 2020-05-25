from helpers import helpers as hp
import random
from random import randrange
import time
import os

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
PICTURES_FILE = os.path.join(THIS_DIR, 'd_pet_pictures.txt')
SUBMISSION_FILE = 'submission.txt'


def main():
    # define our parameters
    first_picture_nb_tags = 20
    pairing_params = {'min_tags': 18, 'max_tags': 30, 'nb_candidates': 100}
    nb_candidates = 3500
    nb_lignes = -1  # for when testing on subset of pictures
    acceptable_score = 20
    interval_search = 1000

    # start timing
    start = time.perf_counter()

    # Read our input
    pictures = hp.load_pictures_from_file(filename=PICTURES_FILE, nb_lines=nb_lignes)

    print(f'{len(pictures)} pictures loaded')

    # separate H and V pictures
    horizontals = [i for i, pic in enumerate(pictures) if pic[0] == 'H']
    verticals = [i for i, pic in enumerate(pictures) if pic[0] == 'V']

    print('H/V splitted')

    # pair vertical pictures
    verticals = hp.pair_verticals(pictures, verticals, pairing_params)

    # assemble H and V pictures
    remaining = set(horizontals + verticals)
    print('Picture set built')

    # delete horizontals & verticals
    del horizontals, verticals

    # intialize slideshow
    slideshow = []
    last_tags = set()

    # look for our first picture with min first_picture_nb_tags tags
    for pic in remaining:
        # get tags (use get_slide_tags with "fake" slideshow of 1 picture)
        tags = hp.get_slide_tags(pictures, [pic], 0)

        if len(tags) <= first_picture_nb_tags:
            slideshow.append(pic)
            last_tags = tags
            remaining.remove(pic)
            break

    # intialize a "tried" set
    tried = set()

    # try to assign all pictures / tuple of pictures
    while len(remaining) > 0 and tried != remaining:
        # store tags of slideshow's last slide
        treshold_score = min(acceptable_score, (len(last_tags) // 2) + 1)

        # choose random nb_candidates pictures
        candidates = random.sample(remaining, min(nb_candidates, len(remaining)))

        # look for best candidates
        max_score = 0
        best_candidate = None
        best_cand_tags = set()
        best_cand_tag_len = 9999

        for cand in candidates:
            # get candidate tags
            cand_tags = hp.get_slide_tags(pictures, [cand], 0)
            # calc score with slideshow's last slide
            score = hp.tag_sets_score(last_tags, cand_tags)

            if score >= treshold_score:
                best_candidate = cand
                best_cand_tags = cand_tags
                break
            elif score == 0:
                tried.add(cand)
                remaining.remove(cand)
            elif score > max_score or (score > 0 and score == max_score and len(cand_tags) < best_cand_tag_len):
                max_score = score
                best_candidate = cand
                best_cand_tags = cand_tags
                best_cand_tag_len = len(cand_tags)

        # append best candidate to slideshow, if any, then remove from remaining pictures
        if best_candidate is not None:
            slideshow.append(best_candidate)
            last_tags = best_cand_tags
            remaining.remove(best_candidate)
            # reinitialize tried pictures
            remaining.update(tried)
            tried = set()
            # display progress
            if len(remaining) % 1000 == 0:
                print(f'Elapsed time: {time.perf_counter() - start} seconds')
                print(f'Remaining: {len(remaining)}')

    print('-' * 40)
    print(f'Slideshow score: {hp.slideshow_score(pictures, slideshow)}')
    print('Save slideshow in case fails later')
    hp.write_submission(slideshow)

    # try to insert remaining pictures in slideshow
    slideshow_len = len(slideshow)

    for pic in tried:
        # pick a random index in slideshow
        rdm_i = randrange(0, max(0, slideshow_len - interval_search))

        # look for best place to insert in range rdm_i + interval_search
        best_i = None
        best_score = 0

        for i in range(rdm_i, max(rdm_i + interval_search, slideshow_len)):
            # check score of index slide, index slide after insert, inserted slide score
            s_before = hp.slide_score(pictures, slideshow, i)
            s_after = hp.slide_score(pictures, slideshow[:i + 1] + [pic], -2)
            s_new = hp.slide_score(pictures, [pic] + slideshow[i + 1:], 0)
            score_increase = s_new + s_after - s_before

            if score_increase > best_score:
                best_i = i
                best_score = score_increase

        # insert at best index (maximum score gain)
        if best_score > 0:
            slideshow = slideshow[:best_i + 1] + [pic] + slideshow[best_i + 1:]
            slideshow_len += 1

    print(f'Built slideshow in: {time.perf_counter() - start} seconds')
    print(f'Slideshow score: {hp.slideshow_score(pictures, slideshow)}')
    print('-' * 40)
    # print results
    print(f'Integrity: {hp.check_slideshow_integrity(pictures, slideshow)}')
    print(f'Total runtime: {time.perf_counter() - start} seconds')
    print('Writing slideshow...')
    hp.write_submission(slideshow)


if __name__ == '__main__':
    main()
