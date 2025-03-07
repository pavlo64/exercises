def is_valid(isbn):
    isbn = isbn.replace("-","")
    if len(isbn) == 10:
        #isbn = isbn.upper().replace('X','10')
        if isbn[-1].upper() == 'X':
            isbn = isbn[:-1] + '10'
        if (isbn).isdigit():
            k = 10
            sum = 0
            if isbn[-2:] == '10':
                for i in range(9):
                    sum += int(isbn[i]) * k
                    k -=1
                sum += 10
            else:
                for i in range(10):
                    sum += int(isbn[i]) * k
                    k -=1
            print(sum % 11)
            return sum % 11 == 0

    
    return False