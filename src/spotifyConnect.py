import dotenv
import os
import time
import spotipy
import webbrowser
import main


class SpotifyConnect():

    def __init__(self, arduinoController, credsFileName):
        self.credsFileName = credsFileName
        self.arduinoController = arduinoController
        self.tokenData = None
        self.currentAlbum = None
        self.changeLights()
        return

    def changeLights(self):
        main.updateLights([255,0,0], self.arduinoController)
        time.sleep(0.5)
        main.updateLights([0,255,0], self.arduinoController)
        time.sleep(0.5)
        main.updateLights([0,0,255], self.arduinoController)
        time.sleep(0.5)
        return

    def connect(self):
        spotifyOauth = self.createSpotifyOauth(self.credsFileName)
        authUrl = spotifyOauth.get_authorize_url()
        webbrowser.open_new_tab(authUrl)
        self.tokenData = spotifyOauth.get_access_token()
        self.getSongs()
        return

    def getSongs(self):
        while True:
            tokenData = self.getToken()
            tokenExpiresAt = tokenData['expires_at']
            timeNow = int(time.time())
            spotify = spotipy.Spotify(auth=tokenData['access_token'])
            currentSong = spotify.currently_playing()
            #print(json.dumps(currentSong, sort_keys=False, indent=5))
            while tokenExpiresAt - timeNow > 60:
                currentSong = spotify.currently_playing()
                print(currentSong)
                if currentSong is not None:
                    type = currentSong['currently_playing_type']
                    if type == 'track':
                        playingAlbum = self.getAlbumName(currentSong)
                        if self.currentAlbum != playingAlbum:
                            self.currentAlbum = playingAlbum
                            # Update Lights
                            main.songUpdated(currentSong, self.arduinoController)
                            print("ALBUM CHANGED:", self.currentAlbum, "----------Token Expiring in:", tokenExpiresAt - timeNow)
                        else:
                            print("ALBUM NOT CHANGED:", self.currentAlbum, "----------Token Expiring in:", tokenExpiresAt - timeNow)
                        time.sleep(1.0)
                    elif type == 'ad':
                        time.sleep(30.0)
                    timeNow = int(time.time())
                else:
                    main.idleLights(self.arduinoController)
                    print("NO SONG PLAYING")
                time.sleep(1.0)
        return

    def getToken(self):
        token = self.tokenData
        if token is None:
            raise "Exception: Cannot get a token"
        timeNow = int(time.time())
        if token['expires_at'] - timeNow < 60:
            spotifyOauth = self.createSpotifyOauth(self.credsFileName)
            self.tokenData = spotifyOauth.refresh_access_token(token['refresh_token'])
        return self.tokenData

    def createSpotifyOauth(self, credsFile):
        dotenv.load_dotenv(credsFile)
        SPOTIPY_CLIENT_ID = os.environ['SPOTIPY_CLIENT_ID']
        SPOTIPY_CLIENT_SECRET = os.environ['SPOTIPY_CLIENT_SECRET']
        #SPOTIPY_REDIRECT_URI = os.environ['SPOTIPY_REDIRECT_URI']
        SPOTIPY_REDIRECT_URI = 'https://www.google.com'
        SCOPE = "user-read-playback-state user-read-currently-playing user-read-recently-played"
        return spotipy.SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET,
                            redirect_uri=SPOTIPY_REDIRECT_URI, scope=SCOPE)

    def getAlbumName(self, currentSong):
        return currentSong['item']['album']['name']