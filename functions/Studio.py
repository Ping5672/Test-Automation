from sikuli import *
import sys, os
import codecs

LogAppPath = r"..\sikuli_Share\Common.sikuli"

sys.path.append(LogAppPath)

import log_record as Log

def OpenApp(AppPath, UIPic):
    #Open Studio UI
    try:
        openApp(AppPath)
        if exists(UIPic, 60):
            print("%s UI is opened Finished") %(AppPath)
            Log.write_log("Studio", ("Info: %s UI is opened Finished") %(AppPath))
            return True
    except:
        print("%s UI is opened Failed") %(AppPath)
        Log.write_log("Studio", ("Error: %s UI is opened Failed") %(AppPath))
        sys.exit()
        return False
        
def CloseApp(AppPath):
    #Close Studio UI
    try:
        closeApp(AppPath)
        print("%s UI is closed Finished") %(AppPath)
        Log.write_log("Studio", ("Info: %s UI is closed Finished") %(AppPath))
        return True
    except:
        print("%s UI is closed Failed") %(AppPath)
        Log.write_log("Studio", ("Error: %s UI is closed Failed") %(AppPath))
        sys.exit()
        return False   

def NewProject(sName, StudioAppPath):
    #Create a New Project
    #Argument: Project Name
    try:
        wait(StudioAppPath + r"\Studio_NewProject.png", 40)
        click(StudioAppPath + r"\Studio_NewProject.png")
        wait(StudioAppPath + r"\Studio_SpecifyFileName.png", 10)
        x = Pattern(StudioAppPath + r"\Studio_Project_Name_Defualt.png").similar(0.90).targetOffset(15,0)
        y = Pattern(StudioAppPath + r"\Studio_Project_name_Empty.png").similar(0.95).targetOffset(15,0)
        i=0
        while (exists(x, 1)  or exists(y, 1)) and i<3:
            click((x)or(y))
            type("a",Key.CTRL)
            paste(sName)
            mouseMove(50,0)
            wait(1)            
            i += 1
        click(StudioAppPath + r"\Btn_OK.png")
        if exists(StudioAppPath + r"\Studio_ProjectReplace.png",3):
            x = find(StudioAppPath + r"\Btn_Yes.png")
            click(x)
        wait(StudioAppPath + r"\Studio_NewRun.png",10)
        print("def NewProject is Finished")
        Log.write_log("Studio", "Info: def NewProject is Finished")
        return True
    except:
        print("def NewProject is Failed")
        Log.write_log("Studio", "Error: def NewProject is Failed")
        sys.exit()
        return False

def OpenProject(ProjectPath, StudioAppPath):
    try:
        if exists(StudioAppPath + r"\Studio_OpenProject.png", 10):
            click(StudioAppPath + r"\Studio_OpenProject.png")
            if exists(StudioAppPath + r"\Studio_FileName.png", 10):
                click(StudioAppPath + r"\Studio_FileName.png")
                paste(ProjectPath)
                click(StudioAppPath + r"\File_Open.png")
                if exists(StudioAppPath + r"\Studio_Upgrade.png", 5):
                    x = find(StudioAppPath + r"\Btn_OK.png")
                    click(x)
                while exists(StudioAppPath + r"\Studio_ReadingFile.png"):                    
                    print("Project is opening...")
                    sleep(6)
        print("def OpenProject is Finished")
        Log.write_log("Studio", "Info: def OpenProject is Finished")
        return True
    except:
        print("def OpenProject is Failed")
        Log.write_log("Studio", "Error: def OpenProject is Failed")
        sys.exit()
        return False

def Home_MoldingType_New(Pic, StudioAppPath):
    """
    Select Studio Run Molding Type
    Argument: Molding Type Position
    offsetx: 0
    offsety: -105: Injection Molding; -85: PIM; -70: FIM; -55: CFM; -30: ICM; -10: CM; 10: GAIM; 27: WAIM; 47: CoIM; 65: BiIM; 85: RTM; 105: Enpsulation
    """
    try:
        wait(3)        
        x = exists(Pattern(StudioAppPath + r"\Studio_Moldex3DSolution.png").targetOffset(-20,-20))
        click(x)
        #wait(StudioAppPath + r"\Studio_MoldingType_All.png", 3)
        wait(Pattern(StudioAppPath + "\\" + Pic + ".png").similar(0.90), 5)
        click(Pattern(StudioAppPath + "\\" + Pic + ".png").similar(0.90))
        print("def Home_MoldingType_New is Finished")
        Log.write_log("Studio", "Info: def Home_MoldingType_New is Finished")
        return True        
    except:
        print("def Home_MoldingType_New is Failed")
        Log.write_log("Studio", "Error: def Home_MoldingType_New is Failed")
        sys.exit()
        return False

def Home_MoldingType(offsetx, offsety, StudioAppPath):
    """
    Select Studio Run Molding Type
    Argument: Molding Type Position
    offsetx: 0
    offsety: -105: Injection Molding; -85: PIM; -70: FIM; -55: CFM; -30: ICM; -10: CM; 10: GAIM; 27: WAIM; 47: CoIM; 65: BiIM; 85: RTM; 105: Enpsulation
    """
    try:
        wait(3)        
        x = exists(Pattern(StudioAppPath + r"\Studio_Moldex3DSolution.png").targetOffset(-20,-20))
        click(x)
        wait(StudioAppPath + r"\Studio_MoldingType_All.png", 3)
        click(Pattern(StudioAppPath + r"\Studio_MoldingType_All.png").targetOffset(offsetx, offsety))
        print("def Home_MoldingType is Finished")
        Log.write_log("Studio", "Info: def Home_MoldingType is Finished")
        return True        
    except:
        print("def Home_MoldingType is Failed")
        Log.write_log("Studio", "Error: def Home_MoldingType is Failed")
        sys.exit()
        return False

def MeshType(sType, StudioAppPath):
    #Select Studio Run Mesh Type
    #Argument: Mesh Type
    try:
        if ((sType != "Solid") and (sType != "eDesign") and (sType != "Shell")):
            print ("Give wrong sType Name %s" %(sType))
            Log.write_log("Studio", ("Error: def MeshType is Failed, Give wrong sType Name %s") %(sType))
            sys.exit()       
            return False
        x = (StudioAppPath + r"\Studio_MeshType_" + sType +".png")
        if (exists(x)):
            pass
        else:
            if(exists(StudioAppPath + r"\Studio_MeshType_eDesign.png",1)):
                Y = find(Pattern(StudioAppPath + r"\Studio_MeshType_eDesign.png").targetOffset(-2,26))
            if(exists(StudioAppPath + r"\Studio_MeshType_Solid.png",1)):
                Y = find(Pattern(StudioAppPath + r"\Studio_MeshType_Solid.png").targetOffset(-2,36))
            if(exists(StudioAppPath + r"\Studio_MeshType_Shell.png",1)):
                Y = find(Pattern(StudioAppPath + r"\Studio_MeshType_Shell.png").targetOffset(-3,37))
            click(Y)
            click(Pattern(StudioAppPath + r"\Studio_MeshType_" + sType + "Check.png").similar(0.9))
            
            if exists(StudioAppPath + r"\Studio_ChangeModel.png",5):
                a = find(StudioAppPath +r"\Btn_Continue.png")
                click(a) 
            if exists(StudioAppPath + r"\Studio_delete_existing_mesh.png",5):
                b = find(StudioAppPath +r"\Btn_OK.png")
                click(b) 
            wait(x,30)
                  
        print("def MeshType is Finished")
        Log.write_log("Studio", "Info: def MeshType is Finished")
        return True        
    except:
        print("def MeshType is Failed")
        Log.write_log("Studio", "Error: def MeshType is Failed")
        sys.exit()
        return False

def Home_Model(sMethod, StudioAppPath):
    #Select Geometry Import Method
    #Argument: Model Import Method
    try:
        wait(2)
        if (sMethod == "Model"):
            doubleClick(StudioAppPath + r"\Studio_Import_Model.png")
        else:
            x = find(Pattern(StudioAppPath + r"\Studio_Tab_Model.png").targetOffset(0,-20))
            click(x)
            wait(StudioAppPath + r"\Btn_ImportGeometrySelection.png",3)
            if sMethod == "ImportGeometry":
                click(StudioAppPath + r"\Btn_ImportGeometry.png")
            elif sMethod == "ImportGeometryAutoHeal":
                click(StudioAppPath + r"\Btn_ImportGeometryAutoHeal.png")
            elif sMethod == "SwapGeometry":
                click(StudioAppPath + r"\Btn_SwapGeometry.png")
            elif sMethod == "ImportMesh":
                click(StudioAppPath + r"\Btn_ImportMesh.png")
        print("def Home_Model is Finished")
        Log.write_log("Studio", "Info: def Home_Model is Finished")
        return True        
    except:
        print("def Home_Model is Failed")
        Log.write_log("Studio", "Error: def Home_Model is Failed")
        sys.exit()
        return False    

