from sikuli import *
import sys, os
CRNpath = r"C:\Users\Administrator\Desktop\eDesign\test.sikuli\Change_Remark_Name.sikuli"
LogAppPath = r"../sikuli_Share/Common.sikuli"

sys.path.append(LogAppPath)

import log_record as Log
"""
Run01 = Pattern(CRNpath + "\\Run01.png").similar(0.92)
Run02 = Pattern(CRNpath + "\\Run02.png").similar(0.94)
Run03 = Pattern(CRNpath + "\\Run03.png").similar(0.94)
Run04 = Pattern(CRNpath + "\\Run04.png").similar(0.94)
Run05 = Pattern(CRNpath + "\\Run05.png").similar(0.92)
Run_list = [Run01, Run02, Run03, Run04, Run05]
"""

def CRN(RunID, Remark_name, CRNpath):
    i = 0
    rightClick(RunID)
    if exists((CRNpath + r"\EditRemark_icon.png"), 3):
        click(CRNpath + r"\EditRemark_icon.png")
    wait(CRNpath + r"\Remark_title.png",3)
    type(Pattern(CRNpath + r"\Remark_input.png").targetOffset(-1,-16),"a",Key.CTRL)
    type(Key.DELETE)
    while exists(Pattern(CRNpath + r"\Remark_Empty.png").similar(0.90), 1) and i <= 2:        
        paste(Remark_name)
    click(CRNpath + r"\Remark_ok.png")



def Run(Remark_name, CRNpath):
    try:
        Run01 = Pattern(CRNpath + r"\Run01.png").similar(0.92)
        Run02 = Pattern(CRNpath + r"\Run02.png").similar(0.94)
        Run03 = Pattern(CRNpath + r"\Run03.png").similar(0.94)
        Run04 = Pattern(CRNpath + r"\Run04.png").similar(0.94)
        Run05 = Pattern(CRNpath + r"\Run05.png").similar(0.92)
        Run06 = Pattern(CRNpath + r"\Run06.png").similar(0.95)
        Run07 = Pattern(CRNpath + r"\Run07.png").similar(0.95)
        Run08 = Pattern(CRNpath + r"\Run08.png").similar(0.95)
        Run_list = [Run01, Run02, Run03, Run04, Run05, Run06, Run07, Run08]
        count = 0
        for i in Remark_name:
            if exists(Run_list[count]): 
                #print(Run_list[count])
                Run_dict = {Run_list[count]:i}
                #print(Run_list[count], Run_dict[Run_list[count]])
                RunID = Run_list[count]
                Remark_name = Run_dict[Run_list[count]]
                CRN(RunID, Remark_name, CRNpath)
                print("Info: Change remark name(Run0{}) done!".format(count + 1))
                Log.write_log("Change_Remark_Name", "Info: Change remark name(Run0{}) done!".format(count + 1))
                count = count + 1
            else:
                print("Error: Change remark name(Run0{}) done!".format(count + 1))
                Log.write_log("Change_Remark_Name", "Error: Change remark name(Run0{}) done!".format(count + 1))
                pass
        return True
    except:
        print("Error: Change remark name failed!")
        Log.write_log("Change_Remark_Name", "Error: Change remark name failed!")
        sys.exit()
        return False

"""
if __name__ == "__main__": 
    Run01 = Pattern("Run01.png").similar(0.92)
    Run02 = Pattern("Run02.png").similar(0.94)
    Run03 = Pattern("Run03.png").similar(0.94)
    Run04 = Pattern("Run04.png").similar(0.94)
    Run05 = Pattern("Run05.png").similar(0.92)
    #RunID
    Run_list = [Run01, Run02, Run03, Run04, Run05]
#==========User Input==========#
#-----Remark_name-----#
    #Remark_name = [Run01, Run02, Run03, Run04, Run05]
    Remark_name = ["1st shot", "2nd shot", "3rd", "4th", "5th"]
    
    count = 0
    for i in Remark_name:
        if exists(Run_list[count]): 
            #print(Run_list[count])
            Run_dict = {Run_list[count]:i}
            #print(Run_list[count], Run_dict[Run_list[count]])
            RunID = Run_list[count]
            Remark_name = Run_dict[Run_list[count]]
            CRN(RunID,Remark_name)
            count = count + 1
        else:
            pass
"""