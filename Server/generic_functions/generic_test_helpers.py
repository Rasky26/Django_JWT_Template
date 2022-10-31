import string
import random


def random_string(length=16, text=string.ascii_letters + string.digits):
    """
    Lazy way to create random information, such as usernames and emails.
    """
    # Removes leading and trailing spaces
    return "".join(random.choice(text) for _ in range(length)).strip()


def random_bell_curve_int(low=1, high=12):
    """
    Random number generator. Numbers are skewed along a bell curve.
    """
    return int(round(random.triangular(low, high), 0))


def random_length_string(low=1, high=12, allow_digits=True):
    """
    Generates a string of random length
    """
    text = string.ascii_letters
    if allow_digits:
        text += string.digits
    return random_string(length=random_bell_curve_int(low=low, high=high), text=text)


def random_sentence(total_len=128, allow_digits=True):
    """
    Creates sentences consisting of random letters and numbers. Purely used for quick filler.
    """
    count, words_to_punctuation = 0, random.randint(5, 16)
    punctuation = [".", "?", "!", ","]
    text_choices = string.ascii_letters
    if allow_digits:
        text_choices += string.digits

    sentence = random_length_string(allow_digits=allow_digits).strip()
    while len(sentence) < total_len:
        count += 1
        if count >= words_to_punctuation:
            sentence += random.choice(punctuation)
            count, words_to_punctuation = 0, random.randint(5, 16)
        else:
            sentence += (
                " " + f"{random_length_string(allow_digits=allow_digits)}".strip()
            )

    # Removes leading and trailing spaces
    return sentence[:total_len]
