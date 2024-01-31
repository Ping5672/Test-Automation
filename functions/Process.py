from time import sleep
from sikuli import *
import sys, os

LogAppPath = r"../sikuli_Share/Common.sikuli"
sys.path.append(LogAppPath)
import log_record as Log

def Home_Process(sType, ProcessAppPath):
    """
    #Click Process to Call Process Wizard
    #Argument: select New Process or Edit
    """
    try:
        Studio_Pro = Pattern(ProcessAppPath + r"\Studio_Pro.png").similar(0.95)
        if exists(Studio_Pro, 30):
            click(Studio_Pro.targetOffset(0,30))
        else:
            print('Cannot Find %s' %Studio_Pro)
        wait(ProcessAppPath + r"\Studio_Pro_Mode.png")
        if sType == "New":
            Studio_Pro = find(ProcessAppPath + r"\Studio_Pro_New.png")
        elif sType =="New_Transfer":
            Studio_Pro = find(ProcessAppPath + r"\Studio_Pro_New_Transfer.png")
        elif sType =="New_Injection":
            Studio_Pro = find(ProcessAppPath + r"\Studio_Pro_New_Injection.png")
        elif sType =="Default":
            Studio_Pro = find(Pattern(ProcessAppPath + r"\Studio_Pro_Default.png").similar(0.8))
        click(Studio_Pro)
        """
        if sType =="Import": 
            click(Pattern(ProcessAppPath + r"\Studio_Pro_Import.png").similar(0.8))
            wait(1)
            click(Pattern(ProcessAppPath + r"\pro_file_name.png").similar(0.8).targetOffset(37, 0))
            paste(Propath)
        """  
        print ("def Home_Process is Finished")
        Log.write_log("Process", "Info: def Home_Process is Finished")
        return True
    except:
        print ("def Home_Process is Failed")
        Log.write_log("Process", "Error: def Home_Process is Failed")
        sys.exit()
        return False

def Select_Machine_Setting(ProcessAppPath):
    try:
        x = ProcessAppPath + r"\Pro_MachineSetting.png"
        if exists(x, 10):
            click(Pattern(x).targetOffset(15, 20))
            click(ProcessAppPath + r"\Pro_New.png")
        else:
            print ("NOT found Machine Setting")
        print ("def Select_Machine_Setting is Finished")
        Log.write_log("Process", "Info: def Select_Machine_Setting is Finished")
        return True
    except:
        print ("def Select_Machine_Setting is Failed")
        Log.write_log("Process", "Error: def Select_Machine_Setting is Failed")
        sys.exit()
        return False
        
def SelectMachine(sMaclist):
    #Select Part Material
    try:
        i = 0
        while (i < len(sMaclist)-1):
            while not exists (Pattern(sMaclist[i]).similar(0.95), 2):
                type(Key.PAGE_DOWN)
            x = wait(sMaclist[i], 2)
            sleep(1)
            click(x)
            sleep(1)
            type(Key.RIGHT)
            sleep(1)
            click(x)
            i += 1
        x = wait(Pattern(sMaclist[i]).similar(0.95), 2)
        click(x)
        rightClick(x)
        print ("def SelectPartMaterial is Finished")
        Log.write_log("Process", "Info: def SelectPartMaterial is Finished")
        return True
    except:
        print ("def SelectPartMaterial is Failed")
        Log.write_log("Process", "Error: def SelectPartMaterial is Failed")
        sys.exit()
        return False
        