def ImportGeometry(sPath, StudioAppPath):
    #Argument: Impot Geometry File (*.mdg)
    try:
        i=0
        wait(StudioAppPath + r"\Studio_Open.png", 3)
        x = Pattern(StudioAppPath + r"\Studio_Filename_empty_2.png").similar(0.9).targetOffset(30,0)
        while (exists(x, 1) <> None) and i<3:
            click(x)
            paste(sPath)
            mouseMove(0,50)
            wait(1)
            i += 1
        x = find(StudioAppPath + r"\Btn_Open.png")
        #hover(x)
        click(x)
        if (".stl" in sPath):
            Wait_Dialog(StudioAppPath, r"\Studio_Unit_select.png")
            x = find(StudioAppPath + r"\Btn_OK.png")
            click(x)
        wait(StudioAppPath + r"\Studio_CmdUpdateRun.png",60)
        print("def ImportGeometry is Finished")
        Log.write_log("Studio", "Info: def ImportGeometry is Finished")
        return True
    except:
        print("def ImportGeometry is Failed")
        Log.write_log("Studio", "Error: def ImportGeometry is Failed")
        sys.exit()
        return False

def SwitchTab(NoSelectTabPic, SelectionTabPic):
    """
    Switch from Current Tab to Next Tab
    Argument
    NoSelectTabPic: The Tab Not Select UI
    SelectionTabPic: The Tab has been selected UI
    """
    try:
        if find(NoSelectTabPic):
            click(NoSelectTabPic)
            wait(SelectionTabPic, 5)
        print ("def SwitchTab is Finished")
        Log.write_log("Studio", "Info: def SwitchTab is Finished")
        return True    
    except:
        print ("def SwitchTab is Failed")
        Log.write_log("Studio", "Error: def SwitchTab is Failed")
        sys.exit()
        return False
    
def Meshing_Generate(StudioAppPath,*return_preprocess):
    #Click Btn Generat and select does not keep solid mesh
    try:
        x = find(StudioAppPath + r"\Studio_Generate.png")
        click(x)
        wait(1)
        if exists(StudioAppPath + r"\Studio_Moldex3DStudio.png", 5):
            x = find(StudioAppPath + r"\Btn_No.png") #for not keep solid mesh
            click(x)
        if len(return_preprocess)!=0:
            if exists(StudioAppPath + r"\Studio_ChangeModel.png",5):
                mouseMove(0, 20)
                a = find(StudioAppPath +r"\Btn_Copy_Run.png")
                click(a)
                if 'Solid' in return_preprocess:
                    Wait_Dialog(StudioAppPath, r"\Studio_Mesh_Process.png") 
                    
        print ("def Meshing_Generate is Finished")
        Log.write_log("Studio", "Info: def Meshing_Generate is Finished")
        return True
    except:
            print ("def Meshing_Generate is Failed")
            Log.write_log("Studio", "Error: def Meshing_Generate is Failed")
            sys.exit()
            return False    

def Meshing_GenerateeDesign(StudioAppPath):
    try:
        i = 0
        while not exists(Pattern(StudioAppPath + r"\Btn_Check.png").similar(0.90), 30) and i < 10:
            i += 1
        click(StudioAppPath + r"\Btn_Check.png")
        x = (StudioAppPath + r"\Btn_Yes.png")
        if exists(x, 10):
            click(x)
        print ("def Meshing_GenerateeDesign is Finished")
        Log.write_log("Studio", "Info: def Meshing_GenerateeDesign is Finished")
        return True                       
    except:
        print ("def Meshing_GenerateeDesign is Failed")
        Log.write_log("Studio", "Error: def Meshing_GenerateeDesign is Failed")
        sys.exit()
        return False

def Meshing_GenerateBLM(sItem, StudioAppPath):
    """
    Click Generate
    Argument
    "Runner" / "Part": for Fast Cool
    "None": for Solid Cool 
    """
    try:
        i = 0
        while not exists(StudioAppPath + r"\Btn_Generate.png", 30) and i < 10:
            i += 1
        if ((sItem == "Runner") or (sItem == "Part") or (sItem == "CompressionZone")):
            if (sItem == "Runner"):
                mouseMove(StudioAppPath + r"\Studio_Runner.png")
                x= find(Pattern(StudioAppPath + r"\Studio_Runner.png").targetOffset(-30,0))
            elif (sItem == "Part"): #for Sample CoIM: Head set
                mouseMove(StudioAppPath + r"\Studio_Part2.png")
                x= find(Pattern(StudioAppPath + r"\Studio_Part2.png").similar(0.90).targetOffset(-50,45))
            elif (sItem == "CompressionZone"):
                mouseMove(StudioAppPath + r"\Studio_CompressionZone.png")
                x= find(Pattern(StudioAppPath + r"\Studio_CompressionZone.png").similar(0.90).targetOffset(-40,0))
            else:
                Log.write_log("Studio", "Error: not found any attribute")
                sys.exit()
                return False
            click(x)
            wait(1)
        x = find(Pattern(StudioAppPath + r"\Btn_Generate.png").targetOffset(0,15))
        click(x)
        while (exists(Pattern(StudioAppPath + r"\Studio_WaitForTheProcessingJob.png").similar(0.90),3)): #122195
            click(StudioAppPath + r"\Btn_Close.png")
            click(x)
        if (exists(Pattern(StudioAppPath + r"\Studio_unusual_interference.png").similar(0.8),5)):
            click(StudioAppPath + r"\Btn_Yes.png")
        
        print ("def Meshing_GenerateBLM is Finished")
        Log.write_log("Studio", "Info: def Meshing_GenerateBLM is Finished")
        return True
    except:
        print ("def Meshing_GenerateBLM is Failed")
        Log.write_log("Studio", "Error: def Meshing_GenerateBLM is Failed")
        sys.exit()
        return False

def Click_Check_Button(StudioAppPath):
   """
   #Click Check Button
   """
   try:
       i = 0
       while not exists(StudioAppPath + r"\Studio_FinalCheck.png", 10) and i < 20:
           i += 1
       click(StudioAppPath + r"\Btn_Check.png")       
       print ("def Click_Check_Button is Finished")
       Log.write_log("Studio", "Info: def Click_Check_Button is Finished")
       return True                       
   except:
       print ("def Click_Check_Button is Failed")
       Log.write_log("Studio", "Error: def Click_Check_Button is Failed")
       sys.exit()
       return False

def TaskNumberSetting(sNumber, StudioAppPath):
    #Task Number Setting
    #Argument: give a number for setting task number
    try:
        if exists(StudioAppPath + r"\Btn_Preference.png", 10):
                  click(StudioAppPath + r"\Btn_Preference.png")
        if exists(StudioAppPath + r"\Studio_Preference_General.png", 10):
                  click(StudioAppPath + r"\Studio_Preference_General.png")
        if exists(StudioAppPath + r"\Studio_Preference_Computation.png", 10):
                  click(StudioAppPath + r"\Studio_Preference_Computation.png")
        if exists(StudioAppPath + r"\Studio_TaskNo.png"):
                  click(Pattern(StudioAppPath + r"\Studio_TaskNo.png").targetOffset(140,0), 10)
                  type("a",Key.CTRL)
                  type(sNumber)
                  #click(StudioAppPath + r"\Btn_OK.png")
        print ("def TaskNumberSetting is Finished")
        Log.write_log("Studio", "Info: def TaskNumberSetting is Finished")
        return True
    except:
        print ("def TaskNumberSetting is Failed")
        Log.write_log("Studio", "Error: def TaskNumberSetting is Failed")
        sys.exit()
        return False

