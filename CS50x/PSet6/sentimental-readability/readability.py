from cs50 import get_string


text = get_string("Text: ")


def main(text):
    # call letters, words and sentences functions
    letters = numLetters(text)
    words = numWords(text)
    sentences = numSentences(text)

    # calculate index
    L = (letters / words * 100)
    S = (sentences / words * 100)
    index = round(0.0588 * L - 0.296 * S - 15.8)

    # print grade
    if index >= 16:
        print("Grade 16+")
    elif index <= 0:
        print("Before Grade 1")
    else:
        print(f"Grade {index}")


# letter function
def numLetters(text):
    letters = 0
    for e in text:
        if e.isalpha() == True:
            letters += 1
    return letters


# words function
def numWords(text):
    listWords = text.split(' ')
    words = len(listWords)
    return words


# sentences function
def numSentences(text):
    sentences = 0
    for e in text:
        if e == "." or e == "?" or e == "!":
            sentences += 1
    return sentences


main(text)