def ProcessWizard_Project_SettingMethod(sMethod, ProcessAppPath):
    """
    #Edit Process Wizard Project Tab
    #Argument: select Mode CAE / Machine Mode1 as M1 / Machine Mode2 as M2
    """
    try:
        wait(ProcessAppPath + r"\Process_Wizard.png",30)
        x = find(Pattern(ProcessAppPath + r"\Pro_Setting_method.png").targetOffset(100,0))
        click(x)            
        if sMethod == "CAE":
            click(ProcessAppPath + r"\Pro_CAE_mode.png")
        elif sMethod == "M1":
            click(ProcessAppPath + r"\Pro_M1_mode.png")
        elif sMethod == "M2":
            click(ProcessAppPath + r"\Pro_M2_mode.png")
        print ("def ProcessWizard_Project_SettingMethod is Finished")
        Log.write_log("Process", "Info: def ProcessWizard_Project_SettingMethod is Finished")
        return True
    except:
        print ("def ProcessWizard_Project_SettingMethod is Failed")
        Log.write_log("Process", "Error: def ProcessWizard_Project_SettingMethod is Failed")
        sys.exit()
        return False

def ProcessWizard_Tab_Next(CurrentTab, NextTab, ProcessAppPath):
    """
    #Change Process Wizard Tab from Current Tab to Next Tab
    #Argument: Tab Picture(s)
    """
    try:
        NextTab = os.path.basename(NextTab)
        NextTab = os.path.join(ProcessAppPath, NextTab)
        if exists(Pattern(CurrentTab).similar(0.95), 5):
            click(ProcessAppPath + r"\Btn_Next.png")
            if not exists (Pattern(NextTab).similar(0.95), 5):
                print ("def ProcessWizard_Tab_Next cannot found %s" %(NextTab))
                Log.write_log("Process", "Error: def ProcessWizard_Tab_Next cannot found NextTab %s" %(NextTab))
                sys.exit()
                return False
        else:
            print ("def ProcessWizard_Tab_Next cannot found %s" %(CurrentTab))
            Log.write_log("Process", "Error: def ProcessWizard_Tab_Next cannot found CurrentTab %s" %(CurrentTab))
            sys.exit()
            return False
        print ("def ProcessWizard_Tab_Next is Finished")
        Log.write_log("Process", "Info: def ProcessWizard_Tab_Next to %s is Finished" %(NextTab))
        return True
    except:
        print ("def ProcessWizard_Tab_Next is Failed")
        Log.write_log("Process", "Error: def ProcessWizard_Tab_Next to %s is Failed" %(NextTab))
        sys.exit()
        return False

def ProcessWizard_FillingPacking_Profile_Section_Value(Profilelist, ProcessAppPath):
    """
    #Edit Process Filling/Packing Profile Setting Tab
    """
    try:
        if (len(Profilelist) < 2):
            print ("Not Enough Arguments")
            Log.write_log("Process", "Error: Not Enough Arguments")
            sys.exit()
            return False
        else:
            i = 1
            while i < len(Profilelist): #Edit Profile Section Value(s)
                if ((i %2 != 0) and (i != len(Profilelist) - 1)): #Get Profile 1st/2nd value position
                    offsety = 30
                else:
                    offsety = 60
                if ((i == 1) or (i == 2)): #Change Section Picture No.
                    s = 1
                elif(i %2 != 0):
                    s += 1
                x = wait(Pattern(ProcessAppPath + (r"\Pro_Section%s.png") %(s)).similar(0.95).targetOffset(0, offsety), 5)
                click(x)
                type(Key.F2)
                type("a",Key.CTRL)
                type(Profilelist[i])
                type(Key.ENTER)
                i += 1
                if exists(ProcessAppPath + r"\Pro_MdxPro.png", 1):
                    if exists(ProcessAppPath + r"\Btn_OK2.png", 1):
                        click(ProcessAppPath + r"\Btn_OK2.png")
                else:
                    pass

        print ("def ProcessWizard_FillingPacking_Profile_Section_Value is Finished")
        Log.write_log("Process", "Info: def ProcessWizard_FillingPacking_Profile_Section_Value is Finished")
        return True
    except:
        print ("def ProcessWizard_FillingPacking_Profile_Section_Value is Failed")
        Log.write_log("Process", "Error: def ProcessWizard_FillingPacking_Profile_Section_Value is Failed")
        sys.exit()
        return False