def AnalysisSetting(Analyzelist, StudioAppPath):
    """
    Setting Run Analysis
    Argument: give a list
    1. All the setting picture
    2. 2nd to last: single Analyze picture(s)
    """
    try:
        if exists(Pattern(StudioAppPath + r"\Btn_Analysis2.png").similar(0.98), 10):
            click(Pattern(StudioAppPath + r"\Btn_Analysis2.png").targetOffset(0,30))
        if exists (Pattern(Analyzelist[0]).similar(0.93), 2):
            click(Pattern(Analyzelist[0]).similar(0.93))
        else:
            click(StudioAppPath + r"\Analysis_Customize.png")
            click(StudioAppPath + r"\Btn_Customize2.png")
            AvailableAnalysis = os.path.join(StudioAppPath, r"CMX_AvailableAnalysis.png")
            count = 0
            print(111)
            for counter in Analyzelist:
                print(112)
                if count == 0: #Analysis Full Name
                    print(113)
                    pass
                    count += 1
                else:
                    print(114)
                    i = 0
                    while not exists(counter,1) and i<5: #If cannot see the Analysis Item in Customize List
                        print(115)
                        mouseMove(AvailableAnalysis)
                        Mouse.wheel(WHEEL_DOWN, 1)
                        i+=1
                    if (('Filling' not in counter) and ('Warpage' not in counter) and ('CoolingCycle2' not in counter)):
                        print(116)
                        target = find(os.path.join(StudioAppPath, r"CMX_AvailableAnalysis2.png")).below().find(Pattern(counter).similar(0.90))
                    else:
                        print(117)
                        target = find(Pattern(counter).similar(0.90))
                    print(118)
                    click(target)
                    click(StudioAppPath + r"\Btn_AddAnalysis2.png") #Add to the list
                    if count == 1:
                        click(Pattern(StudioAppPath + r"\Analysis_Selectedanalysis.png").targetOffset(0,20))
                        click(StudioAppPath + r"\Btn_Delete.png")
                    if exists(Pattern(StudioAppPath + r"\analysis_bottom.png").exact(),1):
                        mouseMove(StudioAppPath + r"\analysis_bar.png")
                        Mouse.wheel(WHEEL_UP,3)
                    count += 1
            click(StudioAppPath + r"\Btn_save.png")
        print ("def AnalysisSetting %s is Finished" %(Analyzelist[0]))
        Log.write_log("Studio", ("Info: def AnalysisSetting %s is Finished") %(Analyzelist[0]))
        return True
    except:
        print ("def AnalysisSetting %s is Failed" %(Analyzelist[0]))
        Log.write_log("Studio", ("Error: def AnalysisSetting %s is Failed") %(Analyzelist[0]))
        sys.exit()
        return False

def Click_IconEx(StudioAppPath, **sikuliarg):
    """
    StudioAppPath = StudioAppPath + r"\Studio_Prefernce_FileUnitandNumber.png"
    sikuliarg = {'similar':0.9, 'offsetx':10, 'offsety': 5}
    """
    try:
        if sikuliarg:
            if 'similar' in sikuliarg:
                similar = float(sikuliarg['similar'])
            else:
                similar = float(0.7)
            if 'offsetx' in sikuliarg:
                offsetx = int(sikuliarg['offsetx'])
            else:
                offsetx = int(0)
            if 'offsety' in sikuliarg:
                offsety = int(sikuliarg['offsety'])
            else:
                offsety = int(0)
            click(Pattern(StudioAppPath).similar(similar).targetOffset(offsetx,offsety))
        else:
            click(Pattern(StudioAppPath).similar(0.9))
        print ("def Click_IconEx is Finished")
        Log.write_log("Studio", ("Info: def Click_IconEx is Finished"))
        return True
    except:
        print ("def Click_IconEx is Failed")
        Log.write_log("Studio", ("Error: def Click_IconEx is Failed"))
        sys.exit()
        return False

def Click_Icon(StudioAppPath, Modelpic, offsetx):
    """
    #Click Icon
    #offsetx: Model_Object -> -40; BC -> -82;  Part -> -30; CR -> -55; MI -> -45; Btn_Fit_To_Window -> -24
    #offsetx: Model_Tree -> 0; Btn_Angle_Perspectived -> 40; Btn_Angle_Top -> 20; Btn_Angle_Bottom -> 30; Btn_Angle_Right -> 20; Btn_Angle_Left -> 20; Btn_Angle_Front -> 20; Btn_Angle_Back -> 20
    """
    try:
        Anglelist = [r"\Btn_Angle_Perspective_Seletected.png", r"\Btn_Angle_Top_Seletected.png", r"\Btn_Angle_Bottom_Seletected.png", r"\Btn_Angle_Right_Seletected.png", r"\Btn_Angle_Left_Seletected.png", r"\Btn_Angle_Front_Seletected.png", r"\Btn_Angle_Back_Seletected.png"]
        ShowMoldlist = [r"\Btn_ShowModeSelected_FeatureMeshShaded2.png", r"\Btn_ShowModeSelected_MeshShaded2.png", r"\Btn_ShowModeSelected_FeatureShaded2.png", r"\Btn_ShowModeSelected_Shaded2.png", r"\Btn_ShowModeSelected_FeatureMesh2.png", r"\Btn_ShowModeSelected_Mesh2.png", r"\Btn_ShowModeSelected_Feature2.png"]
        if ((Modelpic not in Anglelist) and (Modelpic not in ShowMoldlist)): #if not change Angle / Show Mode
            if ("Studio_Tree_BC_MI" in Modelpic or "Studio_Tree_BC_EM" in Modelpic):
                i = 1
                if i < 5:
                    while not exists(StudioAppPath + Modelpic, 2): #whilenot found the Icon
                        Mouse.wheel(WHEEL_DOWN, 3)
                        i += 1
                x = findAll(Pattern(StudioAppPath + Modelpic).similar(0.95))
                for i in x:
                    mouseMove(i)
                    mouseMove(offsetx, 0)
                    mouseDown(Button.LEFT)
                    mouseUp(Button.LEFT)
            else:
                i = 1
                if i < 5:
                    while not exists(Pattern(StudioAppPath + Modelpic).similar(0.85), 5): #whilenot found the Icon
                        mouseMove(StudioAppPath + r"\Studio_ScrollBar_Top.png")
                        Mouse.wheel(WHEEL_DOWN, 3)
                        i += 1
                    click(Pattern(StudioAppPath + Modelpic).similar(0.85).targetOffset(offsetx,0)) #click Icon
                else:
                    print ("{} is not existed".format(Modelpic))
                    Log.write_log("Studio", ("Error: {} is not existed").format(Modelpic))
                    sys.exit()
                    return False
        elif Modelpic in ShowMoldlist: #if wanna setting Show Mode
            for Show in ShowMoldlist:
                if exists(Pattern(StudioAppPath + Show).similar(0.98), 1): #if found specific Show Mode
                    """ #98560
                    if (Modelpic == Show): #if angle is the same as Feature Line Shaded
                        print "Show Model is %s" %(Show)
                        return True
                    else:
                        offsetx = 20
                    """
                    offsetx = 20
                    while not exists(StudioAppPath + r"\Btn_ShowMode_Model.png"): #if Show Model is not found
                        click(Pattern(StudioAppPath + Show).similar(0.90).targetOffset(offsetx,0)) #click Show again
                    click(Pattern(StudioAppPath + r"\Btn_ShowMode_Model.png").similar(0.90).targetOffset(0,-23))#select Feature Line with Saded Faces
                    print ("Setting Show Model is Finished")
                    Log.write_log("Studio", "Setting Show Model is Finished")
                    return True
        elif Modelpic in Anglelist: #if wanna setting Angle
            for Angle in Anglelist:
                if exists(Pattern(StudioAppPath + Angle).similar(0.98), 1): #if found specific angle
                    if (Modelpic == Angle): #if angle is the same as Perspective
                        pass
                    else:
                        if (Angle == r"\Btn_Angle_Perspective_Seletected.png"):
                            offsetx = 40
                        elif (Angle == r"\Btn_Angle_Bottom_Seletected.png"):
                            offsetx = 30
                        else:
                            offsetx = 20
                        while not exists(StudioAppPath + r"\Btn_Angle_Model.png"): #if Angle Model is not found
                            click(Pattern(StudioAppPath + Angle).similar(0.80).targetOffset(offsetx,0)) #click Agnle again
                        element = Anglelist.index(Modelpic)
                        offsety = -80 + (20 * element)
                        click(Pattern(StudioAppPath + r"\Btn_Angle_Model.png").similar(0.85).targetOffset(0,offsety))#select Angle Perspective
                    print ("Setting Angle {} is Finished".format(Angle))
                    Log.write_log("Studio", "Info: Setting Angle {} is Finished".format(Angle))
                    return True
                else: #if NOT found specific angle
                    pass                                             
        else: #if NOT found all of the angle
            print ("%s is not existed" %(Modelpic))
            Log.write_log("Studio", ("Error: %s is not existed") %(Modelpic))
            sys.exit()
            return False
        print ("def Click_Icon %s is Finished" %(Modelpic))
        Log.write_log("Studio", ("Info: def Click_Icon %s is Finished") %(Modelpic))
        return True
    except:
        print ("def Click_Icon %s is Failed" %(Modelpic))
        Log.write_log("Studio", ("Error: def Click_Icon %s is Failed") %(Modelpic))
        sys.exit()
        return False

