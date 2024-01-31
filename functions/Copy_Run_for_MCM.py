from sikuli import *
import sys, os
LogAppPath = r"../sikuli_Share/Common.sikuli"

sys.path.append(LogAppPath)

import log_record as Log


#-----Choose Copy Run-----# 
def Copy_Run(RunID, Copytype, Result, SwitchNewRun, Copypath):    
    try:
        rightClick(RunID)
        wait(1)
        click(Copypath + "\\CopyRun_icon.png")
        wait(Copypath + "\\CopyRun_title.png",5)
        Choose_type(Copytype, SwitchNewRun, Copypath)
        click(Copypath + "\\CopyRun_ok.png")
        wait(Copypath + "\\CheckUpdateRun.png", 5)
        Log.write_log("Copy Run", "Info: Copy Run done!")
        return True
    except:
        Log.write_log("Copy Run", "Error: Copy Run failed!")
        sys.exit()
        return False
#-----Choose Copy Type-----#
def Choose_type(Copytype, SwitchNewRun, Copypath):
    try:
        if Copytype == "RunInputDataOnly":
            click(Copypath + "\\RunInputDataOnly.png")
            wait(1)
            SwitchRun(SwitchNewRun, Copypath)
        elif Copytype == "FullRunData":
            click(Copypath + "\\FullRunData.png")
            wait(1)
            SwitchRun(SwitchNewRun, Copypath)     
        elif Copytype == "Customize":
            click(Copypath + "\\Customize.png")
            SelectResult(Result, Copypath)
        wait(5)
        Log.write_log("Copy Run", "Info: Choose {} done!".format(Copytype))
        return True
    except:
        Log.write_log("Copy Run", "Error: Choose {} failed!".format(Copytype))
        sys.exit()
        return False    
#-----Switch new run or not-----#    
def SwitchRun(SwitchNewRun, Copypath):
    try:
        if SwitchNewRun == Copypath + "\\Dont_switch_new_run.png":
            click(SwitchNewRun)
            wait(1)
            Log.write_log("Copy Run", "Info: Switch new run done!")
        else:
            Log.write_log("Copy Run", "Info: Do not switch new run done!")
            pass
        return True
    except:
        Log.write_log("Copy Run", "Error: Switch run failed!")
        sys.exit()
        return False
        