def ProcessWizard_Rotating_Angularspeed_Profile_Section_Value(Profilelist, ProcessAppPath):
    """
    #Edit Process Rotating Angular Speed Profile Setting Tab
    """
    try:
        if (len(Profilelist) < 2):
            print ("Not Enough Arguments")
            Log.write_log("Process", "Error: Not Enough Arguments")
            sys.exit()
            return False
        else:
            i = len(Profilelist)
            s = (len(Profilelist) / 2) + 1
            lastsection = exists(Pattern(ProcessAppPath + (r"\Pro_Section%s.png") %(s-1)).similar(0.95))
            B1 = find(ProcessAppPath + r'\Pro_Profile_ScrollBar.png')
            if (lastsection == None and B1 <> None):
                mouseMove(Location(B1.x + 200, B1.y + 10))
                mouseDown(Button.LEFT)
                mouseMove(Location(B1.x + 500, B1.y))
                mouseUp(Button.LEFT)            
            while 1 < i <= len(Profilelist): #Edit Profile Section Value(s)
                if (i %2 == 0): #Get Profile 1st/2nd value position
                    offsety = 25                    
                else:
                    offsety = 45
                if ((i == 1) or (i == 2)): #Change Section Picture No.
                    s = s
                elif(i %2 != 0):
                    s -= 1
                i -= 1
                x = wait(Pattern(ProcessAppPath + (r"\Pro_Section%s.png") %(s)).similar(0.95).targetOffset(0, offsety), 5)
                click(x)
                type(Key.F2)
                type("a",Key.CTRL)
                type(Profilelist[i])
                type(Key.ENTER)
                if exists(ProcessAppPath + r"\Pro_MdxPro.png", 1):
                    if exists(ProcessAppPath + r"\Btn_OK2.png", 1):
                        click(ProcessAppPath + r"\Btn_OK2.png")
                else:
                    pass

        print ("def ProcessWizard_Rotating_Angularspeed_Profile_Section_Value is Finished")
        Log.write_log("Process", "Info: def ProcessWizard_Rotating_Angularspeed_Profile_Section_Value is Finished")
        return True
    except:
        print ("def ProcessWizard_Rotating_Angularspeed_Profile_Section_Value is Failed")
        Log.write_log("Process", "Error: def ProcessWizard_Rotating_Angularspeed_Profile_Section_Value is Failed")
        sys.exit()
        return False

def ProcessWizard_Barrel_Temperature_Profile_Section_Value(Profilelist, ProcessAppPath):
    """
    #Edit Process Barrel Temperature Profile Setting Tab
    """
    try:
        if (len(Profilelist) < 2):
            print ("Not Enough Arguments")
            Log.write_log("Process", "Error: Not Enough Arguments")
            sys.exit()
            return False
        else:
            NumberofHeaters = Pattern(ProcessAppPath + r"\Pro_Barrel_NumberofHeaters.png").similar(0.95).targetOffset(100, 0)            
            if (exists(NumberofHeaters) <> None):
                click(NumberofHeaters)
                type("a",Key.CTRL)
                type(str(len(Profilelist)-2))
            i = 1            
            ScrollBar = exists(Pattern(ProcessAppPath + r'\Pro_Barrel_ScrollBar.png').similar(0.95))
            while i < len(Profilelist): #Edit Profile Section Value(s)
                if (i == 1):
                    x = Pattern(ProcessAppPath + r"\Pro_Barrel_SectionNozzle.png").similar(0.95).targetOffset(0, 20)
                    Profile = Profilelist[1]
                else:
                    lastsection = exists(Pattern(ProcessAppPath + (r"\Pro_Barrel_Section%s.png") %(i-1)).similar(0.95))
                    if (lastsection == None and ScrollBar <> None):
                        mouseMove(Location(ScrollBar.x + 200, ScrollBar.y + 10))
                        mouseDown(Button.LEFT)
                        mouseMove(Location(ScrollBar.x + 500, ScrollBar.y))
                        mouseUp(Button.LEFT)                
                    x = Pattern(ProcessAppPath + (r"\Pro_Barrel_Section%s.png") %(i-1)).similar(0.95).targetOffset(0, 20)
                    Profile = Profilelist[i]
                i += 1
                doubleClick(x)
                type(Key.F2)
                type("a",Key.CTRL)
                type(Profile)
                type(Key.ENTER)
                if exists(ProcessAppPath + r"\Pro_MdxPro.png", 1):
                    if exists(ProcessAppPath + r"\Btn_OK2.png", 1):
                        click(ProcessAppPath + r"\Btn_OK2.png")
                else:
                    pass

            click(ProcessAppPath + r'\Btn_OK3.png')

        print ("def ProcessWizard_Barrel_Temperature_Profile_Section_Value is Finished")
        Log.write_log("Process", "Info: def ProcessWizard_Barrel_Temperature_Profile_Section_Value is Finished")
        return True
    except:
        print ("def ProcessWizard_Barrel_Temperature_Profile_Section_Value is Failed")
        Log.write_log("Process", "Error: def ProcessWizard_Barrel_Temperature_Profile_Section_Value is Failed")
        sys.exit()
        return False

