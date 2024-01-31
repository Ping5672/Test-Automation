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


ProjectName = "FIM-S4-P2"
username = "moldex3dqa"
password = "123456"
SVNPath = r"svn://192.168.3.4/QARepository/AutoTest/Moldex3D/2023Series/Moldex3D/CaseReference/ENT/" + ProjectName + r"/Geometry"
Filename= SVNPath.split('/')[-2]
localpath = os.path.normpath((cwd + r"\\" +Filename))
MainInstallPath ,ver = Common.getregkeyvalue(r"HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\CoreTechSystem\MDX_ParallelComputing", "INSTALLDIR")
WorkingFolder = Common.getregkeyvalue(r"HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\CoreTechSystem\MDX_ParallelComputing", "WorkingFolder")
StudioPath = MainInstallPath + r"\Bin\MDXStudio.exe"

CaseReferncePath = Common.gototargetpath('MDX_ENT') + "\\" + ProjectName
SourcePath =CaseReferncePath+ r"\FIM_CBA.mdg"
CMPath = MainInstallPath + r"\Bin\MDXComputingManager" + ver + ".exe"
hostname, local_ip = Common.getcuriphostname()

Bank_Folder = r"C:\Users\Administrator\AppData\Roaming\CoreTechSystem\Moldex3D " + ver + r"\Bank"
Material_Folder = r"C:\Users\Administrator\AppData\Roaming\CoreTechSystem\Moldex3D " + ver + r"\Material"

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
    Studio.Home_MoldingType_New("Module_IM2", StudioAppPath)
    Studio.MeshType("Solid", StudioAppPath)
    Studio.Home_MoldingType_New("Module_FIM", StudioAppPath)
    Studio.Home_Model("ImportGeometry", StudioAppPath)
    Studio.ImportGeometry(SourcePath, StudioAppPath)
    Studio.SpecifyModelName("FIM_CBA_FC",StudioAppPath)
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
    sMatlist = [MaterialAppPath + "\\MaterialPC+ABS.png", MaterialAppPath + "\\MaterialCAE.png",MaterialAppPath + "\\MaterialDA36.png"]
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
    Process.ValueSetting(ProcessAppPath + "\\Pro_Filling_FillingTime.png", 60, 0, "1.5", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_Filling_PackingTime.png", 60, 0, "0.1", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_Filling_MeltTemp3.png", 90, 0, "280", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_Filling_MoldTemp3.png", 90, 0, "100", ProcessAppPath)
    #Process Filling/Packing - Flow Rate Profile Setting
    Process.Click_Icon(ProcessAppPath + "\\Btn_Pro_Flow_rate_profile.png", ProcessAppPath + "\\Pro_Filling_FlowRateProFile.png")
    Process.ProcessWizard_FillingPacking_Profile_Type_Switch("\\Pro_Type_FlowRate%Time%.png", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_SectionNo.png", 60, 0, "1", ProcessAppPath)
    Profilelist = [ProcessAppPath + "\\Pro_Filling_FlowRateProFile.png", "50"]
    Process.ProcessWizard_FillingPacking_Profile_Section_Value(Profilelist, ProcessAppPath)
    Process.Click_Icon(ProcessAppPath + "\\Btn_OK.png", ProcessAppPath + "\\Pro_Tab_FillingPacking.png")
    #Process Filling/Packing - Packing Pressure Profile Setting
    Process.Click_Icon(ProcessAppPath + "\\Btn_Pro_Pack_pressure_profile.png", ProcessAppPath + "\\Pro_Filling_Packingpressureprofile.png")
    Process.ProcessWizard_FillingPacking_Profile_Type_Switch("\\Pro_Type_PackPressure%TimeSec.png", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_SectionNo.png", 60, 0, "1", ProcessAppPath)
    Profilelist = [ProcessAppPath + "\\Pro_Filling_Packingpressureprofile.png", "20"]
    Process.ProcessWizard_FillingPacking_Profile_Section_Value(Profilelist, ProcessAppPath)
    Process.Click_Icon(ProcessAppPath + "\\Btn_OK.png", ProcessAppPath + "\\Pro_Tab_FillingPacking.png")
    #Process Tab Foaming Setting
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_FillingPacking.png", ProcessAppPath + "\\Pro_Tab_Foaming.png", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_Foaming_VolumePercentage.png", 180, 0, "90", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_Foaming_SolidPartWeight.png", 100, 0, "130", ProcessAppPath)
    Process.Click_IconEx(ProcessAppPath + "\\Pro_Foaming_GasDosageAmount.png")
    Process.Click_IconEx(ProcessAppPath + "\\Pro_Foaming_CBA.png")
    Process.ValueSetting(ProcessAppPath + "\\Pro_Foaming_CBADosageAmount.png", 160, 0, "3", ProcessAppPath)
    #Process Tab Cooling Setting
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_Foaming.png", ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_Cooling_Cool_Time.png", 130, 0, "15", ProcessAppPath)
    #Process Tab Summary
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath + "\\Pro_Tab_Summary.png", ProcessAppPath)
    Process.ProcessWizard_Summary_Finish(ProcessAppPath)
    Log.write_log(ProjectName, "Info: Process Wizard Setting is Finished")
    
    #Analyze Setting
    Analyzelist = [StudioAppPath + "\\Analysis_CFAndPCtW.png", StudioAppPath + "\\Analysis_CoolingCycle2.png", StudioAppPath + "\\Analysis_FillingAndPacking_2.png", StudioAppPath + "\\Analysis_CoolingTransient_2.png", StudioAppPath + "\\Analysis_Warpage.png"]
    Studio.AnalysisSetting(Analyzelist, StudioAppPath)
    Log.write_log(ProjectName, "Info: Analyze Setting is Finished")
    
    #Computation Parameter Wizard Setting
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\ComputationLogo.png")    
    #CMX Tab Cool Setting
    CMX.CMX_Tab_Change(CMXAppPath + "\\CMX_Tab_Cool.png")
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\CMX_Cooling_AccurancyLevel_Standard.png")
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\CMX_Btn_OK.png")
    Log.write_log(ProjectName, "Info: Computation Parameter Wizard Setting is Finished")
    
    #Run 02
    #New Run
    Studio.Click_Icon(StudioAppPath, "\\Studio_NewRun2.png", 0)
    Log.write_log(ProjectName, "Info: New Run Setting is Finished")

    #Studio Pre Process Setting
    Studio.MeshType("Solid", StudioAppPath)
    Studio.Home_MoldingType_New("Module_FIM", StudioAppPath)
    Studio.Home_Model("ImportGeometry", StudioAppPath)
    Studio.ImportGeometry(SourcePath, StudioAppPath)
    Studio.SpecifyModelName("FIM_CBA_SC",StudioAppPath)
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
    Material.Wait_Dialog(StudioAppPath, "\\Logo_NonFiber_UnSelected.png", "\\Logo_NonFiber_UnSelected_Blue.png")
    Material.Click_Icon(MaterialAppPath + "\\MaterialLogo.png", 0)
    Material.Click_Icon(MaterialAppPath + "\\Studio_EM1.png", 200)
    Material.MCM2ndRunInsertSelection(MaterialAppPath + "\\StudioPartInsertSelection.png", MaterialAppPath + "\\Studio_DA36.png", MaterialAppPath)
    Log.write_log(ProjectName, "Info: Material Wizard Setting is Finished")
    
    #Process Wizard Setting
    Process.Home_Process("New", ProcessAppPath)
    #Process Tab Filling/Packing Setting  
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_ProjectSetting.png", ProcessAppPath + "\\Pro_Tab_FillingPacking.png", ProcessAppPath)  
    Process.ValueSetting(ProcessAppPath + "\\Pro_Filling_FillingTime.png", 60, 0, "1.5", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_Filling_PackingTime.png", 60, 0, "0.1", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_Filling_MeltTemp3.png", 90, 0, "280", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_Filling_MoldTemp3.png", 90, 0, "100", ProcessAppPath)
    #Process Filling/Packing - Flow Rate Profile Setting
    Process.Click_Icon(ProcessAppPath + "\\Btn_Pro_Flow_rate_profile.png", ProcessAppPath + "\\Pro_Filling_FlowRateProFile.png")
    Process.ProcessWizard_FillingPacking_Profile_Type_Switch("\\Pro_Type_FlowRate%Time%.png", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_SectionNo.png", 60, 0, "1", ProcessAppPath)
    Profilelist = [ProcessAppPath + "\\Pro_Filling_FlowRateProFile.png", "50"]
    Process.ProcessWizard_FillingPacking_Profile_Section_Value(Profilelist, ProcessAppPath)
    Process.Click_Icon(ProcessAppPath + "\\Btn_OK.png", ProcessAppPath + "\\Pro_Tab_FillingPacking.png")
    #Process Filling/Packing - Packing Pressure Profile Setting
    Process.Click_Icon(ProcessAppPath + "\\Btn_Pro_Pack_pressure_profile.png", ProcessAppPath + "\\Pro_Filling_Packingpressureprofile.png")
    Process.ProcessWizard_FillingPacking_Profile_Type_Switch("\\Pro_Type_PackPressure%TimeSec.png", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_SectionNo.png", 60, 0, "1", ProcessAppPath)
    Profilelist = [ProcessAppPath + "\\Pro_Filling_Packingpressureprofile.png", "20"]
    Process.ProcessWizard_FillingPacking_Profile_Section_Value(Profilelist, ProcessAppPath)
    Process.Click_Icon(ProcessAppPath + "\\Btn_OK.png", ProcessAppPath + "\\Pro_Tab_FillingPacking.png")
    #Process Tab Foaming Setting
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_FillingPacking.png", ProcessAppPath + "\\Pro_Tab_Foaming.png", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_Foaming_VolumePercentage.png", 180, 0, "90", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_Foaming_SolidPartWeight.png", 100, 0, "130", ProcessAppPath)
    Process.Click_IconEx(ProcessAppPath + "\\Pro_Foaming_GasDosageAmount.png")
    Process.Click_IconEx(ProcessAppPath + "\\Pro_Foaming_CBA.png")
    Process.ValueSetting(ProcessAppPath + "\\Pro_Foaming_CBADosageAmount.png", 160, 0, "3", ProcessAppPath)
    #Process Tab Cooling Setting
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_Foaming.png", ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_Cooling_Cool_Time.png", 130, 0, "15", ProcessAppPath)
    #Process Tab Summary
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath + "\\Pro_Tab_Summary.png", ProcessAppPath)
    Process.ProcessWizard_Summary_Finish(ProcessAppPath)
    Log.write_log(ProjectName, "Info: Process Wizard Setting is Finished")
    
    #Analyze Setting
    Analyzelist = [StudioAppPath + "\\Analysis_CFAndPCtW.png", StudioAppPath + "\\Analysis_CoolingCycle2.png", StudioAppPath + "\\Analysis_FillingAndPacking_2.png", StudioAppPath + "\\Analysis_CoolingTransient_2.png", StudioAppPath + "\\Analysis_Warpage.png"]
    Studio.AnalysisSetting(Analyzelist, StudioAppPath)
    Log.write_log(ProjectName, "Info: Analyze Setting is Finished")
    
    #Run 03
    #New Run
    Studio.Click_Icon(StudioAppPath, "\\Studio_NewRun2.png", 0)
    Log.write_log(ProjectName, "Info: New Run Setting is Finished")

    #Studio Pre Process Setting
    Studio.MeshType("eDesign", StudioAppPath)
    Studio.Home_MoldingType_New("Module_FIM", StudioAppPath)
    Studio.Home_Model("ImportGeometry", StudioAppPath)
    Studio.ImportGeometry(SourcePath, StudioAppPath)
    Studio.SpecifyModelName("FIM_CBA_eDesign",StudioAppPath)
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
    Material.Wait_Dialog(StudioAppPath, "\\Logo_NonFiber_UnSelected.png", "\\Logo_NonFiber_UnSelected_Blue.png")
    Material.Click_Icon(MaterialAppPath + "\\MaterialLogo.png", 0)
    Material.Click_Icon(MaterialAppPath + "\\Studio_EM1.png", 200)
    Material.MCM2ndRunInsertSelection(MaterialAppPath + "\\StudioPartInsertSelection.png", MaterialAppPath + "\\Studio_DA36.png", MaterialAppPath)
    Log.write_log(ProjectName, "Info: Material Wizard Setting is Finished")
    
    #Process Wizard Setting
    Process.Home_Process("New", ProcessAppPath)
    #Process Tab Filling/Packing Setting  
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_ProjectSetting.png", ProcessAppPath + "\\Pro_Tab_FillingPacking.png", ProcessAppPath)  
    Process.ValueSetting(ProcessAppPath + "\\Pro_Filling_FillingTime.png", 60, 0, "1.5", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_Filling_PackingTime.png", 60, 0, "0.1", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_Filling_MeltTemp3.png", 90, 0, "280", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_Filling_MoldTemp3.png", 90, 0, "100", ProcessAppPath)
    #Process Filling/Packing - Flow Rate Profile Setting
    Process.Click_Icon(ProcessAppPath + "\\Btn_Pro_Flow_rate_profile.png", ProcessAppPath + "\\Pro_Filling_FlowRateProFile.png")
    Process.ProcessWizard_FillingPacking_Profile_Type_Switch("\\Pro_Type_FlowRate%Time%.png", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_SectionNo.png", 60, 0, "1", ProcessAppPath)
    Profilelist = [ProcessAppPath + "\\Pro_Filling_FlowRateProFile.png", "50"]
    Process.ProcessWizard_FillingPacking_Profile_Section_Value(Profilelist, ProcessAppPath)
    Process.Click_Icon(ProcessAppPath + "\\Btn_OK.png", ProcessAppPath + "\\Pro_Tab_FillingPacking.png")
    #Process Filling/Packing - Packing Pressure Profile Setting
    Process.Click_Icon(ProcessAppPath + "\\Btn_Pro_Pack_pressure_profile.png", ProcessAppPath + "\\Pro_Filling_Packingpressureprofile.png")
    Process.ProcessWizard_FillingPacking_Profile_Type_Switch("\\Pro_Type_PackPressure%TimeSec.png", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_SectionNo.png", 60, 0, "1", ProcessAppPath)
    Profilelist = [ProcessAppPath + "\\Pro_Filling_Packingpressureprofile.png", "20"]
    Process.ProcessWizard_FillingPacking_Profile_Section_Value(Profilelist, ProcessAppPath)
    Process.Click_Icon(ProcessAppPath + "\\Btn_OK.png", ProcessAppPath + "\\Pro_Tab_FillingPacking.png")
    #Process Tab Foaming Setting
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_FillingPacking.png", ProcessAppPath + "\\Pro_Tab_Foaming.png", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_Foaming_VolumePercentage.png", 180, 0, "90", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_Foaming_SolidPartWeight.png", 100, 0, "130", ProcessAppPath)
    Process.Click_IconEx(ProcessAppPath + "\\Pro_Foaming_GasDosageAmount.png")
    Process.Click_IconEx(ProcessAppPath + "\\Pro_Foaming_CBA.png")
    Process.ValueSetting(ProcessAppPath + "\\Pro_Foaming_CBADosageAmount.png", 160, 0, "3", ProcessAppPath)
    #Process Tab Cooling Setting
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_Foaming.png", ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_Cooling_Cool_Time.png", 130, 0, "15", ProcessAppPath)
    #Process Tab Summary
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath + "\\Pro_Tab_Summary.png", ProcessAppPath)
    Process.ProcessWizard_Summary_Finish(ProcessAppPath)
    Log.write_log(ProjectName, "Info: Process Wizard Setting is Finished")
    
    #Analyze Setting
    Analyzelist = [StudioAppPath + "\\Analysis_CFAndPCtW.png", StudioAppPath + "\\Analysis_CoolingCycle2.png", StudioAppPath + "\\Analysis_FillingAndPacking_2.png", StudioAppPath + "\\Analysis_CoolingTransient_2.png", StudioAppPath + "\\Analysis_Warpage.png"]
    Studio.AnalysisSetting(Analyzelist, StudioAppPath)
    Log.write_log(ProjectName, "Info: Analyze Setting is Finished")

    #Computation Parameter Wizard Setting
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\ComputationLogo.png")    
    #CMX Tab Cool Setting
    CMX.CMX_Tab_Change(CMXAppPath + "\\CMX_Tab_Cool.png")
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\CMX_Cooling_AccurancyLevel_Standard.png")
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\CMX_Btn_OK.png")
    Log.write_log(ProjectName, "Info: Computation Parameter Wizard Setting is Finished")
    
    #Change Remark Name
    Studio.Click_Icon(StudioAppPath, "\\Studio_Tree_Run.png", 0)
    wait(1)
    Remark_name = ["FC", "SC", "eDesign"]
    CRN.Run(Remark_name, CRNAppPath)
    Log.write_log(ProjectName, "Info: Change Remark Name is Finished")
    
    #Set RC Task Number
    Studio.TaskNumberSetting("4", StudioAppPath)
    click(StudioAppPath + "\\Btn_OK.png")
    Studio.Create_BJS(13,StudioAppPath,ProjectName,WorkingFolder)
    CM.SendRCtoCM(StudioAppPath,CMAppPath)

    #Set Localhost Task Number
    Studio.TaskNumberSetting("1", StudioAppPath)
    click(StudioAppPath + "\\Btn_OK.png")

    #Localhost Server Connect
    Studio.OpenApp(CMPath, CMAppPath + "\\CM_UI.png")
    CM.connectserver("LH",CMAppPath)
    wait(1)
    click(StudioAppPath + "\\Studio_logo.png")
    Log.write_log(ProjectName, "Info: Computing Manager Add Server Setting is Finished")
    wait(1)
    Studio.ClickRun(30, StudioAppPath)
    Studio.Submit_Batch_Run(2,StudioAppPath)
    wait(2)
    
    #Close Studio UI
    Studio.CloseApp(StudioPath)  
    Log.write_log(ProjectName, "Info: %s Test is Finished!" % ProjectName)
    
except:
    os.popen(("python {}").format(exceptprocedureApp))
    print( "ENT-IM-S15-P1 Test is Failed!")
    Log.write_log(ProjectName, "Error: %s Test is Failed!" % ProjectName)
Log.write_log2(ProjectName, "Summary")