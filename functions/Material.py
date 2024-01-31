from sikuli import *
import sys, os

LogAppPath = r"../sikuli_Share/Common.sikuli"
sys.path.append(LogAppPath) 
import log_record as Log

def OpenMaterialWizard(ItemPic, offsetx, offsety, MaterialAppPath, *importmaterial):
    #Open Material Wizard UI
    try:
        wait(Pattern(MaterialAppPath + r"\MaterialLogo.png").similar(0.98), 20)
        x = find(MaterialAppPath + r"\MaterialLogo.png")
        click(x)
        wait(MaterialAppPath + r"\StudioSelectMaterialLogo.png", 20)
        find(ItemPic)
        i = 0
        while(not exists(MaterialAppPath + r"\SelectMaterialWizard.png", 5) and i <= 3):
            click((Pattern(ItemPic).targetOffset(offsetx, offsety)))
            i += 1
        wait(MaterialAppPath + r"\SelectMaterialWizard.png", 20)
        if  len(importmaterial)!=0:
            click(Pattern(MaterialAppPath + r"\Material_Import.png").similar(0.9))
            i=0
            wait(MaterialAppPath + r"\Studio_Open.png", 3)
            y = Pattern(MaterialAppPath + r"\Studio_Filename_empty_2.png").similar(0.9).targetOffset(35,0)
            while (exists(y, 1) <> None) and i<5:
                click(y)
                wait(1)
                paste(importmaterial[0])
                mouseMove(0,50)
                wait(1)
                i += 1
            click(MaterialAppPath + r"\Btn_Open.png")
        else:
            click(MaterialAppPath + r"\MaterialWizardLogo.png")
            wait(MaterialAppPath + r"\Moldex3DMaterialWizardLogo.png", 20)
            print ("def OpenMaterialWizard is Finished")
        Log.write_log("Material", "Info: def OpenMaterialWizard is Finished")
        return True
    except:
        print ("def OpenMaterialWizard is Failed")
        Log.write_log("Material", "Error: def OpenMaterialWizard is Failed")
        sys.exit()
        return False

def ClickMDXBank(MaterialAppPath):
    #Switch Tab to Moldex3D Bank
    try:
        Indentlist = ["Moldex3DBankLogo", "MaterialWizardSelection", "MaterialASchulman", "MaterialABS"]
        for item in Indentlist:
            item = os.path.join(MaterialAppPath, item + ".png")
            if (exists(item, 10) and ("MaterialWizardSelection" not in item)):
                click(item)
            else:
                pass
        print ("def ClickMDXBank is Finished")
        Log.write_log("Material", "Info: def ClickMDXBank is Finished")
        return True
    except:
        print ("def ClickMDXBank is Failed")
        Log.write_log("Material", "Error: def ClickMDXBank is Failed")
        sys.exit()
        return False

def SelectPartMaterial(sMatlist):
    #Select Part Material
    try:
        i = 0
        k = 0
        while (i < len(sMatlist)):
            while (not exists (Pattern(sMatlist[i]).similar(0.93), 2) and k <= 10):
                type(Key.PAGE_DOWN)
                k += 1
            x = wait(sMatlist[i], 2)
            sleep(1)
            if ('MaterialEpoxyEpoxy.png' not in sMatlist[i]):
                click(x)
            else:
                click(Pattern(sMatlist[i]).similar(0.93).targetOffset(0,15))
            i += 1
        print ("def SelectPartMaterial is Finished")
        Log.write_log("Material", "Info: def SelectPartMaterial is Finished")
        return True
    except:
        print ("def SelectPartMaterial is Failed")
        Log.write_log("Material", "Error: def SelectPartMaterial is Failed")
        sys.exit()
        return False        

def MaterialNotAddToUserBank(MaterialAppPath):
    try:
        rightClick()
        x = MaterialAppPath + r"\AddToProject.png"
        if exists(x, 3):
            click(x)        
        else:
            print ("NOT Found %s" %(x))
            Log.write_log("Material", "Error: def SelectPartMaterial is Failed")
            sys.exit()
            return False
        print ("def MaterialNotAddToUserBank is Finished")
        Log.write_log("Material", "Info: def MaterialNotAddToUserBank is Finished")
        return True
    except:
        print ("def MaterialNotAddToUserBank is Failed")
        Log.write_log("Material", "Error: def MaterialNotAddToUserBank is Failed")
        sys.exit()
        return False