#-----Choose Copy Result-----#
def SelectResult(Result, Copypath):
    try:
        #default
        if Result == "default":
            pass
        #Filling
        if Result == "Filling":
            if exists(Pattern(Copypath + "\\Packing.png").similar(0.72)):
                click(Pattern(Copypath + "\\Packing.png").similar(0.72))
                wait(1)
            if exists(Pattern(Copypath + "\\Cooling.png").similar(0.72)):
                click(Pattern(Copypath + "\\Cooling.png").similar(0.72))
                wait(1)
            if exists(Copypath + "\\Warpage.png"):
                click(Copypath + "\\Warpage.png")
                wait(1)
        #Packing
        if Result == "Packing":
            if exists(Pattern(Copypath + "\\Filling.png").similar(0.76)):
                click(Pattern(Copypath + "\\Filling.png").similar(0.76))
                wait(1)
            if exists(Pattern(Copypath + "\\Cooling.png").similar(0.72)):
                click(Pattern(Copypath + "\\Cooling.png").similar(0.72))
                wait(1)
            if exists(Copypath + "\\Warpage.png"):
                click(Copypath + "\\Warpage.png")
                wait(1)
        #Cooling
        if Result == "Cooling":
            if exists(Pattern(Copypath + "\\Filling.png").similar(0.76)):
                click(Pattern(Copypath + "\\Filling.png").similar(0.76))
                wait(1)
            if exists(Pattern(Copypath + "\\Packing.png").similar(0.72)):
                click(Pattern(Copypath + "\\Packing.png").similar(0.72))
                wait(1)
            if exists(Copypath + "\\Warpage.png"):
                click(Copypath + "\\Warpage.png")
                wait(1)
        #Warpage
        if Result == "Warpage":
            if exists(Pattern(Copypath + "\\Filling.png").similar(0.76)):
                click(Pattern(Copypath + "\\Filling.png").similar(0.76))
                wait(1)
            if exists(Pattern(Copypath + "\\Packing.png").similar(0.72)):
                click(Pattern(Copypath + "\\Packing.png").similar(0.72))
                wait(1)
            if exists(Pattern(Copypath + "\\Cooling.png").similar(0.72)):
                click(Pattern(Copypath + "\\Cooling.png").similar(0.72))
                wait(1)
        #F_P
        if Result == "F_P":
            if exists(Pattern(Copypath + "\\Cooling.png").similar(0.72)):
                click(Pattern(Copypath + "\\Cooling.png").similar(0.72))
                wait(1)
            if exists(Copypath + "\\Warpage.png"):
                click(Copypath + "\\Warpage.png")
                wait(1)
        #F_P_C
        if Result == "F_P_C":
            if exists(Copypath + "\\Warpage.png"):
                click(Copypath + "\\Warpage.png")
                wait(1)
        #F_C
        if Result == "F_C":
            if exists(Pattern(Copypath + "\\Packing.png").similar(0.72)):
                click(Pattern(Copypath + "\\Packing.png").similar(0.72))
                wait(1)
            if exists(Copypath + "\\Warpage.png"):
                click(Copypath + "\\Warpage.png")
                wait(1)
        print("Info: Choose Result({}) done!".format(Result))
        Log.write_log("Copy Run", "Info: Choose Result({}) done!".format(Result))
        return True
    except:
        print("Error: Choose Result({}) failed!".format(Result))
        Log.write_log("Copy Run", "Error: Choose Result({}) failed!".format(Result))
        sys.exit()
        return False

"""
if __name__ == "__main__":
    Run01 = Pattern("Run01.png").similar(0.92)
    Run02 = Pattern("Run02.png").similar(0.94)
    Run03 = Pattern("Run03.png").similar(0.94)
    Run04 = Pattern("Run04.png").similar(0.94)
    Run05 = Pattern("Run05.png").similar(0.92)
    Run_list = [Run01, Run02, Run03, Run04, Run05]
    RunInputDataOnly = "RunInputDataOnly.png"
    FullRunData = "FullRunData.png"
    Customize = "Customize.png"
    Copytype_list = [RunInputDataOnly, FullRunData, Customize]
    Filling = Pattern("Filling.png").similar(0.76)
    Packing = Pattern("Packing.png").similar(0.72)
    Cooling = Pattern("Cooling.png").similar(0.72)
    Warpage = "Warpage.png"
    Result_list = ["default", Filling, Packing, Cooling, Warpage, "F_P", "F_P_C", "F_C"]
    Switch_Run = ["default", "Dont_switch_new_run.png"]

#==========User Input==========#
#-----Choose Copy Run-----#  
    #0 = Run01
    #1 = Run02
    #2 = Run03
    #3 = Run04
    #4 = Run05
    RunID = Run_list[0]
#-----Choose Copy Type-----#
    #0 = RunInputDataOnly
    #1 = FullRunData
    #2 = Customize
    Copytype = Copytype_list[0]
#-----Choose Copy Result-----#
    #0 = default
    #1 = Filling
    #2 = Packing
    #3 = Cooling
    #4 = Warpage
    #5 = F_P
    #6 = F_P_C
    #7 = F_C
    Result = Result_list[0]
#-----Switch new run or not-----#
    #0 = default
    #1 = don't switch
    SwitchNewRun = Switch_Run[0]

#==========Run Function==========#
    Copy_Run(RunID, Copytype, Result, SwitchNewRun)

"""
#Copypath = r"C:\Users\Administrator\Desktop\eDesign\test.sikuli\Copy_Run_for_MCM.sikuli"
#Copy_Run(Pattern(Copypath + "\\Run01.png").similar(0.92), "RunInputDataOnly", "default", "default", Copypath)