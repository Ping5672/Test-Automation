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


ProjectName = "IM-S1-P1"
username = "moldex3dqa"
password = "123456"
SVNPath = r"svn://192.168.3.4/QARepository/AutoTest/Moldex3D/2023Series/Moldex3D/CaseReference/ENT/" + ProjectName + r"/Geometry"
Filename= SVNPath.split('/')[-2]
localpath = os.path.normpath((cwd + r"\\" +Filename))
MainInstallPath ,ver = Common.getregkeyvalue(r"HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\CoreTechSystem\MDX_ParallelComputing", "INSTALLDIR")
WorkingFolder = Common.getregkeyvalue(r"HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\CoreTechSystem\MDX_ParallelComputing", "WorkingFolder")
StudioPath = MainInstallPath + r"\Bin\MDXStudio.exe"
#CaseReferncePath = os.path.join(Common.gototargetpath('MDX_ENT'), r'/NEW-MDX-ENT/IM-S1-P1/Geometry')
CaseReferncePath = Common.gototargetpath('MDX_ENT') + "\\" + ProjectName
PartPath =CaseReferncePath+ r"\Part.stp"
PartInsertPath = CaseReferncePath+ r"\PartInsert.stp"
MoldinsertPath =CaseReferncePath + r"\MoldInsert.stp"
CMPath = MainInstallPath + r'\Bin\MDXComputingManager' + ver + r'.exe'
hostname, local_ip = Common.getcuriphostname()


