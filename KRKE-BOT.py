# Own modules
import KRKE_BOT_Variables as var
import KRKE_BOT_Database as db
import KRKE_BOT_Server as ser
import KRKE_BOT_Rpi as rpi

# Argument converters
import KRKE_BOT_Converters as con

# Imports
import sqlite3
import discord
from discord import Intents
from discord.ext import tasks, commands
import datetime
import time
import typing

# Connect to db
conn = sqlite3.connect('bot-reminder.db')
c = conn.cursor()

# Discord intents. Required!
client = commands.Bot(command_prefix='.', intents=Intents.all())

# REMOVED DEFAULT HELP COMMAND!
client.remove_command('help')


# Create embed with error message.
def error_embed(error, desc, ctx_):
    em = discord.Embed(title=error, description=desc, color=0xff0000)
    em.set_footer(text=ctx_.author.display_name, icon_url=ctx_.author.avatar_url)
    return em


@client.event
async def on_connect():
    print('Connected to discord.')


@client.event
async def on_ready():
    print('Logged in as {0.user}!'.format(client))
    # assign bot avatar and name
    # await client.user.edit(avatar=image)
    await client.user.edit(username=var.BOT_NAME)


@client.command(aliases=['s', 'status'])
async def server(ctx):
    status = ser.server_status(var.SERVICE_URLS)
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
    uptime_msg = '{0.user} has been running for '.format(client)
    em = discord.Embed(description=rpi.bot_uptime(var.START_TIME, uptime_msg), color=0x00ff00)
    em.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    await ctx.send(embed=em)
    await ctx.message.delete()


@client.command(aliases=['r', 'restart'])
async def reboot(ctx):
    reboot_msg = '{0.user} will reboot in '.format(client)
    em = discord.Embed(description=rpi.bot_reboot(var.REBOOT_TIME, reboot_msg), color=0x00ff00)
    em.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    await ctx.send(embed=em)
    await ctx.message.delete()


@client.command(aliases=['ip', 'wanip'])
async def ipaddress(ctx):
    # Check if command is allowed in channel and send response.
    if ctx.channel.name in var.ADMIN_CHANNEL:
        em = discord.Embed(title='WAN IP', description=rpi.rpi_wanip(), color=0x00ff00)
        em.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=em)
    # Command not allowed, send error.
    else:
        em = error_embed('Error', 'Command cannot be used in this channel.', ctx)
        await ctx.send(embed=em)
    # delete command message.
    await ctx.message.delete()


# Remind me function
@client.command(aliases=['rem', 'rme', 'remindme'])
async def remind(ctx, day: con.validate_day, month: con.validate_month, year: con.validate_year, hour: int, minute: int,
                 comment: typing.Optional[str] = 'No comment.'):
    # Check if command is allowed in channel and send response.
    if ctx.channel.name in var.ADMIN_CHANNEL:
        # Create datetime obj out of input arguments.
        date = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute))
        # Database INSERT
        db.insert_entry(conn, c, comment, date, ctx.author.display_name, ctx.channel.id, ctx.author.id,
                        datetime.datetime.now().strftime('%d/%m/%Y %H:%M'))
        # Create embed for response.
        em = discord.Embed(title='Reminder set', description='', color=0x00ff00)
        # em.add_field(name=date.strftime('%d %B %Y %H:%M'), value=comment, inline=False)
        em.add_field(name=date.strftime('%d/%m/%Y %H:%M'), value=comment, inline=False)
        em.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        # send discord message
        await ctx.send(embed=em)
    # Command not allowed in this channel.
    else:
        em = error_embed('Error', 'Command cannot be used in this channel.', ctx)
        await ctx.send(embed=em)
    # delete command message.
    await ctx.message.delete()


# # Remind me function error handling. Custom Error messages for commands, maybe some day...
# @remind.error
# async def remind_error(ctx, error):
#     print(error)
#     em = error_embed('Oops, you fucked something up!', 'Correct way to use function: DD MM YYYY HH MM "COMMENT HERE"', ctx)
#     await ctx.send(embed=em)


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
    role = discord.utils.get(member.guild.roles, name=var.AUTO_ROLE)
    await member.add_roles(role, reason=var.AUTO_ROLE_REASON)
    # Send welcome message in Guest chat.
    # Quick and dirty sleep because msg is sent too fast.
    time.sleep(1.0)
    channel = discord.utils.get(member.guild.channels, name=var.WELCOME_CH)
    await channel.send(var.WELCOME_MSG + member.mention + var.WELCOME_MSG_2)


# Global error message.
@client.event
async def on_command_error(ctx, error):
    em = error_embed('Oops, something went wrong!', str(error), ctx)
    await ctx.send(embed=em)


@client.command()
async def test(ctx):
    print(type(ctx.channel.id))
    channel = client.get_channel(ctx.channel.id)
    await channel.send('Test')
    await ctx.message.delete()


# Check for reminders in database every x seconds.
@tasks.loop(seconds=30.0)
async def check_for_reminders():
    # string to search for entries with todays date.
    # now = YYYY-07-04%
    now = datetime.datetime.now().strftime('%Y-%m-%d') + '%'
    # Get database entries with todays date and alert status 0, save in tuple.
    entries_tuple = db.select_date(c, now, 0)
    # Create list for entries.
    entries = []
    for entry in entries_tuple:
        # Convert tuple to list
        tmp_list = list(entry)
        # Convert date field to datetime object. in format YYYY-MM-DD HH:MM
        tmp_list[2] = datetime.datetime.strptime(tmp_list[2], '%Y-%m-%d %H:%M:%S')
        # Add entry to list.
        entries.append(tmp_list)
    # Loop objects in list.
    for entry in entries:
        # Check if the alert time has passed.
        if entry[2] < datetime.datetime.now():
            # Get channel by channel.id
            channel = client.get_channel(entry[7])
            # Get member by member.id. Need to get server first.
            server = client.get_guild(id=var.SERVER_ID)
            member = server.get_member(entry[8])
            # Create embed for alert.
            em = discord.Embed(title='REMINDER', description=entry[1], color=0x00ff00)
            # Embed footer. member.avatar_url might not work?
            em.set_footer(text='Created: ' + entry[9] + " by " + member.display_name, icon_url=member.avatar_url)
            # Send ping and embed. Users will not get notifications for pings within embeds, hence the normal message.
            await channel.send(member.mention)
            await channel.send(embed=em)
            # Update entrys Alert_Status in DB to mark that its ran.
            db.update_entry(conn, c, entry[0])

# Dont start checking for reminders until bot is ready.
@check_for_reminders.before_loop
async def before_checking_for_reminders():
    await client.wait_until_ready()


check_for_reminders.start()
client.run(var.TOKEN)
conn.close()
