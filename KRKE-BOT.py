# NOTES FOR USAGE
# FILL IN THE FOLLOWING:
#   - BOT_NAME
#   - TOKEN
#   - REBOOT_TIME (HOUR, MINUTE, SECOND)
#   - teamspeak ...?address=YOUR TEAMSPEAK ADDRESS HERE
#   - bitwarden ...get('yourdomainhere')
#   - ubooquity ...get('yourdomainhere')
#   - plex ...get('yourdomainhere')

import time
import datetime
import discord
from discord.ext import commands
from discord import Intents
import requests

# FILL IN.
BOT_NAME = 'KRKE'
TOKEN = ''
REBOOT_TIME = datetime.time(6, 30, 0)
START_TIME = time.time()
# Role to autoassign.
AUTO_ROLE = 'Guest'
AUTO_ROLE_REASON = 'Autoassign-guest'
# List of Admin channel names
ADMIN_CHANNEL = ['general', 'private', 'bot-testing']
# Welcome message
WELCOME_CH = 'guest'
WELCOME_MSG = 'Welcome to SERVERNAME '
WELCOME_MSG_2 = ". You've been assigned the role 'Guest'."
# List of web service urls
SERVICE_URLS = {
    'ts': 'https://api.cleanvoice.ru/ts3/?address=',
    'nc': 'https://nextcloud',
    'bt': 'https://bitwarden',
    'ub': 'https://books',
    'pl': 'https://plex'
}

# Discord intents. Required.
client = commands.Bot(command_prefix='.', intents=Intents.all())
# Remove default help command. Implement custom later.
client.remove_command('help')


def server_status():
    status = dict()
    # TS
    teamspeak = requests.get(SERVICE_URLS['ts'])
    teamspeak = teamspeak.json()
    teamspeak = teamspeak['can_connect']
    if teamspeak is True:
        status.update({"teamspeak": 'Online'})
    else:
        status.update({'teamspeak': 'F'})
    # NEXTCLOUD
    nextcloud = requests.get(SERVICE_URLS['nc'])
    if nextcloud.status_code == 200:
        status.update({'nextcloud': 'Online'})
    else:
        status.update({'nextcloud': 'F'})
    # BITWARDEN
    bitwarden = requests.get(SERVICE_URLS['bt'])
    if bitwarden.status_code == 200:
        status.update({'bitwarden': 'Online'})
    else:
        status.update({'bitwarden': 'F'})
    # UBOOQUITY
    ubooquity = requests.get(SERVICE_URLS['ub'])
    if ubooquity.status_code == 200:
        status.update({'ubooquity': 'Online'})
    else:
        status.update({'ubooquity': 'F'})
    # PLEX
    plex = requests.get(SERVICE_URLS['pl'])
    if plex.status_code == 200:
        status.update({'plex': 'Online'})
    else:
        status.update({'plex': 'F'})

    # Check statuses to determine color
    if ('F' in status.values()) is True:
        print('F in status')
        status.update({'color': 0xffe700})
    elif ('F' not in status.values()) is False:
        status.update({'color': 0xff0000})
    else:
        status.update({'color': 0x00ff00})
    return status


# get wan ip
def get_wanip():
    ip = requests.get('https://api.ipify.org').text
    # ip = 'WAN IP: {0}'.format(ip)
    return ip


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


# function that returns bot uptime.
def bot_uptime():
    # Calculate time bot has been running.
    time_since_start_seconds = time.time() - START_TIME
    # Convert seconds to readable format.
    uptime = complile_string(split_seconds(time_since_start_seconds), '{0.user} has been running for '.format(client), '.')
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
        reboot_date = nextday_date.replace(hour=REBOOT_TIME.hour, minute=REBOOT_TIME.minute, second=0, microsecond=0)
    # get seconds until reboot.
    until_reboot = reboot_date - current_date
    # Return time until reboot in seconds
    return until_reboot.seconds


# Check how long it is until the next reboot (6:30)
def bot_reboot():
    # Get seconds until reboot, convert into more readable format (string)
    reboot_time = complile_string(split_seconds(next_reboot_date()), '{0.user} will reboot in '.format(client), '.')
    # Return string.
    return reboot_time


# Create embed with error message.
def error_embed(error, desc, ctx_):
    em = discord.Embed(title=error, description=desc, color=0xff0000)
    em.set_footer(text=ctx_.author.display_name, icon_url=ctx_.author.avatar_url)
    return em


# Get bot avatar.
# with open('bot_avatar.jpg', 'rb') as f:
# image = f.read()


@client.event
async def on_connect():
    print('Connected to discord.')


@client.event
async def on_ready():
    print('Logged in as {0.user}!'.format(client))
    # assign bot avatar and name
    # await client.user.edit(avatar=image)
    await client.user.edit(username=BOT_NAME)


@client.command(aliases=['s', 'status'])
async def server(ctx):
    status = server_status()
    em = discord.Embed(title='AntNAS Status', description='¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯', color=status['color'])
    em.add_field(name='Nextcloud', value=status['nextcloud'], inline=False)
    em.add_field(name='Bitwarden', value=status['bitwarden'], inline=False)
    em.add_field(name='Ubooquity', value=status['ubooquity'], inline=False)
    em.add_field(name='Teamspeak3', value=status['teamspeak'], inline=False)
    em.add_field(name='Plex', value=status['plex'], inline=False)
    em.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)

    await ctx.send(embed=em)
    await ctx.message.delete()


@client.command(aliases=['upt'])
async def uptime(ctx):
    em = discord.Embed(description=bot_uptime(), color=0x00ff00)
    em.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    await ctx.send(embed=em)
    await ctx.message.delete()


@client.command(aliases=['r', 'restart'])
async def reboot(ctx):
    em = discord.Embed(description=bot_reboot(), color=0x00ff00)
    em.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    await ctx.send(embed=em)
    await ctx.message.delete()


@client.command(aliases=['ip', 'wanip'])
async def ipaddress(ctx):
    # Check if command is allowed in channel and send response.
    if ctx.channel.name in ADMIN_CHANNEL:
        em = discord.Embed(title='WAN IP', description=get_wanip(), color=0x00ff00)
        em.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=em)
    # Command not allowed, send error.
    else:
        em = error_embed('Error', 'Command cannot be used in this channel.', ctx)
        await ctx.send(embed=em)
    # delete command message.
    await ctx.message.delete()

# Temporary help command. Redo in future.
@client.command(aliases=['c', 'h', 'help', 'command'])
async def commands(ctx):
    em = error_embed('Error', 'This function is under construction, will be added soon.', ctx)
    await ctx.send(embed=em)
    await ctx.message.delete()


@client.event
async def on_member_join(member):
    print(member.display_name + ' joined the server.')
    # Auto assign Guest role to new members.
    role = discord.utils.get(member.guild.roles, name=AUTO_ROLE)
    await member.add_roles(role, reason=AUTO_ROLE_REASON)
    # Send welcome message in Guest chat.
    # Quick and dirty sleep because msg is sent too fast.
    time.sleep(1.0)
    channel = discord.utils.get(member.guild.channels, name=WELCOME_CH)
    await channel.send(WELCOME_MSG + member.mention + WELCOME_MSG_2)

client.run(TOKEN)
