import os
from datetime import datetime, timedelta

def get_file_size(filepath):
    """Returns the size of a file in kilobytes"""
    size_in_bytes = os.path.getsize(filepath)
    size_in_kb = size_in_bytes / 1024
    return int(size_in_kb)


def get_next_month_date():

    today = datetime.now()
    year = today.year
    month = today.month
    day = today.day

    if month == 12:
        # If current month is December, set the month to January and increment the year
        year += 1
        month = 1
    else:
        month += 1

    # Get the number of days in the next month
    if month == 2:
        # February
        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
            days_in_month = 29
        else:
            days_in_month = 28
    elif month in [4, 6, 9, 11]:
        # April, June, September, November
        days_in_month = 30
    else:
        # January, March, May, July, August, October, December
        days_in_month = 31

    if day > days_in_month:
        # If the current day is greater than the number of days in the next month,
        # set the day to the last day of the next month
        day = days_in_month

    next_month = datetime(year, month, day, today.hour, today.minute, today.second)
    return next_month