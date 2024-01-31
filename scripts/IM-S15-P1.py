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


ProjectName = "IM-S15-P1"
username = "moldex3dqa"
password = "123456"
SVNPath = r"svn://192.168.3.4/QARepository/AutoTest/Moldex3D/2023Series/Moldex3D/CaseReference/ENT/" + ProjectName + r"/Geometry"
Filename= SVNPath.split('/')[-2]
localpath = os.path.normpath((cwd + r"\\" +Filename))
MainInstallPath ,ver = Common.getregkeyvalue(r"HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\CoreTechSystem\MDX_ParallelComputing", "INSTALLDIR")
WorkingFolder = Common.getregkeyvalue(r"HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\CoreTechSystem\MDX_ParallelComputing", "WorkingFolder")
StudioPath = MainInstallPath + r"\Bin\MDXStudio.exe"

CaseReferncePath = Common.gototargetpath('MDX_ENT') + "\\" + ProjectName
IM_FC_1st_SourcePath =CaseReferncePath+ r"\IM-1st shot-FC.mdg"
IM_IM_FC_2nd_SourcePath =CaseReferncePath+ r"\IM-IM-2nd shot-FC.mdg"
IM_SC_1st_SourcePath =CaseReferncePath+ r"\IM-1st shot-SC.mdg"
IM_ICM_SC_2nd_SourcePath =CaseReferncePath+ r"\IM-ICM-2nd shot-SC.mdg"
IM_eDesign_1st_SourcePath =CaseReferncePath+ r"\IM-1st shot-eDesign.mdg"
IM_IM_eDesign_2nd_SourcePath =CaseReferncePath+ r"\IM-IM-2nd shot-eDesign.mdg"
CM_FC_1st_SourcePath =CaseReferncePath+ r"\CM-1st shot-FC.mdg"
CM_FC_1st_Charge_SourcePath =CaseReferncePath+ r"\CM-1st shot-FC-Charge.stl"
CM_IM_FC_2nd_SourcePath =CaseReferncePath+ r"\CM-IM-2nd shot-FC.mdg"

CMPath = MainInstallPath + r"\Bin\MDXComputingManager" + ver + ".exe"
hostname, local_ip = Common.getcuriphostname()