def ClickRun(offsety, StudioAppPath):
    """
    Click Run Method
    Argument
    offsetx: keep 0
    offsety -30: Run; -5: Computing Manager; 5: Create BJS; 30: Submit Batch Run
    """
    try:
        wait(2)
        if exists(Pattern(StudioAppPath + r"\Home_Simulation.png").similar(0.98), 30):
            click(Pattern(StudioAppPath + r"\Home_Simulation.png").targetOffset(0,-10))
        if exists(StudioAppPath + r"\Home_AnalysisList.png", 3):
                  click(Pattern(StudioAppPath + r"\Home_AnalysisList.png").targetOffset(0, offsety))
        if exists(StudioAppPath + r"\Studio_MCM_CurrentAnalysis.png", 2):
                  click(StudioAppPath + r"\Btn_OK.png")
        print ("def ClickRun is Finished")
        Log.write_log("Studio", "Info: def ClickRun is Finished")
        return True
    except:
        print ("def ClickRun is Failed")
        Log.write_log("Studio", "Error: def ClickRun is Failed")
        sys.exit()
        return False

def Wait_Dialog(StudioAppPath, MeshPic):
    """
    #Wait Specific Dialog
    #MeshPic: eDesign -> r"\Log_Generate_Solid_Mesh_Done.png"; Solid Cool -> r"\Studio_FinalCheck.png"; Fast Cool -> r"\Studio_Runner_Check.png"
    """
    try:
        i = 0
        while not exists(Pattern(StudioAppPath + MeshPic).similar(0.90), 30) and i < 30:
            wait(3)
            i += 1
        print ("def Wait_Dialog is Finished")
        Log.write_log("Studio", "Info: def Wait_Dialog is Finished")
        return True                       
    except:
        print ("def Wait_Dialog is Failed")
        Log.write_log("Studio", "Error: def Wait_Dialog is Failed")
        sys.exit()
        return False

def ChangeRunID(StudioAppPath, RunNo):
    try:
        if (len(RunNo) == 1):
            RunNo = RunNo.zfill(2)
        RunID = Pattern(StudioAppPath + r"\\" + RunNo + ".png").similar(0.95)
        click(RunID)
        while exists(StudioAppPath + r"\Studio_ReadingFile.png", 5):
            print ("{} is opening...").format(RunID)
            sleep(3)
        print ("def ChangeRunID {} is Finished").format(RunNo)
        Log.write_log("Studio", "Info: def ChangeRunID {} is Finished".format(RunNo))
        return True
    except:
        print ("def ChangeRunID {} is Failed").format(RunNo)
        Log.write_log("Studio", "Error: def ChangeRunID {} is Failed".format(RunNo))
        sys.exit()
        return False

def CountRunID(StudioAppPath):
    try:
        RunNos = ["Run01", "Run02", "Run03", "Run04", "Run05", "Run06"]
        Run = []
        for RunNo in RunNos:        
            RunID = Pattern(StudioAppPath + "\\" + RunNo + ".png").similar(0.95)
            if exists(RunID):
                Run.append(RunNo)    
        print ("def CountRunID is Finished")
        Log.write_log("Studio", "Info: def CountRunID is Finished")
        return Run
    except:
        print ("def CountRunID is Failed")
        Log.write_log("Studio", "Error: def CountRunID is Failed")
        sys.exit()
        return False

def Final_Check(StudioAppPath):
    """
    #Click Final Check
    """
    try:
        if exists(StudioAppPath + r"\Studio_FinalCheck2.png"):
            click(StudioAppPath + r"\Studio_FinalCheck2.png")
        
        if exists(Pattern(StudioAppPath + r"\Studio_setpartingdirection.png").similar(0.85), 5):
            click(StudioAppPath + r"\Btn_Check.png")                                 
        elif exists(Pattern(StudioAppPath + r"\Studio_MoldbaseWizard.png").similar(0.85), 8):
            click(Pattern(StudioAppPath + r"\Btn_Check.png").similar(0.90).targetOffset(-33,0))
            if exists(StudioAppPath + r"\Btn_Yes.png", 8):
                click(StudioAppPath + r"\Btn_Yes.png")
                if exists(StudioAppPath + r"\Btn_Close.png", 8):
                    click(StudioAppPath + r"\Btn_Close.png")
        
        i = 0
        while not exists(StudioAppPath + r"\Dialog_FInal_Check.png",30) and i <20:
            if exists(StudioAppPath + r"\Btn_Yes.png", 1):
                click(StudioAppPath + r"\Btn_Yes.png")
            i += 1
        if exists(StudioAppPath + r"\Btn_OK.png", 10):
            click(StudioAppPath + r"\Btn_OK.png")      
        print ("def Final_Check is Finished")
        Log.write_log("Studio", "Info: def Final_Check is Finished")
        return True                       
    except:
        print ("def Final_Check is Failed")
        Log.write_log("Studio", "Error: def Final_Check is Failed")
        sys.exit()
        return False

def Tab_Seleted(StudioAppPath, blue, white):
    try:
        if not exists(StudioAppPath + white):
            click(StudioAppPath + blue)
        print ("def Tab_Seleted is Finished")
        Log.write_log("Studio", "Info: def Tabg_Seleted is Finished")
        return True
    except:
        print ("def Tab_Seleted is Failed")
        Log.write_log("Studio", "Error: def Tab_Seleted is Failed")
        sys.exit()
        return False

def Icon_Seleted(StudioAppPath, Icon):
    try:
        if exists(StudioAppPath + Icon):
            click(StudioAppPath + Icon)
            print ("def Icon_Seleted {} is Finished").format(Icon)
            Log.write_log("Studio", "Info: def Icon_Seleted {} is Finished".format(Icon))
            return True
    except:
        print ("def Icon_Seleted {} is Failed").format(Icon)
        Log.write_log("Studio", "Error: def Icon_Seleted {} is Failed".format(Icon))
        sys.exit()
        return False      
 
