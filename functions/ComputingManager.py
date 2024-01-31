from sikuli import *
from time import sleep
import sys, os

LogAppPath = r"..\Common.sikuli"
CMAppPath = r"..\ComputingManager.sikuli"
sys.path.append(LogAppPath)

import Studio as Studio
import log_record as Log

def UIexist(CMPath):
    if os.path.isfile(CMPath):
        while not exists("CM.png", 1):
            os.system(CMPath)
    else:
        print ("File %s is not exist") %(CMPath)
        Log.write_log("CM", ("Error: File %s is not exist") %(CMPath))
        return False
    print ("Open file %s is Finished") %(CMPath)
    Log.write_log("CM", ("Info: Open file %s is Finished") %(CMPath))
    return True

def IconStatus():
    i = 0
    while((exists(Pattern("Submit_StopSubmit.png").similar(0.95)) or (exists(Pattern("Submit_Enabled.png").similar(0.95)))) and i <= 5):
        if (exists(Pattern("Submit_StopSubmit.png").similar(0.95))):
            wait(10)
        if (exists(Pattern("Submit_Enabled.png").similar(0.95))):
            click("Submit_Enabled.png")
            i = i + 1
        print "i = ", i
    if ((exists(Pattern("Submit_StopSubmit.png").similar(0.95)) or (exists(Pattern("Submit_Enabled.png").similar(0.95))))):
        print "Submit Job is Failed"
        Log.write_log("CM", "Error: Submit Job is Failed")
        return False
    else:
        print "Submit Job is Finished"
        Log.write_log("CM", "Info: Submit Job is Finished")
        return True


CMPath = r"C:\Moldex3D\2023\Bin\MDXComputingManager2023.exe"    
UIexist(CMPath)
IconStatus()