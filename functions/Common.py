# -*- coding: UTF-8 -*-
from sikuli import *
#from _winret import *
import sys, os, shutil, socket, subprocess
from datetime import datetime
import ConfigParser
 
LogAppPath = r"../sikuli_Share/Common.sikuli"
sys.path.append(LogAppPath)
import log_record as Log
 
def gototargetpath(target):
    uppath = os.path.abspath(os.path.join(os.getcwd(), os.path.pardir))
    basename = os.path.basename(uppath)
    while (basename <> target):
        uppath = os.path.abspath(os.path.join(uppath, os.path.pardir))
        basename = os.path.basename(uppath)
    return uppath

def readfile(filepath):
    file = open(filepath, "r")
    data = file.readlines()
    for line in data:
        if '#' in line:
            line = None
    file.close()  
    return line

def readfilesection(filepath, startsection, endsection, serachname):
    """
    input: file path
    output: mesh type
    """
    try:
        found_type = False
        t_type = []
        with open(filepath, 'r') as file:
            for line in file:
                if startsection in line:
                    found_type = True
                    continue
                    
                if found_type:
                    if endsection in line:
                        found_type = False
                    else:
                        if serachname in line:
                            meshtype = line.split('\n')[0][-3:]
        print ("def readfilesection {} is Finished".format(meshtype))
        Log.write_log("Common", ("Info: def readfilesection {} is Finished").format(meshtype))
        return meshtype
    except:
        print ("def deletefile {} is Failed".format(meshtype))
        Log.write_log("Common", ("Error: def deletefile {} is Failed").format(meshtype))
        sys.exit()
        return False

def getextensionfilepath(filepath, extension):
    """
    input: file path
    output: mesh type    
    """
    try:      
        for dirPath, dirNames, fileNames in os.walk(filepath):
            for fileName in fileNames:
                filepath = os.path.join(dirPath, fileName)
                if (extension in filepath):
                    print (("def getextensionfilepath {} is Finished").format(filepath))
                    Log.write_log("Common", ("Info: def getextensionfilepath {} is Finished").format(filepath))
                    return filepath
    except:
        print (("def getextensionfilepath {} is Failed").format(filepath))
        Log.write_log("Common", ("Error: def getextensionfilepath {} is Failed").format(filepath))
        sys.exit()
        return False

def deletefile(source_file, destination_folder):
    # delete a specific file
    filename = (os.path.basename(source_file))
    try:
        if (os.path.isfile(source_file) and (os.path.isdir(destination_folder))):    
            os.remove(source_file)
            print ("def deletefile %s is Finished" %(filename))
            Log.write_log("Common", ("Info: def deletefile %s is Finished") %(filename))
        elif (not (os.path.isfile(source_file))):
            print ("def deletefile not found file %s" %(source_file))
            Log.write_log("Common", ("Error: def deletefile not found %s") %(source_file))
        elif (not (os.path.isdir(destination_folder))):
            print ("def deletefile not found path %s" %(destination_folder))
            Log.write_log("Common", ("Error: def deletefile not found path %s") %(destination_folder))
            #sys.exit()
            return False
        return True
    except:
        print ("def deletefile %s is Failed" %(filename))
        Log.write_log("Common", ("Error: def deletefile %s is Failed") %(filename))
        sys.exit()
        return False

def deletepath(destination_folder):
    # delete a specific folder
    try:
        if (os.path.isdir(destination_folder)):
            if ("ProgramData" not in destination_folder):
                print ("destination_folder is %s" %(destination_folder))
                shutil.rmtree(destination_folder)
                print ("def deletepath %s is Finished" %(destination_folder))
                Log.write_log("Common", ("Info: def deletepath %s is Finished") %(destination_folder))
            elif ("ProgramData" in destination_folder):
                files = os.listdir(destination_folder)
                for f in files:
                    if (f != "ServerInfo.ini"):
                        os.remove(destination_folder + f)
        elif (not (os.path.isdir(destination_folder))):
            print ("def deletepath not found path %s" %(destination_folder))
            Log.write_log("Common", ("Error: def deletepath not found path %s") %(destination_folder))
            return False
        return True
    except:
        print ("def deletepath %s is Failed" %(destination_folder))
        Log.write_log("Common", ("Error: def deletepath %s is Failed") %(destination_folder))
        sys.exit()
        return False
        
def copyfile(source_file, destination_folder):
    # Copy a specific file
    filename = (os.path.basename(source_file))
    try:
        if (os.path.isfile(source_file) and (os.path.isdir(destination_folder))):
            shutil.copy(source_file, destination_folder)              
            print ("def copyfile %s is Finished" %(filename))
            Log.write_log("Common", ("Info: def copyfile %s is Finished") %(filename))
        elif (not (os.path.isfile(source_file))):
            print ("def copyfile not found file %s" %(source_file))
            Log.write_log("Common", ("Error: def copyfile not found %s") %(source_file))
            #sys.exit()
            return False
        elif (not (os.path.isdir(destination_folder))):
            print ("def copyfile not found path %s" %(destination_folder))
            Log.write_log("Common", ("Error: def copyfile not found path %s") %(destination_folder))
            #sys.exit()
            return False
        return True
    except:
        print ("def copyfile %s is Failed" %(filename))
        Log.write_log("Common", ("Error: def copyfile %s is Failed") %(filename))
        sys.exit()
        return False 

