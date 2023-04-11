import re


def split_line(line):
    return re.findall('[A-Za-z]+(?:\'[A-Za-z]+)?', line)


def linear_search(aiw, dictionary_word_list):
    line_num = 0
    for line in aiw:
        line = line.strip()
        line_num += 1

        for word in split_line(line):
            if word.upper() not in dictionary_word_list:
                print("Line:", line_num, "Possible misspelled word:", word)


def binary_search(aiw_line_list, dictionary_word_list):
    line_num = 0
    for line in aiw_line_list:
        line_num += 1
        for word in split_line(line):
            lower_bound = 0
            upper_bound = len(dictionary_word_list) - 1  # 47,162 words in the dictionary list. 2,173 words in Aiw
            found = False
            while lower_bound <= upper_bound and not found:
                middle_pos = (lower_bound + upper_bound) // 2
                if dictionary_word_list[middle_pos] < word.upper():
                    lower_bound = middle_pos + 1
                elif dictionary_word_list[middle_pos] > word.upper():
                    upper_bound = middle_pos - 1
                else:
                    found = True
            if not found:
                print("Line:", line_num, "Possible misspelled word:", word)


def main():
   
    # read chapter into a list of lines
    dictionary_words = open("dictionary.txt")
    dictionary_word_list = []
    for line in dictionary_words:
        line = line.strip()
        dictionary_word_list.append(line)
    dictionary_words.close()

    aiw = open("AliceInWonderLand200.txt")
    aiw_line_list = []
    for line in aiw:
        line = line.strip()
        aiw_line_list.append(line)
    aiw.close()

    print("--- Linear Search---")
    linear_search(aiw_line_list, dictionary_word_list)

    print('--- Binary Search ---')
    binary_search(aiw_line_list, dictionary_word_list)


main()
