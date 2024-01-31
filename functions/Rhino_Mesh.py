from sikuli import *
import sys, os

LogAppPath = r"../sikuli_Share/Common.sikuli"
sys.path.append(LogAppPath)
import log_record as Log
import RegistrySetting as REG
import Common as Common 

def OpenRhino(RhinoPath, Zoo, RhinoAppPath):
    #Open Rhino    
    try:
        ret = os.popen('reg query {} /v {}'.format("\"HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\McNeel\Rhinoceros\{}\License Manager\"".format("6.0"), "\"Server\"")).readlines()
        if not ret:
            REG.RhinoRegSetting()
            source_file = r"../../sikuli_Share/Rhino_Mesh.sikuli/59ff75c9-9c71-4ef8-a290-6b590f3fc63a.lic"
            destination_folder = r"C:\ProgramData\McNeel\Rhinoceros\6.0\License Manager\Licenses"
            if not os.path.exists(destination_folder):
                os.makedirs(destination_folder)
            Common.copyfile(source_file, destination_folder)
            wait(3)
        openApp(RhinoPath)
        """
        if not os.path.isfile("C:\Users\Administrator\Desktop\RhinoOpened.txt"):
            openApp(r"\172.16.3.229\QAData\ShareCases\QA2\Sample Cases Reference\Source\Shell\McNeelUpdate.reg")
            wait(RhinoAppPath + r"\1641882191070.png",10)
            click(RhinoAppPath + r"\1641882202445.png")
            wait(RhinoAppPath + r"\1641880451572.png",1)
            click(RhinoAppPath + r"\1633681566681.png")
            wait(RhinoAppPath + r"\1641880451572.png",1)
            click(RhinoAppPath + r"\1633511200484.png")
            wait(1)
    #=====================Rhino 5======================#    
        if exists(RhinoAppPath + r"\1634787897774.png",60):
            click(RhinoAppPath + r"\1634787913274.png")
            wait(RhinoAppPath + r"\1634788048118.png",5)
            click(Pattern(RhinoAppPath + r"\1634788005524.png").targetOffset(-4,12))
            type(Pattern(RhinoAppPath + r"\1634788077712.png").targetOffset(-3,11),"a",Key.CTRL)
            type(Zoo)
            click(RhinoAppPath + r"\1634788110399.png")
            wait(RhinoAppPath + r"\1634788136118.png",10)
            click(RhinoAppPath + r"\1634788155977.png")
            wait(1)
            click(RhinoAppPath + r"\1634788180681.png")
            wait(5)
        if exists(RhinoAppPath + r"\1634807686952.png"):
            click(RhinoAppPath + r"\1634807686952.png")
                    
    #=====================Rhino 7======================#         
        if not os.path.isfile("C:\Users\Administrator\Desktop\RhinoOpened.txt"):
            if exists(RhinoAppPath + r"\1634634843884.png",120):
                click(Pattern(RhinoAppPath + r"\1634635004884.png").targetOffset(-67,1))
                click(RhinoAppPath + r"\1634701473047.png")
                wait(1)
                click(Pattern(RhinoAppPath + r"\1634701492388.png").targetOffset(-6,24))
                wait(RhinoAppPath + r"\1634701627226.png",10)
                click(Pattern(RhinoAppPath + r"\1634701544852.png").targetOffset(-66,9))
                type(Pattern(RhinoAppPath + r"\1634701598468.png").targetOffset(-21,63),Zoo)
                click(RhinoAppPath + r"\1634635045150.png")
                wait(5)
            Log.write_log("Rhino", "Info: Rhino was opened !")
            Log.write_log("C:\Users\Administrator\Desktop\RhinoOpened", "Info: Rhino was opened !")
        """            
        #waitVanish(RhinoAppPath + r"\1634117623818.png",300)
        #if exists(RhinoAppPath + r"\1634806515108.png"):
            #click(RhinoAppPath + r"\1634806515108.png")            
        wait(RhinoAppPath + r"\1634804087529.png",300)
        wait(1)
        if exists(RhinoAppPath + r"\1634806275499.png",5):
            click(Pattern(RhinoAppPath + r"\1634806275499.png").targetOffset(-3,-36))
        if exists(RhinoAppPath + r"\1634806776155.png",5):
            mouseMove(RhinoAppPath + r"\1634806776155.png")
        #click(Pattern(RhinoAppPath + r"\1641890600847.png").similar(0.90))
        #wait(1)
        #click(RhinoAppPath + r"\1641890630128.png")
        #wait(5)
        #click(RhinoAppPath + r"\1641890653159.png")
        #wait(1)
        #if exists(Pattern(RhinoAppPath + r"\1641890676331.png").exact()):
            #click(Pattern(RhinoAppPath + r"\1641890676331.png").targetOffset(-101,0))
        #wait(1)
        #click(RhinoAppPath + r"\1639449461801.png")
        if exists(RhinoAppPath + r"\1634804112232.png", 300):
            print("Open Rhino is Finished")
        Log.write_log("Rhino", "Info: Open Rhino is Finished!")
        return True
            
    except:
        closeApp(RhinoPath)
        print("Open Rhino is Failed")
        Log.write_log("Rhino", "Error: Open Rhino is Failed!")
        sys.exit()
        return False        