def SetAttribute(Attribute,ObjectType, StudioAppPath,**pardict):
    """ 
    pardict:
    1.parameter = {'Type':'Circular','D1red':'2','D1green':'1'}  set runner or gate parameter
    2:Source={'Source':'Part'}  give initial attribute 
    3.mouse={'mouse':'abc'} use mouse set attribute (value can be any string)
    For example:

    par={'Type':'Circular','D1red':'2','D1green':'1','Source':'Part','mouse':'abc'}
    Studio.SetAttribute('ColdRunner','Geometry',StudioAppPath,**par)

    """
    try:
        if ("Source" in pardict):
            if exists(Pattern(StudioAppPath + r"\Studio_"+  pardict.get('Source')+"_not_selected_attributed.png").similar(0.9)):
                click(Pattern(StudioAppPath + r"\Studio_"+ pardict.get('Source')+"_not_selected_attributed.png").similar(0.9).targetOffset(-10,0)) 
        else:
            if exists(Pattern(StudioAppPath + r"\Studio_NON_not_selected_attributed.png").similar(0.9)):
                click(Pattern(StudioAppPath + r"\Studio_NON_not_selected_attributed.png").similar(0.9).targetOffset(-10,0))
         
        if ("Source" in pardict and "mouse" in pardict):
            rightClick(Pattern(StudioAppPath + r"\Studio_"+ pardict.get('Source')+"_attributed.png").similar(0.9))
            Click_Icon(StudioAppPath, r"\Studio_rightclick_attribute",0) 
        elif ("Source" in pardict and "mouse" not in pardict):
            Click_Icon(StudioAppPath, r"\Studio_AttributeIcon.png",0)
            click(Pattern(StudioAppPath + r"\Studio_"+ pardict.get('Source')+"_attributed.png").similar(0.9))  
        elif ("Source" not in pardict and "mouse"  in pardict):
            rightClick(Pattern(StudioAppPath + r"\Studio_NON_attributed.png").similar(0.9))
            Click_Icon(StudioAppPath, r"\Studio_rightclick_attribute",0) 
        else:
            Click_Icon(StudioAppPath, r"\Studio_AttributeIcon.png",0)
            Click_Icon(StudioAppPath, r"\Studio_NON_attributed.png",0) 
        click(Pattern(StudioAppPath+ r"\Studio_attribute_expand.png").similar(0.9).targetOffset(0,39))
        Click_Icon(StudioAppPath, r"\Studio_Attribute_" + Attribute + ".png",0)

        print("Setting attribute is finished")    
        if(ObjectType=='Line')or(Attribute=='HotRunnerMetal'):
            if pardict!={}:              
                for par in pardict:
                    if('HCF' in par):
                       click(StudioAppPath + r"\set_HCF.png")
                       doubleClick(pardict.get('HCF'))
                       click(StudioAppPath + r"\check.png") 

                    elif (par=='Type'):
                        click(Pattern(StudioAppPath + r"\Studio_Type.png").similar(0.65).targetOffset(150,0))
                        Click_Icon(StudioAppPath, r"\Studio_Type_" + pardict.get('Type') + ".png",0) 
                        print('type is finished')                        
                    elif  (par=='Gate'):
                        click(Pattern(StudioAppPath + r"\Studio_Gate.png").similar(0.65).targetOffset(112,10))
                        Click_Icon(StudioAppPath, r"\Studio_Gate_" + pardict.get('Gate') + ".png",0)                        
                    elif (par=='D1red') or (par=='ared') or (par=='Hred') and (par=='D1green') or (par=='agreen') or (par=='Hgreen'):
                        click(Pattern(StudioAppPath + r"\Studio_Parameter_D1.png").similar(0.5).targetOffset(-57,6))
                        type("a",Key.CTRL)
                        type((pardict.get('D1red'))) or type((pardict.get('ared'))) or type((pardict.get('Hred'))) 
                        print('a1red is finished')
                        type(Key.TAB)
                        type((pardict.get('D1green'))) or type((pardict.get('agreen'))) or type((pardict.get('Hgreen')))
                        print('a1green is finished')
                    elif(par=='L'):
                        click(Pattern(StudioAppPath + r"\Studio_Parameter_L.png").similar(0.9).targetOffset(0,0))
                        type("a",Key.CTRL)
                        type((pardict.get('L')))
                    elif(par=='OrientationVector'):
                        click(Pattern(StudioAppPath + r"\Studio_Parameter_OrientationVector.png").similar(0.9).targetOffset(-35,6))
                        type("a",Key.CTRL)
                        type((pardict.get('OrientationVector')))
                    elif (Attribute =='Coolingchannel') or(Attribute=='Heatingrod') and ('D'in par):
                        click(Pattern(StudioAppPath + r"\Studio_Parameter_Cooling.png").similar(0.5).targetOffset(-9,16))
                        type("a",Key.CTRL)
                        type((pardict.get('D')))
                        print('D is finished')       
        Click_Icon(StudioAppPath, r"\Btn_Close.png",0)
        wait(1)        
    except:
        print ("def SetAttribute is Failed")
        Log.write_log("Studio", "Error: def SetAttribute is Failed")
        sys.exit()
        return False
            
def Moldbase_wizard(Parting_Direction,StudioAppPath):
    """
    #Click Moldbase wizard
    """
    try:
        if exists(StudioAppPath + r"\Moldbase_wizard.png",30):
           click(StudioAppPath + r"\Moldbase_wizard.png")
           wait(1)
           click(Pattern(StudioAppPath + r"\Studio_expand.png").similar(0.95)) 
           if exists(Pattern(StudioAppPath + r"\Studio_selected_" +Parting_Direction+".png").similar(0.95)):
               click(Pattern(StudioAppPath + r"\Studio_selected_" +Parting_Direction+".png").similar(0.95))
           else:
               click(Pattern(StudioAppPath + r"\Studio_unselected_" +Parting_Direction+".png").similar(0.95))
           wait(1)

           click(StudioAppPath + r"\check.png")        
    except:
        print("def Moldbase_wizard is failed")
        Log.write_log("Studio", "Error: def Moldbase_wizard is failed")
        sys.exit()
        return False 
    
def Inletoutlet_wizard(StudioAppPath):
    """
    #Click Inletoutlet wizard
    """
    try:
        if exists(StudioAppPath + r"\Add_Inletoutlet.png",30):
            click(StudioAppPath + r"\Add_Inletoutlet.png")
        wait(5)
        click(StudioAppPath + r"\check.png")
    except:
        print ("def Add_Inletoutlet is failed")
        Log.write_log("Studio", "Error: def Add_Inletoutlet is failed")
        sys.exit()
        return False 

def Checkcooling_wizard(StudioAppPath):               
    """
    #click Checkcooling_wizard
    """
    try :
        if  exists(StudioAppPath + r"\Check_cooling.png",30):
            click(StudioAppPath + r"\Check_cooling.png")
            click(StudioAppPath + r"\check.png")
    except:
        print("def Checkcooling_wizard is failed")
        Log.write_log("Studio", "Error: def Checkcooling_wizard is failed")
        sys.exit()
        return False 
    
def Node_Seeding(StudioAppPath,**meshsize):
    """
    meshsize = {'Part':'0.5'}
    """       
    try:
        x=(Pattern(StudioAppPath + r"\Studio_Tree_Moldbase.png").targetOffset(-61,0).similar(0.99))
        click(StudioAppPath + r"\Studio_Tree_Model.png")
        if exists(x):
            click(x)
        if exists(StudioAppPath + r"\Studio_NodeSeeding_Icon.png",2):
            Click_Icon(StudioAppPath, r"\Studio_NodeSeeding_Icon.png",0)
            wait(1)
        else:
            exists(StudioAppPath + r"\Studio_Seeding_Select.png",2)
            click(Pattern(StudioAppPath + r"\Studio_Seeding_Select.png").similar(0.8).targetOffset(-2,8)) 
            click(Pattern(StudioAppPath + r"\Studio_Seeding_select2.png").similar(0.8)) 
            wait(1)
        if meshsize!={}:
            for size in meshsize:
                if exists(StudioAppPath + r"\Studio_NodeSeeding_Icon.png",2):
                    Click_Icon(StudioAppPath, r"\Studio_NodeSeeding_Icon.png",0)
                    wait(1)
                    click(Pattern(StudioAppPath + r"\Studio_Tree_" + size + ".png").similar(0.7)) 
                    Click_Icon(StudioAppPath, r"\Btn_Check.png",0)
                    if exists(StudioAppPath + r"\Studio_reset_global_mesh.png",5):
                        click(StudioAppPath + r"\Btn_Yes_2.png")
                    if exists(StudioAppPath + r"\Studio_mesh_size_reset.png",5):
                        click(StudioAppPath + r"\Btn_Yes_2.png")
                        
                    click(Pattern(StudioAppPath + r"\Studio_mesh_size.png").similar(0.8).targetOffset(57,0)) 
                    type("a",Key.CTRL)
                    type((meshsize.get(size))) 
                    wait(1)
                    Click_Icon(StudioAppPath, r"\Btn_Check.png",0)
                    wait(1)
                    click(Pattern(StudioAppPath + r"\Studio_Btn_check_yellow.png").similar(0.7)) 
                    print("Node seeding is finished")               
        else:
            Click_Icon(StudioAppPath, r"\Studio_Model_Tree.png",0)
            Click_Icon(StudioAppPath, r"\Btn_Check.png",0)
            if exists(StudioAppPath + r"\Studio_reset_global_mesh.png",5):
                        click(StudioAppPath + r"\Btn_Yes_2.png")
            if exists(StudioAppPath + r"\Studio_mesh_size_reset.png",5):
                    click(StudioAppPath + r"\Btn_Yes_2.png")
            click(Pattern(StudioAppPath + r"\Studio_mesh_size.png").targetOffset(57,0).similar(0.8)) 
            type("a",Key.CTRL)
            type("1")
            Click_Icon(StudioAppPath, r"\Btn_Check.png",0)
            wait(3)
            click(Pattern(StudioAppPath + r"\Studio_Btn_check_yellow.png").similar(0.7)) 
            print("Node seeding is finished")        
    except:
        print ("def Node Seeding is Failed")
        Log.write_log("Studio", "Error: def Node Seeding is Failed")
        sys.exit()
        return False
                