def CloseMaterialWizard(MaterialAppPath):
    #Close Material Wizard
    try:
        x = find(MaterialAppPath + r"\Btn_Close.png")
        click(x)
        print ("def CloseMaterialWizard is Finished")
        Log.write_log("Material", "Info: def CloseMaterialWizard is Finished")
        return True
    except:
        print ("def CloseMaterialWizard is Failed")
        Log.write_log("Material", "Error: def CloseMaterialWizard is Failed")
        sys.exit()
        return False

def FAIMSelectEM2Material(InsetPic, offsetx, offsety, ItemPic, MaterialAppPath):
    #For GAIM / WAIM EM#2 GAS / Water
    try:
        x = MaterialAppPath + r"\MaterialLogo.png"
        wait(x, 5)
        find(x)
        click(x)
        wait(MaterialAppPath + r"\StudioSelectMaterialLogo.png", 10)
        find(InsetPic)
        click((Pattern(InsetPic).targetOffset(offsetx, offsety)))
        if exists(ItemPic):
                  click(ItemPic)
        print ("def FAIMSelectEM2Material is Finished")
        Log.write_log("Material", "Info: def FAIMSelectEM2Material is Finished")
        return True
    except:
        print ("def FAIMSelectEM2Material is Failed")
        Log.write_log("Material", "Error: def FAIMSelectEM2Material is Failed")
        sys.exit()
        return False

def MCM2ndRunInsertSelection(InsetPic, ItemPic, MaterialAppPath):
    #For MCM 2nd Run Insert Material Selection
    try:
        #click((Pattern(InsetPic).targetOffset(offsetx, offsety)))
        #find(MaterialAppPath + "\\Studio_Project.png").below().find(ItemPic)
        if exists(Pattern(ItemPic).similar(0.95), 2):
                  click(Pattern(ItemPic).similar(0.90))
        else:
            click(MaterialAppPath + r"\OtherMaterialList.png")
            wait(MaterialAppPath + r"\ProjectMaterial.png", 5)
            if exists(Pattern(ItemPic).similar(0.90), 2):
                  click(Pattern(ItemPic).similar(0.90))
                  click(MaterialAppPath + r"\Btn_Studio_OK.png")
            else:
                print ("NOT Found %s" %(ItemPic))
                print ("def MCM2ndRunInsertSelection is Failed")
        print ("def MCM2ndRunInsertSelection is Finished")
        Log.write_log("Material", "Info: def MCM2ndRunInsertSelection is Finished")
        return True
    except:
        print ("def MCM2ndRunInsertSelection is Failed")
        Log.write_log("Material", "Error: def MCM2ndRunInsertSelection is Failed")
        sys.exit()
        return False

def Click_Icon(ButtonPic, offsetx):
    #Click Button
    #Argument: Buttone Icon Picture
    try:
        if exists(Pattern(ButtonPic).similar(0.98), 10):
            #doubleClick(ButtonPic)
            click(Pattern(ButtonPic).targetOffset(offsetx, 0))
        else:
            print ("NOT Found %s" %(ButtonPic))
            Log.write_log("Material", ("Error: NOT Found %s") %(ButtonPic))
            sys.exit()
            return False
        print ("def Click_Icon %s is Finished" %(ButtonPic))
        Log.write_log("Material", ("Info: def Click_Icon %s is Finished") %(ButtonPic))
        return True
    except:
        print ("def Click_Icon %s is Failed" %(ButtonPic))
        Log.write_log("Material", ("Error: def Click_Icon %s is Failed") %(ButtonPic))
        sys.exit()
        return False

def Wait_Dialog(MaterialAppPath, MaterialPic, MaterialPicBlue):
    """
    #Wait Specific Dialog
    #MeshPic: eDesign -> "\\Log_Generate_Solid_Mesh_Done.png"; Solid Cool -> "\\Studio_FinalCheck.png"; Fast Cool -> "\\Studio_Runner_Check.png"
    """
    try:
        i = 0
        while not (exists(Pattern(MaterialAppPath + MaterialPic).similar(0.90)) and (exists(Pattern(MaterialAppPath + MaterialPicBlue).similar(0.90))), 30) and i < 30:
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