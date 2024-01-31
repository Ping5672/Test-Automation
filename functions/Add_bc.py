from sikuli import *
import sys, os
LogAppPath = r"../sikuli_Share/Common.sikuli"
#LogAppPath = r"C:\Users\Administrator\Desktop\eDesign\sikuli_Share\Common.sikuli"
#AddBCpath = r"C:\Users\Administrator\Desktop\eDesign\sikuli_Share\Studio.sikuli\Add_BC.sikuli"
sys.path.append(LogAppPath)
#sys.path.append(AddBCpath)

import log_record as Log


def M3D_Sol(AddBCpath):
    if exists(AddBCpath + r"\M3D_Sol_IC.png"):
        return "IC"
    elif exists(AddBCpath + r"\M3D_Sol_EWLP.png"):
        return "EWLP"
    elif exists(AddBCpath + r"\M3D_Sol_Potting.png"):
        return "Potting"
    elif exists(AddBCpath + r"\M3D_Sol_TransferMolding.png"):
        return "Transfer Molding"
    elif exists(AddBCpath + r"\M3D_Sol_InjectionCompression.png"):
        return "InjectionCompression"
    elif exists(AddBCpath + r"\M3D_Sol_CoreShift.png"):
        return "Core Shift"

def Add_BC(M3D_Sol, AddBCpath):
    try:
        click(AddBCpath + r"\Fit_to_Window.png")
        wait(1)
        if M3D_Sol == "IC":
            click(AddBCpath + r"\BC.png")
            wait(1)
            click(AddBCpath + r"\Fixed_Constraint_icon.png")
            wait(AddBCpath + r"\Fixed_Constraint_title.png",5)
            if exists(AddBCpath + r"\Check_Analysis.png"):
                click(AddBCpath + r"\Click_Analysis.png")
                click(Pattern(AddBCpath + r"\Change_to_PaddleShift.png").targetOffset(-5,11))
                wait(1)
            click(AddBCpath + r"\Auto_setting.png")
            wait(1)
            click(AddBCpath + r"\Fixed_BC_OK.png")
            wait(1)
        
        if M3D_Sol == "EWLP":
            click(AddBCpath + r"\BC.png")
            wait(1)
            click(AddBCpath + r"\Fixed_Constraint_icon.png")
            wait(AddBCpath + r"\Fixed_Constraint_title.png",5)
            if exists(AddBCpath + r"\Check_Analysis.png"):
                click(AddBCpath + r"\Click_Analysis.png")
                click(Pattern(AddBCpath + r"\Change_to_PaddleShift.png").targetOffset(-5,11))
                wait(1)
            click(AddBCpath + r"\Auto_setting.png")
            wait(1)
            click(AddBCpath + r"\Fixed_BC_OK.png")
            wait(1)

        if M3D_Sol == "Transfer Molding":
            click(AddBCpath + r"\BC.png")
            wait(1)
            click(AddBCpath + r"\Fixed_Constraint_icon.png")
            wait(AddBCpath + r"\Fixed_Constraint_title.png",5)
            if exists(AddBCpath + r"\Check_Analysis.png"):
                click(AddBCpath + r"\Click_Analysis.png")
                click(Pattern(AddBCpath + r"\Change_to_PaddleShift.png").targetOffset(-5,11))
                wait(1)
            click(AddBCpath + r"\Auto_setting.png")
            wait(1)
            click(AddBCpath + r"\Fixed_BC_OK.png")
            wait(1)

        if M3D_Sol == "Core Shift":
            click(AddBCpath + r"\BC.png")
            wait(1)
            click(AddBCpath + r"\Fixed_Constraint_icon.png")
            wait(AddBCpath + r"\Fixed_Constraint_title.png",5)
            if exists(AddBCpath + r"\Check_Analysis.png"):
                click(AddBCpath + r"\Click_Analysis.png")
                click(Pattern(AddBCpath + r"\Change_to_CoreShift.png").targetOffset(-2,10))
                wait(1)
            click(AddBCpath + r"\Auto_setting.png")
            wait(1)
            click(AddBCpath + r"\Fixed_BC_OK.png")
            wait(1)
        print ("Info: Add {} BC done!".format(M3D_Sol))
        Log.write_log("Log", "Info: Add {} BC done!".format(M3D_Sol))
        return True
        
    except:
        print ("Error: Add {} BC failed!".format(M3D_Sol))
        Log.write_log("Log", "Error: Add {} BC failed!".format(M3D_Sol))
        sys.exit()        
        return False

        
