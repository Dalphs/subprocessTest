import RPi.GPIO as GPIO
import time
from threading import Thread

#The GPIO pins which acts as up and down buttons on the Ropox table
down = 16
up = 18

GPIO.setmode(GPIO.BOARD)
GPIO.setup(down, GPIO.OUT)
GPIO.setup(up, GPIO.OUT)

#Variable we use to tel threads if they need to stop even if they are not finished
stop = False

#method which starts the string. It gives the thread an argument which controls the time the thread wil run
def goUp(seconds):
    
    #checkGpioStatus returns true if a GPIO pin is already in use. 
    #If it returns true we will turn of all pins so the table will not be moving since it might be a mistake the table is moving
    #Otherwise
    if not checkGpioStatus():
        l = Thread(target = goUpThread, args = (seconds, ))
        l.daemon = True
        l.start()
    else:
        stopTable()
    

#Same process as goUp() method above
def goDown(seconds):
    if not checkGpioStatus(): 
        l = Thread(target = goDownThread, args = (seconds, ))
        l.daemon = True
        l.start()
    else:   
        stopTable()

#The thread that's getting started in goDown() method
def goDownThread(seconds):
    # Giving global variable stop to the thread so we can stop it if neccesary
    global stop
    #Counter for logging purposes
    counter = 0
    #Turning on GPIO pin
    GPIO.output(down, GPIO.HIGH)

    # Checking wether stop has been changed to true and how long time has passed.
    # It updates every 1/10 second which is why the time in seconds is multiplied by 10
    while not stop and counter < seconds * 10:
        print("Korer ned " + str(counter))
        time.sleep(0.1)
        counter += 1
    # GPIO is turned off after stop has been changes to true or specified time has passed
    GPIO.output(down, GPIO.LOW)


# Same as goDownThread() above

def goUpThread(seconds):
    global stop
    counter = 0
    GPIO.output(up, GPIO.HIGH)

    while not stop and counter < seconds * 10:
        print("Korer op " + str(counter))
        time.sleep(0.1)
        counter += 1
    GPIO.output(up, GPIO.LOW)

#Returns wethert one of the GPIO pins is already turned on
def checkGpioStatus():
    if GPIO.input(up) or GPIO.input(down):
        return True
    return False

# Method which stops the currently running thread
def stopTable():
    #logging
    print("stop")
    global stop
    #When stop is set to true the thrads will stop since stop is a global variable
    stop = True
    #Waiting .2 seconds since threads update every .1 seconds, this is to avoid the change in the boolean will not be read before it is changed back
    time.sleep(0.2)
    #Setting stop boolean to False so a new thread can run, else we would not be able to run another thread
    stop = False

#Releasing the GPIO pins
def cleanUp():
    GPIO.cleanup()

#Test
def test():
    
    goDown(5)
    time.sleep(5)
    goUp(5)
    time.sleep(5)
    goUp(20)
    time.sleep(5)
    stopTable()
    goDown(20)
    time.sleep(5)
    stopTable()
    goDown(5)
    goUp(5)
    time.sleep(3)
    stopTable()
    cleanUp()
