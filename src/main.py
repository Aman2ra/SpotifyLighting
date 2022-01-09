import spotifyConnect
import arduinoController
import requests
from PIL import Image

def songUpdated(playingSong, arduinoCtr):
    albumUrl = getAlbumUrl(playingSong)
    albumImg = getImage(albumUrl)
    domColor = getDomColor(albumImg)
    print(domColor)
    color = suppressNonDom(domColor)
    print(color)
    updateLights(color, arduinoCtr)
    #updateLights(domColor, arduinoCtr)
    #albumImg.show()
    return

def getAlbumUrl(playingSong):
    return playingSong['item']['album']['images'][1]['url']

def getImage(albumUrl):
    img = Image.open(requests.get(albumUrl, stream=True).raw)
    return img

def getDomColor(albumImg, palette_size = 4):
    paletted = albumImg.convert('P', palette=Image.ADAPTIVE, colors=palette_size)
    palette = paletted.getpalette()
    color_counts = sorted(paletted.getcolors(), reverse=True)
    palette_index = color_counts[0][1]
    dominant_color = palette[palette_index * 3:palette_index * 3 + 3]
    return dominant_color

def suppressNonDom(color):
    whiteThreshold = 210
    suppressFactor = (1-0.2)
    if (color[0] > whiteThreshold and color[1] > whiteThreshold and color[2] > whiteThreshold) is False:
        if color[0] < color[1] and color[0] < color[2]:
            color[0] = suppressFactor*color[0]
        elif color[1] < color[0] and color[1] < color[2]:
            color[1] = suppressFactor*color[1]
        elif color[2] < color[0] and color[2] < color[1]:
            color[2] = suppressFactor*color[2]
    return color

def updateLights(domColor, arduinoCtr):
    arduinoCtr.updateLights2(domColor)
    return

def idleLights(arduinoCtr):
    arduinoCtr.idle()
    return

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #Arduino Values:
    board = 'COM3'
    pinRed = 2
    pinGreen = 3
    pinBlue = 4

    #Spotify Creds File
    credsFile = 'src/SpotifyCreds.env'

    try:
        arduinoCtr = arduinoController.ArduinoController(board, pinRed, pinGreen, pinBlue)
        spotifyCtr = spotifyConnect.SpotifyConnect(arduinoCtr, credsFile)
        spotifyCtr.connect()
        arduinoCtr.arduinoDisconnect()
    except KeyboardInterrupt:
        print("Interrupted")
        arduinoCtr.arduinoDisconnect()
