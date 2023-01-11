import os
import cv2
from datetime import datetime,timedelta
import imutils
import time
from pathlib import Path
#----TODO:----#
#Cloud sync.

#--RTSP SETTINGS--#
rtspSource = 1 #0: Use parameters  , 1: Use RTSP string 
rtspString = "rtsp://demo:demo@192.168.1.100:5551/h264_ulaw.sdp" #RTSP_String
IP = "192.168.1.100" #RTSP Parameters
PORT = "5541"
EXTENTION = "h264_ulaw.sdp"
USER = "demo"
PASS = "demo"

#---RECORD SETTINGS---#
recordMin = 3 #record new video every x minutes ( min: 1 - max:59 )
putTime = 1 #Put date and time on recorded video (0:No / 1:Yes)
recordWidth = 320 #only width available, height will set automaticly regarding to source
showImage = 0 #show live stream (0:No / 1:Yes)
fpsVal = 30 #stream and record fps (max:30 - min:1)
restartTime = 3 #System will restart if any error occures! (minute)
recodDays = 5 #How many days will recorded. (depends on free space) [1min ~ 2mb] [7 days = 21GB]
deleteTime = "04:00" #everyday system will delete old records (recodDays) at this time

#Internal settings. Don't change!
lastMin = 0
resDetected = 0
recordHeight = 0
recordCount = 0
functionActive = 0
deleteHour = deleteTime.split(":")[0]
deleteMinute = deleteTime.split(":")[1]
lastCleanDate = datetime(1923, 4, 23)
codec =cv2.VideoWriter_fourcc(*"mp4v")

def timeStamp():
    now = datetime.now()
    current_time = now.strftime("%d.%m.%Y %H:%M:%S")
    return current_time

def frameName():
    now = datetime.now()    
    f_name = now.strftime("%Y_%m_%d_%H_%M_%S")
    frame_name = "{}.mp4".format(f_name)
    return frame_name

def appendLog(textVal):
    with open('LOG.txt', 'a') as fd:
        tm = timeStamp()
        fd.write(tm +">" + textVal + "\n")    

def cleanOldRecords(dayRange):
    print ("Cleaning process started!") #LOG this
    appendLog("Cleaning process started!")
    thatDate = datetime.now().date() - timedelta(days = dayRange)
    for file in os.listdir():
        if file.endswith(".mp4"):
            file_name = file.split(".")[0]
            fileParams = file_name.split("_")
            fileY = fileParams[0]
            fileM = fileParams[1]
            fileD = fileParams[2]
            if thatDate.year >= int(fileY) and thatDate.month >= int(fileM) and thatDate.day >= int(fileD):
                deleteStr = "Deleted : {}".format(file)
                Path.unlink(file) #unComment when it secure!!!
                print (deleteStr) #Log this
                appendLog(deleteStr)

def mainWorkload():
    logStr = "Application started. Wait for RTSP connection and first settings!"
    print (logStr)
    appendLog (logStr)

    global showImage
    global lastMin
    global resDetected
    global recordHeight
    global recordCount
    global restartTime
    global functionActive
    global deleteMinute
    global deleteHour
    global USER
    global PASS
    global IP
    global PORT
    global EXTENTION
    global fpsVal
    global rtspSource
    global rtspString
    global lastCleanDate
    global recodDays

    if rtspSource == 0:
        cap = cv2.VideoCapture("rtsp://{}:{}@{}:{}/{}".format(USER,PASS,IP,PORT,EXTENTION))
    else:
        cap = cv2.VideoCapture(rtspString)
    cap.set(cv2.CAP_PROP_FPS, fpsVal)

    restartTimeSec = restartTime * 60
    lastRecorded = "0000_00_00_00_00_00.mp4"
    c = 0
    functionActive = 1
    
    while(cap.isOpened()):
        ret, frame = cap.read()
        if resDetected == 0:
            width = cap.get(3)
            height = cap.get(4)
            resRate = width / recordWidth
            recordHeight = height / resRate
            recordHeight = int(recordHeight)
            print ("Record resolution set as {}x{}".format(recordWidth, recordHeight))
            resDetected = 1
            
        if recordCount == 0: #first record
            n = datetime.now()
            firstName = "{}_{}_{}_{}_{}_{}.mp4".format(n.year,n.month,n.day,n.hour,n.minute,n.second)
            out = cv2.VideoWriter(firstName ,codec, fpsVal, (recordWidth, recordHeight))
            recordCount = 1
            print ("First record configured and recording started!")
            
        try: 
            frame = imutils.resize(frame, width=recordWidth)            
        except:
            print ("Error occurred while image processing. Server might be closed! Checking!")
            time.sleep (2) #wait before check!
            if cap.isOpened() == False:
                logStr = "RTSP Server seems closed! Check the RTSP server! System restart in {} min!".format(restartTime)
                appendLog(logStr)
                print (logStr)                
                functionActive = 0
                resDetected = 0
                recordCount = 0
                out.release()
                cap.release()
                cv2.destroyAllWindows()
                time.sleep(restartTimeSec)
                return
            else:
                logStr = "RTSP Server seems open! Another unidentified error!! System restart in {} min!".format(restartTime)
                appendLog(logStr)
                print (logStr)
                functionActive = 0
                resDetected = 0
                recordCount = 0
                out.release()
                cap.release()
                cv2.destroyAllWindows()
                time.sleep(restartTimeSec)
                break
                
        if putTime == 1:
            timeText = timeStamp()
            cv2.putText(img=frame, text=timeText, org=(0, 15), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1, color=(0, 0, 255),thickness=0)

        controlTime = datetime.now()

        if lastCleanDate!=controlTime.date() and str(controlTime.hour) == str(deleteHour) and str(controlTime.minute) == str(deleteMinute):
            lastCleanDate = controlTime.date()
            cleanOldRecords(recodDays)
            
        
        schTime = controlTime.minute
        
        if schTime != lastMin and (schTime % recordMin) == 0 :
            out.release()
            lastMin = schTime
            file_name = frameName()
            out = cv2.VideoWriter(file_name ,codec, fpsVal, (recordWidth, recordHeight))
            logStr = "LOG : {} saved. {} started to record. Total frame : {}".format(lastRecorded,file_name,c)
            c= 0
            print (logStr)
            appendLog(logStr)
            lastRecorded = file_name
        out.write(frame)
        c = c+1
        
        if showImage == 1:
            cv2.imshow('TestView', frame)
            
        if cv2.waitKey(20) & 0xFF == ord('q'):
            logStr = "Video screen closed. Application will restart without screen and continue to record!"
            print (logStr)
            appendLog(logStr)
            out.release()
            showImage = 0
            functionActive = 0
            resDetected = 0
            recordCount = 0
            out.release()
            cap.release()
            cv2.destroyAllWindows()
            break
  
while True:
    if functionActive == 0:
        mainWorkload()