def copydata(source_folder, destination_folder):
    # fetch all files
    try:
        for file_name in os.listdir(source_folder):
            # construct full file path
            source = os.path.join(source_folder, file_name)
            destination = os.path.join(destination_folder, file_name)
            # copy only files
            if not os.path.isdir(destination_folder):
                os.makedirs(destination_folder)
            if (file_name not in '.svn'):
                if ((os.path.isfile(source)) and not (os.path.isfile(destination))):
                    shutil.copy(source, destination)
                    print('copied {}'.format(file_name))
        print ("def copydata is Finished")
        Log.write_log("Common", "Info: def copydata is Finished")
        return True
    except:
        print ("def copydata is Failed")
        Log.write_log("Common", "Error: def copydata is Failed")
        sys.exit()
        return False 

def getregkeyvalue(regpath, regkey):
    if ('Office' in regpath):
        ret = os.popen(('reg query {}').format(regpath)).readlines()
        if (ret!= []):
            return ret
        return False
    else: 
        ret = os.popen(('reg query {} /f {}').format(regpath, regkey)).readlines()
        if ('INSTALLDIR' in regkey): #Check MDX
            if(len(ret) > 2): #if installed
                ret.sort()
                path = ret[-3].split('    ')[-1].split('\n')[0]
                ver = ret[-3].split('    ')[1].split('_')[0]
                return path, ver
            else: #not installed
                return False, False
        else: #Check Rhino Path and others
            if(len(ret) > 2): #if installed
                path = ret[-3].split('    ')[-1].split('\n')[0]
                return path
            else: #not installed
                return False
                    
def setregkeyvalue(regpath, regkey, regvalue):
    print (('reg add "%s" /v "%s" /d "%s" /f') %(regpath, regkey, regvalue))
    os.popen(('reg add "%s" /v "%s" /d "%s" /f') %(regpath, regkey, regvalue))
        
def pageupanddown(direction, times):
    """
    #UI Page up or down and time(s)
    """
    if (direction == "up"):
        type(Key.PAGE_UP)
        Mouse.wheel(WHEEL_UP, times)
    elif (direction == "down"):
        type(Key.PAGE_DOWN)
        Mouse.wheel(WHEEL_DOWN, times)
    else:
        print ("def pageupanddown gave a wrong direction which is %s" %(direction))
        Log.write_log("Common", ("Error: def pageupanddown gave a wrong direction which is %s") %(direction))
        sys.exit()
        return False
    print ("def pageupanddown is Finished")
    Log.write_log("Common", "Info: def pageupanddown is Finished")
    return True    
    
def mousemove(direction, position, offset):
    """
    #move mouse focus to specific position and offset
    """
    try:
        mouseMove(position)
        if (direction == "above"):            
            mouseMove.above(offset)
        elif (direction == "below"):
            mouseMove.below(offset)
        elif (direction == "left"):
            mouseMove.left(offset)
        elif (direction == "right"):
            mouseMove.right(offset)
        else:
            print ("def mousemove gave a wrong direction which is %s" %(direction))
            Log.write_log("Common", ("Error: def mousemove gave a wrong direction which is %s") %(direction))
            sys.exit()
            return False
        print ("def mousemove is Finished")
        Log.write_log("Common", "Info: def mousemove is Finished")
        return True
    except:
        print ("def mousemove is Failed")
        Log.write_log("Common", "Error: def mousemove is Failed")
        #sys.exit()
        return False
        
def getcurrentpath(pathname):
    """
    back to specific path
    """
    currentpath = os.path.abspath(os.getcwd()) #Get current path
    lastpath = os.path.split(currentpath)
    while (pathname != lastpath[-1]):
        lastpath = os.path.abspath(os.path.join(lastpath[0], os.path.pardir)) #back to upper path
        lastpath = os.path.split(lastpath) #Get last path name
    lastpath = os.path.join(lastpath[0], lastpath[1])
    return lastpath
    
def getcuriphostname():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)    
    return hostname, local_ip
    
def taskexist(processname):
    call = 'TASKLIST', '/FI', 'imagename eq %s' % processname
    output = subprocess.check_output(call).decode()
    last_line = output.strip().split('\r\n')[-1]
    return last_line.lower().startswith(processname.lower())
    
def SVNDownload(SVNPath, localpath):
    """
    if localpath is exists, than excute svn update; else excute svn checkout
    """
    try:
        print('SVNPath = %s\nlocalpath = %s' %(SVNPath, localpath))
        cmd = "svn ls {}".format(SVNPath)
        print (cmd)
        result = os.system(cmd)
        Log.write_log("Common", "Info: def SVNDownload_svn path check result is %d" %result)
        if (result == 0):
            if (os.path.exists(localpath)):
                cmd = "svn up {}".format(localpath)
                print (cmd)
                os.system(cmd)
            else:
                cmd = "svn co {} {}".format(SVNPath, localpath)
                print (cmd)
                os.system(cmd)
            print ("def SVNDownload is Finished")
            Log.write_log("Common", "Info: def SVNDownload is Finished")
            return True
        else:
            print ("def SVNDownload_svn path check result is Failed")
            Log.write_log("Common", "Error: def SVNDownload_svn path check result is Failed")
            sys.exit()
            #return False
    except:
        print ("def SVNDownload is Failed")
        Log.write_log("Common", "Error: def SVNDownload is Failed")
        sys.exit()
        return False

