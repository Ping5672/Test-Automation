from re import I
from sikuli import *
import sys, os
import codecs

 
CommonAppPath = r"..\..\sikuli_Share\Common.sikuli"
StudioAppPath = r"..\..\sikuli_Share\Studio.sikuli"
CMAppPath = r"..\..\sikuli_Share/CM.sikuli"
if os.path.isdir(CMAppPath):
    cwd = r"..\.."
else:
    cwd = (str(os.getcwd())).split('MDX_')[0] + r'MDX_' + (str(os.getcwd())).split('MDX_')[1].split('\\')[0]

LogAppPath = cwd + r"\sikuli_Share\Common.sikuli"
CMAppPath = cwd + r"\sikuli_Share\CM.sikuli"


sys.path.append(CommonAppPath)
sys.path.append(LogAppPath)
sys.path.append(CMAppPath)
sys.path.append(StudioAppPath)
import Studio as Studio
import log_record as Log
import Common as Common

MainInstallPath, ver = Common.getregkeyvalue(r"HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\CoreTechSystem\MDX_ParallelComputing", "INSTALLDIR")  
if (MainInstallPath <> False):
    CMPath = MainInstallPath + r'\Bin\MDXComputingManager' + ver + r'.exe'

def OpenApp(AppPath, UIPic):
    #Open CM UI
    try:
        openApp(AppPath)
        if exists(UIPic, 60):
            print("%s UI is opened Finished") %(AppPath)
            Log.write_log("CM", ("Info: %s UI is opened Finished") %(AppPath))
            return True
    except:
        print("%s UI is opened Failed") %(AppPath)
        Log.write_log("CM", ("Error: %s UI is opened Failed") %(AppPath))
        sys.exit()
        return False

def Wait_Dialog(AppPath):
   try:
       i = 0
       while exists(Pattern(AppPath).similar(0.90), 5) and i < 5:
           wait(3)
           i += 1
       print ("def Wait_Dialog is Finished")
       Log.write_log("CM", "Info: def Wait_Dialog is Finished")
       return True
   except:
       print ("def Wait_Dialog is Failed")
       Log.write_log("CM", "Error: def Wait_Dialog is Failed")
       sys.exit()
       return False
        
def CloseApp(AppPath):
    #Close CM UI
    try:
        
        closeApp(AppPath)
        print("%s UI is closed Finished") %(AppPath)
        Log.write_log("CM", ("Info: %s UI is closed Finished") %(AppPath))
        return True
    except:
        print("%s UI is closed Failed") %(AppPath)
        Log.write_log("CM", ("Error: %s UI is closed Failed") %(AppPath))
        sys.exit()
        return False
        
def Click_Icon(AppPath):
    try:
        click(Pattern(AppPath).similar(0.90)) #click icon
        Log.write_log("CM", ("Info: click Icon %s is Finished") %(AppPath))
        return True
    except:
        print("%s UI is closed Failed") %(AppPath)
        Log.write_log("CM", ("Error: click Icon %s is Failed") %(AppPath))
        sys.exit()
        return False
        
def ValueSetting(ItemPic, offsetx, offsety, ItemValue):
    try:
        i = 0
        while not exists (Pattern(ItemPic).similar(0.97), 5) and i < 10:
            i += 1
        x = wait(Pattern(ItemPic).similar(0.97).targetOffset(offsetx, offsety), 10)
        click(x)
        #type(Key.F2)
        #type("a",Key.CTRL)
        paste(ItemValue)
        print ("def ValueSetting {} is Finished".format(ItemPic))          
        Log.write_log("CM", "Info: def ValueSetting {} is Finished".format(ItemPic))
        return True
    except:
        print ("def ValueSetting {} is Failed".format(ItemPic))
        Log.write_log("CM", "Error: def ValueSetting {} is Failed".format(ItemPic))
        sys.exit()
        return False
        
def connectserver(TypeofServer,CMAppPath):
    try:
        if(TypeofServer == "RC"):
                print("connect to RC")
                if  exists(Pattern(CMAppPath + r"\CM_Locahost_Connected2.png").similar(0.90), 3): #if Local host status is connected
                    print ("LH is connected")
                    if exists(Pattern(CMAppPath + r"\CM_Available.png").similar(0.90), 10):
                        click(Pattern(CMAppPath + r"\CM_Available.png").similar(0.90))
                        click(Pattern(CMAppPath + r"\CM_Connect.png").similar(0.90))
                    else:
                        print('Not found Status Available!')
                else:
                    print ("RC is connected")
                    Log.write_log("CM", "Info: RC is connected")
                Wait_Dialog(CMAppPath + r"\CM_Connecting.png")
        if(TypeofServer == "LH"):
            print("connect to LH")
            click(Pattern(CMAppPath + r"\Studio_localhost.png").similar(0.8))
            click(Pattern(CMAppPath + r"\CM_Connect.png").similar(0.90))
        print ("def connectserver is Finished")
        Log.write_log("CM", "Info: def connectserver is Finished")
        return True
    except:
        print ("def connectserver is Failed")
        Log.write_log("CM", "Error: def connectserver is Failed")
        sys.exit()
        return False

