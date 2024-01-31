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
import Copy_Run_for_MCM as CRfM

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
Copypath = ArgS.Copypath

ProjectName = "IM-S8-P1"
username = "moldex3dqa"
password = "123456"
SVNPath = r"svn://192.168.3.4/QARepository/AutoTest/Moldex3D/2023Series/Moldex3D/CaseReference/ENT/" + ProjectName + r"/Geometry"
localpath = os.path.normpath((cwd + r"\\" +ProjectName))
RhinoIP = '192.168.130.51'
RhinoPath = Common.getregkeyvalue(r"HKEY_LOCAL_MACHINE\SOFTWARE\McNeel\Rhinoceros\7.0\Install", "ExePath")
MainInstallPath ,ver = Common.getregkeyvalue(r"HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\CoreTechSystem\MDX_ParallelComputing", "INSTALLDIR")
WorkingFolder = Common.getregkeyvalue(r"HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\CoreTechSystem\MDX_ParallelComputing", "WorkingFolder")
StudioPath = MainInstallPath + r"\Bin\MDXStudio.exe"
CaseReferncePath = Common.gototargetpath('MDX_ENT') + "\\" + ProjectName
SourcePath1 = CaseReferncePath + r"\1D\1D(m).3dm"
SourcePath2 = CaseReferncePath + r"\1D_Nozzle_Zone\1D_Zone(m).3dm"
SourcePath3 = CaseReferncePath + r"\3D\Solid_IM_InjectionUnit.mdg"
CMPath = MainInstallPath + r'\Bin\MDXComputingManager' + ver + r'.exe'
hostname, local_ip = Common.getcuriphostname()
SourceExportPath = os.path.join(CaseReferncePath, r"Source")
mesh1path = SourceExportPath + r"\IM-S8-P1(1D_Nozzel).mfe"
mesh2path = SourceExportPath + r"\IM-S8-P1(1D).mfe"

