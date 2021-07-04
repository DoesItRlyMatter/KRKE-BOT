import requests


# Checks status of services on unraid server.
def server_status(URLS):
    status = dict()
    # TS
    teamspeak = requests.get(URLS['ts'])
    teamspeak = teamspeak.json()
    teamspeak = teamspeak['can_connect']
    if teamspeak is True:
        status.update({'teamspeak': 'Online'})
    else:
        status.update({'teamspeak': 'F'})
    # NEXTCLOUD
    nextcloud = requests.get(URLS['nc'])
    if nextcloud.status_code == 200:
        status.update({'nextcloud': 'Online'})
    else:
        status.update({'nextcloud': 'F'})
    # BITWARDEN
    bitwarden = requests.get(URLS['bt'])
    if bitwarden.status_code == 200:
        status.update({'bitwarden': 'Online'})
    else:
        status.update({'bitwarden': 'F'})
    # UBOOQUITY
    ubooquity = requests.get(URLS['ub'])
    if ubooquity.status_code == 200:
        status.update({'ubooquity': 'Online'})
    else:
        status.update({'ubooquity': 'F'})
    # PLEX
    plex = requests.get(URLS['pl'])
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
