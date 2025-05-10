from cs50 import get_string

def main():

    text = get_string("Text: ")
    length = len(text)

    count_l = count_letters(text, length)
    count_w = count_words(text, length)
    count_s = count_sentences(text, length)

    L = count_l / count_w * 100
    S = count_s / count_w * 100
    index = 0.0588 * L - 0.296 * S - 15.8
    index = round(index)

    if index >= 16:
        print("Grade 16+")
    elif index < 1:
        print("Before Grade 1")
    else:
        print(f"Grade ", index)


def count_letters(text, length):
    count = 0
    for i in range(length):
        if text[i].isalpha():
            count += 1
    return count


def count_words(text, length):
    count = 1
    for i in range(length):
        if text[i] == " ":
            count += 1
    return count


def count_sentences(text,length):
    count = 0
    for i in range(length):
        if text[i] in [".","!","?"]:
            count += 1
    return count

main()
