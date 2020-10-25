from __future__ import print_function
from __future__ import division
import easygopigo3 as easy
import cv2
import picamera
import pytesseract
import robot
from gtts import gTTS
import os
import time

camera=picamera.PiCamera()



#function detect text from the cardboard and then say aloud what the text is
def read_text():
     
    #tesseract assume single uniform block of text with this value
    config="--psm 6"
    #threshold value
    threshold=55
    robot_speak("Hei, olen GoPiGo. Osaan lukea.")
    while True:
        
        try:
        #if the cardboard where the text is is closer than 30 cm camera takes a photo and detection is made from it        
            if(robot.read_distance_sensor() < 30):
                #add delay to the execution of the function
                time.sleep(2.5) 
                #file path
                file="/home/pi/environments/Tesseract/image_ocr.png"
                #camera takes a photo and save it to file
                camera.capture(file)
                #read file and gets photo from there
                image=cv2.imread(file)
                #crop smaller area from the image
                crop_image = image[300:550, 400:750]
                #convert cropped image to grayscale
                gray = cv2.cvtColor(crop_image, cv2.COLOR_BGR2GRAY)
                #create black and white photo from areas  which are over threshold value in the gray photo 
                thresh = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)[1]
                #start measure the time of detection
                start_time = time.time()
                #convert text in the black and white image to text, finnish is the language to be detected and confugure is config
                text=pytesseract.image_to_string(thresh, lang="fin", config =config)
                #count the time of the detection 
                elapsed_ms = (time.time() - start_time) 
                
                #if text is not null calls robot_speak function and prints time to the window
                if(text!=None):
                    robot_speak(text)
                    print("Tunnistukseen kulunut aika: {:0.3f}".format(elapsed_ms) +" s")


            #or robot asks user to show a new text   
            else:
                robot_speak("Näytä teksti")
        
        #you can stop the program with ctrl + c
        #when robot says bye bye
        except KeyboardInterrupt:
            robot_speak("Hei Hei")
            break



#says detected text aloud, gets text as a parameter
def robot_speak(text):
  
    #makes mp3.path 
    file="/home/pi/environments/Tesseract/file.mp3"
    #seds text, language id and to google's server to get a file
    #gTTS is googles TextToSpeech API
    tts=gTTS(text, lang= "fi", tld="com")
    #save file
    tts.save(file)
    #os plays the file with mpg123 program
    os.system("mpg123 /home/pi/environments/Tesseract/file.mp3")
    time.sleep(2)



#program starts from main function when you run it
#it calls read_text function and you can stop the program with ctrl + c
if __name__ == "__main__":
    
    read_text()
    

   
    