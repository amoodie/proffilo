


def format_number(number):
    integer = int(round(number, -1))
    string = "{:,}".format(integer)
    return(string)


def format_table(number):
    integer = (round(number, 1))
    string = str(integer)
    return(string)
