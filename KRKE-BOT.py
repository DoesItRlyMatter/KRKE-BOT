# NOTES FOR USAGE
# FILL IN THE FOLLOWING:
#   - BOT_NAME
#   - TOKEN
#   - REBOOT_TIME (HOUR, MINUTE, SECOND)
#   - teamspeak ...?address=YOUR TEAMSPEAK ADDRESS HERE
#   - bitwarden ...get('yourdomainhere')
#   - ubooquity ...get('yourdomainhere')
#   - plex ...get('yourdomainhere')

import discord
from discord.ext import commands
from discord import Intents
import requests
import time
from datetime import datetime
import datetime

# FILL IN.
BOT_NAME = 'KRKE'
TOKEN = ''
REBOOT_TIME = datetime.time(6, 30, 0)
START_TIME = time.time()

client = commands.Bot(command_prefix='.', intents=Intents.all())

# call ts api, return true/false.


def server_status():
    status = dict()
    # TS
    teamspeak = requests.get('https://api.cleanvoice.ru/ts3/?address=')
    teamspeak = teamspeak.json()
    teamspeak = teamspeak['can_connect']
    if teamspeak is True:
        status.update({"ts": "+ Teamspeak3  - OK!"})
    else:
        status.update({"ts": "- Teamspeak3  - F"})
    # NEXTCLOUD
    nextcloud = requests.get('https://nextcloud')
    if nextcloud.status_code == 200:
        status.update({"nextcloud": "+ Nextcloud   - OK!"})
    else:
        status.update({"nextcloud": "- NextCloud   - F"})
    # BITWARDEN
    bitwarden = requests.get('https://bitwarden')
    if bitwarden.status_code == 200:
        status.update({"bitwarden": "+ Bitwarden   - OK!"})
    else:
        status.update({"bitwarden": "+ Bitwarden   - F"})
    # UBOOQUITY
    ubooquity = requests.get('https://books')
    if ubooquity.status_code == 200:
        status.update({"books": "+ Ubooquity   - OK!"})
    else:
        status.update({"books": "- Ubooquity   - F"})
    # PLEX
    plex = requests.get('https://plex')
    if plex.status_code == 200:
        status.update({"plex": "+ Plex        - OK!"})
    else:
        status.update({"plex": "- Plex        - F"})
    return status


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
        start_string += str(time_dict['seconds']) + 's '
    # Add to end of string.
    start_string += end_with
    # Return compiled string.
    return start_string


# function that returns bot uptime.
def bot_uptime():
    # Calculate time bot has been running.
    time_since_start_seconds = time.time() - START_TIME
    # Convert seconds to readable format.
    uptime = complile_string(split_seconds(time_since_start_seconds), BOT_NAME + ' has been running for ', '.')
    # Return string.
    return uptime


# Check if time is between specified times.
def next_reboot_date():
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
    if datetime.time(0, 0, 0) < datetime.time(hour, minute, 0) < REBOOT_TIME:
        # Save reboot date in var.
        reboot_date = current_date.replace(hour=REBOOT_TIME.hour, minute=REBOOT_TIME.minute, second=0, microsecond=0)
    # Check if current time is between 6:30 and 23:59:59.
    if REBOOT_TIME < datetime.time(hour, minute, 0) < datetime.time(23, 59, 59):
        # Save reboot date in var.
        reboot_date = nextday_date.replace(hour=6, minute=30, second=0, microsecond=0)
    # get seconds until reboot.
    until_reboot = reboot_date - current_date
    # Return time until reboot in seconds
    return until_reboot.seconds


# Check how long it is until the next reboot (6:30)
def bot_reboot():
    # Get seconds until reboot, convert into more readable format (string)
    reboot_time = complile_string(split_seconds(next_reboot_date()), BOT_NAME + ' will reboot in ', '.')
    # Return string.
    return reboot_time


# Get bot avatar.
# with open('bot_avatar.jpg', 'rb') as f:
    # image = f.read()


@client.event
async def on_connect():
    print('Bot connected to discord.')


@client.event
async def on_ready():
    print('Bot ready!')
    # assign bot avatar and name
    # await client.user.edit(avatar=image)
    await client.user.edit(username=BOT_NAME)


@client.command(aliases=['s', 'status'])
async def server(ctx):
    status = server_status()
    await ctx.send('```diff\n' + status["nextcloud"] + '\n' + status["bitwarden"] + '\n' + status["books"] + '\n' + status["ts"] + '\n' +
                   status["plex"] + '```')


@client.command(aliases=['upt'])
async def uptime(ctx):
    await ctx.send('```diff\n' + bot_uptime() + '```')


@client.command(aliases=['r', 'restart'])
async def reboot(ctx):
    await ctx.send('```diff\n' + bot_reboot() + '```')


@client.event
async def on_member_join(member):
    print('Someone joined the server.')
    role = discord.utils.get(member.guild.roles, name='Guest')
    await member.add_roles(role, reason='Autoassign-guest')


client.run(TOKEN)