def Add_Potting_BC(Potting_path, AddBCpath):
    try:
        click(Pattern(AddBCpath + r"\Import_Geometry_icon_2023.png").targetOffset(0,18))
        wait(1)
        click(AddBCpath + r"\Import_Geometry.png")
        wait(1)
        wait(AddBCpath + r"\Import_title.png",5)
        click(AddBCpath + r"\File_name.png")
        paste(Potting_path)
        click(AddBCpath + r"\File_open.png")
        wait(1)
        click(AddBCpath + r"\Model_Tree.png")
        wait(1)
        rightClick(AddBCpath + r"\Non_attributed.png")
        wait(1)
        click(AddBCpath + r"\Expand_Sublayer.png")
        wait(1)
        click(Pattern(AddBCpath + r"\Non_attributed.png").targetOffset(0,25))
        wait(1)
        click(AddBCpath + r"\BC_tab.png")
        wait(1)
        click(AddBCpath + r"\Potting_icon.png")
        wait(AddBCpath + r"\Potting_title.png",5)
        if not exists(AddBCpath + r"\SliderUp.png",2):
            Potting_title = find(AddBCpath + r"\Potting_title.png")
            dragDrop(Potting_title, Potting_title.offset(Location(300, 0)))
        click(AddBCpath + r"\Choose_hand.png")
        wait(1)
        dragDrop(Pattern(AddBCpath + r"\SliderUp.png").targetOffset(1,-2),Pattern(AddBCpath + r"\SliderDown.png").targetOffset(-1,10))
        wait(1)
        click(Pattern(AddBCpath + r"\Potting_line2.png").targetOffset(0,-25))
        wait(1)
        click(AddBCpath + r"\Choose_line_ok.png")
        wait(1)
        doubleClick(Pattern(AddBCpath + r"\Weight.png").targetOffset(0,12))
        type("6")
        click(AddBCpath + r"\Choose_hand.png")
        wait(1)
        click(Pattern(AddBCpath + r"\Potting_line2.png").targetOffset(0,0))
        wait(1)
        click(AddBCpath + r"\Choose_line_ok.png")
        wait(1)
        doubleClick(Pattern(AddBCpath + r"\Weight2.png").targetOffset(0,-10))
        type("6")
        type(AddBCpath + r"\Dispenser_Diameter.png","a",Key.CTRL)
        type("1")        
        #click(Pattern(AddBCpath + r"\Reverse.png").similar(0.90))
        #wait(1)
        type(Pattern(AddBCpath + r"\MaxFillingTime.png").targetOffset(52,1),"a",Key.CTRL)
        type("5")
        click(AddBCpath + r"\PottingBC_ok.png")
        wait(1)
        print ("Info: Add Potting BC done!")
        Log.write_log("Log", "Info: Add Potting BC BC done!")
        return True
    except:
        print ("Error: Add Potting BC failed!")
        Log.write_log("Log", "Error: Add Potting BC BC failed!")
        #sys.exit()
        return False

def Add_Potting_MeltInlet(AddBCpath):
    try:
        click(Pattern(AddBCpath + r"\Btn_Perspective.png").targetOffset(39,2))
        wait(1)
        click(Pattern(AddBCpath + r"\Perspective.png").similar(0.90))
        wait(1)
        click(AddBCpath + r"\Fit_to_Window.png")
        wait(1)
        click(AddBCpath + r"\BC.png")
        wait(1)
        click(Pattern(AddBCpath + r"\MeltInlet.png").similar(0.80))
        wait(1)
        click(Pattern(AddBCpath + r"\Moldex3D_Studio.png").similar(0.90).targetOffset(0,350))
        wait(1)
        click(AddBCpath + r"\Choose_line_ok.png")
        wait(1)
        print("Info: Add Melt_Inlet done!")
        Log.write_log("Log", "Info: Add Melt_Inlet done!")
        return True
    except:
        print("Error: Add Melt_Inlet failed!")
        Log.write_log("Log", "Error: Add Melt_Inlet failed!")
        sys.exit()
        return False