try:
   
   
     #svn execution
    Common.SVNLogin(username, password)  
    Common.SVNDownload(SVNPath, localpath)    
    print ("Info: SVN download is Finished")
    Log.write_log("Pre_Setting", "Info: SVN download is Finished")
    
    #Mesh Export *.msh for Studio 
    Rhino.OpenRhino(RhinoPath, RhinoIP, RhinoAppPath)
    Rhino.ImportMesh(SourcePath1, RhinoAppPath)
    Rhino.ExportMesh("Solid", SourceExportPath, ProjectName+'(1D)', ProjectName+'(1D)', "Z Axis", RhinoAppPath)
    Rhino.OpenMesh(SourcePath2, RhinoAppPath)
    Rhino.ExportMesh("Solid", SourceExportPath, ProjectName+'(1D_Nozzel)', ProjectName+'(1D_Nozzel)', "Z Axis", RhinoAppPath)
    Rhino.CloseRhino(RhinoPath, RhinoAppPath)
    
    Log.write_log(ProjectName, "Info: Mesh Setting is Finished") 
    
    #New Project
    Studio.OpenApp(StudioPath, StudioAppPath + "\\Studio_UI.png")
    Log.write_log(ProjectName, "Info: Open Studio is Finished")
    Studio.NewProject(ProjectName, StudioAppPath)
    Log.write_log(ProjectName, "Info: New Project Setting is Finished")
    #Studio Pre Process Setting
    Studio.MeshType("Solid", StudioAppPath)
    Studio.Home_MoldingType(0, -105, StudioAppPath)
    Studio.Home_Model("ImportMesh", StudioAppPath)
    Studio.ImportGeometry(mesh1path, StudioAppPath)
    #Material Wizard Setting
    sMatlist = [MaterialAppPath + r"\MaterialABS_2023.png", MaterialAppPath + r"\MaterialASchulman_2023.png", MaterialAppPath + r"\MaterialRABS9000UV5.png"]
   
    Material.OpenMaterialWizard(MaterialAppPath + "\\Studio_EM1.png", 200, 0, MaterialAppPath)
    Material.ClickMDXBank(MaterialAppPath)
    Material.SelectPartMaterial(sMatlist)
    Material.MaterialNotAddToUserBank(MaterialAppPath)
    Material.CloseMaterialWizard(MaterialAppPath)
    Log.write_log(ProjectName, "Info: Material Wizard Setting is Finished")
    #Process Wizard Setting
    
    Process.Home_Process("New", ProcessAppPath)
    Process.ProcessWizard_Project_SettingMethod("M1", ProcessAppPath)
    machinepath=CaseReferncePath+ r"\QA_Machine.mchs"
    Process.Select_Machine_Setting(ProcessAppPath)
    Process.Select_Machine_Setting_Advanced(ProcessAppPath,"Import",machinepath)  
    wait(2)
    click(Pattern(ProcessAppPath+ r"\Process_machine_qa.png").similar(0.9))
    click(ProcessAppPath+ r"\Studio_OK.png")
    if exists(ProcessAppPath+ r"\Process_mdxpro.png"):
        click(Pattern(ProcessAppPath+ r"\Process_Yes.png").similar(0.9))
    #Process Tab Filling/Packing Setting
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_ProjectSetting.png", ProcessAppPath + "\\Pro_Tab_FillingPacking.png", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + r"\Pro_Filling_PackingTime.png", 60, 0, "0.3", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\process_VP_switch.png", 200, 25, "5", ProcessAppPath)
    #Process Filling/Packing - Flow Rate Profile Setting
    Process.Click_Icon(ProcessAppPath + "\\Btn_Pro_Flow_rate_profile.png", ProcessAppPath + "\\Pro_Filling_FlowRateProFile.png")
    Process.ProcessWizard_FillingPacking_Profile_Type_Switch("\\Pro_Type_InjectionVelocity%RamPositionmm.png", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_SectionNo.png", 60, 0, "1", ProcessAppPath)
    Profilelist = [ProcessAppPath + "\\Pro_Filling_FlowRateProFile.png", "17", "50"]
    Process.ProcessWizard_FillingPacking_Profile_Section_Value(Profilelist, ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\process_suck_back.png", 0, 20, "1", ProcessAppPath)
    #Process Filling/Packing - Injection Pressure Profile Setting
    Process.Click_Icon(ProcessAppPath + "\\Btn_Pro_Inject_pressure_profile.png", ProcessAppPath + "\\Pro_Filling_Injectionpressureprofile.png")
    Process.ProcessWizard_FillingPacking_Profile_Type_Switch("\\Pro_Type_InjectionPressure%RamPositionmm.png", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_SectionNo.png", 60, 0, "1", ProcessAppPath)
    Profilelist = [ProcessAppPath + "\\Pro_Filling_Injectionpressureprofile.png", "100"]
    Process.ProcessWizard_FillingPacking_Profile_Section_Value(Profilelist, ProcessAppPath)
    Process.Click_Icon(ProcessAppPath + "\\Btn_OK.png", ProcessAppPath + "\\Pro_Tab_FillingPacking.png")
    #Process Filling/Packing - Packing Pressure Profile Setting
    Process.Click_Icon(ProcessAppPath + "\\Btn_Pro_Pack_pressure_profile.png", ProcessAppPath + "\\Pro_Filling_Packingpressureprofile.png")
    Process.ProcessWizard_FillingPacking_Profile_Type_Switch("\\Pro_Type_PackPressure%TimeSec.png", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_SectionNo.png", 60, 0, "1", ProcessAppPath)
    Profilelist = [ProcessAppPath + r"\Pro_Filling_Packingpressureprofile.png","50"]
    Process.ProcessWizard_FillingPacking_Profile_Section_Value(Profilelist, ProcessAppPath)
    Process.Click_Icon(ProcessAppPath + "\\Btn_OK.png", ProcessAppPath + "\\Pro_Tab_FillingPacking.png")
    #Process Tab Cooling Setting
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_FillingPacking.png", ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath)  
    #Process Tab Summary
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath + "\\Pro_Tab_Summary.png", ProcessAppPath)
    Process.ProcessWizard_Summary_Finish(ProcessAppPath)
    Log.write_log(ProjectName, "Info: Process Wizard Setting is Finished")
    #Analyze Setting
    Analyzelist = [StudioAppPath + "\\Analysis_FPW.png", StudioAppPath + "\\Analysis_Filling_2.png",StudioAppPath + "\\Analysis_Packing2.png",StudioAppPath + "\\Analysis_Warpage.png"]
    Studio.AnalysisSetting(Analyzelist, StudioAppPath)
    Log.write_log(ProjectName, "Info: Analyze Setting is Finished")
    
    #CMX Tab Flow/Pack Setting
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\ComputationLogo_2023.png")
    #CMX Tab Cool Setting
    CMX.CMX_Tab_Change(CMXAppPath + "\\CMX_Tab_Cool.png")
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\CMX_Btn_OK.png")
    Log.write_log(ProjectName, "Info: Computation Parameter Wizard Setting is Finished")
    
    wait(1)
    click(StudioAppPath+r"\Studio_NewRun2.png")
    wait(1)
    #Studio Pre Process Setting
    Studio.MeshType("Solid", StudioAppPath)
    Studio.Home_MoldingType(0, -105, StudioAppPath)
    Studio.Home_Model("ImportMesh", StudioAppPath)
    Studio.ImportGeometry(mesh2path, StudioAppPath)
    #Material Wizard Setting
    sMatlist = [MaterialAppPath + r"\MaterialABS_2023.png", MaterialAppPath + r"\MaterialASchulman_2023.png", MaterialAppPath + r"\MaterialRABS9000UV5.png"]
    Material.OpenMaterialWizard(MaterialAppPath + "\\Studio_EM1.png", 200, 0, MaterialAppPath)
    Material.ClickMDXBank(MaterialAppPath)
    Material.SelectPartMaterial(sMatlist)
    Material.MaterialNotAddToUserBank(MaterialAppPath)
    Material.CloseMaterialWizard(MaterialAppPath)
    Log.write_log(ProjectName, "Info: Material Wizard Setting is Finished")
    #Process Wizard Setting
    Process.Home_Process("New", ProcessAppPath)
    Process.ProcessWizard_Project_SettingMethod("M1", ProcessAppPath)
    click(Pattern(ProcessAppPath+ r"\Pro_MachineSetting.png").targetOffset(15, 20))
    click(Pattern(ProcessAppPath+ r"\Process_Machine_QA1_2.png").similar(0.9))
    if exists(ProcessAppPath+ r"\Process_mdxpro.png"):
        click(Pattern(ProcessAppPath+ r"\Process_Yes.png").similar(0.9))
    #Process Tab Filling/Packing Setting
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_ProjectSetting.png", ProcessAppPath + "\\Pro_Tab_FillingPacking.png", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + r"\Pro_Filling_PackingTime.png", 60, 0, "0.3", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\process_VP_switch.png", 200, 25, "5", ProcessAppPath)
    #Process Filling/Packing - Flow Rate Profile Setting
    Process.Click_Icon(ProcessAppPath + "\\Btn_Pro_Flow_rate_profile.png", ProcessAppPath + "\\Pro_Filling_FlowRateProFile.png")
    Process.ProcessWizard_FillingPacking_Profile_Type_Switch("\\Pro_Type_InjectionVelocity%RamPositionmm.png", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_SectionNo.png", 60, 0, "1", ProcessAppPath)
    Profilelist = [ProcessAppPath + "\\Pro_Filling_FlowRateProFile.png", "17", "50"]
    Process.ProcessWizard_FillingPacking_Profile_Section_Value(Profilelist, ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\process_suck_back.png", 0, 20, "1", ProcessAppPath)
    #Process Filling/Packing - Injection Pressure Profile Setting
    Process.Click_Icon(ProcessAppPath + "\\Btn_Pro_Inject_pressure_profile.png", ProcessAppPath + "\\Pro_Filling_Injectionpressureprofile.png")
    Process.ProcessWizard_FillingPacking_Profile_Type_Switch("\\Pro_Type_InjectionPressure%RamPositionmm.png", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_SectionNo.png", 60, 0, "1", ProcessAppPath)
    Profilelist = [ProcessAppPath + "\\Pro_Filling_Injectionpressureprofile.png", "100"]
    Process.ProcessWizard_FillingPacking_Profile_Section_Value(Profilelist, ProcessAppPath)
    Process.Click_Icon(ProcessAppPath + "\\Btn_OK.png", ProcessAppPath + "\\Pro_Tab_FillingPacking.png")
    #Process Filling/Packing - Packing Pressure Profile Setting
    Process.Click_Icon(ProcessAppPath + "\\Btn_Pro_Pack_pressure_profile.png", ProcessAppPath + "\\Pro_Filling_Packingpressureprofile.png")
    Process.ProcessWizard_FillingPacking_Profile_Type_Switch("\\Pro_Type_PackPressure%TimeSec.png", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_SectionNo.png", 60, 0, "1", ProcessAppPath)
    Profilelist = [ProcessAppPath + r"\Pro_Filling_Packingpressureprofile.png","50"]
    Process.ProcessWizard_FillingPacking_Profile_Section_Value(Profilelist, ProcessAppPath)
    Process.Click_Icon(ProcessAppPath + "\\Btn_OK.png", ProcessAppPath + "\\Pro_Tab_FillingPacking.png")
    #Process Tab Cooling Setting
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_FillingPacking.png", ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath)  
    #Process Tab Summary
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath + "\\Pro_Tab_Summary.png", ProcessAppPath)
    Process.ProcessWizard_Summary_Finish(ProcessAppPath)
    Log.write_log(ProjectName, "Info: Process Wizard Setting is Finished")
    #Analyze Setting
    Analyzelist = [StudioAppPath + "\\Analysis_FPW.png", StudioAppPath + "\\Analysis_Filling_2.png",StudioAppPath + "\\Analysis_Packing2.png",StudioAppPath + "\\Analysis_Warpage.png"]
    Studio.AnalysisSetting(Analyzelist, StudioAppPath)
    Log.write_log(ProjectName, "Info: Analyze Setting is Finished")
    
    #CMX Tab Flow/Pack Setting
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\ComputationLogo_2023.png")
    #CMX Tab Cool Setting
    CMX.CMX_Tab_Change(CMXAppPath + "\\CMX_Tab_Cool.png")
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\CMX_Btn_OK.png")
    Log.write_log(ProjectName, "Info: Computation Parameter Wizard Setting is Finished")
    
    wait(1)
    click(StudioAppPath+r"\Studio_NewRun2.png")
    wait(1)
    #Studio Pre Process Setting
    Studio.MeshType("Solid", StudioAppPath)
    Studio.Home_MoldingType(0, -105, StudioAppPath)
    Studio.Home_Model("ImportGeometry", StudioAppPath)
    Studio.Click_Icon(StudioAppPath, "\\Studio_Import_icon.png", 0)
    wait(2)
    Studio.ImportGeometry(SourcePath3, StudioAppPath)
    Studio.Click_Icon(StudioAppPath, "\\Studio_Tree_Model.png",0)
    Studio.Click_Icon(StudioAppPath, "\\Studio_Tree_Model_Object.png", -38)
    
    dragDrop(StudioAppPath + r"\Studio_S8_Bar.png",StudioAppPath + r"\Studio_S4_Bottom.png")
    click(Pattern(StudioAppPath + r"\Studio_Tree_NonAttribute.png").similar(0.92).targetOffset(-60,0))
    Studio.SetView("Top",StudioAppPath)
    Studio.Click_Icon(StudioAppPath, "\\Btn_Fit_Window.png",0)
    Studio.Nozzlezone_wizard(StudioAppPath + r"\Studio_Nozzel_point.png","General","TypeB",StudioAppPath)
    Studio.SwitchTab(StudioAppPath + "\\Studio_Tab_Mesh.png", StudioAppPath + "\\Studio_Tab_Meshing.png")
    Studio.Meshing_Generate(StudioAppPath)
    Studio.Meshing_GenerateBLM("None", StudioAppPath)
    Studio.Wait_Dialog(StudioAppPath, "\\Studio_FinalCheck.png")
    Studio.Click_Icon(StudioAppPath, "\\Btn_Angle_Perspective_Seletected.png", 40)
    Studio.Click_Icon(StudioAppPath, "\\Btn_Fit_To_Window.png", -24)
    Studio.Click_Icon(StudioAppPath, "\\Btn_ShowModeSelected_FeatureShaded2.png", 40)
    Studio.Final_Check(StudioAppPath)
  #Material Wizard Setting
    sMatlist = [MaterialAppPath + r"\MaterialABS_2023.png", MaterialAppPath + r"\MaterialASchulman_2023.png", MaterialAppPath + r"\MaterialRABS9000UV5.png"]
    Material.OpenMaterialWizard(MaterialAppPath + "\\Studio_EM1.png", 200, 0, MaterialAppPath)
    Material.ClickMDXBank(MaterialAppPath)
    Material.SelectPartMaterial(sMatlist)
    Material.MaterialNotAddToUserBank(MaterialAppPath)
    Material.CloseMaterialWizard(MaterialAppPath)
    Log.write_log(ProjectName, "Info: Material Wizard Setting is Finished")
    #Process Wizard Setting
    Process.Home_Process("New", ProcessAppPath)
    Process.ProcessWizard_Project_SettingMethod("M1", ProcessAppPath)
    machinepath2=CaseReferncePath+ r"\QA_Machine2.mchs"
    Process.Select_Machine_Setting(ProcessAppPath)
    Process.Select_Machine_Setting_Advanced(ProcessAppPath,"Import",machinepath2)  
    wait(2)
    click(Pattern(ProcessAppPath+ r"\Process_Machine_QA2.png").similar(0.9))
    click(ProcessAppPath+ r"\Studio_OK.png")
    if exists(ProcessAppPath+ r"\Process_mdxpro.png"):
        click(Pattern(ProcessAppPath+ r"\Process_Yes.png").similar(0.9))
    #Process Tab Filling/Packing Setting
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_ProjectSetting.png", ProcessAppPath + "\\Pro_Tab_FillingPacking.png", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + r"\Pro_Filling_PackingTime.png", 60, 0, "0.3", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\process_VP_switch.png", 200, 25, "5", ProcessAppPath)
    #Process Filling/Packing - Flow Rate Profile Setting
    Process.Click_Icon(ProcessAppPath + "\\Btn_Pro_Flow_rate_profile.png", ProcessAppPath + "\\Pro_Filling_FlowRateProFile.png")
    Process.ProcessWizard_FillingPacking_Profile_Type_Switch("\\Pro_Type_InjectionVelocity%RamPositionmm.png", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_SectionNo.png", 60, 0, "1", ProcessAppPath)
    Profilelist = [ProcessAppPath + "\\Pro_Filling_FlowRateProFile.png", "17", "50"]
    Process.ProcessWizard_FillingPacking_Profile_Section_Value(Profilelist, ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\process_suck_back.png", 0, 20, "1", ProcessAppPath)
    #Process Filling/Packing - Injection Pressure Profile Setting
    Process.Click_Icon(ProcessAppPath + "\\Btn_Pro_Inject_pressure_profile.png", ProcessAppPath + "\\Pro_Filling_Injectionpressureprofile.png")
    Process.ProcessWizard_FillingPacking_Profile_Type_Switch("\\Pro_Type_InjectionPressure%RamPositionmm.png", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_SectionNo.png", 60, 0, "1", ProcessAppPath)
    Profilelist = [ProcessAppPath + "\\Pro_Filling_Injectionpressureprofile.png", "100"]
    Process.ProcessWizard_FillingPacking_Profile_Section_Value(Profilelist, ProcessAppPath)
    Process.Click_Icon(ProcessAppPath + "\\Btn_OK.png", ProcessAppPath + "\\Pro_Tab_FillingPacking.png")
    #Process Filling/Packing - Packing Pressure Profile Setting
    Process.Click_Icon(ProcessAppPath + "\\Btn_Pro_Pack_pressure_profile.png", ProcessAppPath + "\\Pro_Filling_Packingpressureprofile.png")
    Process.ProcessWizard_FillingPacking_Profile_Type_Switch("\\Pro_Type_PackPressure%TimeSec.png", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_SectionNo.png", 60, 0, "1", ProcessAppPath)
    Profilelist = [ProcessAppPath + r"\Pro_Filling_Packingpressureprofile.png","50"]
    Process.ProcessWizard_FillingPacking_Profile_Section_Value(Profilelist, ProcessAppPath)
    Process.Click_Icon(ProcessAppPath + "\\Btn_OK.png", ProcessAppPath + "\\Pro_Tab_FillingPacking.png")
    #Process Tab Cooling Setting
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_FillingPacking.png", ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath)  
    #Process Tab Summary
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath + "\\Pro_Tab_Summary.png", ProcessAppPath)
    Process.ProcessWizard_Summary_Finish(ProcessAppPath)
    Log.write_log(ProjectName, "Info: Process Wizard Setting is Finished")
    
    #Analyze Setting
    Analyzelist = [StudioAppPath + "\\Analysis_CFAndPCtW.png", StudioAppPath + "\\Analysis_CoolingCycle4.png",StudioAppPath + "\\Analysis_FillingAndPacking_2.png",StudioAppPath + "\\Analysis_CoolingTransient_2.png",StudioAppPath + "\\Analysis_Warpage.png"]
    Studio.AnalysisSetting(Analyzelist, StudioAppPath)
    Log.write_log(ProjectName, "Info: Analyze Setting is Finished")
    
    #CMX Tab Flow/Pack Setting
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\ComputationLogo_2023.png")
    #CMX Tab Cool Setting
    CMX.CMX_Tab_Change(CMXAppPath + "\\CMX_Tab_Cool.png")
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\CMX_Btn_OK.png")
    Log.write_log(ProjectName, "Info: Computation Parameter Wizard Setting is Finished")
    
    Studio.SwitchTab(StudioAppPath + "\\Studio_Tab_Mesh.png", StudioAppPath + "\\Studio_Tab_Meshing.png")
    return_preprocess=['1']
    Studio.Meshing_Generate(StudioAppPath,*return_preprocess)
   
    Studio.Wait_Dialog(StudioAppPath, r"\Studio_Mesh_Process.png")
    Studio.Meshing_GenerateBLM("Runner", StudioAppPath)
   
    Studio.Click_Icon(StudioAppPath, "\\Btn_Fit_To_Window.png", -24)
    Studio.Click_Icon(StudioAppPath, "\\Btn_ShowModeSelected_FeatureShaded2.png", 40)
    if exists(StudioAppPath + r"\Studio_FinalCheck2.png"):
        click(StudioAppPath + r"\Studio_FinalCheck2.png")  
    if exists(Pattern(StudioAppPath + r"\Studio_setpartingdirection.png").similar(0.85), 10):
        click(StudioAppPath + r"\Btn_Check.png")
    if exists(StudioAppPath + r"\Btn_Yes.png", 5):
        click(StudioAppPath + r"\Btn_Yes.png")
    i = 0
    while not exists(StudioAppPath + r"\Dialog_FInal_Check.png",30) and i <20:
        if exists(StudioAppPath + r"\Btn_Yes.png", 1):
            click(StudioAppPath + r"\Btn_Yes.png")
        i += 1
    if exists(StudioAppPath + r"\Btn_Yes.png", 5):
        click(StudioAppPath + r"\Btn_Yes.png")
    if exists(StudioAppPath + r"\Btn_OK.png", 10):
        click(StudioAppPath + r"\Btn_OK.png") 
    Log.write_log(ProjectName, "Info: Studio Pre Process Setting is Finished")
    Log.write_log(ProjectName, "Info: Studio Pre Process Setting is Finished")
      #Material Wizard Setting
    sMatlist = [MaterialAppPath + r"\MaterialABS_2023.png", MaterialAppPath + r"\MaterialASchulman_2023.png", MaterialAppPath + r"\MaterialRABS9000UV5.png"]
    Material.OpenMaterialWizard(MaterialAppPath + "\\Studio_EM1.png", 200, 0, MaterialAppPath)
    Material.ClickMDXBank(MaterialAppPath)
    Material.SelectPartMaterial(sMatlist)
    Material.MaterialNotAddToUserBank(MaterialAppPath)
    Material.CloseMaterialWizard(MaterialAppPath)
    Log.write_log(ProjectName, "Info: Material Wizard Setting is Finished")
    #Process Wizard Setting
    wait(2)
    Process.Home_Process("New", ProcessAppPath)
    Process.ProcessWizard_Project_SettingMethod("M1", ProcessAppPath)
    Process.Select_Machine_Setting(ProcessAppPath)
    click(Pattern(ProcessAppPath+ r"\Process_Machine_QA2").similar(0.9))
    click(ProcessAppPath+ r"\Studio_OK.png")
    if exists(ProcessAppPath+ r"\Process_mdxpro.png"):
        click(Pattern(ProcessAppPath+ r"\Process_Yes.png").similar(0.9))
    #Process Tab Filling/Packing Setting
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_ProjectSetting.png", ProcessAppPath + "\\Pro_Tab_FillingPacking.png", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + r"\Pro_Filling_PackingTime.png", 60, 0, "0.3", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\process_VP_switch.png", 200, 25, "5", ProcessAppPath)
    #Process Filling/Packing - Flow Rate Profile Setting
    Process.Click_Icon(ProcessAppPath + "\\Btn_Pro_Flow_rate_profile.png", ProcessAppPath + "\\Pro_Filling_FlowRateProFile.png")
    Process.ProcessWizard_FillingPacking_Profile_Type_Switch("\\Pro_Type_InjectionVelocity%RamPositionmm.png", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_SectionNo.png", 60, 0, "1", ProcessAppPath)
    Profilelist = [ProcessAppPath + "\\Pro_Filling_FlowRateProFile.png", "17", "50"]
    Process.ProcessWizard_FillingPacking_Profile_Section_Value(Profilelist, ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\process_suck_back.png", 0, 20, "1", ProcessAppPath)
    #Process Filling/Packing - Injection Pressure Profile Setting
    Process.Click_Icon(ProcessAppPath + "\\Btn_Pro_Inject_pressure_profile.png", ProcessAppPath + "\\Pro_Filling_Injectionpressureprofile.png")
    Process.ProcessWizard_FillingPacking_Profile_Type_Switch("\\Pro_Type_InjectionPressure%RamPositionmm.png", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_SectionNo.png", 60, 0, "1", ProcessAppPath)
    Profilelist = [ProcessAppPath + "\\Pro_Filling_Injectionpressureprofile.png", "100"]
    Process.ProcessWizard_FillingPacking_Profile_Section_Value(Profilelist, ProcessAppPath)
    Process.Click_Icon(ProcessAppPath + "\\Btn_OK.png", ProcessAppPath + "\\Pro_Tab_FillingPacking.png")
    #Process Filling/Packing - Packing Pressure Profile Setting
    Process.Click_Icon(ProcessAppPath + "\\Btn_Pro_Pack_pressure_profile.png", ProcessAppPath + "\\Pro_Filling_Packingpressureprofile.png")
    Process.ProcessWizard_FillingPacking_Profile_Type_Switch("\\Pro_Type_PackPressure%TimeSec.png", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_SectionNo.png", 60, 0, "1", ProcessAppPath)
    Profilelist = [ProcessAppPath + r"\Pro_Filling_Packingpressureprofile.png","50"]
    Process.ProcessWizard_FillingPacking_Profile_Section_Value(Profilelist, ProcessAppPath)
    Process.Click_Icon(ProcessAppPath + "\\Btn_OK.png", ProcessAppPath + "\\Pro_Tab_FillingPacking.png")
    #Process Tab Cooling Setting
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_FillingPacking.png", ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath)  
    #Process Tab Summary
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath + "\\Pro_Tab_Summary.png", ProcessAppPath)
    Process.ProcessWizard_Summary_Finish(ProcessAppPath)
    Log.write_log(ProjectName, "Info: Process Wizard Setting is Finished")
    #Analyze Setting
    Analyzelist = [StudioAppPath + "\\Analysis_CFAndPCtW.png", StudioAppPath + "\\Analysis_CoolingCycle.png",StudioAppPath + "\\Analysis_FillingAndPacking_2.png",StudioAppPath + "\\Analysis_CoolingTransient.png",StudioAppPath + "\\Analysis_Warpage.png"]
    Studio.AnalysisSetting(Analyzelist, StudioAppPath)
    Log.write_log(ProjectName, "Info: Analyze Setting is Finished")
    
    #CMX Tab Flow/Pack Setting
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\ComputationLogo_2023.png")
    #CMX Tab Cool Setting
    CMX.CMX_Tab_Change(CMXAppPath + "\\CMX_Tab_Cool.png")
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\CMX_Btn_OK.png")
    Log.write_log(ProjectName, "Info: Computation Parameter Wizard Setting is Finished")

    #Change Remark Name
    Studio.Click_Icon(StudioAppPath, r"\Studio_Tree_Run.png", 0)
    wait(1)
    Remark_name = ["1D_Nozzel","1D","SC","FC"]
    CRN.Run(Remark_name, CRNAppPath)
    Log.write_log(ProjectName, "Info: Change Remark Name is Finished")

    #Set RC task Number  
    Studio.TaskNumberSetting("4", StudioAppPath)
    click(StudioAppPath + r"\Btn_OK.png")
    Studio.Create_BJS(13,StudioAppPath,ProjectName,WorkingFolder)
    CM.SendRCtoCM(StudioAppPath,CMAppPath)

    #Set lh task Number
    Studio.TaskNumberSetting("1", StudioAppPath)
    click(StudioAppPath + r"\Btn_OK.png")
 
    #LH Server Connect
    Studio.OpenApp(CMPath, CMAppPath + r"\CM_UI.png")
    CM.connectserver("LH",CMAppPath)
    wait(1)
    click(StudioAppPath + r"\Studio_logo.png")
    Log.write_log("Initial", "Info: Computing Manager Add Server Setting is Finished")
    wait(1)
    Studio.ClickRun(30, StudioAppPath)
    Studio.Submit_Batch_Run(2,StudioAppPath)
    wait(2)
      
    #Close Studio UI
    Studio.CloseApp(StudioPath)  
    Log.write_log(ProjectName, "Info: %s Test is Finished!" % ProjectName)
       
except:
    os.popen(("python {}").format(exceptprocedureApp))
    print( ProjectName+ "Test is Failed!")
    Log.write_log(ProjectName,"Error: %s Test is Failed!" % ProjectName)
    Log.write_log2(ProjectName, "Summary")
