from sikuli import *
from time import sleep
import sys, os
CMXAppPath = r"../../sikuli_Share/CMX.sikuli"
LogAppPath = r"../sikuli_Share/Common.sikuli"
sys.path.append(LogAppPath)
import log_record as Log

def CMX_Tab_Change(NextTab):
    #Change Computatation Wizard Tab from Current Tab to Other Tab
    #Argument: Tab Picture
    try: 
        i=0            
        while not exists(NextTab, 2)and i<5:
            
            click(CMXAppPath + r"\CMX_Btn_Right.png")
            i+=1
        click(NextTab)
        wait(NextTab, 10)
        #else:
            #print ("Cannot find %s" %(NextTab))
            #Log.write_log("CMX", ("Error: Cannot find %s") %(NextTab))
            #sys.exit()
           # return False
        print ("def CMX_Tab_Change is Finished")
        Log.write_log("CMX", "Info: def CMX_Tab_Change is Finished")
        return True
    except:
        print ("def CMX_Tab_Change is Failed")
        Log.write_log("CMX", "Error: def CMX_Tab_Change is Failed")
        sys.exit()
        return False
 
def Checkbox(ItemPic, offsetx, offsety, CMXAppPath):
    #Check / Unchkecbox
    #SolverTypePic:
    #Argument: All the CMX Selection Item Picture(s)
    try:
        if "Flow" in ItemPic:
            mouseMove(Pattern(CMXAppPath + r"\CMX_Flow_Solver.png").targetOffset(200, 300)) #Move Mouse to Solver: Place
        elif "Warp" in ItemPic:
            mouseMove(Pattern(CMXAppPath + r"\CMX_Warp_Solver2.png").targetOffset(345, 0)) #Move Mouse to Solver: Place
        while not exists(ItemPic, 1):
            wheel(WHEEL_DOWN, 3)
            #type(Mouse.WHEEL_DOWN)
        click(Pattern(ItemPic).targetOffset(offsetx, offsety))
        print ("def Checkbox is Finished")
        Log.write_log("CMX", "Info: def Checkbox is Finished")
        return True
    except:
        print ("def Checkbox is Failed")
        Log.write_log("CMX", "Error: def Checkbox is Failed")
        sys.exit()
        return False

def ClickButton(CMXAppPath, ButtonPic):
    """
    Click Button
    Argument: Buttone Icon Picture
    """
    try:
        if ("CMX_Cooling_AccurancyLevel" in ButtonPic):
            Cooling_AccurancyLevel = Pattern(CMXAppPath + r"\CMX_Cooling_AccurancyLevel.png").similar(0.90)
            DataEditor_AccuracyLevel = Pattern(CMXAppPath + r"\CMX_DataEditor_AccuracyLevel.png").similar(0.90)
            mouseMove(Pattern(CMXAppPath + r"\CMX_Tab_Cool.png").similar(0.80).targetOffset(0, 150)) #Move Mouse to Solver: Place
            while not exists (Cooling_AccurancyLevel):
                wheel(WHEEL_DOWN, 3)
            if not exists(Pattern(ButtonPic).similar(0.90), 1):
                doubleClick(Cooling_AccurancyLevel.targetOffset(310, 0))
                if exists(DataEditor_AccuracyLevel):
                    click(DataEditor_AccuracyLevel.targetOffset(100, 0))
                    if ("Standard" in ButtonPic):
                        click(CMXAppPath + r"\CMX_DataEditor_Standard.png")
                    else:
                        click(CMXAppPath + r"\CMX_DataEditor_Dense.png")
                    click(DataEditor_AccuracyLevel.targetOffset(110, 140))
                    print ("Change %s is Finished" %(ButtonPic))
                    Log.write_log("CMX", ("Info: Change %s is Finished") %(ButtonPic))
                    return True
                else:
                    print ("Change %s is Failed" %(ButtonPic))
                    Log.write_log("CMX", ("Error: Change %s is Failed") %(ButtonPic))
                    return False
            else:
                print ("AccuracyLevel is the same as required")
                Log.write_log("CMX", "Info: AccuracyLevel is the same as required")
                return True
        else:
            if ("CMX_DLG_Moldex3DStudio" in ButtonPic):
                click(Pattern(ButtonPic).similar(0.98).targetOffset(260,120))
            elif exists(Pattern(ButtonPic).similar(0.85), 10):
                click(ButtonPic)
                if(exists(Pattern(CMXAppPath + r"\CMX_inconsistent.png").similar(0.8),2)):
                    click(Pattern(CMXAppPath + r"\Studio_Reset_Inconsistent.png").similar(0.8).targetOffset(-125,0))
                    click(Pattern(CMXAppPath + r"\Remark_ok.png").similar(0.7))
            else:
                print ("NOT Found %s" %(ButtonPic))
                Log.write_log("CMX", ("Error: NOT Found %s") %(ButtonPic))
                return False
        print ("def ClickButton %s is Finished" %(ButtonPic))
        Log.write_log("CMX", ("Info: def ClickButton %s is Finished") %(ButtonPic))
        return True
    except:
        print ("def ClickButton %s is Failed" %(ButtonPic))
        Log.write_log("CMX", ("Error: def ClickButton %s is Failed") %(ButtonPic))
        sys.exit()
        return False
    
