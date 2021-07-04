import datetime

skips = ['/', 'skip', 's', 'none']


def validate_day(argument):
    # if arugment given is /, skip and make it todays date.
    if argument.lower() in skips:
        return datetime.datetime.now().day
    # if argument is not /, convert it to Int and check if its a valid number of day.
    else:
        argument = int(argument)
        # Check if its a valid day of month, Yes...all months dont have 31 days, i know.
        if argument <= 31 and argument >= 1:
            return argument
        # if its not valid, return today day.
        else:
            return datetime.datetime.now().day


def validate_month(argument):
    # if arugment given is /, skip and make it todays date.
    if argument.lower() in skips:
        return datetime.datetime.now().month
    # if argument is not /, convert it to Int and check if its a valid number of day.
    else:
        argument = int(argument)
        # Check if its a valid month.
        if argument <= 12 and argument >= 1:
            return argument
        # if its not valid, return todays month.
        else:
            return datetime.datetime.now().month


def validate_year(argument):
    # if arugment given is /, skip and make it todays year.
    if argument.lower() in skips:
        return datetime.datetime.now().year
    # if argument is not /, convert it to Int and check if its a valid year.
    else:
        argument = int(argument)
        # Check if its a valid month.
        if datetime.datetime.now().year <= argument:
            return argument
        # if its not valid, return todays month.
        else:
            return datetime.datetime.now().year
