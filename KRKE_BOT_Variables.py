import datetime
import time

# FILL IN.
BOT_NAME = 'KRKE'
SERVER_ID = 0
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
