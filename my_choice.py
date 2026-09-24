"""
Your choice rule, for Part 3.

You design the rule. Claude asks you questions about it, writes it here from your answers, and
shows you the code. Then `uv run python hand_check.py` shows each step of your rule on a
two-artist case, so you can say whether each step does what you meant.
"""

from artists import TRUE_POPULARITY
from choose import normalize, step


def my_choice(shown, counts, social_influence):
    """Return the chance that a user picks each shown artist: a list of numbers, one per artist
    in `shown` and in the same order, summing to 1.

    shown              the artists on the list, top first (positions 0, 1, 2, ...)
    counts             the download counts shown with the artists, artist -> number; an artist
                       shown without a count is missing, so read it as counts.get(artist, 0)
    social_influence   from 0 (users ignore the counts) to 1 (users go by the counts alone)

    The rule may use `normalize`, which scales a list of weights so they sum to 1, and
    TRUE_POPULARITY, which gives each artist its hidden true popularity. `step` labels each
    stage of the rule, so that hand_check.py can show it.
    """
    taste = step("taste: hidden true popularity", [TRUE_POPULARITY[artist] for artist in shown])
    visible_counts = step(
        "downloads: the counts shown to the user, with a tiny floor for zero-download artists",
        [max(counts.get(artist, 0), 0.01) for artist in shown],
    )
    social_mix = step(
        "social mix: a coin toss at 0.5, but popularity dominates otherwise",
        [
            ((1 - social_influence) * taste_i) + (social_influence * count_i)
            for taste_i, count_i in zip(taste, visible_counts)
        ],
    )
    position = step(
        "position: a small boost for artists nearer the top of the list",
        [1.2 - (0.1 * i) for i in range(len(shown))],
    )
    weighted = step(
        "final weights: social mix times position",
        [social_i * position_i for social_i, position_i in zip(social_mix, position)],
    )
    return step("choice chances: normalize the final weights", normalize(weighted))
