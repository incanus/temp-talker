import time

import adafruit_thermistor
import board
import busio
import digitalio

try:
    from audiocore import WaveFile
except ImportError:
    from audioio import WaveFile

try:
    from audioio import AudioOut
except ImportError:
    try:
        from audiopwmio import PWMAudioOut as AudioOut
    except ImportError:
        pass

button_a = digitalio.DigitalInOut(board.BUTTON_A)
button_a.switch_to_input(pull=digitalio.Pull.DOWN)

button_b = digitalio.DigitalInOut(board.BUTTON_B)
button_b.switch_to_input(pull=digitalio.Pull.DOWN)

speaker_enable = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
speaker_enable.direction = digitalio.Direction.OUTPUT
speaker_enable.value = True

thermistor = adafruit_thermistor.Thermistor(
    board.TEMPERATURE,
    10000,
    10000,
    25,
    3950)

uart = busio.UART(board.TX, board.RX, baudrate=115200)

def play_file(base):
    wave_file = open('clips/' + str(base) + '.wav', 'rb')
    with WaveFile(wave_file) as wave:
        with AudioOut(board.SPEAKER) as audio:
            audio.play(wave)
            while audio.playing:
                pass

while True:
    data = uart.read(1)
    if data is not None or button_a.value or button_b.value:
        temp_f = thermistor.temperature * 9 / 5 + 32
        uart.write(('Temp: ' + str(temp_f) + "\r\n").encode('utf-8'))
        hundreds = 100 if temp_f >= 100 else None
        tens = int(temp_f / 10) * 10 if temp_f >= 10 else None
        ones = int(temp_f % 10)
        ones = ones if ones > 0 else None
        if hundreds:
            play_file(hundreds)
        if tens:
            play_file(tens)
        if ones:
            play_file(ones)
        play_file('degrees')
        time.sleep(1)