def Symmetry_wizard(StudioAppPath,type):
    """"
    #click Symmetry-wizard
    """
    try :
        if  exists(StudioAppPath + r"\Symmetry.png",30):
            click(StudioAppPath + r"\Symmetry.png")
            click(Pattern(StudioAppPath + r"\Studio_Symmetrytype.png").targetOffset(70,0).similar(0.7)) 
            click(Pattern(StudioAppPath + r"\Studio_Symmetrytype_" + type + ".png").similar(0.7))
            wait(1)
            click(StudioAppPath + r"\check.png")
    except:
        print ("def Symmetry_wizard is failed")
        Log.write_log("Studio", "Error: def Symmetry-wizard is failed")
        sys.exit()
        return False 

def CoolingChannel_wizard(Channel_Direction,StudioAppPath):
    """"
    Channel_Direction= "X" or "Y" or "Z"
    #click CoolingChannel-wizard
    """
    try :

        if  exists(StudioAppPath + r"\CoolingChannel.png",30):
            click(StudioAppPath + r"\CoolingChannel.png",5)
            click(StudioAppPath + r"\CoolingChannelwizard.png")
            wait(1)
            click(Pattern(StudioAppPath + r"\Studio_"+ Channel_Direction +"_Axis.png").targetOffset(-25,0).similar(0.95)) 
            wait(1)
            click(StudioAppPath + r"\check.png")
        
    except:
        print ("def Checkcooling_wizard is failed")
        Log.write_log("Studio", "Error: def CoolingChannel-wizard is failed")
        sys.exit()
        return False 

def Compression_Setting_Zone(attribute,Vector,Stroke, StudioAppPath):
    """
    #Click Compression zoine
    """   
    try:
        if exists(StudioAppPath + r"\Compression_wizard.png",30):
                click(StudioAppPath + r"\Compression_wizard.png")                
        click(StudioAppPath + r"\Studio_Tree_Model.png")
        click(Pattern(StudioAppPath + r"\Studio_"+ attribute +"_attributed.png").similar(0.9)) 
        click(Pattern(StudioAppPath + r"\Compression_Vector.png"))   
        type("a",Key.CTRL)
        type(Vector)
        click(Pattern(StudioAppPath + r"\Compression_stroke.png"))   
        type("a",Key.CTRL)
        type(Stroke)  

        print("def Compression_Setting_Zone is Finished")
        Log.write_log("Studio", "Info: def Compression_Setting_Zone is Finished")
        return True
    except:
        print("def Compression_Setting_Zone is failed")
        Log.write_log("Studio", "Error: def Compression_Setting_Zone is failed")
        sys.exit()
        return False  
          
def Compression_Setting_Region(type,selection_way,StudioAppPath,*face_angle):
    """
    #edit selectin tool
    """   
    try:
        if len(face_angle)>0:
            click(Pattern(StudioAppPath + r"\Compression_Face_Angle.png").similar(0.9).targetOffset(60,0))
            type("a",Key.CTRL)
            type(face_angle[0])
        click(StudioAppPath + r"\Compression_"+ type+ ".png")
        wait(1)
        click(StudioAppPath + r"\Compression_"+ selection_way+ ".png")
        print("def Compression_Setting_Region is Finished")
        Log.write_log("Studio", "Info: def Compression_Setting_Region is Finished")
        return True
    except:
        print("def Compression_Setting_Region is failed")
        Log.write_log("Studio", "Error: def Compression_Setting_Region is failed")
        sys.exit()
        return False 


def Gate_wizard(StudioAppPath,gatelocation):
    try :
        if exists(StudioAppPath + r"\Studio_Gate_wziard.png",30):
            click(Pattern(StudioAppPath + r"\Studio_Gate_wziard.png").targetOffset(0,-14).similar(0.7))
            wait(1) 
            click(Pattern(StudioAppPath + r"\Studio_Gate_wziard.png").targetOffset(0,-14).similar(0.7))
            click(Pattern(StudioAppPath + r"\Studio_Add_pin_gate.png").targetOffset(23,10).similar(0.7))             
            type("a",Key.CTRL)
            type(gatelocation)
            type(Key.ENTER)
            wait(1)
            click(StudioAppPath + r"\check.png")
    except:
        print ("def Gate_wizard is failed")
        Log.write_log("Studio", "Error: def Gate_wizard is failed")
        sys.exit()
        return False 
    
def Runner_wizard(StudioAppPath):
    """"
    #click CoolingChannel-wizard
    """
    try :
        if  exists(StudioAppPath + r"\Studio_Runner_wizard.png",30):
            click(Pattern(StudioAppPath + r"\Studio_Runner_wizard.png").targetOffset(0,30).similar(0.7)) 
            click(StudioAppPath + r"\Studio_Runner_wizard_btn.png")
            wait(1)
            click(StudioAppPath + r"\check.png")
    except:
        print ("def Runner Wizard is failed")
        Log.write_log("Studio", "Error: def Runner wizard is failed")
        sys.exit()
        return False     
 
def SetMovingSurface(itempic,similar,offsetx,offsety,moving_direction,StudioAppPath):
    """0.6 -400 -150
    itempic's offset and similar should reset everytime    
    """       
    try:
        click(StudioAppPath + r"\Studio_Moving_Surface_icon.png")
        click(Pattern(itempic).similar(similar).targetOffset(offsetx,offsety))   # itempic's offset and similar should reset everytime
        doubleClick(Pattern(StudioAppPath + r"\Studio_Moving_Direction_ICON.png").targetOffset(0,21))
        type(moving_direction)
        type(Key.ENTER)
        click(StudioAppPath + r"\check.png")     
    except:
        print ("def SetMovingSurface is Failed")
        Log.write_log("Studio", "Error: def SetMovingSurface is Failed")
        sys.exit()
        return False           
    
def SetView(View,StudioAppPath):
    """   
    SetView("Top",StudioAppPath)
    """
    try:
        click(Pattern(StudioAppPath + r"\Studio_set_view.png").similar(0.85).targetOffset(25,-15))
        Click_Icon(StudioAppPath, r"\Studio_View_" + View + ".png",0)
        print("Setting View is finished")           
    except:
        print ("def Setting View is Failed")
        Log.write_log("Studio", "Error: def Set View is Failed")
        sys.exit()
        return False
            
def SetMeshParameter(ObjectType,Attribute,Meshtype,StudioAppPath):
    """
    SetMeshParameter(Hybridmesh,Compressionzone,BLM,StudioApppath)
    """       
    try:
        click(StudioAppPath + r"\Studio_Mesh_Parameter.png")
       
        if (ObjectType=='Geoemetry'):
            click(Pattern(StudioAppPath + r"\Studio_Object_Geometry.png").targetOffset(120,0))
            click(Pattern(StudioAppPath + r"\Studio_ObjectAttribute_" + Attribute + ".png").similar(0.8)) 
            click(Pattern(StudioAppPath + r"\Studio_Object_Geometry.png").targetOffset(120,23))
            click(Pattern(StudioAppPath + r"\Studio_GeometryMeshType_" + Meshtype + ".png").similar(0.99))          
        elif(ObjectType=='Hybrid'):
            click(Pattern(StudioAppPath + r"\Studio_Object_Hybrid.png").targetOffset(60,-10)) 
            Click_Icon(StudioAppPath, r"\Studio_ObjectAttribute_" + Attribute + ".png",0)
            click(Pattern(StudioAppPath + r"\Studio_Object_Hybrid.png").targetOffset(93,10))
            click(Pattern(StudioAppPath + r"\Studio_HybridMeshType_" + Meshtype + ".png").similar(0.8)) 
        click(StudioAppPath + r"\Btn_Check.png")
    except:
        print ("def Set Mesh Parameter is Failed")
        Log.write_log("Studio", "Error: def Set Mesh Parameter is Failed")
        sys.exit()
        return False
    