def Add_Metal_BC(CustomizePath, AddBCpath):
    try:
        if not exists(Pattern(AddBCpath + r"\Home_tab_2.png").similar(0.95)):
            click(Pattern(AddBCpath + r"\Home_tab.png").similar(0.90))
            wait(1)
        if not exists(Pattern(AddBCpath + r"\Project_tree_1.png").exact()):
            click(Pattern(AddBCpath + r"\Project_tree_2.png").exact())
            wait(1)
        rightClick(AddBCpath + r"\Run01.png")
        wait(1)
        click(AddBCpath + r"\Btn_Result_List.png")
        wait(1)
        B1 = find(AddBCpath + r"\BlueResult_List.png")
        mouseMove(Location(B1.x + 200, B1.y))
        wait(1)
        click(Pattern(AddBCpath + r"\Btn_Import.png").similar(0.90))
        wait(AddBCpath + r"\Import_title.png", 5)
        click(Pattern(AddBCpath + r"\File_name_1.png").targetOffset(70,0))
        wait(1)
        paste(CustomizePath)
        wait(1)
        click(Pattern(AddBCpath + r"\File_Open_1.png").similar(0.90))
        wait(1)
        click(Pattern(AddBCpath + r"\Customize_Group.png").similar(0.90))
        wait(1)
        if not exists(Pattern(AddBCpath + r"\BlueMetalFixed.png").exact()):
            click(Pattern(AddBCpath + r"\MetalFixed.png").similar(0.95))
            wait(1)
        if exists(AddBCpath + r"\BC.png"):
            click(AddBCpath + r"\BC.png")
            wait(1)
        click(Pattern(AddBCpath + r"\Fixed_Constraint_icon.png").similar(0.90))
        wait(Pattern(AddBCpath + r"\Fixed_Constraint_title.png").similar(0.90), 10)
        click(Pattern(AddBCpath + r"\Btn_BC_setting.png").similar(0.90))
        wait(1)
        if not exists(Pattern(AddBCpath + r"\Spread_Vertex.png").exact()):
            click(Pattern(AddBCpath + r"\Spread_Vertex_on.png").similar(0.90))
            wait(1)
        click(AddBCpath + r"\Choose_line_ok.png") 
        wait(1)
        FixedBC_list = [Pattern(AddBCpath + r"\FixedBC_2023.png").targetOffset(85,120), Pattern(AddBCpath + r"\FixedBC_2023.png").targetOffset(-475,-125), Pattern(AddBCpath + r"\FixedBC_2023.png").targetOffset(470,-140)]
        count = 0
        for x in FixedBC_list:
            keyDown(Key.SHIFT)
            click(FixedBC_list[count])
            keyUp()
            if exists(Pattern(AddBCpath + r"\Surface_mesh_face.png").similar(0.90)):
                click(Pattern(AddBCpath + r"\Surface_mesh_face.png").similar(0.90))
                wait(1)
            count = count + 1
        click(AddBCpath + r"\Fixed_BC_OK.png")
        wait(1)
        print("Info: Add FixedBC done!!")
        Log.write_log("AddBC", "Info: Add FixedBC done!")
        if not exists (Pattern(AddBCpath + r"\BlueMetalForce_2.png").exact()):
            click(Pattern(AddBCpath + r"\MetalForce.png").similar(0.95))
            wait(1)
        if exists(AddBCpath + r"\BC.png"):
            click(AddBCpath + r"\BC.png")
            wait(1)
        click(AddBCpath + r"\Force_icon.png")
        wait(Pattern(AddBCpath + r"\Force_title.png").similar(0.90), 10)
        mouseMove((Pattern(AddBCpath + r"\Force_title.png").similar(0.90)))
        mouseDown(Button.LEFT)
        mouseMove(-150, -150)
        mouseUp(Button.LEFT)
        click(Pattern(AddBCpath + r"\Btn_BC_setting.png").similar(0.90))
        wait(1)
        if not exists(Pattern(AddBCpath + r"\Spread_Vertex.png").exact()):
            click(Pattern(AddBCpath + r"\Spread_Vertex_on.png").similar(0.90))
            wait(1)
        click(AddBCpath + r"\Choose_line_ok.png") 
        wait(1)
        
        ForceBC_list = [Pattern(AddBCpath + r"\ForceBC_2023.png").targetOffset(-330,-70), Pattern(AddBCpath + r"\ForceBC_2023.png").targetOffset(380,-70)]
        count = 0
        for x in ForceBC_list:
            keyDown(Key.SHIFT)
            click(ForceBC_list[count])
            keyUp()
            if exists(Pattern(AddBCpath + r"\Surface_mesh_face.png").similar(0.90)):
                click(Pattern(AddBCpath + r"\Surface_mesh_face.png").similar(0.90))
                wait(1)
            count = count + 1
        type(Pattern(AddBCpath + r"\Force_Z.png").similar(0.95).targetOffset(65,0), "a",Key.CTRL)
        type("980700")
        click(AddBCpath + r"\Fixed_BC_OK.png")
        wait(1)
        print("Info: Add ForceBC done!")
        Log.write_log("AddBC", "Info: Add ForceBC done!")        
        if not exists(Pattern(AddBCpath + r"\BlueMetalPressure_1.png").exact()):
            click(Pattern(AddBCpath + r"\MetalPressure_1.png").similar(0.95))
            wait(1) 
        if exists(AddBCpath + r"\BC.png"):
            click(AddBCpath + r"\BC.png")
            wait(1)
        click(AddBCpath + r"\Pressure_icon.png")
        wait(Pattern(AddBCpath + r"\Pressure_title.png").similar(0.90), 10)
        click(Pattern(AddBCpath + r"\Btn_BC_setting.png").similar(0.90))
        wait(1)
        if not exists(Pattern(AddBCpath + r"\Spread_Vertex_2.png").exact()):
            click(Pattern(AddBCpath + r"\Spread_Vertex_on.png").similar(0.90))
            wait(1)
        click(AddBCpath + r"\Choose_line_ok.png") 
        wait(1)
        click(AddBCpath + r"\PressureBC_2023.png")
        if exists(Pattern(AddBCpath + r"\Surface_mesh_face.png").similar(0.90)):
            click(Pattern(AddBCpath + r"\Surface_mesh_face.png").similar(0.90))
            wait(1)
        type(Pattern(AddBCpath + r"\PressureMPa.png").similar(0.90).targetOffset(90,0), "a",Key.CTRL)
        type("1")
        click(AddBCpath + r"\Fixed_BC_OK.png")
        wait(1)
        print("Info: Add PressureBC done!")
        Log.write_log("AddBC", "Info: Add PressureBC done!")
        rightClick(Pattern(AddBCpath + r"\MetalFixed.png").similar(0.95))
        click(Pattern(AddBCpath + r"\DeleteResult.png").similar(0.85))
        wait(1)
        rightClick(Pattern(AddBCpath + r"\MetalForce.png").similar(0.95))
        click(Pattern(AddBCpath + r"\DeleteResult.png").similar(0.85))
        wait(1)
        click(Pattern(AddBCpath + r"\Customize_Group.png").similar(0.90))
        wait(1)
        rightClick(Pattern(AddBCpath + r"\BlueMetalPressure_1.png").exact())
        click(Pattern(AddBCpath + r"\DeleteResult.png").similar(0.85))
        wait(1)
        if not exists(Pattern(AddBCpath + r"\Home_tab_2.png").similar(0.95)):
            click(Pattern(AddBCpath + r"\Home_tab.png").similar(0.90))
            wait(1)
        print("Info: Delete Customize_Group done!")
        Log.write_log("AddBC", "Info: Delete Customize_Group done!!")
        return True
    except:
        print("Error: Add Metal BC failed!")
        Log.write_log("AddBC", "Error: Add Metal BC failed!")
        sys.exit()
        return False

