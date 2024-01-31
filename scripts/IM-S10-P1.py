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

ProjectName = "IM-S10-P1"
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
SourcePath1 = CaseReferncePath + r"\ValvePin_NoZone.3dm" 
SourcePath2 = CaseReferncePath + r"\ValvePin_Geometry.mdg"
SourcePath3 = CaseReferncePath + r"\ValvePin_Line.mdg"
CMPath = MainInstallPath + r'\Bin\MDXComputingManager' + ver + r'.exe'
hostname, local_ip = Common.getcuriphostname()
SourceExportPath = os.path.join(CaseReferncePath, r"Source")
mesh1path = SourceExportPath + r"\IM-S10-P1(ValvePin_NoZone).mfe"


try:
   
     #svn execution
    Common.SVNLogin(username, password)  
    Common.SVNDownload(SVNPath, localpath)    
    print ("Info: SVN download is Finished")
    Log.write_log("Pre_Setting", "Info: SVN download is Finished")
    
    #Mesh Export *.msh for Studio 
    Rhino.OpenRhino(RhinoPath, RhinoIP, RhinoAppPath)
    Rhino.ImportMesh(SourcePath1, RhinoAppPath)
    Rhino.ExportMesh("Solid", SourceExportPath, ProjectName+'(ValvePin_NoZone)', ProjectName+'(ValvePin_NoZone)', "Z Axis", RhinoAppPath)
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
    Process.ProcessWizard_Project_SettingMethod("CAE", ProcessAppPath)
    #Process Tab Filling/Packing Setting
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_ProjectSetting.png", ProcessAppPath + "\\Pro_Tab_FillingPacking.png", ProcessAppPath)
    Process.Click_Icon(ProcessAppPath + r"\Btn_AdvancedSetting.png", ProcessAppPath + r"\Pro_AdvancedSetting.png")
    Process.ValueSetting(ProcessAppPath + "\\Process_Control_Point.png", 0, 25, "2", ProcessAppPath)
    click(Pattern(ProcessAppPath+ r"\process_valve_time.png").similar(0.9))
    click(Pattern(ProcessAppPath+ r"\process_valve_fill_volume.png").similar(0.9))
    Process.ValueSetting(ProcessAppPath + "\\process_value.png", 0, 70, "50", ProcessAppPath)
    click(Pattern(ProcessAppPath+ r"\Process_valve_open.png").similar(0.9))
    click(Pattern(ProcessAppPath+ r"\Process_valve_close.png").similar(0.9))
   
    Process.ValueSetting(ProcessAppPath + "\\Process_Control_Point.png", 0, 85, "2", ProcessAppPath)
    click(Pattern(ProcessAppPath+ r"\process_valve_time.png").similar(0.9))
    click(Pattern(ProcessAppPath+ r"\process_valve_fill_volume.png").similar(0.9))
    Process.ValueSetting(ProcessAppPath + "\\process_value.png", 0, 130, "50", ProcessAppPath)
    click(Pattern(ProcessAppPath+ r"\Process_valve_open_2.png").similar(0.92).targetOffset(120, 0))
    click(Pattern(ProcessAppPath+ r"\Process_valve_close.png").similar(0.9))
    Process.Click_Icon(ProcessAppPath + "\\Btn_OK.png", ProcessAppPath + "\\Pro_Tab_FillingPacking.png")
    #Process Tab Cooling Setting
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_FillingPacking.png", ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath)  
    #Process Tab Summary
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath + "\\Pro_Tab_Summary.png", ProcessAppPath)
    Process.ProcessWizard_Summary_Finish(ProcessAppPath)
    Log.write_log(ProjectName, "Info: Process Wizard Setting is Finished")
    
    #Analyze Setting
    Analyzelist = [StudioAppPath + "\\Analysis_CtFandPCtW.png",StudioAppPath + "\\Analysis_CoolingTransient_2.png", StudioAppPath + "\\Analysis_FandP_2.png",StudioAppPath + "\\Analysis_CoolingTransient_2.png",StudioAppPath + "\\Analysis_Warpage.png"]
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
    Studio.ImportGeometry(SourcePath3, StudioAppPath)
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
    Process.ProcessWizard_Project_SettingMethod("CAE", ProcessAppPath)
    #Process Tab Filling/Packing Setting
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_ProjectSetting.png", ProcessAppPath + "\\Pro_Tab_FillingPacking.png", ProcessAppPath)
    Process.Click_Icon(ProcessAppPath + r"\Btn_AdvancedSetting.png", ProcessAppPath + r"\Pro_AdvancedSetting.png")

    Process.ValueSetting(ProcessAppPath + "\\Process_Control_Point.png", 0, 25, "2", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\process_value.png", 0, 70, "0.5", ProcessAppPath)
    click(Pattern(ProcessAppPath+ r"\process_action.png").similar(0.90).targetOffset(0, 50))
    click(Pattern(ProcessAppPath+ r"\Process_valve_close.png").similar(0.9))
   
    Process.ValueSetting(ProcessAppPath + "\\Process_Control_Point.png", 0, 85, "2", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\process_value.png", 0, 130, "0.5", ProcessAppPath)
    click(Pattern(ProcessAppPath+ r"\process_action.png").similar(0.90).targetOffset(0, 110))
    click(Pattern(ProcessAppPath+ r"\Process_valve_close.png").similar(0.9))

    Process.ValueSetting(ProcessAppPath + "\\Process_Control_Point.png", 0, 155, "2", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\process_value.png", 0, 200, "0.5", ProcessAppPath)
    click(Pattern(ProcessAppPath+ r"\process_action.png").similar(0.90).targetOffset(0, 200))
    click(Pattern(ProcessAppPath+ r"\Process_valve_close.png").similar(0.9))
   
    Process.ValueSetting(ProcessAppPath + "\\Process_Control_Point.png", 0, 220, "2", ProcessAppPath)
    dragDrop(StudioAppPath + r"\process_bar.png",StudioAppPath + r"\Process_bottom.png")
    click(Pattern(ProcessAppPath+ r"\process_action.png").similar(0.90).targetOffset(0, 180))
   
    click(Pattern(ProcessAppPath+ r"\Process_valve_close.png").similar(0.9))
    Process.ValueSetting(ProcessAppPath + "\\process_value.png", 0, 200, "0.5", ProcessAppPath)
   
    Process.Click_Icon(ProcessAppPath + "\\Btn_OK.png", ProcessAppPath + "\\Pro_Tab_FillingPacking.png")
    #Process Tab Cooling Setting
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_FillingPacking.png", ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath)  
    #Process Tab Summary
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath + "\\Pro_Tab_Summary.png", ProcessAppPath)
    Process.ProcessWizard_Summary_Finish(ProcessAppPath)
    Log.write_log(ProjectName, "Info: Process Wizard Setting is Finished")
   
    #Analyze Setting
    Analyzelist = [StudioAppPath + "\\Analysis_CtFandPCtW.png",StudioAppPath + "\\Analysis_CoolingTransient_2.png", StudioAppPath + "\\Analysis_FandP_2.png",StudioAppPath + "\\Analysis_CoolingTransient_2.png",StudioAppPath + "\\Analysis_Warpage.png"]
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
    Studio.ImportGeometry(SourcePath2, StudioAppPath)
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
    Process.ProcessWizard_Project_SettingMethod("CAE", ProcessAppPath)
    #Process Tab Filling/Packing Setting
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_ProjectSetting.png", ProcessAppPath + "\\Pro_Tab_FillingPacking.png", ProcessAppPath)
    Process.Click_Icon(ProcessAppPath + r"\Btn_AdvancedSetting.png", ProcessAppPath + r"\Pro_AdvancedSetting.png")

    Process.ValueSetting(ProcessAppPath + "\\Process_Control_Point.png", 0, 25, "2", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\process_value.png", 0, 70, "0.5", ProcessAppPath)
    click(Pattern(ProcessAppPath+ r"\process_action.png").similar(0.90).targetOffset(0, 50))
    click(Pattern(ProcessAppPath+ r"\Process_valve_close.png").similar(0.9))
    
    Process.ValueSetting(ProcessAppPath + "\\Process_Control_Point.png", 0, 90, "2", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\process_value.png", 0, 135, "0.5", ProcessAppPath)
    click(Pattern(ProcessAppPath+ r"\process_action.png").similar(0.90).targetOffset(0, 135))
    click(Pattern(ProcessAppPath+ r"\Process_valve_close.png").similar(0.9))

    Process.Click_Icon(ProcessAppPath + "\\Btn_OK.png", ProcessAppPath + "\\Pro_Tab_FillingPacking.png")
    #Process Tab Cooling Setting
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_FillingPacking.png", ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath)  
    #Process Tab Summary
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath + "\\Pro_Tab_Summary.png", ProcessAppPath)
    Process.ProcessWizard_Summary_Finish(ProcessAppPath)
    Log.write_log(ProjectName, "Info: Process Wizard Setting is Finished")
    
    #Analyze Setting
    Analyzelist = [StudioAppPath + "\\Analysis_CtFandPCtW.png",StudioAppPath + "\\Analysis_CoolingTransient_2.png", StudioAppPath + "\\Analysis_FandP_2.png",StudioAppPath + "\\Analysis_CoolingTransient_2.png",StudioAppPath + "\\Analysis_Warpage.png"]
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
    Remark_name = ["Rhino","Line","Geometry"]
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