def ImportMesh(rPath_1, RhinoAppPath, *RhinoPath):
	#Import Mesh    
    try:
        rightClick(RhinoAppPath + r"\1634118255911.png")
        wait(RhinoAppPath + r"\1634118315833.png",10)
        click(Pattern(RhinoAppPath + r"\1634118342583.png").targetOffset(11,-2))
        wait(1)
        paste(rPath_1)
        wait(1)
        click(RhinoAppPath + r"\Rhino_Open.png")
        if exists(RhinoAppPath + r"\1634808605309.png"):
            click(RhinoAppPath + r"\1634808613246.png")
        print("Import Mesh is done!")
        Log.write_log("Rhino", "Info: Import Mesh is Finished!")
        return True		
    except:
        if not RhinoPath:
            pass
        else:
            closeApp(RhinoPath)
        print("Import Mesh is Failed!")
        Log.write_log("Rhino", "Error: Import Mesh is Failed!")
        sys.exit()
        return False

def CheckModel(RhinoAppPath):
    #Check Model
    click(RhinoAppPath + r"\1634174820464.png")
    click(RhinoAppPath + r"\1634174851902.png")
    click(RhinoAppPath + r"\1634808941230.png")
    wait(RhinoAppPath + r"\1634871102955.png",5) 

def ExportMesh(Modeltype, rPath_2, Model_name, Mesh_name, PD, RhinoAppPath, *RhinoPath):
    #Export Mesh
    #ModelType: "Shell" or "Solid" 
    #PD: "X Axis" or "Y Axis" or "Z Axis"    
    try:
        if not os.path.exists(rPath_2):
            os.makedirs(rPath_2)
        click(RhinoAppPath + r"\1639127017978.png") #Edit
        wait(1)
        click(RhinoAppPath + r"\1639127066666.png") #Layers
        wait(1)
        click(RhinoAppPath + r"\1639127100197.png") #All Layers On
        wait(1)
        type("a",Key.CTRL)
        if Modeltype == "Shell":
            click(RhinoAppPath + r"\1634173253280.png") #Shell Output Icon
            wait(1)
        else:
            click(RhinoAppPath + r"\1639126096744.png") #Solid Output Icon
            wait(1)
        if exists(Pattern(RhinoAppPath + r"\1639386384672.png").similar(0.85)): #Save
            click(Pattern(RhinoAppPath + r"\Wnd_Browse.png").targetOffset(-40,1)) #Browse
            #click(Pattern(RhinoAppPath + r"\1643102232612.png").targetOffset(-40,1)) #Browse
            wait(1)
            paste(rPath_2)
            wait(1)
            type(Key.ENTER)
            wait(3)
            type(Pattern(RhinoAppPath + r"\1639126227150.png").targetOffset(65,0),"a",Key.CTRL) #File Name
            wait(1)
            type(Model_name + Key.ENTER)
            if exists(Pattern(RhinoAppPath + r"\1640847651858.png").similar(0.85), 5): #Yes
                click(RhinoAppPath + r"\1640847651858.png") #Yes
                wait(3)
        if exists(Pattern(RhinoAppPath + r"\Wnd_SaveAS.png").similar(0.8)): #Save As
            click(Pattern(RhinoAppPath + r"\Wnd_Browse.png").targetOffset(-29,1)) #Browse
            wait(1)
            paste(rPath_2)
            wait(1)
            type(Key.ENTER)
            wait(3)
            type(Pattern(RhinoAppPath + r"\1639126227150.png").targetOffset(65,0),"a",Key.CTRL) #File Name
            wait(1)
            type(Mesh_name + Key.ENTER)
            #wait(5)
            #if exists(Pattern(RhinoAppPath + r"\1640847628733.png").similar(0.85), 5): #replace
            if exists(Pattern(RhinoAppPath + r"\1640847651858.png").similar(0.85), 5): #Yes
                click(RhinoAppPath + r"\1640847651858.png") #Yes
                wait(3)
        if exists(RhinoAppPath + r"\1634175588340.png", 10): #Parting Direction Setting
            if PD == "X Axis":
                if not exists(Pattern(RhinoAppPath + r"\1639619227056.png").similar(0.90)): #X Axis
                    click(Pattern(RhinoAppPath + r"\1639619160431.png").similar(0.90).targetOffset(60,0)) #PD
                    wait(3)
                    click(Pattern(RhinoAppPath + r"\1639619262572.png").similar(0.90)) #X Axis
                    wait(3)            
            elif PD == "Y Axis":
                if not exists(Pattern(RhinoAppPath + r"\1639619326196.png").similar(0.90)): #Y Axis
                    click(Pattern(RhinoAppPath + r"\1639619160431.png").similar(0.90).targetOffset(60,0)) #PD
                    wait(3)            
                    click(Pattern(RhinoAppPath + r"\1639619360212.png").similar(0.90)) #Y Axis
                    wait(3)
            if PD == "Z Axis":
                if not exists(Pattern(RhinoAppPath + r"\1639619431494.png").similar(0.95)): #Z Axis
                    click(Pattern(RhinoAppPath + r"\1639619160431.png").similar(0.90).targetOffset(60,0)) #PD
                    wait(3)            
                    click(Pattern(RhinoAppPath + r"\1639619467603.png").similar(0.95)) #Z Axis
                    wait(3)
            click(RhinoAppPath + r"\1641195178844.png") #OK
            wait(3)
        if exists(Pattern(RhinoAppPath + r"\1639706236098.png").similar(0.90)): #Are you sure
            click(Pattern(RhinoAppPath + r"\1639449461801.png").similar(0.90)) #OK
            wait(3)
        mouseMove(100, 100)
        if Modeltype == "Shell":
            if exists(RhinoAppPath + r"\1640847911624.png", 10): #Moldex3D Mesh
                if exists(RhinoAppPath + r"\1640847651858.png"): #Yes
                    click(RhinoAppPath + r"\1640847651858.png") #Yes                
                if exists(RhinoAppPath + r"\1639449461801.png", 30): #OK
                    click(RhinoAppPath + r"\1639449461801.png") #OK
        if Modeltype == "Solid":
            if exists(RhinoAppPath + r"\1640847911624.png", 300): #Moldex3D Mesh
                if exists(RhinoAppPath + r"\1640847651858.png"): #Yes
                    click(RhinoAppPath + r"\1640847651858.png")  #Yes           
                if exists(Pattern(RhinoAppPath + r"\1639645502540.png").similar(0.90), 100): #Solid Mesh export sucees
                    click(RhinoAppPath + r"\1639449461801.png") #OK
        #if exists(RhinoAppPath + r"\1640847911624.png", 90):
            #if exists(RhinoAppPath + r"\1640847651858.png"):
                #click(RhinoAppPath + r"\1640847651858.png")
            #if exists(RhinoAppPath + r"\1639449461801.png"):
                #click(RhinoAppPath + r"\1639449461801.png")
        wait(5)
        print("Export mesh is Finished!")
        Log.write_log("Rhino", "Info: Export Mesh is Finished!")
        return True        
    except:
        if not RhinoPath:
            pass
        else:
            closeApp(RhinoPath)
        print("Export Mesh is Failed!")
        Log.write_log("Rhino", "Error: Export Mesh is Failed!")
        sys.exit()
        return False

