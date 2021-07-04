import requests
import time
import datetime


# seconds split into days, hours, minutes and seconds.
def split_seconds(seconds):
    # Dict for storing days, hours, minutes and seconds.
    split_time = {
        'days': 0,
        'hours': 0,
        'minutes': 0,
        'seconds': 0
    }

    # Convert seconds to days, hours, minutes and seconds.
    days = seconds // (24 * 3600)
    split_time.update({'days': int(days)})
    seconds = seconds % (24 * 3600)
    hours = seconds // 3600
    split_time.update({'hours': int(hours)})
    seconds %= 3600
    minutes = seconds // 60
    split_time.update({'minutes': int(minutes)})
    seconds %= 60
    seconds = seconds
    split_time.update({'seconds': int(seconds)})
    # Return dict with values.
    return split_time


# Convert split_time dict to string (String xD xH xM xS)
def complile_string(time_dict, start_string, end_with):
    if time_dict['days'] != 0:
        start_string += str(time_dict['days']) + 'd '
    if time_dict['hours'] != 0:
        start_string += str(time_dict['hours']) + 'h '
    if time_dict['minutes'] != 0:
        start_string += str(time_dict['minutes']) + 'm '
    if time_dict['seconds'] != 0:
        start_string += str(time_dict['seconds']) + 's'
    # Add to end of string.
    start_string += end_with
    # Return compiled string.
    return start_string


# Get rpi wan ip
def rpi_wanip():
    ip = requests.get('https://api.ipify.org').text
    return ip


# start_string = '{0.user} has been running for '.format(client)
# function that returns bot uptime.
def bot_uptime(start_time, start_string):
    # Calculate time bot has been running.
    time_since_start_seconds = time.time() - start_time
    # Convert seconds to readable format.
    uptime = complile_string(split_seconds(time_since_start_seconds), start_string, '.')
    # Return string.
    return uptime


# Check if time is between specified times.
def next_reboot_date(reboot_time):
    # get current date.
    current_date = datetime.datetime.now()
    # next days date.
    nextday_date = current_date + datetime.timedelta(days=1)
    # Save hour and minute in integer variables for easier use.
    # Hour
    hour = int(time.strftime('%H', current_date.timetuple()))
    # Minute
    minute = int(time.strftime('%M', current_date.timetuple()))
    # Check if current time is between 00:00 and 6:30.
    if datetime.time(0, 0, 0) < datetime.time(hour, minute, 0) < reboot_time:
        # Save reboot date in var.
        reboot_date = current_date.replace(hour=reboot_time.hour, minute=reboot_time.minute, second=0, microsecond=0)
    # Check if current time is between 6:30 and 23:59:59.
    if reboot_time < datetime.time(hour, minute, 0) < datetime.time(23, 59, 59):
        # Save reboot date in var.
        reboot_date = nextday_date.replace(hour=reboot_time.hour, minute=reboot_time.minute, second=0, microsecond=0)
    # get seconds until reboot.
    until_reboot = reboot_date - current_date
    # Return time until reboot in seconds
    return until_reboot.seconds


# start_string = '{0.user} has been running for '.format(client)
# Check how long it is until the next reboot (6:30)
def bot_reboot(reboot_time, start_string):
    # Get seconds until reboot, convert into more readable format (string)
    reboot_time = complile_string(split_seconds(next_reboot_date(reboot_time)), start_string, '.')
    # Return string.
    return reboot_time
