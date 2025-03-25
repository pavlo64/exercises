"""
A palindrome is a word, phrase, number, or other sequence of characters which reads the same backward as forward. Examples of numerical palindromes are:

2332
110011
54322345

For a given number num, write a function to test if it's a numerical palindrome or not and return a boolean (true if it is and false if not).

Return "Not valid" if the input is not an integer or less than 0.

"""

def palindrome(num):
    if type(num)!= int or num<0:
        return 'Not valid'
    num_list = list(str(num))
    k =-1
    for i in range(len(num_list)//2):
        if num_list[i]!=num_list[k]:
            return False
        k-=1
    return True