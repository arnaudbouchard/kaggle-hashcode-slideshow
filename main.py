from helpers import helpers as hp
import time
import os

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
PICTURES_FILE = os.path.join(THIS_DIR, 'd_pet_pictures.txt')
SUBMISSION_FILE = 'submission.txt'


def main():
    # Read our input
    pictures = hp.load_pictures_from_file(filename=PICTURES_FILE, nb_lines=100)

    min_score = 1
    slideshow = []
    reserve = []

    for i in range(len(pictures)):
        # for first image
        if len(slideshow) == 0:
            slideshow.append(i)
            continue

        # if by appending to slideshow the score of this slide is at min min_score
        if hp.slide_score(pictures, slideshow[-1], i) >= min_score:
            slideshow.append(i)
        else:
            reserve.append(i)

    hp.write_submission(slideshow)
    start = time.perf_counter()
    slides, score = hp.submission_score('submission.txt')
    print(
        f'Score of {score} for {slides} slides, calculated in {time.perf_counter() - start}'
    )
    print('-' * 40)

    # insert reserve images
    res_i = 0

    while res_i < len(reserve):
        i = 0

        while i + 1 < len(slideshow):
            before_score = hp.slide_score(pictures, slideshow[i],
                                          slideshow[i + 1])
            after_score = hp.slide_score(pictures, reserve[res_i],
                                         slideshow[i + 1])

            if after_score >= before_score:
                slideshow.insert(i + 1, reserve[res_i])
                del reserve[res_i]
                res_i = 0
                break

            i += 1
        res_i += 1

    # write submission, calc score
    print(
        f'Slideshow is valid: {hp.check_slideshow_integrity(pictures, slideshow)}'
    )
    hp.write_submission(slideshow)
    start = time.perf_counter()
    slides, score = hp.submission_score('submission.txt')
    print(
        f'Score of {score} for {slides} slides, calculated in {time.perf_counter() - start}'
    )


if __name__ == '__main__':
    main()