def CloseRhino(RhinoPath, RhinoAppPath):
    #Close Rhino    
    try:
        #click(Pattern(RhinoAppPath + r"\1634806776155.png").targetOffset(45,1))
        closeApp(RhinoPath)
        wait(1)
        if exists(RhinoAppPath + r"\1634807167186.png"):
            click(RhinoAppPath + r"\1634807183749.png")
        if exists(RhinoAppPath + r"\1634806410905.png"):
            click(RhinoAppPath + r"\1634806422499.png")
        print("Close Rhino is done!")
        Log.write_log("Rhino", "Info: Close Rhino is Finished!")
        return True		
    except:
        closeApp(RhinoPath)
        print("Close Rhino is Failed!")
        Log.write_log("Rhino", "Error: Close Rhino is Failed!")
        sys.exit()
        return False		

if __name__ == "__main__":
	RhinoPath = r"C:\Program Files\Rhinoceros 5 (64-Bit)\System\Rhino.exe"
	RhinoPath = r"C:\Program Files\Rhino 7\System\Rhino.exe"
	Zoo = "192.168.130.51"
	res = OpenRhino(RhinoPath,Zoo)
	print(res)
	if res == True:
		rPath_1 = r"C:\Users\Administrator\Desktop\Rhino_Mesh\Gas-assisted\Front Cover\Front Cover(m)"
		ImportMesh(rPath_1)
		CheckModel()
		rPath_2 = r"C:\Users\Administrator\Desktop\Rhino_Mesh\Gas-assisted\Front Cover"
		Model_name = "Front Cover_1"
		Mesh_name = "Front Cover_1"
		ExportMesh(rPath_2,Model_name,Mesh_name)
		CloseRhino()


def OpenMesh(rPath_1, RhinoAppPath, *RhinoPath):
	#Open Mesh    
    try:
        click(RhinoAppPath + r"\1634118255911.png")
        wait(Pattern(RhinoAppPath + r"\Rhino_Open_Mesh.png").similar(0.9),10)
        click(Pattern(RhinoAppPath + r"\1634118342583.png").targetOffset(11,-2))
        wait(1)
        paste(rPath_1)
        wait(1)
        click(RhinoAppPath + r"\Rhino_Open.png")
        if exists(RhinoAppPath + r"\1634808605309.png"):
            click(RhinoAppPath + r"\1634808613246.png")
        print("Open Mesh is done!")
        Log.write_log("Rhino", "Info: Open Mesh is Finished!")
        return True		
    except:
        if not RhinoPath:
            pass
        else:
            closeApp(RhinoPath)
        print("Open Mesh is Failed!")
        Log.write_log("Rhino", "Error: Open Mesh is Failed!")
        sys.exit()
        return False