def ProcessWizard_FillingPacking_Profile_Type_Switch(TypePic, ProcessAppPath):
    """
    Change Tab FillingPacking Profile Type
    """
    try:
        if exists(ProcessAppPath + r"\Pro_Type.png", 10):
            click(Pattern(ProcessAppPath + r"\Pro_Type.png").similar(0.90).targetOffset(120,0))
            click(ProcessAppPath + TypePic)
        print ("def ProcessWizard_FillingPacking_Profile_Type_Switch is Finished")
        Log.write_log("Process", "Info: def ProcessWizard_FillingPacking_Profile_Type_Switch is Finished")
        return True
    except:
        print ("def ProcessWizard_FillingPacking_Profile_Type_Switch is Failed")
        Log.write_log("Process", "Error: def ProcessWizard_FillingPacking_Profile_Type_Switch is Failed")
        sys.exit()
        return False
        
def ProcessWizard_Advanced_Tab_Switch(NextTab, ProcessAppPath):
    """
    #Change Process Wizard Tab from Current Tab to Next Tab
    #Argument: Tab Picture(s)
    """
    try:
        if exists(ProcessAppPath + NextTab):
            click(ProcessAppPath + NextTab)
        print ("def ProcessWizard_Advanced_Tab_Switch is Finished")
        Log.write_log("Process", "Info: def ProcessWizard_Advanced_Tab_Switch is Finished")
        return True
    except:
        print ("def ProcessWizard_Advanced_Tab_Switch is Failed")
        Log.write_log("Process", "Error: def ProcessWizard_Advanced_Tab_Switch is Failed")
        sys.exit()
        return False
    
def ProcessWizard_Summary_Finish(ProcessAppPath):
    #Click Finish Button and Close Process Wizard
    try:
        i = 0
        if (exists(ProcessAppPath + r"\Pro_Tab_Summary.png") or exists(ProcessAppPath + r"\Pro_Tab_Cooling.png")):
            #xists(Pattern(NextTab).similar(0.95)
            while (not exists(ProcessAppPath + r"\Btn_OK2.png", 2) and i < 3):
                i += 1
                click(ProcessAppPath + r"\Btn_Pro_Finish.png")
        else:
            print ("Find Pro_Tab_Summary is Failed")
            Log.write_log("Process", "Error: def Pro_Tab_Summary is Failed")
            sys.exit()
            return False
        click(ProcessAppPath + r"\Btn_OK2.png")
        print ("def ProcessWizard_Summary_Finish is Finished")
        Log.write_log("Process", "Info: def ProcessWizard_Summary_Finish is Finished")
        return True
    except:
        print ("def ProcessWizard_Summary_Finish is Failed")
        Log.write_log("Process", "Error: def ProcessWizard_Summary_Finish is Failed")
        sys.exit()
        return False
 
