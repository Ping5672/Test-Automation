import os, sys
sikuliShareAppPath = r"..\..\sikuli_Share"
if os.path.isdir(sikuliShareAppPath):
    cwd = r"..\.."
else:
    cwd = os.getcwd()
sikuliShareAppPath = cwd + r"\sikuli_Share"
sys.path.append(sikuliShareAppPath)

import ArgumentSetup as ArgS
import Studio
import CM
import Common
import log_record as Log

StudioAppPath = ArgS.StudioAppPath
CMAppPath = ArgS.CMAppPath
CommonAppPath = ArgS.CommonAppPath

try:
    hostname, local_ip = Common.getcuriphostname()
    #Install Moldex3D
    if (len(sys.argv)==2):
        setuppath = sys.argv[1]
        lastpath = os.path.split(setuppath)[1]
        if (lastpath <> "Setup_cmd.exe"):
            if ("Build" in lastpath):
                if os.path.isdir(setuppath + r"\Moldex3D"):
                    setuppath = setuppath + r"\Moldex3D"
            for path, file_dir, files in os.walk(setuppath):
                for file_name in files:
                    setuptmp = os.path.join(path, file_name)
                    if ("Setup_cmd.exe" in setuptmp):
                        setuppath = setuptmp
        RhinoPath = Common.getregkeyvalue(r"HKEY_LOCAL_MACHINE\SOFTWARE\McNeel\Rhinoceros\7.0\Install", "ExePath")
        if ((RhinoPath == False)): #Rhino is not installed
            inipath = cwd + r"\sikuli_Share\CaseReference\AutoInstall(2022)_WRhino.ini"
        else: #Rhino is installed
            inipath = cwd + r"\sikuli_Share\CaseReference\AutoInstall(2022)_WoRhino.ini"
        print(" ""\"{}""\" /i ""\"{}""\" /HideFinishDialog").format(setuppath, inipath)
        fo = open("install.bat", "w") #open bat file with write
        print ("file name is: %s" %fo.name)
        str = (" ""\"{}""\" /i ""\"{}""\" /HideFinishDialog").format(setuppath, inipath) 
        print ("str is: %s" %str)
        fo.write(str) #write bat file
        fo.close() #close bat file
        os.system(fo.name) #execute bat file
        print ("Install is Finished")
        Log.write_log("Initial", "Info: Moldex3D Install is Finished")
    #Arguments Setting
    MainInstallPath, ver = Common.getregkeyvalue(r"HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\CoreTechSystem\MDX_ParallelComputing", "INSTALLDIR")
    WorkingFolder = Common.getregkeyvalue(r"HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\CoreTechSystem\MDX_ParallelComputing", "WorkingFolder")
    StudioPath = MainInstallPath + r"\Bin\MDXStudio.exe"
    CMPath = MainInstallPath + r"\Bin\MDXComputingManager" + ver + ".exe"
    destination_folder = r"C:\ProgramData\CoreTechSystem\Moldex3D " + ver + "\\"
    Bank_Folder = r"C:\Users\Administrator\AppData\Roaming\CoreTechSystem\Moldex3D " + ver + r"\Bank"
    Material_Folder = r"C:\Users\Administrator\AppData\Roaming\CoreTechSystem\Moldex3D " + ver + r"\Material"
    #delete specific path
    Common.deletepath(destination_folder)
    Common.deletepath(Bank_Folder)
    Common.deletepath(Material_Folder)
    print ("Delete specific path is Finished")
    Log.write_log("Initial", "Info: Delete specific path is Finished")
    mod = Common.dateevenodd()
    #Open Studio UI
    Studio.OpenApp(StudioPath, StudioAppPath + r"\Studio_UI.png")
    print ("Open Studio is Finished")
    Log.write_log("Initial", "Info: Open Studio is Finished")
    sleep(3)
    #Open Preference UI
    Studio.TaskNumberSetting("4", StudioAppPath) 
    fileunit = {'offsetx':0, 'offsety':-15}
    summary = {'offsetx':-144}
    Studio.Click_IconEx(StudioAppPath + r"\Studio_Prefernce_FileUnitandNumber.png", **fileunit)
    if exists(Pattern(StudioAppPath + r"\Studio_Prefernce_ShowSummaryCheck.png").similar(0.98), 3):
        Studio.Click_IconEx(StudioAppPath + r"\Studio_Prefernce_ShowSummary.png", **summary)
    Studio.Click_Icon(StudioAppPath, r"\Studio_Preference_Mesh.png", 0)
    Studio.Click_Icon(StudioAppPath, r"\Studio_Prefernce_eDesign.png", 0)
    if exists(Pattern(StudioAppPath + r"\Studio_Preference_GenerateMB.png").similar(0.98), 3):
        Studio.Click_Icon(StudioAppPath, r"\Studio_Preference_CreateMBAndCooling.png", -10)
    Studio.Click_Icon(StudioAppPath, r"\Studio_Prefernce_Solid.png", 0)
    if exists(Pattern(StudioAppPath + r"\Studio_Preference_GenerateMB.png").similar(0.98), 3):
        Studio.Click_Icon(StudioAppPath, r"\Studio_Preference_CreateMBAndCooling.png", -10)
    click(StudioAppPath + r"\Btn_OK.png")
    Log.write_log("Initial", "Info: Studio Setting is Finished")
    #Close Studio UI
    Studio.CloseApp(StudioPath)
    Log.write_log("Initial", "Info: Close Studio is Finished")
    #Open CM UI
    CM.OpenApp(CMPath, CMAppPath + r"\CM_UI.png")
    print ("Open Computing Manager is Finished")   
    Log.write_log("Initial", "Info: Open Computing Manager is Finished")    
    #Add Server Info Setting
    print('hostname = %s\nlocal_ip = %s' %(hostname, local_ip))
    mod = Common.dateevenodd()
    if (mod == 0):
        CM.AddServer(CMAppPath, hostname)
    else:
        CM.AddServer(CMAppPath, local_ip)
    #Server Connect
    CM.connectserver("RC", CMAppPath)
    print ("Computing Manager Add Server Setting is Finished")   
    Log.write_log("Initial", "Info: Computing Manager Add Server Setting is Finished")    
    #Check Auto Download
    CM.Click_Icon(CMAppPath + r"\CM_Option.png")
    wait(CMAppPath + r"\Options.png", 10)
    mouseMove(CMAppPath + r"\Options.png")
    if exists(Pattern(CMAppPath + r"\Options_Uncheck.png").similar(0.90), 1):
        click(Pattern(CMAppPath + r"\Options_Uncheck.png").targetOffset(1,-25))
    if exists(Pattern(CMAppPath + r"\Options_Select_Top.png").similar(0.80), 1):
        click(Pattern(CMAppPath + r"\Options_Select_Top.png").targetOffset(1,12))
    CM.Click_Icon(CMAppPath + r"\Btn_OK.png")
    print ("Computing Manager Option Setting is Finished")
    Log.write_log("Initial", "Info: Computing Manager Option Setting is Finished")
    #Close CM UI
    CM.CloseApp(CMPath)
    Log.write_log("Initial", "Info: Close Computing Manager is Finished")
    print ("Initial is Finished")
    Log.write_log("Initial", "Info: Initial is Finished")
except:
    print ("Initial is Failed")
    Log.write_log("Initial", "Error: Initial is Failed")
Log.write_log2("Initial", "Summary")
