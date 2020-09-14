import RPi.GPIO as GPIO 
import Keypad
import sys
import time
import serial
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
	return (seq)
print('comeca o jogo')

def getGPS():
	SERIAL_PORT= "/dev/ttyAMA0"
	ser = serial.Serial(SERIAL_PORT, baudrate=9600 , timeout=5)
	ser.write("AT+CGPSPWR=1\r".encode('utf-8'))
	print("GPS ATIVADO")
	time.sleep(2)
	ser.write("AT+CGPSSTATUS?\r".encode('utf-8'))
	time.sleep(6)
	ser.write("AT+CGPSINF=4\r".encode('utf-8'))
	time.sleep(2)
	response =  ser.readlines()
	#print(response[7])
	posta=str(response[7]).split(',');
	#print(posta)
	latitude=posta[1]
	ns=posta[2]
	longitude=posta[3]
	ew=posta[4]
	resposta="GPS: "+ns+" lat:"+latitude+" "+ew+" long:"+longitude
	return(resposta)
	
def sendSMS(conteudo):
	
	SERIAL_PORT= "/dev/ttyAMA0"
	ser = serial.Serial(SERIAL_PORT, baudrate=9600 , timeout=5)
	ser.write("ATH\r".encode('utf-8'))
	time.sleep(3)
	ser.write("AT+CMGF=1\r".encode('utf-8'))
	print("SMS ATIVADO")
	time.sleep(3)
	ser.write('AT+CMGS= "79996344527"\r'.encode('utf-8'))
	print("mandando mensagem")
	time.sleep(3)
	msg=conteudo+chr(26)
	ser.write(msg.encode('utf-8'))
	time.sleep(3)
	print("mensagem enviada")
	

try:
	while(True):
		sequencia=loopMatriz()
		
		coordenadas=getGPS()
	
		sms="sequencia: "+sequencia+" "+coordenadas
		sendSMS(sms)
except KeyboardInterrupt:
	GPIO.cleanup()