def ProcessWizardTypeChange(CurrentTtype, NewType):
    #Change Process Wizard Type from Current Tab to Next Type
    #Argument: Type picture
    try:
        if exists(CurrentTtype):
            x = find(NewType)
            click(x)
        print ("def ProcessWizardTypeChange is Finished")
        Log.write_log("Process", "Info: def ProcessWizardTypeChange is Finished")
        return True
    except:
        print ("def ProcessWizardTypeChange is Failed")
        Log.write_log("Process", "Error: def ProcessWizardTypeChange is Failed")
        sys.exit()
        return False

def ValueSetting(ItemPic, offsetx, offsety, ItemValue, ProcessAppPath):
    """
    #Setting Process UI Value
    #Argument
    #ItemPic: select item picture
    #offsetx, offsety: ItemPic offset position
    #ItemValue: the item value
    """
    try:
        i = 0
        while not exists (Pattern(ItemPic).similar(0.97).targetOffset(offsetx, offsety), 2) and i < 10:
            type(Key.PAGE_DOWN)
            i += 1
        x = wait(Pattern(ItemPic).similar(0.97).targetOffset(offsetx, offsety), 10)
        click(x)
        type(Key.F2)
        type("a",Key.CTRL)
        type(ItemValue)
        #124914
        if ("Pro_SectionNo.png" not in ItemPic and "Pro_Plasticizing_BackPressure.png" not in ItemPic  and "Pro_Plasticizing_ScrewSpeed.png" not in ItemPic):
            type(Key.ENTER)
        if exists(ProcessAppPath + r"\Pro_MdxPro.png", 1): #if found the warrning message
            if exists(ProcessAppPath + r"\Btn_OK2.png", 1):
                click(ProcessAppPath + r"\Btn_OK2.png")
        print ("def ValueSetting {} is Finished".format(ItemPic))          
        Log.write_log("Process", "Info: def ValueSetting {} is Finished".format(ItemPic))
        return True
    except:
        print ("def ValueSetting {} is Failed".format(ItemPic))
        Log.write_log("Process", "Error: def ValueSetting {} is Failed".format(ItemPic))
        sys.exit()
        return False

def InsetValueSetting(ProcessAppPath, ItemPic, ItemValue):
    try:
        while (exists(os.path.join(ProcessAppPath, ItemPic + ".png"))):
            click(os.path.join(ProcessAppPath, ItemPic + ".png"))
            type(Key.F2)
            click(os.path.join(ProcessAppPath, r"Userdefined.png"))
            type("a",Key.CTRL)
            type(ItemValue)
            type(Key.ENTER)
            if exists(ProcessAppPath + r"\Pro_MdxPro.png", 1): #if found the warrning message
                if exists(ProcessAppPath + r"\Btn_OK2.png", 1):
                    click(ProcessAppPath + r"\Btn_OK2.png")
        print ("def InsetValueSetting {} is Finished".format(ItemPic))
        Log.write_log("Process", "Info: def ProcessWizardTypeChange {} is Finished".format(ItemPic))
        return True
    except:
        print ("def InsetValueSetting {} is Failed".format(ItemPic))
        Log.write_log("Process", "Error: def ProcessWizardTypeChange {} is Failed".format(ItemPic))
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
        Log.write_log("Process", ("Info: def Click_IconEx is Finished"))
        return True
    except:
        print ("def Click_IconEx is Failed")
        Log.write_log("Process", ("Error: def Click_IconEx is Failed"))
        sys.exit()
        return False

