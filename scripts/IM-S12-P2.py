import os, sys, time

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
import Material
import Process
import CMX 
import Common
import Rhino_Mesh as Rhino
import Add_BC as AddBC
import Change_Remark_Name as CRN
import log_record as Log

StudioAppPath = ArgS.StudioAppPath
CMAppPath = ArgS.CMAppPath
CommonAppPath = ArgS.CommonAppPath
MaterialAppPath = ArgS.MaterialAppPath
ProcessAppPath = ArgS.ProcessAppPath
CMXAppPath = ArgS.CMXAppPath
RhinoAppPath = ArgS.RhinoAppPath
BCAppPath = ArgS.BCAppPath
CRNAppPath = ArgS.CRNAppPath
exceptprocedureApp = ArgS.exceptprocedureApp


ProjectName = "IM-S12-P2"
username = "moldex3dqa"
password = "123456"
SVNPath = r"svn://192.168.3.4/QARepository/AutoTest/Moldex3D/2023Series/Moldex3D/CaseReference/ENT/" + ProjectName + r"/Geometry"
Filename= SVNPath.split('/')[-2]
localpath = os.path.normpath((cwd + r"\\" +Filename))
MainInstallPath ,ver = Common.getregkeyvalue(r"HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\CoreTechSystem\MDX_ParallelComputing", "INSTALLDIR")
WorkingFolder = Common.getregkeyvalue(r"HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\CoreTechSystem\MDX_ParallelComputing", "WorkingFolder")
StudioPath = MainInstallPath + r"\Bin\MDXStudio.exe"

CaseReferncePath = Common.gototargetpath('MDX_ENT') + "\\" + ProjectName
Run01_SourcePath =CaseReferncePath+ r"\InjectionUnit.mdg"
Run02_SourcePath =CaseReferncePath+ r"\SolidIM-001_Simple.mdg"
Run03_SourcePath =CaseReferncePath+ r"\eDesign.mdg"
Run04_SourcePath =CaseReferncePath+ r"\FQ_Solid_Bumper.mdg"
Run05_SourcePath =CaseReferncePath+ r"\FQ_eDesign_Bumper.mdg"
MachinePath = CaseReferncePath+ r"\QA-T2-2002.mchs"

CMPath = MainInstallPath + r"\Bin\MDXComputingManager" + ver + ".exe"
hostname, local_ip = Common.getcuriphostname()

Bank_Folder = r"C:\Users\Administrator\AppData\Roaming\CoreTechSystem\Moldex3D " + ver + r"\Bank"
Material_Folder = r"C:\Users\Administrator\AppData\Roaming\CoreTechSystem\Moldex3D " + ver + r"\Material"

