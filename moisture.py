import RPi.GPIO as GPIO
import time
import smtplib
import datetime


#GPIO SETUP
moisture = 21
pump = 26

GPIO.setmode(GPIO.BCM)
GPIO.setup(moisture, GPIO.IN)
GPIO.setup(pump, GPIO.OUT)

#email kuldeshez szukseges parameterek
smtpUser = 'robinorbi127@gmail.com'
smtpPass = 'NorbiRobi123'
toAdd = 'skrapits.robert99@gmail.com'
fromAdd = smtpUser
subject = 'Locsolasi ertesites'
header = 'To: ' + toAdd + '\n' + 'From: ' + fromAdd + '\n' + 'Subject: ' + subject


def callback(moisture):
    if GPIO.input(moisture): 
        print "Szaraz"
        GPIO.output(pump, GPIO.HIGH)
        print "Locsolas inditasa"
        
        #fajl letrehozas es fajlba iras
        d=open("idopontok.txt").read()
        d=d+datetime.datetime.now().strftime("%Y-%m-%d / %H:%M:%S")+"\n"
        f=open("idopontok.txt","w").write(d)
        d=open("idopontok.txt").read().strip().split()
        
        #email kuldes
        body = 'Hello!\n\nMeglocsoltam a viragodat, ekkor:  ' + datetime.datetime.now().strftime("%Y-%m-%d / %H:%M:%S") + '\nTovabbi szep napot!\nUdvozlettel: Raspberry Pi.'
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(smtpUser, smtpPass)
        s.sendmail(fromAdd, toAdd, header + '\n\n' +body)
        s.quit()
        
        
        time.sleep(5)
        GPIO.output(pump, GPIO.LOW)
       

    else:
        print "Nedves"
       
        
#infinite loop
while True:
    callback(moisture)
    print "-------------------------------------"
    time.sleep(10)
    
    
    