def Click_Icon(Btn, CurrentTab):
    """
    #Click Cooling Advanced Setting
    #Argument
    #Btn: Btn picture
    #CurrentTab: Advanced UI picture
    """
    try:
        if exists(Btn):
            click(Btn)
            while (not exists(CurrentTab, 5)):
                click(Btn)
        else:
            print ("NOT Found %s" %(Btn))
            Log.write_log("Process", ("Error: NOT Found %s") %(Btn))
            sys.exit()
            return False
        print ("def Click_Icon %s is Finished" %(Btn))
        Log.write_log("Process", ("Info: Click_Icon %s is Finished") %(Btn))
        return True
    except:
        print ("def Click_Icon %s is Failed" %(Btn))
        Log.write_log("Process", ("Error: def Click_Icon %s is Failed") %(Btn))
        sys.exit()
        return False

def SelectMoldMetalMaterial(MoldmetalIDPic, offsetx, offsety, MaterialPic):
    """
    Select Cooling Mold Metal Material
    """
    try:
        if exists(MoldmetalIDPic):
            click(Pattern(MoldmetalIDPic).targetOffset(offsetx, offsety))
            type(Key.F2)
        while not exists(Pattern(MaterialPic).similar(0.99)):
            type(Key.PAGE_DOWN)
        click(Pattern(MaterialPic).similar(0.99))
        print ("def SelectMoldMetalMaterial is Finished")
        Log.write_log("Process", "Info: def SelectMoldMetalMaterial is Finished")
        return True
    except:
        print ("def SelectMoldMetalMaterial is Failed")
        Log.write_log("Process", "Error: def SelectMoldMetalMaterial is Failed")
        sys.exit()
        return False

def mousemove(position, offsetx, offsety):
    try:
        B1 = find(position)
        if (B1 <> None):
            hover(Location(B1.x + offsetx, B1.y + offsety))
        else:
            print ("cannot find position ()".format(position))
            Log.write_log("Process", "Error: cannot find position {}".format(position))
            sys.exit()
            return False               
        print ("def mousemove to {} is Finished".format(position))
        Log.write_log("Process", "Info: def mousemove to {} is Finished".format(position))
        return True
    except:
        print ("def mousemove to {} is Failed".format(position))
        Log.write_log("Process", "Error: def mousemove to {} is Failed".format(position))
        sys.exit()
        return False        

def pageupanddown(direction, times):
    """
    #UI Page up or down and time(s)
    """
    try:
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
    except:
        print ("def pageupanddown is Failed")
        Log.write_log("Common", ("Error: def pageupanddown is Failed"))
        sys.exit()
        return False

def Wait_Dialog(Pic):
    """
    #Wait Specific Dialog
    #MeshPic: eDesign -> r"\Log_Generate_Solid_Mesh_Done.png"; Solid Cool -> r"\Studio_FinalCheck.png"; Fast Cool -> r"\Studio_Runner_Check.png"
    """
    try:
        i = 0
        while not exists(Pattern(Pic).similar(0.90), 30) and i < 30:
            wait(3)
            i += 1            
        if exists(Pic):
            print ("def Wait_Dialog is Finished")
            Log.write_log("Process", "Info: def Wait_Dialog is Finished")
            return True
        else:
            print ("def Wait_Dialog is Failed")
            Log.write_log(("Process", "Error: def Wait_Dialog not find {}").format(Pic))
            return False
    except:
        print ("def Wait_Dialog is Failed")
        Log.write_log("Process", "Error: def Wait_Dialog is Failed")
        sys.exit()
        return False