try:
    #svn execution
    Common.SVNLogin(username, password)
    Common.SVNDownload(SVNPath, localpath)
    print ("Info: SVN download is Finished")
    Log.write_log("Pre_Setting", "Info: SVN download is Finished")
    
    #Open Studio UI
    Studio.OpenApp(StudioPath, StudioAppPath + "\\Studio_UI.png")
    Log.write_log(ProjectName , "Info: Open Studio is Finished")
    #New Project
    Studio.NewProject(ProjectName , StudioAppPath)
    Log.write_log(ProjectName , "Info: New Project Setting is Finished")
    #Studio Pre Process Setting
    Studio.MeshType("Solid", StudioAppPath)
    Studio.Home_MoldingType(0, -105, StudioAppPath)
    Studio.Click_Icon(StudioAppPath, "\\Studio_Tree_Model.png",0)
    Studio.Click_Icon(StudioAppPath, "\\Studio_Import_icon.png", 0)
    Studio.ImportGeometry(MoldinsertPath, StudioAppPath)
    Studio.SetAttribute("Moldinsert","Geoemetry", StudioAppPath)
    #set Moldinsert attribute
    Studio.Click_Icon(StudioAppPath, "\\Studio_Import_icon.png", 0)
    Studio.ImportGeometry(PartPath, StudioAppPath)
    Studio.SetAttribute("Part","Geoemetry", StudioAppPath)
     
    #set part attribute
    Studio.Click_Icon(StudioAppPath, "\\Studio_Import_icon.png", 0)
    Studio.ImportGeometry(PartInsertPath, StudioAppPath)
    Studio.SetAttribute("PartInsert","Geoemetry", StudioAppPath)
    #set part insert attribute
    
    
    wait(3)
    Studio.Gate_wizard(StudioAppPath,'19.823,0.001,0.001')
   
    wait(2)
    Studio.Runner_wizard(StudioAppPath)
    Studio.Moldbase_wizard(StudioAppPath)
    Studio.CoolingChannel_wizard(StudioAppPath)
    Studio.SwitchTab(StudioAppPath + "\\Studio_Tab_Mesh.png", StudioAppPath + "\\Studio_Tab_Meshing.png")
    nodesize1={'Part':'0.8'}
    nodesize2={'Moldinsert':'0.8'}
    nodesize3={'Partinsert':'0.8'}
    Studio.Node_Seeding(StudioAppPath,**nodesize1)
    
    Studio.Node_Seeding(StudioAppPath,**nodesize2)
    
    Studio.Node_Seeding(StudioAppPath,**nodesize3)
    wait(2)
    Studio.Meshing_Generate(StudioAppPath)
    Studio.Meshing_GenerateBLM("None", StudioAppPath)
    Studio.Wait_Dialog(StudioAppPath, "\\Studio_FinalCheck.png")
    Studio.Click_Icon(StudioAppPath, "\\Btn_Angle_Perspective_Seletected.png", 40)
    Studio.Click_Icon(StudioAppPath, "\\Btn_Fit_To_Window.png", -24)
    Studio.Click_Icon(StudioAppPath, "\\Btn_ShowModeSelected_FeatureShaded2.png", 40)
    Studio.Final_Check(StudioAppPath)
    Log.write_log(ProjectName, "Info: Studio Pre Process Setting is Finished")
    wait(3)

    #Material Wizard Setting
    sMatlist = [MaterialAppPath + r"\MaterialABS_2023.png", MaterialAppPath + r"\MaterialASchulman_2023.png", MaterialAppPath + r"\MaterialRABS9050UV5_2023.png"]
    sMatlist2 = [MaterialAppPath + "\\MaterialMetal_2023.png", MaterialAppPath + "\\MaterialCAE_2023.png", MaterialAppPath + "\\MaterialBrass_2023.png"]
    Material.OpenMaterialWizard(MaterialAppPath + "\\Studio_EM1.png", 200, 0, MaterialAppPath)
    Material.ClickMDXBank(MaterialAppPath)
    Material.SelectPartMaterial(sMatlist)
    Material.MaterialNotAddToUserBank(MaterialAppPath)
    Material.CloseMaterialWizard(MaterialAppPath)

    #Part Insert
    Studio.Wait_Dialog(StudioAppPath, "\\Logo_Fiber2.png")
    Material.OpenMaterialWizard(MaterialAppPath + "\\StudioPartInsert1.png", 200, 0, MaterialAppPath)
    Material.ClickMDXBank(MaterialAppPath)
    Material.SelectPartMaterial(sMatlist2)
    Material.MaterialNotAddToUserBank(MaterialAppPath)
    Material.CloseMaterialWizard(MaterialAppPath)
    Log.write_log(ProjectName, "Info: Material Wizard Setting is Finished")
    
    #Process Wizard Setting
    Process.Home_Process("New", ProcessAppPath)
    Process.ProcessWizard_Project_SettingMethod("M1", ProcessAppPath) 
    #Process Tab Filling/Packing Setting
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_ProjectSetting.png", ProcessAppPath + "\\Pro_Tab_FillingPacking.png", ProcessAppPath)
    
    Process.ValueSetting(ProcessAppPath + "\\Pro_Filling_PackingTime.png", 60, 0, "4.27", ProcessAppPath)
    #Process Filling/Packing - Flow Rate Profile Setting
    Process.Click_Icon(ProcessAppPath + "\\Btn_Pro_Flow_rate_profile.png", ProcessAppPath + "\\Pro_Filling_FlowRateProFile.png")
    Process.ProcessWizard_FillingPacking_Profile_Type_Switch("\\Pro_Type_InjectionVelocity%RamPositionmm.png", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_SectionNo.png", 60, 0, "3", ProcessAppPath)
    Profilelist = [ProcessAppPath + "\\Pro_Filling_FlowRateProFile.png", "10.3296", "30","8.4083","67.2","0.8408","50.4"]
    Process.ProcessWizard_FillingPacking_Profile_Section_Value(Profilelist, ProcessAppPath)
    Process.Click_Icon(ProcessAppPath + "\\Btn_OK.png", ProcessAppPath + "\\Pro_Tab_FillingPacking.png")
    #Process Filling/Packing - Injection Pressure Profile Setting
    Process.Click_Icon(ProcessAppPath + "\\Btn_Pro_Inject_pressure_profile.png", ProcessAppPath + "\\Pro_Filling_Injectionpressureprofile.png")
    Process.ProcessWizard_FillingPacking_Profile_Type_Switch("\\Pro_Type_InjectionPressure%RamPositionmm.png", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_SectionNo.png", 60, 0, "1", ProcessAppPath)
    Process.Click_Icon(ProcessAppPath + "\\Btn_OK.png", ProcessAppPath + "\\Pro_Tab_FillingPacking.png")
    #Process Filling/Packing - Packing Pressure Profile Setting
    Process.Click_Icon(ProcessAppPath + "\\Btn_Pro_Pack_pressure_profile.png", ProcessAppPath + "\\Pro_Filling_Packingpressureprofile.png")
    Process.ProcessWizard_FillingPacking_Profile_Type_Switch("\\Pro_Type_PackPressure%TimeSec.png", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_SectionNo.png", 60, 0, "3", ProcessAppPath)
    Process.Click_Icon(ProcessAppPath + "\\Btn_OK.png", ProcessAppPath + "\\Pro_Tab_FillingPacking.png")
    #Process Tab Cooling Setting
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_FillingPacking.png", ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath)  
  
    #Process Tab Summary
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath + "\\Pro_Tab_Summary.png", ProcessAppPath)
    Process.ProcessWizard_Summary_Finish(ProcessAppPath)
    Log.write_log(ProjectName, "Info: Process Wizard Setting is Finished")
    


    #Analyze Setting
    Analyzelist = [StudioAppPath + "\\Analysis_CtFPCtW.png", StudioAppPath + "\\Analysis_CoolingTransient_2.png", StudioAppPath + "\\Analysis_Filling.png", StudioAppPath + "\\Analysis_Packing2.png", StudioAppPath + "\\Analysis_CoolingTransient_2.png", StudioAppPath + "\\Analysis_Warpage.png"]
    Studio.AnalysisSetting(Analyzelist, StudioAppPath)
    Log.write_log(ProjectName, "Info: Analyze Setting is Finished")
    #Computation Parameter Wizard Setting
    
    #CMX Tab Flow/Pack Setting
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\ComputationLogo_2023.png")
    CMX.FPSolverTypeChange(CMXAppPath + "\\CMX_Flow_Solver.png", "Enhanced")
    CMX.Checkbox(CMXAppPath + "\\CMX_Flow_Weldline_particle.png", -55, 0, CMXAppPath)
    CMX.Checkbox(CMXAppPath + "\\CMX_Flow_ParticleTrackingFrom.png", -60, 0, CMXAppPath)
    
    #CMX Tab Cool Setting
    CMX.CMX_Tab_Change(CMXAppPath + "\\CMX_Tab_Cool.png")
    CMX.Checkbox(CMXAppPath + "\\CMX_Cool_CoolingChannelAnalysisBy2.png", -82, 0, CMXAppPath)
    CMX.SelectDropDownMenu(CMXAppPath + "\\CMX_Cool_CoolingChannelAnalysisBy2.png", -10, 30, CMXAppPath + "\\CMX_Cool_Run3DSolidCoolingChannelAnalysis2.png", 0, 0)
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\CMX_Btn_OK.png")
    
    Log.write_log("TP", "Info: Computation Parameter Wizard Setting is Finished")
 
    
    wait(1)
    Studio.Click_Icon(StudioAppPath, "\\Studio_Tree_Run.png", 0)
    CRfM.Copy_Run(Pattern(Copypath + "\\Run01.png").similar(0.92), "RunInputDataOnly", "None", "default", Copypath)
    Log.write_log(ProjectName, "Info: Copy SC to eDesign  is Finished")
    #copy run to edesign
    Studio.MeshType("eDesign", StudioAppPath)
    wait(2)
    Studio.SwitchTab(StudioAppPath +"\\Studio_Tab_Mesh.png", StudioAppPath + "\\Studio_Tab_Meshing.png")
    Studio.Meshing_Generate(StudioAppPath)
    Studio.Meshing_GenerateeDesign(StudioAppPath)
    Studio.Wait_Dialog(StudioAppPath, "\\Log_Generate_Solid_Mesh_Done.png")
    Studio.Final_Check(StudioAppPath)
    wait(3)
    

    #Process Wizard Setting
    Process.Home_Process("New", ProcessAppPath)
    Process.ProcessWizard_Project_SettingMethod("M1", ProcessAppPath) 
    #Process Tab Filling/Packing Setting
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_ProjectSetting.png", ProcessAppPath + "\\Pro_Tab_FillingPacking.png", ProcessAppPath)
    
    Process.ValueSetting(ProcessAppPath + "\\Pro_Filling_PackingTime.png", 60, 0, "4.27", ProcessAppPath)
    #Process Filling/Packing - Flow Rate Profile Setting
    Process.Click_Icon(ProcessAppPath + "\\Btn_Pro_Flow_rate_profile.png", ProcessAppPath + "\\Pro_Filling_FlowRateProFile.png")
    Process.ProcessWizard_FillingPacking_Profile_Type_Switch("\\Pro_Type_InjectionVelocity%RamPositionmm.png", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_SectionNo.png", 60, 0, "3", ProcessAppPath)
    Profilelist = [ProcessAppPath + "\\Pro_Filling_FlowRateProFile.png", "10.3296", "30","8.4083","67.2","0.8408","50.4"]
    Process.ProcessWizard_FillingPacking_Profile_Section_Value(Profilelist, ProcessAppPath)
    Process.Click_Icon(ProcessAppPath + "\\Btn_OK.png", ProcessAppPath + "\\Pro_Tab_FillingPacking.png")
    #Process Filling/Packing - Injection Pressure Profile Setting
    Process.Click_Icon(ProcessAppPath + "\\Btn_Pro_Inject_pressure_profile.png", ProcessAppPath + "\\Pro_Filling_Injectionpressureprofile.png")
    Process.ProcessWizard_FillingPacking_Profile_Type_Switch("\\Pro_Type_InjectionPressure%RamPositionmm.png", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_SectionNo.png", 60, 0, "1", ProcessAppPath)
    Process.Click_Icon(ProcessAppPath + "\\Btn_OK.png", ProcessAppPath + "\\Pro_Tab_FillingPacking.png")
    #Process Filling/Packing - Packing Pressure Profile Setting
    Process.Click_Icon(ProcessAppPath + "\\Btn_Pro_Pack_pressure_profile.png", ProcessAppPath + "\\Pro_Filling_Packingpressureprofile.png")
    Process.ProcessWizard_FillingPacking_Profile_Type_Switch("\\Pro_Type_PackPressure%TimeSec.png", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_SectionNo.png", 60, 0, "3", ProcessAppPath)
    Process.Click_Icon(ProcessAppPath + "\\Btn_OK.png", ProcessAppPath + "\\Pro_Tab_FillingPacking.png")
    #Process Tab Cooling Setting
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_FillingPacking.png", ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath)  
  
    #Process Tab Summary
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath + "\\Pro_Tab_Summary.png", ProcessAppPath)
    Process.ProcessWizard_Summary_Finish(ProcessAppPath)
    Log.write_log(ProjectName, "Info: Process Wizard Setting is Finished")
    
    wait(5)
    #Computation Parameter Wizard Setting
    #CMX Tab Flow/Pack Setting
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\ComputationLogo_2023.png")
    CMX.FPSolverTypeChange(CMXAppPath + "\\CMX_Flow_Solver.png", "Enhanced")
    CMX.Checkbox(CMXAppPath + "\\CMX_Flow_Weldline_particle.png", -55, 0, CMXAppPath)
    CMX.Checkbox(CMXAppPath + "\\CMX_Flow_ParticleTrackingFrom.png", -60, 0, CMXAppPath)
    
    #CMX Tab Cool Setting
    CMX.CMX_Tab_Change(CMXAppPath + "\\CMX_Tab_Cool.png")
    CMX.Checkbox(CMXAppPath + "\\CMX_Cool_CoolingChannelAnalysisBy2.png", -82, 0, CMXAppPath)
    CMX.SelectDropDownMenu(CMXAppPath + "\\CMX_Cool_CoolingChannelAnalysisBy2.png", -10, 30, CMXAppPath + "\\CMX_Cool_Run cooling_channel_network_analysis.png", 0, 0)
    CMX.ClickButton(CMXAppPath, "\\CMX_Cooling_AccurancyLevel_Standard.png")
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\CMX_Btn_OK.png")
    Log.write_log(ProjectName, "Info: Computation Parameter Wizard Setting is Finished")
    
    wait(1)
    Studio.Click_Icon(StudioAppPath, "\\Studio_Tree_Run.png", 0)
    Studio.Click_Icon(StudioAppPath, "\\Run01.png",0)
    wait(3)
    Studio.SwitchTab(StudioAppPath + "\\Studio_Tab_Mesh.png", StudioAppPath + "\\Studio_Tab_Meshing.png")
    Studio.Meshing_Generate(StudioAppPath)
    Log.write_log(ProjectName, "Info: Copy SC to FC  is Finished")
    #copy run to fc

    Studio.Meshing_GenerateBLM("Runner", StudioAppPath)
    Studio.Wait_Dialog(StudioAppPath, "\\Studio_Runner_Check.png")
    Studio.Click_Icon(StudioAppPath, "\\Btn_Angle_Perspective_Seletected.png", 40)
    Studio.Click_Icon(StudioAppPath, "\\Btn_Fit_To_Window.png", -24)
    Studio.Click_Icon(StudioAppPath, "\\Btn_ShowModeSelected_FeatureShaded2.png", 40)
    Studio.Final_Check(StudioAppPath)
    wait(3)
    #Process Wizard Setting
    Process.Home_Process("New", ProcessAppPath)
    Process.ProcessWizard_Project_SettingMethod("M1", ProcessAppPath) 
    #Process Tab Filling/Packing Setting
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_ProjectSetting.png", ProcessAppPath + "\\Pro_Tab_FillingPacking.png", ProcessAppPath)
    
    Process.ValueSetting(ProcessAppPath + "\\Pro_Filling_PackingTime.png", 60, 0, "4.27", ProcessAppPath)
    #Process Filling/Packing - Flow Rate Profile Setting
    Process.Click_Icon(ProcessAppPath + "\\Btn_Pro_Flow_rate_profile.png", ProcessAppPath + "\\Pro_Filling_FlowRateProFile.png")
    Process.ProcessWizard_FillingPacking_Profile_Type_Switch("\\Pro_Type_InjectionVelocity%RamPositionmm.png", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_SectionNo.png", 60, 0, "3", ProcessAppPath)
    Profilelist = [ProcessAppPath + "\\Pro_Filling_FlowRateProFile.png", "10.3296", "30","8.4083","67.2","0.8408","50.4"]
    Process.ProcessWizard_FillingPacking_Profile_Section_Value(Profilelist, ProcessAppPath)
    Process.Click_Icon(ProcessAppPath + "\\Btn_OK.png", ProcessAppPath + "\\Pro_Tab_FillingPacking.png")
    #Process Filling/Packing - Injection Pressure Profile Setting
    Process.Click_Icon(ProcessAppPath + "\\Btn_Pro_Inject_pressure_profile.png", ProcessAppPath + "\\Pro_Filling_Injectionpressureprofile.png")
    Process.ProcessWizard_FillingPacking_Profile_Type_Switch("\\Pro_Type_InjectionPressure%RamPositionmm.png", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_SectionNo.png", 60, 0, "1", ProcessAppPath)
    Process.Click_Icon(ProcessAppPath + "\\Btn_OK.png", ProcessAppPath + "\\Pro_Tab_FillingPacking.png")
    #Process Filling/Packing - Packing Pressure Profile Setting
    Process.Click_Icon(ProcessAppPath + "\\Btn_Pro_Pack_pressure_profile.png", ProcessAppPath + "\\Pro_Filling_Packingpressureprofile.png")
    Process.ProcessWizard_FillingPacking_Profile_Type_Switch("\\Pro_Type_PackPressure%TimeSec.png", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_SectionNo.png", 60, 0, "3", ProcessAppPath)
    Process.Click_Icon(ProcessAppPath + "\\Btn_OK.png", ProcessAppPath + "\\Pro_Tab_FillingPacking.png")
    #Process Tab Cooling Setting
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_FillingPacking.png", ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath)  
  
    #Process Tab Summary
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath + "\\Pro_Tab_Summary.png", ProcessAppPath)
    Process.ProcessWizard_Summary_Finish(ProcessAppPath)
    Log.write_log(ProjectName, "Info: Process Wizard Setting is Finished")
    
    wait(5)
    #Computation Parameter Wizard Setting
    #CMX Tab Flow/Pack Setting
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\ComputationLogo_2023.png")
    CMX.FPSolverTypeChange(CMXAppPath + "\\CMX_Flow_Solver.png", "Enhanced")
    CMX.Checkbox(CMXAppPath + "\\CMX_Flow_Weldline_particle.png", -55, 0, CMXAppPath)
    CMX.Checkbox(CMXAppPath + "\\CMX_Flow_ParticleTrackingFrom.png", -60, 0, CMXAppPath)

    
    #CMX Tab Cool Setting
    CMX.CMX_Tab_Change(CMXAppPath + "\\CMX_Tab_Cool.png")
    CMX.Checkbox(CMXAppPath + "\\CMX_Cool_CoolingChannelAnalysisBy2.png", -82, 0, CMXAppPath)
    CMX.SelectDropDownMenu(CMXAppPath + "\\CMX_Cool_CoolingChannelAnalysisBy2.png", -10, 30, CMXAppPath + "\\CMX_Cool_Run cooling_channel_network_analysis.png", 0, 0)
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\CMX_Cooling_AccurancyLevel_Standard.png")
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\CMX_Btn_OK.png")
    Log.write_log(ProjectName, "Info: Computation Parameter Wizard Setting is Finished")
   
    wait(1)
    #Change Remark Name
    Studio.Click_Icon(StudioAppPath, r"\Studio_Tree_Run.png", 0)
    wait(1)
    Remark_name = ["SC", "FC", "eDesign"]
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
    print( "ENT-IM-S1-P1 Test is Failed!")
    Log.write_log(ProjectName, "Error: %s Test is Failed!" % ProjectName)
Log.write_log2(ProjectName, "Summary")