def SelectDropDownMenu(ItemPic, offsetx, offsety, PickupPic, offsetx2, offsety2):
    """
    Select Drop Down Menu
    Argument
    ItemPic: Item select picture
    offsetx, offsety: Item offset position
    PickupPic: Item select blue picture
    offsetx2, offsety2: offsety: PickupPic offset position
    """
    try:
        if exists(ItemPic):
            x = wait(Pattern(ItemPic).targetOffset(offsetx, offsety), 5)
            click(x)
        while not exists(Pattern(PickupPic).similar(0.95),1):
            #keyDown()
            type(Key.DOWN)
        click(Pattern(PickupPic).similar(0.95).targetOffset(offsetx2, offsety2), 5)
        print ("def SelectDropDownMenu is Finished")
        Log.write_log("CMX", "Info: def SelectDropDownMenu is Finished")
        return True
    except:
        print ("def SelectDropDownMenu is Failed")
        Log.write_log("CMX", "Error: def SelectDropDownMenu is Failed")
        sys.exit()
        return False

def ValueSetting(ItemPic, offsetx, offsety, ItemValue):
    """
    Setting CMX UI Value
    Argument
    ItemPic: Item select picture
    offsetx, offsety: Item offset position
    ItemValue: Item setting value
    """
    try:
        while not exists (ItemPic, 2):
            type(Key.PAGE_DOWN)
        x = Pattern(ItemPic).similar(0.97).targetOffset(offsetx, offsety)
        click(x)
        #if not exists("CMX_Tab_VEOptics.png", 1):
        #    doubleClick(x)
        i = 0
        while i <= 2:
            type(Key.BACKSPACE)
            i = i + 1
        type(ItemValue)
        type(Key.ENTER)
        print ("def ValueSetting is Finished")
        Log.write_log("CMX", "Info: def ValueSetting is Finished")
        return True
    except:
        print ("def ValueSetting is Failed")
        Log.write_log("CMX", "Error: def ValueSetting is Failed")
        sys.exit()
        return False

def FPSolverTypeChange(ItemPic, stype):
    """
    #Select Tab FP Solver Type
    #Argument ItemPic = CMXAppPath + r"\CMX_Flow_Solver.png"
    #Argument stype = "Standard" or "Enhanced" or "VF"
    """
    try:
        x = Pattern(ItemPic).targetOffset(40,0)
        if ((stype != "Standard") and (stype != "Enhanced") and (stype != "VF")):
            print ("The argument %s is wrong." %(stype))
            sys.exit()
            return False
        elif exists(x, 5):
            click (x)
            type(Key.UP*2)
        if stype == "Standard":
            pass
        elif stype == "Enhanced":
            type(Key.DOWN*1)
        elif stype == "VF":
            type(Key.DOWN*2)       
        click (x)
        print ("def FPSolverTypeChange is Finished")
        Log.write_log("CMX", "Info: def FPSolverTypeChange is Finished")
        return True
    except:
        print ("def FPSolverTypeChange is Failed")
        Log.write_log("CMX", "Error: def FPSolverTypeChange is Failed")
        sys.exit()
        return False

def WarpSolverTypeChange(ItemPic, stype):
    """
    #Select Tab Warp Solver Type
    #Argument ItemPic = CMXAppPath + r"\CMX_Warp_Solver.png"
    #Argument stype = "Standard" or "Enhanced" or "Nonlinear"
    """
    try:
        x = Pattern(ItemPic).targetOffset(40,0)
        if ((stype != "Standard") and (stype != "Enhanced") and (stype != "Nonlinear")):
            print ("The argument %s is wrong." %(stype))
            sys.exit()
            return False
        elif exists(x, 5):
            click (x)
            type(Key.UP*2)
        if stype == "Standard":
            pass
        elif stype == "Enhanced":
            type(Key.DOWN*1)
        elif stype == "Nonlinear":
            type(Key.DOWN*2)       
        click (x)
        print ("def WarpolverTypeChange is Finished")
        Log.write_log("CMX", "Info: def WarpSolverTypeChange is Finished")
        return True
    except:
        print ("def WarpSolverTypeChange is Failed")
        Log.write_log("CMX", "Error: def WarpSolverTypeChange is Failed")
        sys.exit()
        return False