def SetCharge(StudioAppPath):
    try:
        click(StudioAppPath + r"\Studio_Tree_Model.png")
        Click_Icon(StudioAppPath, r"\Studio_Charge_Icon.png",0)
        while not exists(Pattern(StudioAppPath + r"\Studio_NON_Attributed.png").similar(0.90),2):
            dragDrop(StudioAppPath + r"\Studio_ObjectBar.png",StudioAppPath + r"\Studio_ObjectBar_Bottom.png")
        Click_Icon(StudioAppPath, r"\Studio_NON_Attributed.png",0)
        wait(1)
        Click_Icon(StudioAppPath, r"\Fixed_BC_OK.png",0)
        if exists(StudioAppPath + r"\Btn_Close.png", 3):
            Click_Icon(StudioAppPath, r"\Btn_Close.png",0)
        wait(3)
    except:
        print ("def SetCharge is Failed")
        Log.write_log("Studio", "Error: def SetCharge is Failed")
        sys.exit()
        return False    

def click_result(StudioAppPath, solver):
    try:
        mouseMove(os.path.join(StudioAppPath, "Studio_Tree_Run.png"))
        mouseMove(0, 20)
        solver = os.path.join(StudioAppPath, solver + ".png")
        if not exists(Pattern(solver).similar(0.95), 1):
            Mouse.wheel(WHEEL_DOWN, 5)
        if exists(Pattern(solver).similar(0.95), 1):
            click(Pattern(solver).similar(0.95))
        else:
            print ("def click_result: No Solver {}".format(solver))
            Log.write_log("Studio", ("Warning: def click_result: No Solver {}".format(solver)))
            return False
        print ("def click_result {} is Finished".format(solver))
        Log.write_log("Studio", ("Info: def click_result {} is Finished".format(solver)))
        return True
    except:
        print ("def click_result {} is Failed".format(solver))
        Log.write_log("Studio", ("Error: def click_result {} is Failed".format(solver)))
        return False
    
    
def Create_BJS(offsety, StudioAppPath, *ExportInformation):
    #offsetx: keep -21
    #offsety 13: ALL Run; Run1: 35 ; Run2: 50  ; Run3: 70
    #project_name, project_location = ExportInformation
    #Creat_BJS(13,StudioAppPath,ProjectName,Location)
    try:
        wait(2)
        if exists(Pattern(StudioAppPath + r"\Home_Simulation.png").similar(0.98), 30):
            click(Pattern(StudioAppPath + r"\Home_Simulation.png").targetOffset(0,-10))
            if exists(StudioAppPath + r"\Home_AnalysisList.png", 3):
                  click(Pattern(StudioAppPath + r"\Home_AnalysisList.png").targetOffset(0, 5))
            if exists(StudioAppPath + r"\Studio_Jobs_Lists.png", 3):
                  click(Pattern(StudioAppPath + r"\Studio_Jobs_Lists.png").similar(0.9).targetOffset(-21, offsety))
            click(StudioAppPath + r"\Btn_Add.png")
            click(Pattern(StudioAppPath + r"\BJS_Export.png").similar(0.8).targetOffset(-80,0))
            if len(ExportInformation) == 2:
                [project_name, project_location] = ExportInformation
                click(Pattern(StudioAppPath + r"\Studio_Project_Name.png").similar(0.9).targetOffset(40, 0)) 
                type("a", Key.CTRL)
                type(project_name+"(RC)")
                click(Pattern(StudioAppPath + r"\Studio_Project_Location.png").similar(0.9).targetOffset(40, 0)) 
                type("a", Key.CTRL)
                paste(project_location)
            elif len(ExportInformation) == 1:
                if (os.path.isdir(ExportInformation[0])):
                    project_location = ExportInformation[0]
                    click(Pattern(StudioAppPath + r"\Studio_Project_Location.png").similar(0.9).targetOffset(40, 0)) 
                    type("a", Key.CTRL)
                    paste(project_location)
            else:
                project_name = ExportInformation[0]
                click(Pattern(StudioAppPath + r"\Studio_Project_Name.png").similar(0.9).targetOffset(40, 0)) 
                type("a", Key.CTRL)
                type(project_name+"(RC)")
            click(StudioAppPath + r"\Btn_Create.png")
            Wait_Dialog(StudioAppPath, r"\Studio_Export_Done.png")
            click(Pattern(StudioAppPath + r"\Open_BJS_Folder.png").similar(0.85))
            wait(1)
            click(Pattern(StudioAppPath + r"\Route_win11.png").similar(0.80).targetOffset(-50,0))
            type("c",KeyModifier.CTRL)
            click(StudioAppPath + r"\close.png")
            wait(1)
            click(StudioAppPath + r"\Btn_Close.png")
            print ("def Create_BJS is Finished")
            Log.write_log("Studio", "Info: def Create_BJS is Finished")
            return True
    except:
        print ("def Create_BJS is Failed")
        Log.write_log("Studio", "Error: def Create_BJS is Failed")
        sys.exit()
        return False
 
def Export_Run(offsety,ProjectName,StudioAppPath,*ProjectLocation):
    #offsetx: keep -30
    #offsety 2: ALL Run; Run1: 20 ; Run2: 40  ; Run3: 60
    #RClocation=['C:\p\RC'] 
    # Export_Run(2,ABC,StudioAppPath,*RClocation)
    try:    
        wait(2)
        if exists(Pattern(StudioAppPath + r"\Run01.png").similar(0.90), 10):
           rightClick(StudioAppPath + r"\Run01.png")
        if exists(StudioAppPath + r"\Studio_ExportRun.png", 3):
            click(Pattern(StudioAppPath + r"\Studio_ExportRun.png").similar(0.9))
        if exists(StudioAppPath + r"\Studio_ProjectName.png", 3):
            click(Pattern(StudioAppPath + r"\Studio_ProjectName.png").similar(0.9).targetOffset(52, 0)) 
            type("a",Key.CTRL)
            paste(ProjectName)  
        if len(ProjectLocation)!=0:
            click(Pattern(StudioAppPath + r"\Studio_Project_Location.png").similar(0.9).targetOffset(33, 0)) 
            type("a",Key.CTRL)
            paste(ProjectLocation[0]) 
        if exists(StudioAppPath + r"\Studio_Export_ChoseRun.png", 3):
            click(Pattern(StudioAppPath + r"\Studio_Export_ChoseRun.png").similar(0.9).targetOffset(-30, offsety))
                  
        click(Pattern(StudioAppPath + r"\Btn_Export.png").similar(0.9))
        Wait_Dialog(StudioAppPath, r"\Studio_Export_Done.png")
        click(StudioAppPath + r"\Btn_Close.png")
        print ("def Export_Run is Finished")
        Log.write_log("Studio", "Info: def Export_Run is Finished")
        return True
    except:
        print ("def Export_Run is Failed")
        Log.write_log("Studio", "Error: def Export_Run is Failed")
        sys.exit()
        return False   
    
    
def Submit_Batch_Run(offsety,StudioAppPath):
    #offsetx: keep -30
    #offsety 2: ALL Run; Run1: 20 ; Run2: 40  ; Run3: 60
    #RClocation=['C:\p\RC'] 
    # Export_Run(2,ABC,StudioAppPath,*RClocation)
    try:    
        wait(2)
        if exists(StudioAppPath + r"\Studio_Export_ChoseRun.png", 3):
            print(1)
            click(Pattern(StudioAppPath + r"\Studio_Export_ChoseRun.png").similar(0.9).targetOffset(-30, offsety))
        click(StudioAppPath + r"\Btn_Add.png")
        print(2)      
        click(Pattern(StudioAppPath + r"\Studio_BachRun_OK.png").similar(0.9))
        print(3)
        print ("def Submit_Batch_Run is Finished")
        Log.write_log("Studio", "Info: def Submit_Batch_Run is Finished")
        return True
    except:
        print ("def Submit_Batch_Run is Failed")
        Log.write_log("Studio", "Error: def Submit_Batch_Run is Failed")
        sys.exit()
        return False 
    
     #Click_Icon(StudioAppPath, r"\Btn_Check.png",0)
def Create_RC_Folder(StudioAppPath):
    try:
        click(Pattern(StudioAppPath + r"\Studio_open_WorkingFolder.png").similar(0.9))      
        Click_Icon(StudioAppPath, r"\Preious_Layer.png",0)
        wait(1)
        if exists(StudioAppPath + r"\Studio_RC_Folder.png"):
            doubleClick(StudioAppPath + r"\Studio_RC_Folder.png")
        else:
            click(Pattern(StudioAppPath + r"\New.png").similar(0.8).targetOffset(27,4))
            Click_Icon(StudioAppPath, "\\Folder.png",0)
            type("RC")
            type(Key.ENTER)
            wait(1)
            type(Key.ENTER)
        wait(1)
        click(Pattern(StudioAppPath + r"\Studio_RC_Route.png").similar(0.99).targetOffset(30,0))
        type("c",KeyModifier.CTRL)
        wait(1)
        RCroute=Env.getClipboard().strip()
        Click_Icon(StudioAppPath, "\\close.png",0)
        RClocation=[RCroute] 
        Create_BJS(13,StudioAppPath,*RClocation)
        return True
    except:
        print ("def Create_RC_Folder is Failed")
        Log.write_log("Studio", "Error: def Create_RC_Folder is Failed")
        sys.exit()
        return False 