def AddServer(CMAppPath, iphostname):
    try:
        if exists(Pattern(CMAppPath + r"\CM_Locahost_Connected.png").similar(0.90), 5):
            if not exists(Pattern(CMAppPath + r"\CM_Available.png")):
                Click_Icon(CMAppPath + r"\CM_New.png")
                ValueSetting(CMAppPath + r"\CM_IPHostaname.png", 130, 0, iphostname)
                ValueSetting(CMAppPath + r"\CM_Account.png", 145, 0, "administrator") #type Account
                ValueSetting(CMAppPath + r"\CM_Password.png", 145, 0, "moldex3d!") #type Password
                Click_Icon(CMAppPath + r"\CM_OK.png")
        print ("def AddServer is Finished")
        Log.write_log("CM", "Info: def AddServer is Finished")
        return True
    except:
        print ("def AddServer is Failed")
        Log.write_log("CM", "Error: def AddServer is Failed")
        sys.exit()
        return False

def IconSubmitStatus():
    try:
        i = 0
        while((exists(Pattern(CMAppPath + r"\Submit_StopSubmit.png").similar(0.95)) or (exists(Pattern(CMAppPath + r"\Submit_Enabled.png").similar(0.95)))) and i <= 5):
            if (exists(Pattern(CMAppPath + r"\Submit_StopSubmit.png").similar(0.95))):
                wait(10)
            if (exists(Pattern(CMAppPath + r"\Submit_Enabled.png").similar(0.95))):
                click(CMAppPath + r"\Submit_Enabled.png")
            i = i + 1
            print ("i = %d" %i)
        if ((exists(Pattern(CMAppPath + r"\Submit_StopSubmit.png").similar(0.95)) or (exists(Pattern(CMAppPath + r"\Submit_Enabled.png").similar(0.95))))):
            print ("def IconSubmitStatus is Failed")
            Log.write_log("CM", "Error: def IconSubmitStatus is Failed")
            return False
        else:
            print ("def IconSubmitStatus is Finished")
            Log.write_log("CM", "Info: def IconSubmitStatus is Finished")
            return True
    except:
        
        print ("def IconSubmitStatus is Failed")
        Log.write_log("CM", "Error: def IconSubmitStatus is Failed")
        return False

def DragDrop():
    try:
        if not exists(Pattern(CMAppPath + r"\SlideDown.png").similar(0.80), 3):
            dragDrop(CMAppPath + r"\SlideUp.png", CMAppPath + r"\SlideBottom.png")
            print ("def DragDrop is Finished")
            Log.write_log("CM", "Info: def DragDrop is Finished")
            return True
        else:
            print ("def DragDrop which slide has been SlideDown")
            Log.write_log("CM", "Info: def DragDrop which slide has been SlideDown")
            return True            
    except:
        print ("def DragDrop is Failed")
        Log.write_log("CM", "Error: def DragDrop is Failed")
        return False

def RunningStatus():
    try:
        while (exists(CMAppPath + r"\Status_Running.png") or exists(CMAppPath + r"\Status_Queued.png")):
            print ("Job is running")
            wait(10)
        print ("def RunningStatus is Finished")
        Log.write_log("CM", "Info: RunningStatus is Finished")
        return True
    except:
        print ("def RunningStatus is Failed")
        Log.write_log("CM", "Error: def RunningStatus is Failed")
        return False

def Downloading():
    try:
        while (exists(Pattern(CMAppPath + r"\Status_Downloading.png").similar(0.80))):
            print ("Job is downloading")
            wait(10)
        print ("def Downloading is Finished")
        Log.write_log("CM", "Info: Downloading is Finished")
        return True
    except:
        print ("def Downloading is Failed")
        Log.write_log("CM", "Error: def Downloading is Failed")
        return False

def SendRCtoCM(StudioAppPath,CMAppPath):
    try:
        Studio.OpenApp(CMPath, CMAppPath + r"\CM_UI.png")
        click(CMAppPath + r"\CM_Logo.png")
        click(CMAppPath + r"\CM_Submission.png")
        connectserver("RC",CMAppPath) 
        click(StudioAppPath + r"\Studio_add.png")
        i=0
        wait(CMAppPath + r"\CM_Open.png", 3)
        x = Pattern(CMAppPath + r"\CM_Filename_empty.png").similar(0.9).targetOffset(-15,0)
        while (exists(x, 1) <> None) and i<3:
            click(x)
            type("v",KeyModifier.CTRL)
            type("\MDXBatchRun.bjs")
            mouseMove(0,50)
            wait(1)
            i += 1
        click(StudioAppPath + r"\File_Open.png")
        IconSubmitStatus()
        wait(1)
        click(CMAppPath + r"\CM_Submission.png")
        return True
    except:
        print ("def SendRCtoCM is Failed")
        Log.write_log("CM", "Error: def SendRCtoCM is Failed")
        return False