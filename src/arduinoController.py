from pyfirmata2 import ArduinoMega, util
import time

class ArduinoController():

    def __init__(self, boardPort, pinRed, pinGreen, pinBlue):
        self.board = ArduinoMega(boardPort)
        self.pinRed = self.board.get_pin('d:' + str(pinRed) + ':p')
        self.pinGreen = self.board.get_pin('d:' + str(pinGreen) + ':p')
        self.pinBlue = self.board.get_pin('d:' + str(pinBlue) + ':p')
        self.pinRed2 = self.board.get_pin('d:8:p')
        self.pinGreen2 = self.board.get_pin('d:9:p')
        self.pinBlue2 = self.board.get_pin('d:10:p')
        self.arduinoConnect()

        self.currRed = 0
        self.currGreen = 0
        self.currBlue = 0
        return

    def arduinoConnect(self):
        print("Arduino: Connecting")
        iterator = util.Iterator(self.board)
        iterator.start()
        print("Arduino: Connected")
        return

    def arduinoDisconnect(self):
        self.updateLights([0,0,0])
        self.board.exit()
        print("Arduino: Disconnected")
        return

    def updateLights(self, color):
        RED = color[0]
        GREEN = color[1]
        BLUE = color[2]
        self.pinRed.write(RED/256)
        self.pinGreen.write(GREEN/256)
        self.pinBlue.write(BLUE/256)
        self.pinRed2.write(RED / 256)
        self.pinGreen2.write(GREEN / 256)
        self.pinBlue2.write(BLUE / 256)
        print("Arduino: Color Changed To [" + str(RED) + "," + str(GREEN) + "," + str(BLUE) + "]")


        self.currRed = color[0]
        self.currGreen = color[1]
        self.currBlue = color[2]
        return

    def updateLights2(self, color):
        timeChange = 0.10
        RED = color[0]
        GREEN = color[1]
        BLUE = color[2]
        self.pinRed.write(RED/255)
        self.pinGreen.write(GREEN/255)
        self.pinBlue.write(BLUE/255)
        self.pinRed2.write(RED / 255)
        self.pinGreen2.write(GREEN / 255)
        self.pinBlue2.write(BLUE / 255)
        time.sleep(timeChange)
        self.pinRed.write(self.currRed/255)
        self.pinGreen.write(self.currGreen/255)
        self.pinBlue.write(self.currBlue/255)
        self.pinRed2.write(self.currRed / 255)
        self.pinGreen2.write(self.currGreen / 255)
        self.pinBlue2.write(self.currBlue / 255)
        time.sleep(timeChange)
        self.pinRed.write(RED/255)
        self.pinGreen.write(GREEN/255)
        self.pinBlue.write(BLUE/255)
        self.pinRed2.write(RED / 255)
        self.pinGreen2.write(GREEN / 255)
        self.pinBlue2.write(BLUE / 255)
        time.sleep(timeChange)
        self.pinRed.write(self.currRed/255)
        self.pinGreen.write(self.currGreen/255)
        self.pinBlue.write(self.currBlue/255)
        self.pinRed2.write(self.currRed / 255)
        self.pinGreen2.write(self.currGreen / 255)
        self.pinBlue2.write(self.currBlue / 255)
        time.sleep(timeChange)
        self.pinRed.write(RED/255)
        self.pinGreen.write(GREEN/255)
        self.pinBlue.write(BLUE/255)
        self.pinRed2.write(RED / 255)
        self.pinGreen2.write(GREEN / 255)
        self.pinBlue2.write(BLUE / 255)
        time.sleep(timeChange)
        print("Arduino: Color Changed To [" + str(RED) + "," + str(GREEN) + "," + str(BLUE) + "]")
        self.currRed = RED
        self.currGreen = GREEN
        self.currBlue = BLUE
        return

    def idle(self):
        RED = 255
        GREEN = 0
        BLUE = 0
        self.pinRed.write(RED / 256)
        self.pinGreen.write(GREEN / 256)
        self.pinBlue.write(BLUE / 256)
        self.pinRed2.write(RED / 256)
        self.pinGreen2.write(GREEN / 256)
        self.pinBlue2.write(BLUE / 256)
        time.sleep(0.25)

        for i in range(255):
            RED -= 1
            GREEN += 1
            self.pinRed.write(RED / 256)
            self.pinGreen.write(GREEN / 256)
            self.pinRed2.write(RED / 256)
            self.pinGreen2.write(GREEN / 256)
            print("Current Color: [", RED, ",", GREEN, ",", BLUE, "]")
            time.sleep(0.10)

        RED = 0
        GREEN = 255
        BLUE = 0

        for i in range(255):
            GREEN -= 1
            BLUE += 1
            self.pinGreen.write(GREEN / 256)
            self.pinBlue.write(BLUE / 256)
            self.pinGreen2.write(GREEN / 256)
            self.pinBlue2.write(BLUE / 256)
            print("Current Color: [", RED, ",", GREEN, ",", BLUE, "]")
            time.sleep(0.10)

        RED = 0
        GREEN = 0
        BLUE = 255

        for i in range(255):
            BLUE -= 1
            RED += 1
            self.pinBlue.write(BLUE / 256)
            self.pinRed.write(RED / 256)
            self.pinBlue2.write(BLUE / 256)
            self.pinRed2.write(RED / 256)
            print("Current Color: [", RED, ",", GREEN, ",", BLUE, "]")
            time.sleep(0.10)
        return