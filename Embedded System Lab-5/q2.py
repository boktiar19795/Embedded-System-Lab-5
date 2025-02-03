import RPi.GPIO as GPIO
import time

SDI1 = 12
RCLK1 = 16
SRCLK1 = 18

SDI2 = 29
RCLK2 = 31
SRCLK2 = 36

# Specify segment codes for digits 0 through 9
numCode = [0x3f, 0x06, 0x5b, 0x4f, 0x66, 0x6d, 0x7d, 0x07, 0x7f, 0x6f]

# Specify segment codes for letters A through Z.
alphaCode = [
    0x77, 0x7C, 0x5A, 0x5E, 0x79, 0x71, 0x6F, 0x74, 0x10, 0x0E, 0x70, 0x18, 0x49, 0x54, 0x5C, 0x73,
    0x67, 0x50, 0x6D, 0x78, 0x1C, 0x62, 0x36, 0x52, 0x72, 0x43
]

def print_msg():
    print('Program is executing...')
    print('Please press Ctrl+C to exit the program...')

def setup():
    GPIO.setmode(GPIO.BOARD)   
    GPIO.setup(SDI2, GPIO.OUT)
    GPIO.setup(RCLK2, GPIO.OUT)
    GPIO.setup(SRCLK2, GPIO.OUT)

    GPIO.setup(SDI3, GPIO.OUT)
    GPIO.setup(RCLK3, GPIO.OUT)
    GPIO.setup(SRCLK3, GPIO.OUT)

    GPIO.output(SDI2, GPIO.LOW)
    GPIO.output(RCLK2, GPIO.LOW)
    GPIO.output(SRCLK2, GPIO.LOW)

    GPIO.output(SDI3, GPIO.LOW)
    GPIO.output(RCLK3, GPIO.LOW)
    GPIO.output(SRCLK3, GPIO.LOW)

def hc595_shift(dat1, sdi1, rclk1, srclk1):
    for bit in range(0, 8):
        GPIO.output(sdi1, 0x80 & (dat1 << bit))
        GPIO.output(srclk1, GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(srclk1, GPIO.LOW)
    GPIO.output(rclk1, GPIO.HIGH)
    time.sleep(0.001)
    GPIO.output(rclk1, GPIO.LOW)

def display_number(num1):
    T = num1 // 10
    T1 = num1 % 10

    hc595_shift(numCode[tens], SDI1, RCLK1, SRCLK1)
    hc595_shift(numCode[units], SDI2, RCLK2, SRCLK2)

def display_alphabet(char):
    char_index = ord(char.upper()) - ord('A')

    hc595_shift(alphaCode[char_index], SDI1, RCLK1, SRCLK1)
    hc595_shift(0x00, SDI2, RCLK2, SRCLK2)

def loop():
    while True:
        for num1 in range(1, 26):
            display_number(num1)
            time.sleep(0.5)

        for letter in range(ord('A'), ord('Z')+1):
            display_alphabet(chr(char))
            time.sleep(1)

def destroy():
    GPIO.cleanup()

print_msg()
setup()
try:
    loop()
except KeyboardInterrupt:
    destroy()