def AddProbeNode(ProbeNodeList, AddBCpath):
    try:
        if not exists(Pattern(AddBCpath + r"\Inspection_tab_2.png").similar(0.95)):
            click(Pattern(AddBCpath + r"\Inspection_tab.png").similar(0.90))
            wait(1)
        count = 0
        click(AddBCpath + r"\Probe_icon.png")
        wait(1)
        for x in ProbeNodeList:
            click(Pattern(AddBCpath + r"\Point_input.png").targetOffset(150,0))
            type("a", Key.CTRL)
            paste(ProbeNodeList[count])
            type(Key.ENTER)
            wait(1)
            print("Info: Add ProbeNode_{} done!".format(count + 1))
            Log.write_log("AddBC", "Info: Add ProbeNode_{} done!".format(count + 1))
            count = count + 1
        click(Pattern(AddBCpath + r"\Btn_X").similar(0.90))
        if not exists(Pattern(AddBCpath + r"\Home_tab_2.png").similar(0.95)):
            click(Pattern(AddBCpath + r"\Home_tab.png").similar(0.90))
        return True        
    except:
        print("Error: Add ProbeNode done!")
        Log.write_log("AddBC", "Error: Add ProbeNode failed!")
        sys.exit()
        return False
        
"""        
def AddFixedBC_Customize(CustomizeGrouppath, BlueCustomizeGroup, CustomizeGroup, Displacementtarget, Displacementlist, BC_list):
    try:
        BlueCustomizeGroup = [AddBCpath + r"\BlueMetalFixed_1.png", AddBCpath + r"\BlueMetalFixed_2.png", AddBCpath + r"\BlueMetalFixed_3.png"]
        CustomizeGroup = [Pattern(AddBCpath + r"\FixedBC_1.png").targetOffset(-13,-116), AddBCpath + r"\FixedBC_2.png", AddBCpath + r"\FixedBC_3.png"]  
        Fixedtarget = []
        count = 0
            for x in CustomizeGroup:
                if not exists(Pattern(BlueCustomizeGroup[count]).exact()):
                    click(CustomizeGroup[count])
                    wait(3)
                if exists(Pattern(AddBCpath + r"\BC_tab.png").similar(0.90)):
                    click(Pattern(AddBCpath + r"\BC_tab.png").similar(0.90))
                    wait(1)
                click(Pattern(AddBCpath + r"\Fixed_Constraint_icon.png").similar(0.90))
                wait(Pattern(AddBCpath + r"\Fixed_Constraint_title.png").similar(0.90), 10)
                click(Pattern(AddBCpath + r"\Btn_BC_setting.png").similar(0.90))
                wait(3)
                if not exists(Pattern(AddBCpath + r"\Spread_Vertex.png").exact()):
                    click(Pattern(AddBCpath + r"\Spread_Vertex_on.png").similar(0.90))
                    wait(3)
                click(AddBCpath + r"\Choose_line_ok.png") 
                wait(3)
                click(Fixedtarget[count])
                if exists(Pattern(AddBCpath + r"\Surface_mesh_face.png").similar(0.90)):
                    click(Pattern(AddBCpath + r"\Surface_mesh_face.png").similar(0.90))
                    wait(3)
                if Fixedin == "x":
                    click()
                    wait(1)
                    click()
                    wait(1)
                if Fixedin == "y":
                    click()
                    wait(1)
                    click()
                    wait(1)                
                if Fixedin == "z":
                    click()
                    wait(1)
                    click()
                    wait(1)                
                if Fixedin == "xy":
                    click()
                    wait(1)
                if Fixedin == "yz":
                    click()
                    wait(1)               
                if Fixedin == "zx":
                    click()
                    wait(1)                           
                if Fixedin == "xyz":
                    pass                
                click(AddBCpath + r"\Fixed_BC_OK.png")
                wait(3)
                print("Info: Add FixedBC_{} done!".format(count + 1))
                Log.write_log("Log", "Info: Add FixedBC_{} done!".format(count + 1))
                count = count + 1
        return True
    except:
        return False

def AddDisplacementBC_Customize(CustomizeGrouppath, BlueCustomizeGroup, CustomizeGroup, Fixedin, BC_list):
    try:
        BlueCustomizeGroup = [AddBCpath + r"\BlueMetalForce_1.png", AddBCpath + r"\BlueMetalForce_2.png"]
        CustomizeGroup = [AddBCpath + r"\ForceBC_1.png", AddBCpath + r"\ForceBC_2.png"]
        Displacementtarget = []
        count = 0
        d = 0
        for x in BlueCustomizeGroup:
            if not exists(Pattern(BlueCustomizeGroup[count]).exact()):
                click(CustomizeGroup[count])
                wait(3)
            if exists(AddBCpath + r"\BC_tab.png"):
                click(AddBCpath + r"\BC_tab.png")
                wait(1)
            click(AddBCpath + r"\Force_icon.png")
            wait(Pattern(AddBCpath + r"\Force_title.png").similar(0.90), 10)
            click(Pattern(AddBCpath + r"\Btn_BC_setting.png").similar(0.90))
            wait(3)
            if not exists(Pattern(AddBCpath + r"\Spread_Vertex.png").exact()):
                click(Pattern(AddBCpath + r"\Spread_Vertex_on.png").similar(0.90))
                wait(3)
            click(AddBCpath + r"\Choose_line_ok.png") 
            wait(3)
            click(Displacementtarget[count])
            if exists(Pattern(AddBCpath + r"\Surface_mesh_face.png").similar(0.90)):
                click(Pattern(AddBCpath + r"\Surface_mesh_face.png").similar(0.90))
                wait(3)
            type(Pattern(AddBCpath + r"\Force_X.png").similar(0.95).targetOffset(65,0), "a",Key.CTRL)
            type(Displacementlist[d])
            type(Pattern(AddBCpath + r"\Force_Y.png").similar(0.95).targetOffset(65,0), "a",Key.CTRL)
            type(Displacementlist[d + 1])
            type(Pattern(AddBCpath + r"\Force_Z.png").similar(0.95).targetOffset(65,0), "a",Key.CTRL)
            type(Displacementlist[d + 2])
            click(AddBCpath + r"\Fixed_BC_OK.png")
            wait(3)
            print("Info: Add DisplacementBC_{} done!".format(count + 1))
            Log.write_log("Log", "Info: Add DisplacementBC_{} done!".format(count + 1))
            count = count + 1
            d = d + 3    

def AddForceBC_Customize(CustomizeGrouppath, BlueCustomizeGroup, CustomizeGroup, Forcetarget, Forcelist, BC_list):
    try:
        BlueCustomizeGroup = [AddBCpath + r"\BlueMetalForce_1.png", AddBCpath + r"\BlueMetalForce_2.png"]
        CustomizeGroup = [AddBCpath + r"\ForceBC_1.png", AddBCpath + r"\ForceBC_2.png"]
        Forcetarget = []
        count = 0
        f = 0
        for x in BlueCustomizeGroup:
            if not exists(Pattern(BlueCustomizeGroup[count]).exact()):
                click(CustomizeGroup[count])
                wait(3)
            if exists(AddBCpath + r"\BC_tab.png"):
                click(AddBCpath + r"\BC_tab.png")
                wait(1)
            click(AddBCpath + r"\Force_icon.png")
            wait(Pattern(AddBCpath + r"\Force_title.png").similar(0.90), 10)
            click(Pattern(AddBCpath + r"\Btn_BC_setting.png").similar(0.90))
            wait(3)
            if not exists(Pattern(AddBCpath + r"\Spread_Vertex.png").exact()):
                click(Pattern(AddBCpath + r"\Spread_Vertex_on.png").similar(0.90))
                wait(3)
            click(AddBCpath + r"\Choose_line_ok.png") 
            wait(3)
            click(Forcetarget[count])
            if exists(Pattern(AddBCpath + r"\Surface_mesh_face.png").similar(0.90)):
                click(Pattern(AddBCpath + r"\Surface_mesh_face.png").similar(0.90))
                wait(3)
            type(Pattern(AddBCpath + r"\Force_X.png").similar(0.95).targetOffset(65,0), "a",Key.CTRL)
            type(Forcelist[f])
            type(Pattern(AddBCpath + r"\Force_Y.png").similar(0.95).targetOffset(65,0), "a",Key.CTRL)
            type(Forcelist[f + 1])
            type(Pattern(AddBCpath + r"\Force_Z.png").similar(0.95).targetOffset(65,0), "a",Key.CTRL)
            type(Forcelist[f + 2])
            click(AddBCpath + r"\Fixed_BC_OK.png")
            wait(3)
            print("Info: Add ForceBC_{} done!".format(count + 1))
            Log.write_log("Log", "Info: Add ForceBC_{} done!".format(count + 1))
            count = count + 1
            f = f + 3

def AddPressure_Customize(CustomizeGrouppath, BlueCustomizeGroup, CustomizeGroup, Pressuretarget, Pressurelist, BC_list):
    try:
        BlueCustomizeGroup = [AddBCpath + r"\BlueMetalForce_1.png", AddBCpath + r"\BlueMetalForce_2.png"]
        CustomizeGroup = [AddBCpath + r"\ForceBC_1.png", AddBCpath + r"\ForceBC_2.png"]
        Pressuretarget = []
        count = 0
        for x in BlueCustomizeGroup:
            if not exists(Pattern(BlueCustomizeGroup[count]).exact()):
                click(CustomizeGroup[count])
                wait(3) 
            if exists(AddBCpath + r"\BC_tab.png"):
                click(AddBCpath + r"\BC_tab.png")
                wait(1)
            click(AddBCpath + r"\Pressure_icon.png")
            wait(Pattern(AddBCpath + r"\Pressure_title.png").similar(0.90), 10)
            click(Pattern(AddBCpath + r"\Btn_BC_setting.png").similar(0.90))
            wait(3)
            if not exists(Pattern(AddBCpath + r"\Spread_Vertex.png").exact()):
                click(Pattern(AddBCpath + r"\Spread_Vertex_on.png").similar(0.90))
                wait(3)
            click(AddBCpath + r"\Choose_line_ok.png") 
            wait(3)
            click(Pressuretarget[count])
            if exists(Pattern(AddBCpath + r"\Surface_mesh_face.png").similar(0.90)):
                click(Pattern(AddBCpath + r"\Surface_mesh_face.png").similar(0.90))
                wait(3)
            type(Pattern(AddBCpath + r"\PressureMPa.png").similar(0.90).targetOffset(90,0), "a",Key.CTRL)
            type(Pressurelist[count])
            click(AddBCpath + r"\Fixed_BC_OK.png")
            wait(3)
            print("Info: Add PressureBC_{} done!".format(count + 1))
            Log.write_log("Log", "Info: Add PressureBC_{} done!".format(count + 1))
            count = count + 1            
"""
if __name__ == "__main__":
    M3D_Sol()
    print(M3D_Sol())
    Potting_path = r"C:\Users\Administrator\Desktop\Encapsulation\Potting\CAD Data\Potting.igs"
    Add_BC(M3D_Sol(), Potting_path, AddBCpath)
    Add_Metal_BC()
    AddBCPath = r"C:\Users\Administrator\Desktop\eDesign\sikuli_Share\Studio.sikuli\Add_BC.sikuli"
    ProbeNodeList = ["11.52,-47.90,10.47", "11.52,-48.87,10.47", "11.52,-49.84,10.47", "11.52,-50.82,10.47"]
    AddProbeNode(ProbeNodeList, AddBCpath)
