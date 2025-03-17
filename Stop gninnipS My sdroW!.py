'''
Write a function that takes in a string of one or more words, and returns the same string, but with all words that have five or more letters reversed (Just like the name of this Kata). Strings passed in will consist of only letters and spaces. Spaces will be included only when more than one word is present.

Examples:

"Hey fellow warriors"  --> "Hey wollef sroirraw" 
"This is a test        --> "This is a test" 
"This is another test" --> "This is rehtona test"

'''


def spin_words(sentence):
    words = sentence.split()
    reverse_words = []
    for i in words:
        if len(i) >= 5:
            reverse_words.append(i[::-1])
        else:
            reverse_words.append(i)
    sentence = " ".join(reverse_words)
    return sentence