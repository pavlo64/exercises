def solution(s):
    new_phrase = ''
    for char in s:
        if char.isupper():
            new_phrase += ' ' + char
        else:
            new_phrase += char
    return new_phrase
    
if __name__ == '__main__':
    s = "camelCasing"
    print (solution(s))