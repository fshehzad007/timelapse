from time import sleep
from datetime import datetime
from sh import gphoto2 as gp

import signal, os, subprocess

shot_date = datetime.now().strftime("%Y-%m-%d")
shot_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
picID = "wv"
deviceID ="cam1"


# Set capturing target
capturetarget = ["--set-config", "capturetarget=1"]

gp(capturetarget)

# clear the sd card
clearCommand = ["--folder", "/store_00020001/DCIM/100CANON", "-R", "--delete-all-files"]

triggerCommand = ["--trigger-capture"]
downloadCommand = ["--get-all-files"]

folder_name = shot_date+ picID + "-" + deviceID
save_location = "/home/pi/Desktop/wvtest/pics/" + folder_name

def createSaveFolder():
    try:
        os.makedirs(save_location)
    except:
        print("folder already existant or failed to create the folder.")
    os.chdir(save_location)


def captureImages():
    gp(triggerCommand)
    sleep(1)
    gp(downloadCommand)
    gp(clearCommand)
    
    
def renameFiles(ID, deviceID):
    for filename in os.listdir("."):
            if len(filename) < 13:
                if filename.endswith(".JPG"):
                        os.rename(filename, (shot_time +"_"+ ID + "-" + deviceID + ".JPG"))
                        print("Rename the JPG")
                #elif filename.endswith(".CR2")
                    #os.rename(filename, (shot_timme + ID + ".CR2"))
                    #print("REname the CR2")


# kill the gphto2 process
# that starts whenever we connect the camera

def  killgphoto2Process():
    p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
    out, err = p.communicate()
    
    #search fot the line that has the process
    #we eant to kill
    for line in out.splitlines():
        if b'gvfsd-gphoto2' in line:
            # Kill the process
            pid = int(line.split(None,1)[0])
            os.kill(pid, signal.SIGKILL)



killgphoto2Process()
gp(clearCommand)

while True:
	createSaveFolder()
	captureImages()
	renameFiles(picID,deviceID)
	sleep(1)
	shot_date = datetime.now().strftime("%Y-%m-%d")
	shot_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                