try:
    #Delete Bank and Material Folder
    Common.deletepath(Bank_Folder)
    Common.deletepath(Material_Folder)
    Log.write_log("Pre_Setting", "Info: Delete Bank and Material Folder is Finished")
    #svn execution
    Common.SVNLogin(username, password)
    Common.SVNDownload(SVNPath, localpath)
    print ("Info: SVN download is Finished")
    Log.write_log("Pre_Setting", "Info: SVN download is Finished")
    
    #Open Studio UI
    Studio.OpenApp(StudioPath, StudioAppPath + "\\Studio_UI.png")
    Log.write_log(ProjectName, "Info: Open Studio is Finished")
    #New Project
    Studio.NewProject(ProjectName, StudioAppPath)
    Log.write_log(ProjectName, "Info: New Project Setting is Finished")
    
    #Studio Pre Process Setting
    Studio.MeshType("Solid", StudioAppPath)
    Studio.Home_MoldingType_New("Module_IM2", StudioAppPath)
    Studio.Home_Model("ImportGeometry", StudioAppPath)
    Studio.ImportGeometry(Run01_SourcePath, StudioAppPath)
    Studio.SwitchTab(StudioAppPath + "\\Studio_Tab_Mesh.png", StudioAppPath + "\\Studio_Tab_Meshing.png")
    Studio.Meshing_Generate(StudioAppPath)
    Studio.Meshing_GenerateBLM("None", StudioAppPath)
    Studio.Wait_Dialog(StudioAppPath, "\\Studio_FinalCheck.png")
    Studio.Click_Icon(StudioAppPath, "\\Studio_Tree_Model.png", 0)
    Studio.Click_Icon(StudioAppPath, "\\Studio_Tree_MB.png", -45)
    Studio.Click_Icon(StudioAppPath, "\\Studio_Tree_CoolingChannel.png", -65)
    Studio.Click_Icon(StudioAppPath, "\\Btn_Angle_Perspective_Seletected.png", 40)
    Studio.Click_Icon(StudioAppPath, "\\Btn_Fit_To_Window.png", -24)
    Studio.Click_Icon(StudioAppPath, "\\Btn_ShowModeSelected_FeatureShaded2.png", 40)
    Studio.Final_Check(StudioAppPath)
    Log.write_log(ProjectName, "Info: Studio Pre Process Setting is Finished")
    
    #Material Wizard Setting
    sMatlist = [MaterialAppPath + "\\MaterialABS.png", MaterialAppPath + "\\MaterialASchulman.png",MaterialAppPath + "\\MaterialRABS9000UV5.png"]
    Material.OpenMaterialWizard(MaterialAppPath + "\\Studio_EM1.png", 200, 0, MaterialAppPath)
    Material.ClickMDXBank(MaterialAppPath)
    Material.SelectPartMaterial(sMatlist)
    Material.MaterialNotAddToUserBank(MaterialAppPath)
    Material.CloseMaterialWizard(MaterialAppPath)
    Log.write_log(ProjectName, "Info: Material Wizard Setting is Finished")
    
    #Process Wizard Setting
    Process.Home_Process("New", ProcessAppPath)
    #Process Tab Project Setting
    #Process.ProcessWizard_Project_SettingMethod("M1", ProcessAppPath)
    Process.Select_Machine_Setting(ProcessAppPath)
    Process.Select_Machine_Setting_Advanced(ProcessAppPath, "Import", MachinePath)
    Process.Wait_Dialog(ProcessAppPath + r"\Mac_QA_T2_2002.png")
    Process.Click_IconEx(ProcessAppPath + r"\Mac_QA_T2_2002.png")
    Process.Click_IconEx(ProcessAppPath + r"\Btn_OK.png")
    #Process Tab Filling/Packing Setting
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_ProjectSetting.png", ProcessAppPath + "\\Pro_Tab_FillingPacking.png", ProcessAppPath)  
    Process.ValueSetting(ProcessAppPath + "\\Pro_Filling_RamPosition.png", 190, 0, "5", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_Filling_PackingTime.png", 60, 0, "0.3", ProcessAppPath)
    #Process Filling/Packing - Injection Pressure Profile Setting
    Process.Click_Icon(ProcessAppPath + r"\Btn_Pro_Flow_rate_profile.png", ProcessAppPath + r"\Pro_Filling_FlowRateProFile3.png")
    Process.ValueSetting(ProcessAppPath + r"\Pro_SectionNo.png", 60, 0, "1", ProcessAppPath)
    Profilelist = [ProcessAppPath + r"\Pro_Filling_FlowRateProFile3.png", "17", "50"]
    Process.ProcessWizard_FillingPacking_Profile_Section_Value(Profilelist, ProcessAppPath)
    Process.Click_Icon(ProcessAppPath + r"\Btn_OK.png", ProcessAppPath + r"\Pro_Tab_FillingPacking.png")
    #Process Plasticizing Setting
    Process.PlasticizingSetting(ProcessAppPath, **{"BackPressure":"1", "ScrewSpeed":"100", "BarrelTemperature":""})
    Profilelist = [ProcessAppPath + r"\Pro_Barrel_TemperatureProfile.png", "220", "220", "210", "190"]
    Process.ProcessWizard_Barrel_Temperature_Profile_Section_Value(Profilelist, ProcessAppPath)
    Process.Click_IconEx(ProcessAppPath + r"\Btn_OK.png")
    #Process Tab Cooling Setting
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_FillingPacking.png", ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_Cooling_Cool_Time.png", 130, 0, "1", ProcessAppPath)
    #Process Tab Summary
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath + "\\Pro_Tab_Summary.png", ProcessAppPath)
    Process.ProcessWizard_Summary_Finish(ProcessAppPath)
    Log.write_log(ProjectName, "Info: Process Wizard Setting is Finished")
    
    #Analyze Setting
    Analyzelist = [StudioAppPath + "\\Analysis_PL.png"]
    Studio.AnalysisSetting(Analyzelist, StudioAppPath)
    Log.write_log(ProjectName, "Info: Analyze Setting is Finished")
    
    #Run 02
    #New Run
    Studio.Click_Icon(StudioAppPath, "\\Studio_NewRun2.png", 0)
    Log.write_log(ProjectName, "Info: New Run Setting is Finished")

    #Studio Pre Process Setting
    Studio.MeshType("Solid", StudioAppPath)
    Studio.Home_MoldingType_New("Module_IM2", StudioAppPath)
    Studio.Home_Model("ImportGeometry", StudioAppPath)
    Studio.ImportGeometry(Run02_SourcePath, StudioAppPath)
    Studio.Wait_Dialog(StudioAppPath, "\\Studio_UpdateJoint.png")
    Studio.SwitchTab(StudioAppPath + "\\Studio_Tab_Mesh.png", StudioAppPath + "\\Studio_Tab_Meshing.png")
    Studio.Meshing_Generate(StudioAppPath)
    Studio.Meshing_GenerateBLM("None", StudioAppPath)
    Studio.Wait_Dialog(StudioAppPath, "\\Studio_FinalCheck.png")
    Studio.Click_Icon(StudioAppPath, "\\Studio_Tree_Model.png", 0)
    Studio.Click_Icon(StudioAppPath, "\\Studio_Tree_MB.png", -45)
    Studio.Click_Icon(StudioAppPath, "\\Studio_Tree_CoolingChannel.png", -65)
    Studio.Click_Icon(StudioAppPath, "\\Btn_Angle_Perspective_Seletected.png", 40)
    Studio.Click_Icon(StudioAppPath, "\\Btn_Fit_To_Window.png", -24)
    Studio.Click_Icon(StudioAppPath, "\\Btn_ShowModeSelected_FeatureShaded2.png", 40)
    Studio.Final_Check(StudioAppPath)
    Log.write_log(ProjectName, "Info: Studio Pre Process Setting is Finished")
    
    #Material Wizard Setting
    #Part Material Setting
    Material.OpenMaterialWizard(MaterialAppPath + "\\Studio_EM1.png", 200, 0, MaterialAppPath)
    sMatlist = [MaterialAppPath + "\\MaterialABS.png", MaterialAppPath + "\\MaterialASchulman.png",MaterialAppPath + "\\MaterialRABS9050UV5.png"]
    Material.ClickMDXBank(MaterialAppPath)
    Material.SelectPartMaterial(sMatlist)
    Material.MaterialNotAddToUserBank(MaterialAppPath)
    Material.CloseMaterialWizard(MaterialAppPath)
    
    #Partinsert Material Setting
    sMatlist = [MaterialAppPath + "\\MaterialMetal.png", MaterialAppPath + "\\MaterialCAE.png",MaterialAppPath + "\\MaterialIron40.png"]
    Material.Wait_Dialog(StudioAppPath, "\\Logo_Fiber2.png", "\\Logo_NonFiber_UnSelected_Blue.png")
    #Material.Click_Icon(MaterialAppPath + "\\StudioPartInsert1.png", 200) 
    Material.OpenMaterialWizard(MaterialAppPath + "\\StudioPartInsert1.png", 200, 0, MaterialAppPath)
    Material.ClickMDXBank(MaterialAppPath)
    Material.SelectPartMaterial(sMatlist)
    Material.MaterialNotAddToUserBank(MaterialAppPath)
    Material.CloseMaterialWizard(MaterialAppPath)
    Log.write_log(ProjectName, "Info: Material Wizard Setting is Finished")
    
    #Process Wizard Setting
    Process.Home_Process("New", ProcessAppPath)
    #Process Tab Project Setting
    Process.ProcessWizard_Project_SettingMethod("M2", ProcessAppPath)
    Process.Click_IconEx(ProcessAppPath + r"\Pro_MachineSetting.png", **{"offsetx":15, "offsety":20})
    Process.Click_IconEx(ProcessAppPath + r"\Pro_QA_T2_2002.png")
    Process.Click_IconEx(ProcessAppPath + r"\Btn_No.png")
    #Process Tab Filling/Packing Setting
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_ProjectSetting.png", ProcessAppPath + "\\Pro_Tab_FillingPacking.png", ProcessAppPath)  
    Process.ValueSetting(ProcessAppPath + "\\Pro_Filling_InjectionTime.png", 100, 0, "2", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_Filling_RamPosition.png", 190, 0, "5", ProcessAppPath)
    #Process Filling/Packing - Flow Rate Profile Setting
    Process.Click_Icon(ProcessAppPath + r"\Btn_Pro_Flow_rate_profile.png", ProcessAppPath + r"\Pro_Filling_FlowRateProFile.png")
    Process.ValueSetting(ProcessAppPath + r"\Pro_SectionNo.png", 60, 0, "1", ProcessAppPath)
    Profilelist = [ProcessAppPath + r"\Pro_Filling_FlowRateProFile.png", "30", "50"]
    Process.ProcessWizard_FillingPacking_Profile_Section_Value(Profilelist, ProcessAppPath)
    Process.Click_Icon(ProcessAppPath + r"\Btn_OK.png", ProcessAppPath + r"\Pro_Tab_FillingPacking.png")
    Process.PlasticizingSetting(ProcessAppPath, **{"BackPressure":"1", "ScrewSpeed":"100", "BarrelTemperature":""})
    Profilelist = [ProcessAppPath + r"\Pro_Barrel_TemperatureProfile.png", "220", "220", "210", "190"]
    Process.ProcessWizard_Barrel_Temperature_Profile_Section_Value(Profilelist, ProcessAppPath)
    Process.Click_IconEx(ProcessAppPath + r"\Btn_OK.png")
    #Process Tab Cooling Setting
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_FillingPacking.png", ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath)
    #Process Tab Summary
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath + "\\Pro_Tab_Summary.png", ProcessAppPath)
    Process.ProcessWizard_Summary_Finish(ProcessAppPath)
    Log.write_log(ProjectName, "Info: Process Wizard Setting is Finished")
    
    #Analyze Setting
    Analyzelist = [StudioAppPath + "\\Analysis_PL.png"]
    Studio.AnalysisSetting(Analyzelist, StudioAppPath)
    Log.write_log(ProjectName, "Info: Analyze Setting is Finished")
    
    #Run 03
    #New Run
    Studio.Click_Icon(StudioAppPath, "\\Studio_NewRun2.png", 0)
    Log.write_log(ProjectName, "Info: New Run Setting is Finished")

    #Studio Pre Process Setting
    Studio.MeshType("eDesign", StudioAppPath)
    Studio.Home_MoldingType_New("Module_IM2", StudioAppPath)
    Studio.Home_Model("ImportGeometry", StudioAppPath)
    Studio.ImportGeometry(Run03_SourcePath, StudioAppPath)
    Studio.SwitchTab(StudioAppPath + "\\Studio_Tab_Mesh.png", StudioAppPath + "\\Studio_Tab_Meshing.png")
    Studio.Meshing_Generate(StudioAppPath)
    Studio.Meshing_GenerateeDesign(StudioAppPath)
    Studio.Wait_Dialog(StudioAppPath, "\\Log_Generate_Solid_Mesh_Done.png")
    Studio.Click_Icon(StudioAppPath, "\\Btn_Angle_Perspective_Seletected.png", 40)
    Studio.Click_Icon(StudioAppPath, "\\Btn_Fit_To_Window.png", -24)
    Studio.Click_Icon(StudioAppPath, "\\Btn_ShowModeSelected_FeatureShaded2.png", 40)
    Studio.Final_Check(StudioAppPath)
    Log.write_log(ProjectName, "Info: Studio Pre Process Setting is Finished")
    
    #Material Wizard Setting
    Material.Click_Icon(MaterialAppPath + "\\MaterialLogo.png", 0)
    Material.Click_Icon(MaterialAppPath + "\\Studio_EM1.png", 200)
    Material.MCM2ndRunInsertSelection(MaterialAppPath + "\\StudioPartInsertSelection.png", MaterialAppPath + "\\Studio_90950UV5.png", MaterialAppPath)
    #Partinsert Material Setting
    Material.Wait_Dialog(StudioAppPath, "\\Logo_Fiber2.png", "\\Logo_NonFiber_UnSelected_Blue.png")
    Material.Click_Icon(MaterialAppPath + "\\StudioPartInsert1.png", 200)
    Material.MCM2ndRunInsertSelection(MaterialAppPath + "\\StudioPartInsertSelection.png", MaterialAppPath + "\\Studio_Iron40.png", MaterialAppPath)
    Log.write_log(ProjectName, "Info: Material Wizard Setting is Finished")
    
    #Process Wizard Setting
    Process.Home_Process("New", ProcessAppPath)
    #Process Tab Project Setting
    Process.ProcessWizard_Project_SettingMethod("M1", ProcessAppPath)
    Process.Click_IconEx(ProcessAppPath + r"\Pro_MachineSetting.png", **{"offsetx":15, "offsety":20})
    Process.Click_IconEx(ProcessAppPath + r"\Pro_QA_T2_2002.png")
    Process.Click_IconEx(ProcessAppPath + r"\Btn_No.png")
    #Process Tab Filling/Packing Setting
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_ProjectSetting.png", ProcessAppPath + "\\Pro_Tab_FillingPacking.png", ProcessAppPath)  
    Process.ValueSetting(ProcessAppPath + "\\Pro_Filling_PackingTime.png", 60, 0, "3", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_Filling_RamPosition.png", 190, 0, "5", ProcessAppPath)
    #Process Filling/Packing - Flow Rate Profile Setting
    Process.Click_Icon(ProcessAppPath + r"\Btn_Pro_Flow_rate_profile.png", ProcessAppPath + r"\Pro_Filling_FlowRateProFile.png")
    Process.ValueSetting(ProcessAppPath + r"\Pro_SectionNo.png", 60, 0, "1", ProcessAppPath)
    Profilelist = [ProcessAppPath + r"\Pro_Filling_FlowRateProFile.png", "60", "50"]
    Process.ProcessWizard_FillingPacking_Profile_Section_Value(Profilelist, ProcessAppPath)
    Process.Click_Icon(ProcessAppPath + r"\Btn_OK.png", ProcessAppPath + r"\Pro_Tab_FillingPacking.png")
    Process.PlasticizingSetting(ProcessAppPath, **{"BackPressure":"1", "ScrewSpeed":"100", "BarrelTemperature":""})
    Profilelist = [ProcessAppPath + r"\Pro_Barrel_TemperatureProfile.png", "220", "220", "210", "190"]
    Process.ProcessWizard_Barrel_Temperature_Profile_Section_Value(Profilelist, ProcessAppPath)
    Process.Click_IconEx(ProcessAppPath + r"\Btn_OK.png")
    #Process Tab Cooling Setting
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_FillingPacking.png", ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath)
    #Process Tab Summary
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath + "\\Pro_Tab_Summary.png", ProcessAppPath)
    Process.ProcessWizard_Summary_Finish(ProcessAppPath)
    Log.write_log(ProjectName, "Info: Process Wizard Setting is Finished")
    
    #Analyze Setting
    Analyzelist = [StudioAppPath + "\\Analysis_PL.png"]
    Studio.AnalysisSetting(Analyzelist, StudioAppPath)
    Log.write_log(ProjectName, "Info: Analyze Setting is Finished")
    
    #Run 04
    #New Run
    Studio.Click_Icon(StudioAppPath, "\\Studio_NewRun2.png", 0)
    Log.write_log(ProjectName, "Info: New Run Setting is Finished")

    #Studio Pre Process Setting
    Studio.MeshType("Solid", StudioAppPath)
    Studio.Home_MoldingType_New("Module_IM2", StudioAppPath)
    Studio.Home_Model("ImportGeometry", StudioAppPath)
    Studio.ImportGeometry(Run04_SourcePath, StudioAppPath)
    Studio.SwitchTab(StudioAppPath + "\\Studio_Tab_Mesh.png", StudioAppPath + "\\Studio_Tab_Meshing.png")
    Studio.Meshing_Generate(StudioAppPath)
    Studio.Meshing_GenerateBLM("None", StudioAppPath)
    Studio.Wait_Dialog(StudioAppPath, "\\Studio_FinalCheck.png")
    Studio.Click_Icon(StudioAppPath, "\\Btn_Angle_Perspective_Seletected.png", 40)
    Studio.Click_Icon(StudioAppPath, "\\Btn_Fit_To_Window.png", -24)
    Studio.Click_Icon(StudioAppPath, "\\Btn_ShowModeSelected_FeatureShaded2.png", 40)
    Studio.Final_Check(StudioAppPath)
    Log.write_log(ProjectName, "Info: Studio Pre Process Setting is Finished")
    
    #Material Wizard Setting
    #Part Material Setting
    Material.OpenMaterialWizard(MaterialAppPath + "\\Studio_EM1.png", 200, 0, MaterialAppPath)
    sMatlist = [MaterialAppPath + "\\MaterialPP.png", MaterialAppPath + "\\MaterialCAE.png", MaterialAppPath + "\\Material125.png"]
    Material.ClickMDXBank(MaterialAppPath)
    Material.SelectPartMaterial(sMatlist)
    Material.MaterialNotAddToUserBank(MaterialAppPath)
    Material.CloseMaterialWizard(MaterialAppPath)
    
    #Process Wizard Setting
    Process.Home_Process("Default", ProcessAppPath)
    Log.write_log(ProjectName, "Info: Process Wizard Setting is Finished")
    
    #Analyze Setting
    Analyzelist = [StudioAppPath + "\\Analysis_Fq.png"]
    Studio.AnalysisSetting(Analyzelist, StudioAppPath)
    Log.write_log(ProjectName, "Info: Analyze Setting is Finished")
    
    #Run 05
    #New Run
    Studio.Click_Icon(StudioAppPath, "\\Studio_NewRun2.png", 0)
    Log.write_log(ProjectName, "Info: New Run Setting is Finished")

    #Studio Pre Process Setting
    Studio.MeshType("eDesign", StudioAppPath)
    Studio.Home_MoldingType_New("Module_IM2", StudioAppPath)
    Studio.Home_Model("ImportGeometry", StudioAppPath)
    Studio.ImportGeometry(Run05_SourcePath, StudioAppPath)
    Studio.SwitchTab(StudioAppPath + "\\Studio_Tab_Mesh.png", StudioAppPath + "\\Studio_Tab_Meshing.png")
    Studio.Meshing_Generate(StudioAppPath)
    Studio.Meshing_GenerateeDesign(StudioAppPath)
    Studio.Wait_Dialog(StudioAppPath, "\\Log_Generate_Solid_Mesh_Done.png")
    Studio.Click_Icon(StudioAppPath, "\\Btn_Angle_Perspective_Seletected.png", 40)
    Studio.Click_Icon(StudioAppPath, "\\Btn_Fit_To_Window.png", -24)
    Studio.Click_Icon(StudioAppPath, "\\Btn_ShowModeSelected_FeatureShaded2.png", 40)
    Studio.Final_Check(StudioAppPath)
    Log.write_log(ProjectName, "Info: Studio Pre Process Setting is Finished")
    
    #Material Wizard Setting
    #Part Material Setting
    Material.OpenMaterialWizard(MaterialAppPath + "\\Studio_EM1.png", 200, 0, MaterialAppPath)
    sMatlist = [MaterialAppPath + "\\MaterialPP.png", MaterialAppPath + "\\MaterialCAE.png", MaterialAppPath + "\\Material125.png"]
    Material.ClickMDXBank(MaterialAppPath)
    Material.SelectPartMaterial(sMatlist)
    Material.MaterialNotAddToUserBank(MaterialAppPath)
    Material.CloseMaterialWizard(MaterialAppPath)
    
    #Process Wizard Setting
    Process.Home_Process("Default", ProcessAppPath)
    Log.write_log(ProjectName, "Info: Process Wizard Setting is Finished")
    
    #Analyze Setting
    Analyzelist = [StudioAppPath + "\\Analysis_Fq.png"]
    Studio.AnalysisSetting(Analyzelist, StudioAppPath)
    Log.write_log(ProjectName, "Info: Analyze Setting is Finished")
    
    #Change Remark Name
    Studio.Click_Icon(StudioAppPath, "\\Studio_Tree_Run.png", 0)
    wait(1)
    Remark_name = ["PL-InjectionUnit", "PL-Solid", "PL-eDesign", "FQ-Solid", "FQ-eDesign"]
    CRN.Run(Remark_name, CRNAppPath)
    Log.write_log(ProjectName, "Info: Change Remark Name is Finished")
    
    #Set RC Task Number
    Studio.TaskNumberSetting("4", StudioAppPath)
    click(StudioAppPath + "\\Btn_OK.png")
    Studio.Create_BJS(13,StudioAppPath,ProjectName,WorkingFolder)
    CM.SendRCtoCM(StudioAppPath,CMAppPath)
    Log.write_log(ProjectName, "Info: Set RC Task Number is Finished")
    
    #Set Localhost Task Number
    Studio.TaskNumberSetting("1", StudioAppPath)
    click(StudioAppPath + "\\Btn_OK.png")
    Log.write_log(ProjectName, "Info: Set Localhost Task Number is Finished")

    #Localhost Server Connect
    Studio.OpenApp(CMPath, CMAppPath + "\\CM_UI.png")
    CM.connectserver("LH",CMAppPath)
    wait(1)
    click(StudioAppPath + "\\Studio_logo.png")
    Log.write_log(ProjectName, "Info: Computing Manager Add Server Setting is Finished")
    wait(1)
    Studio.ClickRun(30, StudioAppPath)
    Studio.Submit_Batch_Run(2,StudioAppPath)
    Log.write_log(ProjectName, "Info: Run the Analyze is Finished")
    wait(2)
    
    #Close Studio UI
    Studio.CloseApp(StudioPath)  
    Log.write_log(ProjectName, "Info: %s Test is Finished!" % ProjectName)
    
except:
    os.popen(("python {}").format(exceptprocedureApp))
    print( "ENT-IM-S15-P1 Test is Failed!")
    Log.write_log(ProjectName, "Error: %s Test is Failed!" % ProjectName)
Log.write_log2(ProjectName, "Summary")