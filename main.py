import sys
import spotipy
import spotipy.util as util
import os
import json

keys = json.load(open('./credentials.json'))

os.environ['SPOTIPY_CLIENT_ID'] = keys['SPOTIPY_CLIENT_ID']
os.environ['SPOTIPY_CLIENT_SECRET'] = keys['SPOTIPY_CLIENT_SECRET']
os.environ['SPOTIPY_REDIRECT_URI'] = 'https://example.com/callback/'

errorlog = open('errorlog.txt', 'w')
lineupfile = open('lineup.txt', 'r')
lineup = [x.strip('\n') for x in lineupfile.readlines()]

numberofbands = len(lineup)
tracks = []

if len(sys.argv) > 2:
    username = sys.argv[1]
    playlist_id = sys.argv[2]
else:
    print('Usage: %s username playlist_id ...' % (sys.argv[0]))
    sys.exit()

index = 0
scope = 'playlist-modify-public'
token = util.prompt_for_user_token(username, scope, redirect_uri='https://example.com/callback/')

if token:
    sp = spotipy.Spotify(auth=token)
    sp.trace = False

    for x in range(0, len(lineup)):
        results = sp.search(q=str(lineup[x]), limit=5)
        for i, t in enumerate(results['tracks']['items']):
            tracks.append(str(t['id'].strip('u')))
            print('adding ', t['id'], t['name'])
    while tracks:
        print('adding song ', index)
        index = index + 1
        try:
            results = sp.user_playlist_add_tracks(username, playlist_id, tracks[:1], position=None)
        except Exception as e:
            print('Adding song failed: ')
            print(e)
        tracks = tracks[1:]
else:
    print('Cannnot get token for ', username)

print('Playlist Complete!')
