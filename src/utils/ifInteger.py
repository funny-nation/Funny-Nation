def if_integer(string):
    if string[0] == '-' or string[0] == '+':
        return string[1:].isdigit()

    else:
        return string.isdigit()