def SVNLogin(username, password):
    """
    if localpath is exists, than excute svn update; else excute svn checkout
    """
    try:
        cmd = "svn update --username {} --password {}".format(username, password)
        print (cmd)
        os.system(cmd)
        print ("def SVNDownload is Finished")
        Log.write_log("Common", "Info: def SVNDownload is Finished")
        return True
    except:
        print ("def SVNDownload is Failed")
        Log.write_log("Common", "Error: def SVNDownload is Failed")
        sys.exit()
        return False

def openfolderUI(path):
    try:
        FILEBROWSER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe')
        path = os.path.normpath(path)
        if os.path.isdir(path):
            subprocess.Popen([FILEBROWSER_PATH, path])
        elif os.path.isfile(path):
            subprocess.Popen([FILEBROWSER_PATH, '/select,', path])
        print ("def openfolderUI is Finished")
        Log.write_log("Common", "Info: def openfolderUI is Finished")
        return True
    except:
        print ("def openfolderUI is Failed")
        Log.write_log("Common", "Error: def openfolderUI is Failed")
        sys.exit()
        return False
        
def getfilepath(path, name):
    try:
        result = []
        for root, dirs, files in os.walk(path):
            for file in files:
                if name in file:
                    result.append(os.path.join(root, file))
        print ("def getfilepath is Finished")
        Log.write_log("Common", "Info: def getfilepath is Finished")
        return result
    except:
        print ("def getfilepath is Failed")
        Log.write_log("Common", "Error: def getfilepath is Failed")
        sys.exit()
        return False
    
def instaloffice(ISOpath):
    currentpath = os.getcwd()    
    exe = ISOpath + "Setup.exe"
    exe = os.path.normpath(exe)
    xml = ISOpath + "Config.xml"
    xml = os.path.normpath(xml)
    #os.chdir(ISOpath)
    print (('{} {} {}').format(exe, "/config", xml))
    os.popen(('{} {} {}').format(exe, "/config", xml))
    #os.chdir(currentpath)

def mfeMatching(path):
    try:
        self.studio = studio_in_win32
        studio = Studio("MDX_FEA", "2022")
        studio.Launch_Studio()
        dic = studio.studio.ExtractFileInfo2Dict(meshfile)
        print("dic is: {}".format(dic))

        print ("def mfeMatching is Finished")
        Log.write_log("Common", "Info: def mfeMatching is Finished")
        return True
    except:
        print ("def mfeMatching is Failed")
        Log.write_log("Common", "Error: def mfeMatching is Failed")
        sys.exit()
        return False

def getinisectionvalue(inipath, section, name):
    try:
        config = ConfigParser.ConfigParser()
        config.read(inipath)
        value = config.get(section, name)        
        print ("def getsectionresult is Finished")
        Log.write_log("Common", "Info: def getsectionresult {} is Finished".format(value))
        return value       
    except:
        print ("def getsectionresult is Failed")
        Log.write_log("Common", "Error: def getsectionresult is Failed")
        sys.exit()
        return False

    
def ENTDOWNTLOAD(username,password,SVNPath,localpath,ENTFolderList):

#svn execution
    try:
        SVNLogin(username, password)
        if (len(ENTFolderList) <> 0):
            if (ENTFolderList[0][0] == "-"):
                SVNDownload(SVNPath, localpath)
                for ENT in ENTFolderList:
                        localdownloadpath = os.path.normpath(localpath + r"\\" + ENT[1:])
                        print("Delete local path: {}".format(localdownloadpath))
                        deletepath(localdownloadpath)
            else:
                for ENT in ENTFolderList:
                    SVNdownloadpath = SVNPath + r"/" + ENT
                    localdownloadpath = os.path.normpath(localpath + r"\\" + ENT)
                    SVNDownload(SVNdownloadpath, localdownloadpath)
        else:
               SVNDownload(SVNPath, localpath)
               print ("Info: SVN download is Finished")
    except:
        print ("def ENTDOWNTLOAD is Failed")
        Log.write_log("Common", "Error: def ENTDOWNTLOAD is Failed")
        sys.exit()
        return False

def dateevenodd():
    try:
        now = datetime.now()
        day = int(now.strftime("%d"))
        mod = day % 2
        #print('day = %s\nmod = %d' %(day, mod))
        print ("def dateevenodd is Finished")
        Log.write_log("Common", "Info: def dateevenodd {} is Finished".format(mod))
        return mod       
    except:
        print ("def dateevenodd is Failed")
        Log.write_log("Common", "Error: def dateevenodd is Failed")
        sys.exit()
        return False