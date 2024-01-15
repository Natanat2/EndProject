from django import template
import string

register = template.Library()

@register.filter(name='censor')
def censor(value):
    bad_words = ['сука', 'дура', 'блять']
    words = value.split()
    censored_words = []

    for word in words:
        punctuation = ''
        current_word = word

        if word[-1] in string.punctuation:
            punctuation = word[-1]
            current_word = word[:-1]

        for bad_word in bad_words:
            if bad_word == current_word.lower():
                censored_word = current_word[0] + '*' * (len(current_word) - 1) + punctuation
                censored_words.append(censored_word)
                break
        else:
            censored_words.append(word)

    return ' '.join(censored_words)
