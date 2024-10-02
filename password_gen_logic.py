from wonderwords import RandomWord
import secrets as scr
import string as str
def generate_password():
    
    
    w = RandomWord()

    first_word = w.word(
        word_min_length= 6,
        word_max_length= 9,
        include_categories=['adjective']
    )
    first_word = first_word[0].upper() + first_word[1:]

    second_word = w.word(
        word_min_length= 4,
        word_max_length= 7,
        include_categories=['noun']
    )
    second_word = second_word[0].upper() + second_word[1:]

    number = scr.choice(str.digits) + scr.choice(str.digits) + scr.choice(str.digits)

    symbol = scr.choice(str.punctuation)
    
    return first_word + second_word + number + symbol

