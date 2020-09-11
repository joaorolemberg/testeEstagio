import RPi.GPIO as GPIO 
import Keypad

import time
import busio
import board
import adafruit_amg88xx
i2c = busio.I2C(board.SCL, board.SDA)
amg = adafruit_amg88xx.AMG88XX(i2c)

GPIO.setmode(GPIO.BCM)
ROWS = 4
COLS = 4
keys = ['1','2','3','A',
	'4','5','6','B',
	'7','8','9','C',
	'*','0','#','D']


rowsPins = [18,23,24,25]
colsPins = [10,22,27,17]



def loopMatriz():
	arquivo = open("leituras.txt", "a")
	seq = ''
	keypad = Keypad.Keypad(keys,rowsPins,colsPins,ROWS,COLS)
	keypad.setDebounceTime(50)
	while(True):
		key=keypad.getKey()
		if(key != keypad.NULL):
			if(key != "D"):
				#seq.append(key)
				seq=seq+key
				
				print(key)
			else: 
				break
	print('A sequencia foi: ')
	print(seq)
	arquivo.write(seq)
	arquivo.write('\n')
	
	terma= list()
	for row in amg.pixels:
		print(['{0:.1f}'.format(temp) for temp in row])
		terma.append(['{0:.1f}'.format(temp) for temp in row])
		print("")
	print("\n")
	for x in terma:
		arquivo.write(str(x))
		arquivo.write('\n')
	arquivo.write('---\n')
	arquivo.close()
print('comeca o jogo')
try:
	while(True):
		loopMatriz()
except KeyboardInterrupt:
	GPIO.cleanup()