def SetPressure(itempic,pressure,StudioAppPath):
    """
    itempic's offset and similar should reset everytime    
    """       
    try:
        click(StudioAppPath + r"\Studio_Pressure_Icon.png")
        wait(1)
        doubleClick(Pattern(itempic).similar(0.8).targetOffset(0,0))   # itempic's offset and similar should reset everytime
        click(Pattern(StudioAppPath + r"\Studio_Pressure_Value.png").targetOffset(59,0))
        type("a",Key.CTRL)
        type(pressure)
        type(Key.ENTER)
        click(StudioAppPath + r"\Fixed_BC_OK.png")     
    except:
        print ("def SetPressure is Failed")
        Log.write_log("Studio", "Error: def SetPressure is Failed")
        sys.exit()
        return False    


def SetFixConstraint(Analysis,Target,StudioAppPath,*setting):
    """
    itempic's offset and similar should reset everytime    
    """       
    try:
        click(StudioAppPath + r"\Studio_FIX_Constraint_ICON.png")
        wait(1)
        click(StudioAppPath + r"\studio_fixconstraint_analysis.png")
        if(Analysis=='Stress'):
            click(Pattern(StudioAppPath + r"\Studio_FixConstraint_analysis_stress.png").similar(0.95))
        elif(Analysis=='MoldDeformation'):
            click(Pattern(StudioAppPath + r"\Studio_FixConstraint_analysis_molddeformation.png").similar(0.95))
        else:
            click(StudioAppPath + r"\Studio_FixConstraint_analysis_core_shift.png")
            click(StudioAppPath + r"\Studio_logo.png")
        if len(setting)!=0:
            click(StudioAppPath + r"\Studio_FixConstraint_Setting.png")
            if setting[0] == "0":   
                click(Pattern(StudioAppPath + r"\Studio_Vertex_Selection.png").similar(0.7).targetOffset(-55, 0))
                wait(1)
                click(StudioAppPath + r"\Btn_Check.png")
            else:
                click(StudioAppPath + r"\Studio_face_face_angle.png")
                type("a",Key.CTRL)
                type(setting) 
                click(StudioAppPath + r"\Btn_Check.png")

        doubleClick(Target)   # itempic's offset and similar should reset everytime
        click(StudioAppPath + r"\Fixed_BC_OK.png")   
    except:
        print ("def SetFixConstraint is Failed")
        Log.write_log("Studio", "Error: def SetFixConstraint is Failed")
        sys.exit()
        return False   

def SetHeatConduction(itempic,Name,StudioAppPath):
    """
    itempic's offset and similar should reset everytime    
    """       
    try:
        click(StudioAppPath + r"\Studio_HeatConduction_Icon.png")
        click(Name)
        click(itempic)   # itempic's offset and similar should reset everytime
        click(StudioAppPath + r"\check.png")     
    except:
        print ("def SetHeatConduction is Failed")
        Log.write_log("Studio", "Error: def SetHeatConduction is Failed")
        sys.exit()
        return False           

def SpecifyModelName(Name,StudioAppPath):
    """
    Specify mdg file name
    """
    try:
        #rightClick(StudioAppPath + r"\Studio_Tab_Object_Tree_Model.png") #124227
        rightClick(Pattern(StudioAppPath + r"\Studio_ActiveRun.png").similar(0.9).targetOffset(30,20))
        wait(1)
        click(StudioAppPath + r"\Studio_SpecifyModelName.png")
        x = Pattern(StudioAppPath + r"\Studio_Name.png").similar(0.9).targetOffset(50,0)
        i = 0
        while exists(x, 1) and i < 3:
            click(x)
            #type('a', Key.CTRL)
            paste(Name)
            mouseMove(0,50)
            wait(1)
            i += 1
        x = find(StudioAppPath + r"\SpecifyModelName_Btn_Save.png")
        click(x)
        Log.write_log("Studio", "Error: def SpecifyModelName is Finished")
    except:
        print ("def SpecifyModelName is Failed")
        Log.write_log("Studio", "Error: def SpecifyModelName is Failed")
        sys.exit()
    

    
 
def Nozzlezone_wizard(target,tip,body,StudioAppPath):
    
    #click Nozzlezone-wizard
    
    try :
        if  exists(StudioAppPath + r"\NozzleZone_wizard.png",30):
            click(StudioAppPath + r"\NozzleZone_wizard.png",5)
            click(target)
            click(StudioAppPath + r"\Studio_Nozzel_Tip.png")
            click(StudioAppPath + r"\Studio_Nozzel_Tip_"+ tip +".png")
            click(StudioAppPath + r"\Studio_Nozzel_Body.png")
            click(StudioAppPath + r"\Studio_Nozzel_Body_"+ body +".png")
            click(StudioAppPath + r"\Btn_OK.png")
    except:
        print ("def Nozzlezone-wizard is failed")
        Log.write_log("Studio", "Error: def Nozzlezone-wizard is failed")
        sys.exit()
  

def WindowSelect(StudioAppPath, Pic, Sx, Sy, Ex, Ey):
    StartPosition = Pattern(StudioAppPath + Pic).targetOffset(Sx,Sy)
    EndPosition = Pattern(StudioAppPath + Pic).targetOffset(Ex,Ey)
    mouseMove(StartPosition)
    mouseDown(Button.LEFT)
    mouseMove(EndPosition)
    mouseUp(Button.LEFT)
    
def SetMeltInlet(itempic,StudioAppPath):       
    try:
        click(Pattern(StudioAppPath + r"\Studio_MeltInlet_Icon.png").similar(0.9))
        click(itempic) 
        wait(2)
        click(StudioAppPath + r"\check.png")     
    except:
        print ("def SetMeltInlet is Failed")
        Log.write_log("Studio", "Error: def SetMeltInlet is Failed")
        sys.exit()
        return False   

def SetIMD(Thickness,itempic,StudioAppPath,*face_angle):
    """
    itempic's offset and similar should reset everytime    
    """       
    try:
        click(StudioAppPath + r"\Studio_IMD_logo.png")
        wait(1)
        if len(face_angle)>0:
            click(Pattern(StudioAppPath + r"\Studio_face_angle.png").similar(0.9).targetOffset(100,0))
            type("a",Key.CTRL)
            type(face_angle[0])
            type(Key.ENTER)
        wait(1)
        doubleClick(Pattern(StudioAppPath + r"\Studio_IMD_Thickness.png").similar(0.9).targetOffset(0,21))
        type(Thickness)
        type(Key.ENTER)
        doubleClick(itempic)   # itempic's offset and similar should reset everytime
        wait(1)
        click(StudioAppPath + r"\Btn_Check.png")  
    except:
        print ("def SetIMD is Failed")
        Log.write_log("Studio", "Error: def SetIMD is Failed")
        sys.exit()

def SetVenting(StudioAppPath):
    try:
        click(StudioAppPath + r"\Studio_Tree_Model.png")
        Click_IconEx(StudioAppPath + "\\BC2.png")
        Click_IconEx(StudioAppPath + "\\Studio_Venting_Icon.png")
        while not exists(Pattern(StudioAppPath + r"\Studio_NON_Attributed.png").similar(0.90),2):
            dragDrop(StudioAppPath + r"\Studio_ObjectBar.png",StudioAppPath + r"\Studio_ObjectBar_Bottom.png")
        Click_IconEx(StudioAppPath + "\\Studio_NON_Attributed.png")
        wait(1)
        Click_IconEx(StudioAppPath + "\\Btn_OK.png")
        wait(1)
        if exists(StudioAppPath + r"\Btn_OK.png", 3):
            Click_IconEx(StudioAppPath + "\\Btn_OK.png")
        wait(3)
        print ("def SetVenting is Finished")
        Log.write_log("Studio", "Error: def SetVenting is Finished")
    except:
        print ("def SetVenting is Failed")
        Log.write_log("Studio", "Error: def SetVenting is Failed")
        sys.exit()
        return False 