ProcessAppPath = r"C:\Users\Administrator\Desktop\MDX_SAM\sikuli_Share\Process.sikuli"
#Profilelist = [ProcessAppPath + r"\Btn_Pro_Flow_rate_profile.png", ProcessAppPath + r"\Pro_Filling_FlowRateProFile.png", "3", "25", "12.5", "50", "25", "100", "50"]
Profilelist = [ProcessAppPath + r"\Btn_Pro_Flow_rate_profile.png", ProcessAppPath + r"\Pro_Filling_FlowRateProFile.png", "1", "100", "50"]
"""
Click_Icon(ProcessAppPath + r"\Btn_Setting.png", ProcessAppPath + r"\Pro_MoldPreheatSetting.png")
ValueSetting(ProcessAppPath + r"\Pro_MaxPreheatTime.png", 100, 0, "250", ProcessAppPath)
ValueSetting(ProcessAppPath + r"\Pro_EC1.png", 190, 0, "120", ProcessAppPath)
Click_Icon(ProcessAppPath + r"\Btn_ApplyCurrentSettingToAll.png", ProcessAppPath + r"\Pro_MoldPreheatSetting.png")
Click_Icon(ProcessAppPath + r"\Btn_OK.png", ProcessAppPath + r"\Pro_Tab_Cooling.png")
ProcessWizard_Tab_Next(ProcessAppPath + r"\Pro_Tab_Cooling.png", ProcessAppPath + r"\Pro_Tab_Summary.png", ProcessAppPath)
Click_Icon(ProcessAppPath + r"\Btn_CoolingHeating.png", ProcessAppPath + r"\Pro_CoolingAdvancedSetting.png")
ValueSetting(ProcessAppPath + r"\Pro_EC1_2.png", 80, 0, "80", ProcessAppPath)
Click_Icon(ProcessAppPath + r"\Btn_ApplyCurrentSettingToAll.png", ProcessAppPath + r"\Pro_Tab_Cooling.png")
Click_Icon(ProcessAppPath + r"\Btn_OK.png", ProcessAppPath + r"\Pro_Tab_Cooling.png")
"""

def Select_Machine_Setting_Advanced(ProcessAppPath, Type, Path):
    try:
        if exists(ProcessAppPath + r"\Pro_Machine_Advanced.png", 10):
            Click_IconEx(ProcessAppPath + r"\Pro_Machine_Advanced.png")
            if Type == "Import":
                Click_IconEx(ProcessAppPath + r"\Pro_Machine_Import.png")
                x = Pattern(ProcessAppPath + r"\pro_file_name.png").similar(0.9).targetOffset(30,0)
                click(x)
                paste(Path)
                type(Key.ENTER)
            elif Type == "Search":
                Click_IconEx(ProcessAppPath + r"\Pro_Machine_Search.png")
            print ("def Select_Machine_Setting_Advanced is Finished")
        else:
            print ("def Select_Machine_Setting_Advanced is Failed. The Advanced Icon is not exists.")
    except:
        print ("def Select_Machine_Setting_Advanced is Failed")
        Log.write_log("Process", "Error: def Select_Machine_Setting_Advanced is Failed")
        sys.exit()

def PlasticizingSetting(ProcessAppPath, **sikuliarg):
    try:
        Click_IconEx(ProcessAppPath + r"\Btn_AdvancedSetting.png")
        Click_IconEx(ProcessAppPath + r"\Tab_AdvancedSetting_Plasticizing.png")
        if sikuliarg:
            if "BackPressure" in sikuliarg:
                ValueSetting(ProcessAppPath + r"\Pro_Plasticizing_BackPressure.png", 120, 0, sikuliarg["BackPressure"], ProcessAppPath)
            if "ScrewSpeed" in sikuliarg:
                ValueSetting(ProcessAppPath + r"\Pro_Plasticizing_ScrewSpeed.png", 120, 0, sikuliarg["ScrewSpeed"], ProcessAppPath)
            if "BarrelTemperature" in sikuliarg:
                Click_IconEx(ProcessAppPath + r"\Btn_Plasticizing_Edit.png")
        print ("def PlasticizingSetting is Finished")
    except:
        print ("def PlasticizingSetting is Failed")
        Log.write_log("Process", "Error: def PlasticizingSetting is Failed")
        sys.exit()