def SetRuducedmesh(ProjectPath, CMXAppPath):
    try:
        print(1)
        if exists(CMXAppPath + r"\CMX_Select.png", 10):
            click(Pattern(CMXAppPath + r"\CMX_Select.png").similar(0.8))
            print(2)
            if exists(CMXAppPath + r"\CMX_FileName.png", 10):
                click(CMXAppPath + r"\CMX_FileName.png")
                print(3)
                paste(ProjectPath)
                click(CMXAppPath + r"\CMX_File_Open.png")
        print("def SetRuducedmes is Finished")
        Log.write_log("Studio", "Info: def SetRuducedmes is Finished")
        return True
    except:
        print("def SetRuducedmes is Failed")
        Log.write_log("Studio", "Error: def SetRuducedmes is Failed")
        sys.exit()
        return False                 

def StressAnalysisType(ItemPic, stresstype):
    """
    #Select Tab Warp Solver Type
    #Argument ItemPic = CMXAppPath + r"\.png"
    #Argument type = "Stress" or "Annealing"
    """
    try:
        x = Pattern(ItemPic).targetOffset(375,0)
        if ((stresstype != "Stress") and (stresstype != "Annealing")):
            print ("The argument %s is wrong." %(stresstype))
            sys.exit()
            return False
        elif exists(x, 5):
            click (x)
            type(Key.UP*1)
        if stresstype == "Stress":
           pass
        elif stresstype == "Annealing":
            type(Key.DOWN*1)

        click (x)
        print(4)
        print ("def StressAnalysisType is Finished")
        Log.write_log("CMX", "Info: def StressAnalysisType is Finished")
        return True
    except:
        print ("def StressAnalysisType is Failed")
        Log.write_log("CMX", "Error: def StressAnalysisType is Failed")
        sys.exit()
        return False  


def sethotrunnerpressure(*gatepressure):
    """
    give gatepressure(Mpa) 
    give Gate picture
    ex: sethotrunnerpressure("4",Pattern(CMXAppPath + r"\Gate_1_1.png").similar(0.9).targetOffset(165,0), Pattern(CMXAppPath + r"\Gate_2_1.png").similar(0.9).targetOffset(165,0))
    """
    try:
        if len(gatepressure)!=0:
            counter=1
            while counter<len(gatepressure)+1:  
                click(Pattern(CMXAppPath + r"\Gate_"+ str(counter) + ".png").similar(0.95).targetOffset(165,0))
                type(gatepressure[counter-1])
                counter+=1
        else:
              click(CMXAppPath + r"\Studio_Default.png")
        Log.write_log("CMX", "Info: def sethotrunnerpressure is Finished")
        return True
    except:
        print ("def sethotrunnerpressure is Failed")
        Log.write_log("CMX", "Error: def sethotrunnerpressure is Failed")
        sys.exit()
        return False  
    
def coreshiftcalculation(coreshifttype):
    """
    #Select Tab Warp Solver Type
    #Argument ItemPic = CMXAppPath + r"\.png"
    #Argument type = "Stress" or "Annealing"
    """
    try:
        if(exists(Pattern(CMXAppPath + r"\CMX_coreshift.png").similar(0.95).targetOffset(-64,0))):
            click(Pattern(CMXAppPath + r"\CMX_coreshift.png").similar(0.95))
        if(exists(Pattern(CMXAppPath + r"\CMX_Btn_Down.png").similar(0.9))):
            click(Pattern(CMXAppPath + r"\CMX_Btn_Down.png").similar(0.9))
            if (coreshifttype == "two_way"):
                type(Key.DOWN*1)
       
            elif (coreshifttype == "one_way"):
                type(Key.UP*1)
            else:
                print("The argument %s is wrong." %(coreshifttype))
                sys.exit()
                return False
            click(Pattern(CMXAppPath + r"\CMX_Btn_Down.png").similar(0.9))
    except:
        print ("def StressAnalysisType is Failed")
        Log.write_log("CMX", "Error: def StressAnalysisType is Failed")
        sys.exit()
        return False  