try:
    #Delete Bank and Material Folderg
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
    Studio.ImportGeometry(IM_FC_1st_SourcePath, StudioAppPath)
    Studio.Wait_Dialog(StudioAppPath, "\\Studio_UpdateJoint.png")
    Studio.SwitchTab(StudioAppPath + "\\Studio_Tab_Mesh.png", StudioAppPath + "\\Studio_Tab_Meshing.png")
    Studio.Meshing_Generate(StudioAppPath)
    Studio.Meshing_GenerateBLM("Runner", StudioAppPath)
    Studio.Wait_Dialog(StudioAppPath, "\\Studio_Runner_Check.png")
    Studio.Click_Icon(StudioAppPath, "\\Btn_Angle_Perspective_Seletected.png", 40)
    Studio.Click_Icon(StudioAppPath, "\\Btn_Fit_To_Window.png", -24)
    Studio.Click_Icon(StudioAppPath, "\\Btn_ShowModeSelected_FeatureShaded2.png", 40)
    Studio.Final_Check(StudioAppPath)
    Log.write_log(ProjectName, "Info: Studio Pre Process Setting is Finished")
    
    #Material Wizard Setting
    sMatlist = [MaterialAppPath + "\\MaterialPC.png", MaterialAppPath + "\\MaterialSABIC.png",MaterialAppPath + "\\MaterialLEXANEXL1414.png"]
    Material.OpenMaterialWizard(MaterialAppPath + "\\Studio_EM1.png", 200, 0, MaterialAppPath)
    Material.ClickMDXBank(MaterialAppPath)
    Material.SelectPartMaterial(sMatlist)
    Material.MaterialNotAddToUserBank(MaterialAppPath)
    Material.CloseMaterialWizard(MaterialAppPath)
    Log.write_log(ProjectName, "Info: Material Wizard Setting is Finished")
    
    #Process Wizard Setting
    Process.Home_Process("New", ProcessAppPath)
    #Process Tab Filling/Packing Setting  
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_ProjectSetting.png", ProcessAppPath + "\\Pro_Tab_FillingPacking.png", ProcessAppPath)  
    Process.ValueSetting(ProcessAppPath + "\\Pro_Filling_FillingTime.png", 60, 0, "0.45", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_Filling_PackingTime.png", 60, 0, "3.15", ProcessAppPath)
    #Process Filling/Packing - Flow Rate Profile Setting
    Process.Click_Icon(ProcessAppPath + "\\Btn_Pro_Flow_rate_profile.png", ProcessAppPath + "\\Pro_Filling_FlowRateProFile.png")
    Process.ProcessWizard_FillingPacking_Profile_Type_Switch("\\Pro_Type_FlowRate%Time%.png", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_SectionNo.png", 60, 0, "1", ProcessAppPath)
    Profilelist = [ProcessAppPath + "\\Pro_Filling_FlowRateProFile.png", "50"]
    Process.ProcessWizard_FillingPacking_Profile_Section_Value(Profilelist, ProcessAppPath)
    Process.Click_Icon(ProcessAppPath + "\\Btn_OK.png", ProcessAppPath + "\\Pro_Tab_FillingPacking.png")
    #Process Tab Cooling Setting
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_FillingPacking.png", ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_Cooling_Cool_Time.png", 130, 0, "10", ProcessAppPath)
    #Process Tab Summary
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath + "\\Pro_Tab_Summary.png", ProcessAppPath)
    Process.ProcessWizard_Summary_Finish(ProcessAppPath)
    Log.write_log(ProjectName, "Info: Process Wizard Setting is Finished")
    
    #Analyze Setting
    Analyzelist = [StudioAppPath + "\\Analysis_FPCWO.png", StudioAppPath + "\\Analysis_Filling_2.png", StudioAppPath + "\\Analysis_Packing2.png", StudioAppPath + "\\Analysis_CoolingCycle2.png", StudioAppPath + "\\Analysis_Warpage.png", StudioAppPath + "\\Analysis_Optics2.png"]
    Studio.AnalysisSetting(Analyzelist, StudioAppPath)
    Log.write_log(ProjectName, "Info: Analyze Setting is Finished")
    
    #Computation Parameter Wizard Setting
    #CMX Tab Flow/Pack Setting
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\ComputationLogo.png")    
    #CMX Tab Cool Setting
    CMX.CMX_Tab_Change(CMXAppPath + "\\CMX_Tab_Cool.png")
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\CMX_Cooling_AccurancyLevel_Standard.png")
    #CMX Tab VE/Optics Setting
    CMX.CMX_Tab_Change(CMXAppPath + "\\CMX_Tab_VEOptics.png")
    CMX.Checkbox(CMXAppPath + "\\CMX_VEOptics_EstimateFillingPackingStage.png", -90, 0, CMXAppPath)
    CMX.Checkbox(CMXAppPath + "\\CMX_VEOptics_EstimateCoolingStage.png", -73, 0, CMXAppPath)
    CMX.Checkbox(CMXAppPath + "\\CMX_VEOptics_EstimateOpticsProperties.png", -73, 0, CMXAppPath)
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\CMX_Btn_Add.png")
    CMX.ValueSetting(CMXAppPath + "\\CMX_Direction_X.png", 0, 20, "0.00")
    CMX.ValueSetting(CMXAppPath + "\\CMX_Direction_Y.png", 0, 20, "0.00")
    CMX.ValueSetting(CMXAppPath + "\\CMX_Direction_Z.png", 0, 20, "1.00")
    CMX.Checkbox(CMXAppPath + "\\CMX_VEOptics_PlanePolariscope.png", -30, 0, CMXAppPath)
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\CMX_Btn_OK.png")
    Log.write_log(ProjectName, "Info: Computation Parameter Wizard Setting is Finished")

    #Run 02
    #New Run
    Studio.Click_Icon(StudioAppPath, "\\Studio_NewRun2.png", 0)
    Log.write_log(ProjectName, "Info: New Run Setting is Finished")

    #Studio Pre Process Setting
    Studio.MeshType("Solid", StudioAppPath)
    Studio.Home_MoldingType_New("Module_IM2", StudioAppPath)
    Studio.Home_Model("ImportGeometry", StudioAppPath)
    Studio.ImportGeometry(IM_IM_FC_2nd_SourcePath, StudioAppPath)
    Studio.Wait_Dialog(StudioAppPath, "\\Studio_UpdateJoint.png")
    Studio.SwitchTab(StudioAppPath + "\\Studio_Tab_Mesh.png", StudioAppPath + "\\Studio_Tab_Meshing.png")
    Studio.Meshing_Generate(StudioAppPath)
    Studio.Meshing_GenerateBLM("Runner", StudioAppPath)
    Studio.Wait_Dialog(StudioAppPath, "\\Studio_Runner_Check.png")
    Studio.Click_Icon(StudioAppPath, "\\Btn_Angle_Perspective_Seletected.png", 40)
    Studio.Click_Icon(StudioAppPath, "\\Btn_Fit_To_Window.png", -24)
    Studio.Click_Icon(StudioAppPath, "\\Btn_ShowModeSelected_FeatureShaded2.png", 40)
    Studio.Final_Check(StudioAppPath)
    Log.write_log(ProjectName, "Info: Studio Pre Process Setting is Finished")

    #Material Wizard Setting
    #Part Material Setting
    Material.OpenMaterialWizard(MaterialAppPath + "\\Studio_EM1.png", 200, 0, MaterialAppPath)
    sMatlist = [MaterialAppPath + "\\MaterialPC.png", MaterialAppPath + "\\MaterialCoverstro.png", MaterialAppPath + "\\MaterialApecDP99331.png"]
    Material.ClickMDXBank(MaterialAppPath)
    Material.SelectPartMaterial(sMatlist)
    Material.MaterialNotAddToUserBank(MaterialAppPath)
    Material.CloseMaterialWizard(MaterialAppPath)
    #Partinsert Material Setting
    Material.Wait_Dialog(StudioAppPath, "\\Logo_NonFiber_UnSelected.png", "\\Logo_NonFiber_UnSelected_Blue.png")
    Material.Click_Icon(MaterialAppPath + "\\StudioPartInsert1.png", 200) 
    Material.MCM2ndRunInsertSelection(MaterialAppPath + "\\StudioPartInsertSelection.png", MaterialAppPath + "\\Studio_LEXANEXL1414.png", MaterialAppPath)
    Log.write_log(ProjectName, "Info: Material Wizard Setting is Finished")

    #Process Wizard Setting
    Process.Home_Process("New", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + r"\Pro_Project_MaxInjectPressure.png", 150, 0, "350", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + r"\Pro_Project_MaxPackPressure.png", 150, 0, "350", ProcessAppPath)
    #Process Tab Filling/Packing Setting  
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_ProjectSetting.png", ProcessAppPath + "\\Pro_Tab_FillingPacking.png", ProcessAppPath)  
    Process.ValueSetting(ProcessAppPath + "\\Pro_Filling_FillingTime.png", 60, 0, "0.5", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_Filling_PackingTime.png", 60, 0, "3", ProcessAppPath)
    #Process Filling/Packing - Flow Rate Profile Setting
    Process.Click_Icon(ProcessAppPath + "\\Btn_Pro_Flow_rate_profile.png", ProcessAppPath + "\\Pro_Filling_FlowRateProFile.png")
    Process.ProcessWizard_FillingPacking_Profile_Type_Switch("\\Pro_Type_FlowRate%Time%.png", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_SectionNo.png", 60, 0, "1", ProcessAppPath)
    Profilelist = [ProcessAppPath + "\\Pro_Filling_FlowRateProFile.png", "50"]
    Process.ProcessWizard_FillingPacking_Profile_Section_Value(Profilelist, ProcessAppPath)
    Process.Click_Icon(ProcessAppPath + "\\Btn_OK.png", ProcessAppPath + "\\Pro_Tab_FillingPacking.png")
    #Process Tab Cooling Setting
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_FillingPacking.png", ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath)
    #Process Tab Summary
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath + "\\Pro_Tab_Summary.png", ProcessAppPath)
    Process.ProcessWizard_Summary_Finish(ProcessAppPath)
    Log.write_log(ProjectName, "Info: Process Wizard Setting is Finished")

    #Analyze Setting
    Analyzelist = [StudioAppPath + "\\Analysis_CFPCtWO.png", StudioAppPath + "\\Analysis_CoolingCycle2.png", StudioAppPath + "\\Analysis_Filling_2.png", StudioAppPath + "\\Analysis_Packing2.png", StudioAppPath + "\\Analysis_CoolingTransient_2.png", StudioAppPath + "\\Analysis_Warpage.png", StudioAppPath + "\\Analysis_Optics2.png"]
    Studio.AnalysisSetting(Analyzelist, StudioAppPath)
    Log.write_log(ProjectName, "Info: Analyze Setting is Finished")
    
    #Computation Parameter Wizard Setting
    #CMX Tab Flow/Pack Setting
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\ComputationLogo.png")    
    #CMX Tab Cool Setting
    CMX.CMX_Tab_Change(CMXAppPath + "\\CMX_Tab_Cool.png")
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\CMX_Cooling_AccurancyLevel_Standard.png")
    #CMX Tab MCM Setting
    CMX.CMX_Tab_Change(CMXAppPath + "\\CMX_Tab_MCM.png")
    CMX.Checkbox(CMXAppPath + "\\CMX_MCM_LinkWithThePreviousShot.png", -75, 0, CMXAppPath)
    CMX.SelectDropDownMenu(CMXAppPath + "\\CMX_MCM_Run.png", 100, 0, CMXAppPath + "\\CMX_MCM_Run01.png", 0, 0)
    #CMX Tab VE/Optics Setting
    CMX.CMX_Tab_Change(CMXAppPath + "\\CMX_Tab_VEOptics.png")
    CMX.Checkbox(CMXAppPath + "\\CMX_VEOptics_EstimateFillingPackingStage.png", -90, 0, CMXAppPath)
    CMX.Checkbox(CMXAppPath + "\\CMX_VEOptics_EstimateCoolingStage.png", -73, 0, CMXAppPath)
    CMX.Checkbox(CMXAppPath + "\\CMX_VEOptics_EstimateOpticsProperties.png", -73, 0, CMXAppPath)
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\CMX_Btn_Add.png")
    CMX.ValueSetting(CMXAppPath + "\\CMX_Direction_X.png", 0, 20, "0.00")
    CMX.ValueSetting(CMXAppPath + "\\CMX_Direction_Y.png", 0, 20, "0.00")
    CMX.ValueSetting(CMXAppPath + "\\CMX_Direction_Z.png", 0, 20, "1.00")
    CMX.Checkbox(CMXAppPath + "\\CMX_VEOptics_PlanePolariscope.png", -30, 0, CMXAppPath)
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\CMX_Btn_OK.png")
    if exists(CMXAppPath + "\\CMX_DLG_Moldex3DStudio.png"):    
        CMX.ClickButton(CMXAppPath, CMXAppPath + "\\CMX_Btn_OK_2.png")
    Log.write_log(ProjectName, "Info: Computation Parameter Wizard Setting is Finished")
    
    #Run 03
    #New Run
    Studio.Click_Icon(StudioAppPath, "\\Studio_NewRun2.png", 0)
    Log.write_log(ProjectName, "Info: New Run Setting is Finished")

    #Studio Pre Process Setting
    Studio.MeshType("eDesign", StudioAppPath)
    Studio.Home_MoldingType_New("Module_IM2", StudioAppPath)
    Studio.Home_Model("ImportGeometry", StudioAppPath)
    Studio.ImportGeometry(IM_eDesign_1st_SourcePath, StudioAppPath)
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
    sMatlist = [MaterialAppPath + "\\MaterialPC+ABS.png", MaterialAppPath + "\\MaterialAlmmak.png",MaterialAppPath + "\\Material05580GF20.png"]
    Material.OpenMaterialWizard(MaterialAppPath + "\\Studio_EM1.png", 200, 0, MaterialAppPath)
    Material.ClickMDXBank(MaterialAppPath)
    Material.SelectPartMaterial(sMatlist)
    Material.MaterialNotAddToUserBank(MaterialAppPath)
    Material.CloseMaterialWizard(MaterialAppPath)
    Log.write_log(ProjectName, "Info: Material Wizard Setting is Finished")
    
    #Process Wizard Setting
    Process.Home_Process("New", ProcessAppPath)
    #Process Tab Filling/Packing Setting  
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_ProjectSetting.png", ProcessAppPath + "\\Pro_Tab_FillingPacking.png", ProcessAppPath)  
    Process.ValueSetting(ProcessAppPath + "\\Pro_Filling_FillingTime.png", 60, 0, "0.1", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_Filling_PackingTime.png", 60, 0, "3.15", ProcessAppPath)
    #Process Filling/Packing - Flow Rate Profile Setting
    Process.Click_Icon(ProcessAppPath + "\\Btn_Pro_Flow_rate_profile.png", ProcessAppPath + "\\Pro_Filling_FlowRateProFile.png")
    Process.ProcessWizard_FillingPacking_Profile_Type_Switch("\\Pro_Type_FlowRate%Time%.png", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_SectionNo.png", 60, 0, "1", ProcessAppPath)
    Profilelist = [ProcessAppPath + "\\Pro_Filling_FlowRateProFile.png", "50"]
    Process.ProcessWizard_FillingPacking_Profile_Section_Value(Profilelist, ProcessAppPath)
    Process.Click_Icon(ProcessAppPath + "\\Btn_OK.png", ProcessAppPath + "\\Pro_Tab_FillingPacking.png")
    #Process Tab Cooling Setting
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_FillingPacking.png", ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_Cooling_Cool_Time.png", 130, 0, "10", ProcessAppPath)
    #Process Tab Summary
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath + "\\Pro_Tab_Summary.png", ProcessAppPath)
    Process.ProcessWizard_Summary_Finish(ProcessAppPath)
    Log.write_log(ProjectName, "Info: Process Wizard Setting is Finished")
    
    #Analyze Setting
    Analyzelist = [StudioAppPath + "\\Analysis_CFC.png", StudioAppPath + "\\Analysis_CoolingCycle2.png", StudioAppPath + "\\Analysis_Filling_2.png", StudioAppPath + "\\Analysis_CoolingCycle2.png"]
    Studio.AnalysisSetting(Analyzelist, StudioAppPath)
    Log.write_log(ProjectName, "Info: Analyze Setting is Finished")
    
    #Computation Parameter Wizard Setting
    #CMX Tab Flow/Pack Setting
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\ComputationLogo.png")    
    #CMX Tab Cool Setting
    CMX.CMX_Tab_Change(CMXAppPath + "\\CMX_Tab_Cool.png")
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\CMX_Cooling_AccurancyLevel_Standard.png")
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\CMX_Btn_OK.png")
    Log.write_log(ProjectName, "Info: Computation Parameter Wizard Setting is Finished")
    
    #Run 04
    #New Run
    Studio.Click_Icon(StudioAppPath, "\\Studio_NewRun2.png", 0)
    Log.write_log(ProjectName, "Info: New Run Setting is Finished")

    #Studio Pre Process Setting
    Studio.MeshType("eDesign", StudioAppPath)
    Studio.Home_MoldingType_New("Module_IM2", StudioAppPath)
    Studio.Home_Model("ImportGeometry", StudioAppPath)
    Studio.ImportGeometry(IM_IM_eDesign_2nd_SourcePath, StudioAppPath)
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
    sMatlist = [MaterialAppPath + "\\MaterialABS.png", MaterialAppPath + "\\MaterialASchulman.png", MaterialAppPath + "\\MaterialRABS9050UV5.png"]
    Material.ClickMDXBank(MaterialAppPath)
    Material.SelectPartMaterial(sMatlist)
    Material.MaterialNotAddToUserBank(MaterialAppPath)
    Material.CloseMaterialWizard(MaterialAppPath)
    #Partinsert Material Setting
    Material.Wait_Dialog(StudioAppPath, "\\Logo_NonFiber_UnSelected.png", "\\Logo_NonFiber_UnSelected_Blue.png")
    Material.Click_Icon(MaterialAppPath + "\\StudioPartInsert1.png", 200) 
    Material.MCM2ndRunInsertSelection(MaterialAppPath + "\\StudioPartInsertSelection.png", MaterialAppPath + "\\Studio_05580GF20.png", MaterialAppPath)
    Log.write_log(ProjectName, "Info: Material Wizard Setting is Finished")

    #Process Wizard Setting
    Process.Home_Process("New", ProcessAppPath)
    #Process Tab Filling/Packing Setting  
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_ProjectSetting.png", ProcessAppPath + "\\Pro_Tab_FillingPacking.png", ProcessAppPath)  
    Process.ValueSetting(ProcessAppPath + "\\Pro_Filling_FillingTime.png", 60, 0, "0.1", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_Filling_PackingTime.png", 60, 0, "3.4", ProcessAppPath)
    #Process Filling/Packing - Flow Rate Profile Setting
    Process.Click_Icon(ProcessAppPath + "\\Btn_Pro_Flow_rate_profile.png", ProcessAppPath + "\\Pro_Filling_FlowRateProFile.png")
    Process.ProcessWizard_FillingPacking_Profile_Type_Switch("\\Pro_Type_FlowRate%Time%.png", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_SectionNo.png", 60, 0, "1", ProcessAppPath)
    Profilelist = [ProcessAppPath + "\\Pro_Filling_FlowRateProFile.png", "50"]
    Process.ProcessWizard_FillingPacking_Profile_Section_Value(Profilelist, ProcessAppPath)
    Process.Click_Icon(ProcessAppPath + "\\Btn_OK.png", ProcessAppPath + "\\Pro_Tab_FillingPacking.png")
    #Process Tab Cooling Setting
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_FillingPacking.png", ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath)
    #Process Tab Summary
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath + "\\Pro_Tab_Summary.png", ProcessAppPath)
    Process.ProcessWizard_Summary_Finish(ProcessAppPath)
    Log.write_log(ProjectName, "Info: Process Wizard Setting is Finished")

    #Analyze Setting
    Analyzelist = [StudioAppPath + "\\Analysis_CFPCtW.png", StudioAppPath + "\\Analysis_CoolingCycle2.png", StudioAppPath + "\\Analysis_Filling_2.png", StudioAppPath + "\\Analysis_Packing2.png", StudioAppPath + "\\Analysis_CoolingTransient_2.png", StudioAppPath + "\\Analysis_Warpage.png"]
    Studio.AnalysisSetting(Analyzelist, StudioAppPath)
    Log.write_log(ProjectName, "Info: Analyze Setting is Finished")
    
    #Computation Parameter Wizard Setting
    #CMX Tab Flow/Pack Setting
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\ComputationLogo.png")    
    #CMX Tab Cool Setting
    CMX.CMX_Tab_Change(CMXAppPath + "\\CMX_Tab_Cool.png")
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\CMX_Cooling_AccurancyLevel_Standard.png")
    #CMX Tab MCM Setting
    CMX.CMX_Tab_Change(CMXAppPath + "\\CMX_Tab_MCM.png")
    CMX.Checkbox(CMXAppPath + "\\CMX_MCM_LinkWithThePreviousShot.png", -75, 0, CMXAppPath)
    CMX.SelectDropDownMenu(CMXAppPath + "\\CMX_MCM_Run.png", 100, 0, CMXAppPath + "\\CMX_MCM_Run03.png", 0, 0)
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\CMX_Btn_OK.png")
    if exists(CMXAppPath + "\\CMX_DLG_Moldex3DStudio.png"):    
        CMX.ClickButton(CMXAppPath, CMXAppPath + "\\CMX_Btn_OK_2.png")
    Log.write_log(ProjectName, "Info: Computation Parameter Wizard Setting is Finished")
    
    #Run 05
    #New Run
    Studio.Click_Icon(StudioAppPath, "\\Studio_NewRun2.png", 0)
    Log.write_log(ProjectName, "Info: New Run Setting is Finished")

    #Studio Pre Process Setting
    Studio.MeshType("Solid", StudioAppPath)
    Studio.Home_MoldingType_New("Module_IM2", StudioAppPath)
    Studio.Home_Model("ImportGeometry", StudioAppPath)
    Studio.ImportGeometry(IM_SC_1st_SourcePath, StudioAppPath)
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
    sMatlist = [MaterialAppPath + "\\MaterialPC+ABS.png", MaterialAppPath + "\\MaterialSABIC.png",MaterialAppPath + "\\MaterialC4210.png"]
    Material.OpenMaterialWizard(MaterialAppPath + "\\Studio_EM1.png", 200, 0, MaterialAppPath)
    Material.ClickMDXBank(MaterialAppPath)
    Material.SelectPartMaterial(sMatlist)
    Material.MaterialNotAddToUserBank(MaterialAppPath)
    Material.CloseMaterialWizard(MaterialAppPath)
    Log.write_log(ProjectName, "Info: Material Wizard Setting is Finished")
    
    #Process Wizard Setting
    Process.Home_Process("New", ProcessAppPath)
    #Process Tab Filling/Packing Setting  
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_ProjectSetting.png", ProcessAppPath + "\\Pro_Tab_FillingPacking.png", ProcessAppPath)  
    Process.ValueSetting(ProcessAppPath + "\\Pro_Filling_FillingTime.png", 60, 0, "1.3", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_Filling_PackingTime.png", 60, 0, "3.3", ProcessAppPath)
    #Process Filling/Packing - Flow Rate Profile Setting
    Process.Click_Icon(ProcessAppPath + "\\Btn_Pro_Flow_rate_profile.png", ProcessAppPath + "\\Pro_Filling_FlowRateProFile.png")
    Process.ProcessWizard_FillingPacking_Profile_Type_Switch("\\Pro_Type_FlowRate%Time%.png", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_SectionNo.png", 60, 0, "1", ProcessAppPath)
    Profilelist = [ProcessAppPath + "\\Pro_Filling_FlowRateProFile.png", "50"]
    Process.ProcessWizard_FillingPacking_Profile_Section_Value(Profilelist, ProcessAppPath)
    Process.Click_Icon(ProcessAppPath + "\\Btn_OK.png", ProcessAppPath + "\\Pro_Tab_FillingPacking.png")
    #Process Tab Cooling Setting
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_FillingPacking.png", ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_Cooling_Cool_Time.png", 130, 0, "10", ProcessAppPath)
    #Process Tab Summary
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath + "\\Pro_Tab_Summary.png", ProcessAppPath)
    Process.ProcessWizard_Summary_Finish(ProcessAppPath)
    Log.write_log(ProjectName, "Info: Process Wizard Setting is Finished")
    
    #Analyze Setting
    Analyzelist = [StudioAppPath + "\\Analysis_CFC.png", StudioAppPath + "\\Analysis_CoolingCycle2.png", StudioAppPath + "\\Analysis_Filling_2.png", StudioAppPath + "\\Analysis_CoolingCycle2.png"]
    Studio.AnalysisSetting(Analyzelist, StudioAppPath)
    Log.write_log(ProjectName, "Info: Analyze Setting is Finished")
    
    #Run 06
    #New Run
    Studio.Click_Icon(StudioAppPath, "\\Studio_NewRun2.png", 0)
    Log.write_log(ProjectName, "Info: New Run Setting is Finished")

    #Studio Pre Process Setting
    Studio.MeshType("Solid", StudioAppPath)
    Studio.Home_MoldingType_New("Module_ICM", StudioAppPath)
    Studio.Home_Model("ImportGeometry", StudioAppPath)
    Studio.ImportGeometry(IM_ICM_SC_2nd_SourcePath, StudioAppPath)
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
    sMatlist = [MaterialAppPath + "\\MaterialABS.png", MaterialAppPath + "\\MaterialASchulman.png", MaterialAppPath + "\\MaterialRABS9000UV5.png"]
    Material.ClickMDXBank(MaterialAppPath)
    Material.SelectPartMaterial(sMatlist)
    Material.MaterialNotAddToUserBank(MaterialAppPath)
    Material.CloseMaterialWizard(MaterialAppPath)
    #Partinsert Material Setting
    Material.Wait_Dialog(StudioAppPath, "\\Logo_NonFiber_UnSelected.png", "\\Logo_NonFiber_UnSelected_Blue.png")
    Material.Click_Icon(MaterialAppPath + "\\StudioPartInsert1.png", 200) 
    Material.MCM2ndRunInsertSelection(MaterialAppPath + "\\StudioPartInsertSelection.png", MaterialAppPath + "\\Studio_C4210.png", MaterialAppPath)
    Log.write_log(ProjectName, "Info: Material Wizard Setting is Finished")

    #Process Wizard Setting
    Process.Home_Process("New", ProcessAppPath)
    #Process Tab Filling/Packing Setting  
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_ProjectSetting.png", ProcessAppPath + "\\Pro_Tab_FillingPacking.png", ProcessAppPath)  
    Process.ValueSetting(ProcessAppPath + "\\Pro_Filling_FillingTime.png", 60, 0, "1.8", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_Filling_PackingTime.png", 60, 0, "13", ProcessAppPath)
    #Process Filling/Packing - Flow Rate Profile Setting
    Process.Click_Icon(ProcessAppPath + "\\Btn_Pro_Flow_rate_profile.png", ProcessAppPath + "\\Pro_Filling_FlowRateProFile.png")
    Process.ProcessWizard_FillingPacking_Profile_Type_Switch("\\Pro_Type_FlowRate%Time%.png", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_SectionNo.png", 60, 0, "1", ProcessAppPath)
    Profilelist = [ProcessAppPath + "\\Pro_Filling_FlowRateProFile.png", "50"]
    Process.ProcessWizard_FillingPacking_Profile_Section_Value(Profilelist, ProcessAppPath)
    Process.Click_Icon(ProcessAppPath + "\\Btn_OK.png", ProcessAppPath + "\\Pro_Tab_FillingPacking.png")
    #Process Tab Compression Setting
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_FillingPacking.png", ProcessAppPath + "\\Pro_Tab_Compression.png", ProcessAppPath)  
    Process.ValueSetting(ProcessAppPath + "\\Pro_Compression_CompressionTime.png", 75, 0, "2", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_Compression_ColumeFilled.png", 175, 0, "60", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_Comression_MaxCompressionSpeed.png", 120, 0, "10", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_Compression_MaxCompressionForce.png", 120, 0, "200", ProcessAppPath)
    #Process Tab Cooling Setting
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_Compression.png", ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath)
    #Process Tab Summary
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath + "\\Pro_Tab_Summary.png", ProcessAppPath)
    Process.ProcessWizard_Summary_Finish(ProcessAppPath)
    Log.write_log(ProjectName, "Info: Process Wizard Setting is Finished")

    #Analyze Setting
    Analyzelist = [StudioAppPath + "\\Analysis_CFAndPCtW.png", StudioAppPath + "\\Analysis_CoolingCycle2.png", StudioAppPath + "\\Analysis_FillingAndPacking_2.png", StudioAppPath + "\\Analysis_CoolingTransient_2.png", StudioAppPath + "\\Analysis_Warpage.png"]
    Studio.AnalysisSetting(Analyzelist, StudioAppPath)
    Log.write_log(ProjectName, "Info: Analyze Setting is Finished")
    
    #Computation Parameter Wizard Setting
    #CMX Tab Flow/Pack Setting
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\ComputationLogo.png")    
    #CMX Tab Cool Setting
    CMX.CMX_Tab_Change(CMXAppPath + "\\CMX_Tab_Cool.png")
    #CMX Tab MCM Setting
    CMX.CMX_Tab_Change(CMXAppPath + "\\CMX_Tab_MCM.png")
    CMX.Checkbox(CMXAppPath + "\\CMX_MCM_LinkWithThePreviousShot.png", -75, 0, CMXAppPath)
    CMX.SelectDropDownMenu(CMXAppPath + "\\CMX_MCM_Run.png", 100, 0, CMXAppPath + "\\CMX_MCM_Run05.png", 0, 0)
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\CMX_Btn_OK.png")
    if exists(CMXAppPath + "\\CMX_DLG_Moldex3DStudio.png"):    
        CMX.ClickButton(CMXAppPath, CMXAppPath + "\\CMX_Btn_OK_2.png")
    Log.write_log(ProjectName, "Info: Computation Parameter Wizard Setting is Finished")
    
    #Run 07
    #New Run
    Studio.Click_Icon(StudioAppPath, "\\Studio_NewRun2.png", 0)
    Log.write_log(ProjectName, "Info: New Run Setting is Finished")

    #Studio Pre Process Setting
    Studio.MeshType("Solid", StudioAppPath)
    Studio.Home_MoldingType_New("Module_CM", StudioAppPath)
    Studio.Home_Model("ImportGeometry", StudioAppPath)
    Studio.ImportGeometry(CM_FC_1st_SourcePath, StudioAppPath)
    Studio.SwitchTab(StudioAppPath + "\\Studio_Tab_Mesh.png", StudioAppPath + "\\Studio_Tab_Meshing.png")
    Studio.Meshing_Generate(StudioAppPath)
    Studio.Meshing_GenerateBLM("CompressionZone", StudioAppPath)
    Studio.Wait_Dialog(StudioAppPath, "\\Studio_CompressionZone_Check.png")
    Studio.Click_Icon(StudioAppPath, "\\Btn_Angle_Perspective_Seletected.png", 40)
    Studio.Click_Icon(StudioAppPath, "\\Btn_Fit_To_Window.png", -24)
    Studio.Click_Icon(StudioAppPath, "\\Btn_ShowModeSelected_FeatureShaded2.png", 40)
    Studio.Final_Check(StudioAppPath)
    Studio.Home_Model("ImportGeometry", StudioAppPath)
    Studio.ImportGeometry(CM_FC_1st_Charge_SourcePath, StudioAppPath)
    Studio.SwitchTab(StudioAppPath + "\\Studio_Tab_Home_Blue.png", StudioAppPath + "\\Studio_Tab_Home.png")
    Studio.SetCharge(StudioAppPath)
    Log.write_log(ProjectName, "Info: Studio Pre Process Setting is Finished")
    
    #Material Wizard Setting
    sMatlist = [MaterialAppPath + "\\MaterialSMC.png", MaterialAppPath + "\\MaterialCAE.png",MaterialAppPath + "\\MaterialCAESMC1.png"]
    Material.OpenMaterialWizard(MaterialAppPath + "\\Studio_Charge1.png", 200, 0, MaterialAppPath)
    Material.ClickMDXBank(MaterialAppPath)
    Material.SelectPartMaterial(sMatlist)
    Material.MaterialNotAddToUserBank(MaterialAppPath)
    Material.CloseMaterialWizard(MaterialAppPath)
    Log.write_log(ProjectName, "Info: Material Wizard Setting is Finished")
    
    #Process Wizard Setting
    Process.Home_Process("New", ProcessAppPath)
    #Process Tab Compression Setting
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_ProjectSetting.png", ProcessAppPath + "\\Pro_Tab_Compression.png", ProcessAppPath)  
    Process.ValueSetting(ProcessAppPath + "\\Pro_Compression_CompressionTime.png", 75, 0, "5", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_Comression_MaxCompressionSpeed.png", 120, 0, "10", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_Compression_MaxCompressionForce.png", 120, 0, "10", ProcessAppPath)
    #Process Tab Cooling Setting
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_Compression.png", ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath)
    #Process Tab Summary
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath + "\\Pro_Tab_Summary.png", ProcessAppPath)
    Process.ProcessWizard_Summary_Finish(ProcessAppPath)
    Log.write_log(ProjectName, "Info: Process Wizard Setting is Finished")
    
    #Analyze Setting
    Analyzelist = [StudioAppPath + "\\Analysis_FAndPCt.png", StudioAppPath + "\\Analysis_FillingAndPacking_2.png", StudioAppPath + "\\Analysis_CoolingTransient_2.png"]
    Studio.AnalysisSetting(Analyzelist, StudioAppPath)
    Log.write_log(ProjectName, "Info: Analyze Setting is Finished")
    
    #Computation Parameter Wizard Setting
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\ComputationLogo.png")    
    #CMX Tab Cool Setting
    CMX.CMX_Tab_Change(CMXAppPath + "\\CMX_Tab_Cool.png")
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\CMX_Cooling_AccurancyLevel_Standard.png")
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\CMX_Btn_OK.png")
    Log.write_log(ProjectName, "Info: Computation Parameter Wizard Setting is Finished")
    
    #Run 08
    #New Run
    Studio.Click_Icon(StudioAppPath, "\\Studio_NewRun2.png", 0)
    Log.write_log(ProjectName, "Info: New Run Setting is Finished")

    #Studio Pre Process Setting
    Studio.MeshType("Solid", StudioAppPath)
    Studio.Home_MoldingType_New("Module_IM2", StudioAppPath)
    Studio.Home_Model("ImportGeometry", StudioAppPath)
    Studio.ImportGeometry(CM_IM_FC_2nd_SourcePath, StudioAppPath)
    Studio.Wait_Dialog(StudioAppPath, "\\Studio_UpdateJoint.png")
    Studio.SwitchTab(StudioAppPath + "\\Studio_Tab_Mesh.png", StudioAppPath + "\\Studio_Tab_Meshing.png")
    Studio.Meshing_Generate(StudioAppPath)
    Studio.Meshing_GenerateBLM("Runner", StudioAppPath)
    Studio.Wait_Dialog(StudioAppPath, "\\Studio_Runner_Check.png")
    Studio.Click_Icon(StudioAppPath, "\\Btn_Angle_Perspective_Seletected.png", 40)
    Studio.Click_Icon(StudioAppPath, "\\Btn_Fit_To_Window.png", -24)
    Studio.Click_Icon(StudioAppPath, "\\Btn_ShowModeSelected_FeatureShaded2.png", 40)
    Studio.Final_Check(StudioAppPath)
    Log.write_log(ProjectName, "Info: Studio Pre Process Setting is Finished")

    #Material Wizard Setting
    #Part Material Setting
    Material.OpenMaterialWizard(MaterialAppPath + "\\Studio_EM1.png", 200, 0, MaterialAppPath)
    sMatlist = [MaterialAppPath + "\\MaterialABS.png", MaterialAppPath + "\\MaterialCAE.png", MaterialAppPath + "\\MaterialSTYLACVA29.png"]
    Material.ClickMDXBank(MaterialAppPath)
    Material.SelectPartMaterial(sMatlist)
    Material.MaterialNotAddToUserBank(MaterialAppPath)
    Material.CloseMaterialWizard(MaterialAppPath)
    #Partinsert Material Setting
    Material.Wait_Dialog(StudioAppPath, "\\Logo_NonFiber_UnSelected.png", "\\Logo_NonFiber_UnSelected_Blue.png")
    Material.Click_Icon(MaterialAppPath + "\\StudioPartInsert1.png", 200)
    Material.MCM2ndRunInsertSelection(MaterialAppPath + "\\StudioPartInsertSelection.png", MaterialAppPath + "\\Studio_CAESMC1.png", MaterialAppPath)
    Log.write_log(ProjectName, "Info: Material Wizard Setting is Finished")
    
    #Process Wizard Setting
    Process.Home_Process("New", ProcessAppPath)
    #Process Tab Filling/Packing Setting  
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_ProjectSetting.png", ProcessAppPath + "\\Pro_Tab_FillingPacking.png", ProcessAppPath)  
    Process.ValueSetting(ProcessAppPath + "\\Pro_Filling_FillingTime.png", 60, 0, "1.3", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_Filling_PackingTime.png", 60, 0, "4", ProcessAppPath)
    #Process Filling/Packing - Flow Rate Profile Setting
    Process.Click_Icon(ProcessAppPath + "\\Btn_Pro_Flow_rate_profile.png", ProcessAppPath + "\\Pro_Filling_FlowRateProFile.png")
    Process.ProcessWizard_FillingPacking_Profile_Type_Switch("\\Pro_Type_FlowRate%Time%.png", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_SectionNo.png", 60, 0, "1", ProcessAppPath)
    Profilelist = [ProcessAppPath + "\\Pro_Filling_FlowRateProFile.png", "50"]
    Process.ProcessWizard_FillingPacking_Profile_Section_Value(Profilelist, ProcessAppPath)
    Process.Click_Icon(ProcessAppPath + "\\Btn_OK.png", ProcessAppPath + "\\Pro_Tab_FillingPacking.png")
    #Process Tab Cooling Setting
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_FillingPacking.png", ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath)
    #Process Tab Summary
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath + "\\Pro_Tab_Summary.png", ProcessAppPath)
    Process.ProcessWizard_Summary_Finish(ProcessAppPath)
    Log.write_log(ProjectName, "Info: Process Wizard Setting is Finished")

    #Analyze Setting
    Analyzelist = [StudioAppPath + "\\Analysis_CFPCtW.png", StudioAppPath + "\\Analysis_CoolingCycle2.png", StudioAppPath + "\\Analysis_Filling_2.png", StudioAppPath + "\\Analysis_Packing2.png", StudioAppPath + "\\Analysis_CoolingTransient_2.png", StudioAppPath + "\\Analysis_Warpage.png"]
    Studio.AnalysisSetting(Analyzelist, StudioAppPath)
    Log.write_log(ProjectName, "Info: Analyze Setting is Finished")
    
    #Computation Parameter Wizard Setting
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\ComputationLogo.png")    
    #CMX Tab Cool Setting
    CMX.CMX_Tab_Change(CMXAppPath + "\\CMX_Tab_Cool.png")
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\CMX_Cooling_AccurancyLevel_Standard.png")
    #CMX Tab MCM Setting
    CMX.CMX_Tab_Change(CMXAppPath + "\\CMX_Tab_MCM.png")
    CMX.Checkbox(CMXAppPath + "\\CMX_MCM_LinkWithThePreviousShot.png", -75, 0, CMXAppPath)
    CMX.SelectDropDownMenu(CMXAppPath + "\\CMX_MCM_Run.png", 100, 0, CMXAppPath + "\\CMX_MCM_Run07.png", 0, 0)
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\CMX_Btn_OK.png")
    if exists(CMXAppPath + "\\CMX_DLG_Moldex3DStudio.png"):    
        CMX.ClickButton(CMXAppPath, CMXAppPath + "\\CMX_Btn_OK_2.png")
    Log.write_log(ProjectName, "Info: Computation Parameter Wizard Setting is Finished")
    
    #Change Remark Name
    Studio.Click_Icon(StudioAppPath, "\\Studio_Tree_Run.png", 0)
    wait(1)
    Remark_name = ["IM-1st shot-FC", "IM-2nd shot-FC", "IM-1st shot-eDesign", "IM-2nd shot-eDesign", "IM-1st shot-SC", "ICM-2nd shot-SC", "CM-1st shot-FC", "IM-2nd shot-FC"]
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
    #Studio.Submit_Batch_Run(2,StudioAppPath) #124333
    CMX.Checkbox(StudioAppPath + r"\Studio_Run02.png", -38, 0, CMXAppPath)
    CMX.Checkbox(StudioAppPath + r"\Studio_Run04.png", -38, 0, CMXAppPath)
    CMX.Checkbox(StudioAppPath + r"\Studio_Run06.png", -38, 0, CMXAppPath)
    Studio.Click_Icon(StudioAppPath, r"\Btn_AddBat.png", 0)
    Studio.Click_Icon(StudioAppPath, r"\Btn_OK.png", 0)
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