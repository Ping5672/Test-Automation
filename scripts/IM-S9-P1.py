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

ProjectName = "IM-S9-P1"
username = "moldex3dqa"
password = "123456"
SVNPath = r"svn://192.168.3.4/QARepository/AutoTest/Moldex3D/2023Series/Moldex3D/CaseReference/ENT/" + ProjectName + r"/Geometry"
localpath = os.path.normpath((cwd + r"\\" +ProjectName))
MainInstallPath ,ver = Common.getregkeyvalue(r"HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\CoreTechSystem\MDX_ParallelComputing", "INSTALLDIR")
WorkingFolder = Common.getregkeyvalue(r"HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\CoreTechSystem\MDX_ParallelComputing", "WorkingFolder")
StudioPath = MainInstallPath + r"\Bin\MDXStudio.exe"
MPCaseReferncePath = Common.gototargetpath('MDX_ENT') + "\\" + ProjectName +"\Mold Plate"
PartPath = MPCaseReferncePath + r"\Part.stp"
RunnerPath = MPCaseReferncePath + r"\Runner.stp"
CoolingChannelPath = MPCaseReferncePath + r"\Cooling Channel.stp"
MoldplatePath1 = MPCaseReferncePath + r"\MoldPlate(fixed).stp"
MoldplatePath2 = MPCaseReferncePath + r"\MoldPlate(move).stp"
IMDCaseReferncePath = Common.gototargetpath('MDX_ENT') + "\\" + ProjectName
IMDSourcePath= IMDCaseReferncePath+ r"\Solid_IM_IMD.mdg"
CMPath = MainInstallPath + r'\Bin\MDXComputingManager' + ver + r'.exe'
hostname, local_ip = Common.getcuriphostname()

try:
   
    #svn execution
    Common.SVNLogin(username, password)
    Common.SVNDownload(SVNPath, localpath)
    #Open Studio UI 
    
    Studio.OpenApp(StudioPath, StudioAppPath + "\\Studio_UI.png")
    Log.write_log(ProjectName, "Info: Open Studio is Finished")
    #New Project
    Studio.NewProject(ProjectName, StudioAppPath)
    Log.write_log(ProjectName, "Info: New Project Setting is Finished")

    #Studio Pre Process Setting
    Studio.MeshType("Solid", StudioAppPath)
    Studio.Home_MoldingType(0, -105, StudioAppPath)
    Studio.Click_Icon(StudioAppPath, "\\Studio_Import_icon.png", 0)
    wait(2)
    Studio.ImportGeometry(PartPath, StudioAppPath)
    Studio.Click_Icon(StudioAppPath, "\\Studio_Tree_Model.png",0)
    Studio.SetAttribute("Part","Geoemetry", StudioAppPath)
    #set part attribute
    Studio.Click_Icon(StudioAppPath, "\\Studio_Import_icon.png", 0)
    Studio.ImportGeometry(RunnerPath, StudioAppPath)
    #Studio.Click_Icon(StudioAppPath, "\\Studio_Tree_Model.png",0)
    Studio.SetAttribute("ColdRunner","Geoemetry", StudioAppPath) 
    #set runner attribute
    Studio.Click_Icon(StudioAppPath, "\\Studio_Import_icon.png", 0)
    Studio.ImportGeometry(MoldplatePath1, StudioAppPath)
    Studio.SetAttribute("MoldPlate_Fix","Geoemetry", StudioAppPath)
    #set MoldPlate_Fix attribute
    Studio.Click_Icon(StudioAppPath, "\\Studio_Import_icon.png", 0)
    Studio.ImportGeometry(MoldplatePath2, StudioAppPath)
    Studio.SetAttribute("MoldPlate_move","Geoemetry", StudioAppPath)
    #set MoldPlate_move attribute 
    
    Studio.Click_Icon(StudioAppPath, "\\Studio_Import_icon.png", 0)
    Studio.ImportGeometry(CoolingChannelPath, StudioAppPath)
    Studio.SetAttribute("CoolingChannel","Line", StudioAppPath)
    c = {'D':'8'}
    #set  cooling channel attribute
    Studio.Click_Icon(StudioAppPath, "\\Studio_MeltEntrance_Icon.png", 0)
    Studio.Inletoutlet_wizard(StudioAppPath)
   
    Studio.SwitchTab(StudioAppPath + "\\Studio_Tab_Mesh.png", StudioAppPath + "\\Studio_Tab_Meshing.png")
    
    part_seed_mesh={'Part':'5'} 
    Studio.Node_Seeding(StudioAppPath,**part_seed_mesh)
    runner_seed_mesh={'ColdRunner':'2'}
    Studio.Node_Seeding(StudioAppPath,**runner_seed_mesh)
    cc_seed_mesh={'Cooling_Channel':'5'} 
    Studio.Node_Seeding(StudioAppPath,**cc_seed_mesh)
    runner_seed_mesh={'MoldPlate_Move':'10','MoldPlate_Fix':'10'}
    Studio.Node_Seeding(StudioAppPath,**runner_seed_mesh)
  
    wait(3)
    click(StudioAppPath + r"\Studio_Generate.png")
    #if exists(StudioAppPath + r"\Btn_Yes.png", 3):
        #click(StudioAppPath + r"\Btn_Yes.png")
    Studio.Wait_Dialog(StudioAppPath, r"\Studio_Mesh_Process.png")
   
    Studio.Meshing_GenerateBLM("None", StudioAppPath)
    Studio.Wait_Dialog(StudioAppPath, "\\Studio_FinalCheck.png")
    Studio.Click_Icon(StudioAppPath, "\\Btn_Angle_Perspective_Seletected.png", 40)
    Studio.Click_Icon(StudioAppPath, "\\Btn_Fit_To_Window.png", -24)
    Studio.Click_Icon(StudioAppPath, "\\Btn_ShowModeSelected_FeatureShaded2.png", 40)
    
    if exists(StudioAppPath + r"\Studio_FinalCheck2.png"):
        click(StudioAppPath + r"\Studio_FinalCheck2.png")  
    if exists(Pattern(StudioAppPath + r"\Studio_setpartingdirection.png").similar(0.85), 10):
        click(StudioAppPath + r"\Btn_Check.png")
    i = 0
    
    while not exists(StudioAppPath + r"\Dialog_FInal_Check.png",30) and i <20:
        if exists(StudioAppPath + r"\Btn_Yes_2.png", 1):
            click(StudioAppPath + r"\Btn_Yes_2.png")
        i += 1
    
    if exists(StudioAppPath + r"\Btn_OK.png", 10):
        click(StudioAppPath + r"\Btn_OK.png") 
    Log.write_log(ProjectName, "Info: Studio Pre Process Setting is Finished")
    

    #Material Wizard Setting
    sMatlist =[MaterialAppPath + r"\MaterialABS_2023.png", MaterialAppPath + r"\MaterialASchulman_2023.png", MaterialAppPath + r"\MaterialRABS9000UV5_2023.png"]
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
    #Process Tab Cooling Setting
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_FillingPacking.png", ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath)  

    Process.Click_Icon(ProcessAppPath + r"\Btn_Setting.png", ProcessAppPath + r"\Pro_MoldPreheatSetting.png")
    Process.InsetValueSetting(ProcessAppPath, "\inset_temp", "50")
    Process.Click_Icon(ProcessAppPath + r"\Btn_ApplyCurrentSettingToAll.png", ProcessAppPath + r"\Pro_MoldPreheatSetting.png")
    Process.Click_Icon(ProcessAppPath + r"\Btn_OK.png", ProcessAppPath + r"\Pro_Tab_Cooling.png")
    Process.Click_Icon(ProcessAppPath + r"\Btn_CoolingHeating.png", ProcessAppPath + r"\Pro_CoolingAdvancedSetting.png")
    Process.InsetValueSetting(ProcessAppPath, "\inset_temp", "50")
    Process.Click_Icon(ProcessAppPath + r"\Btn_ApplyCurrentSettingToAll.png", ProcessAppPath + r"\Pro_Tab_Cooling.png")
    Process.Click_Icon(ProcessAppPath + r"\Btn_OK.png", ProcessAppPath + r"\Pro_Tab_Cooling.png")
    Process.Click_Icon(ProcessAppPath + r"\Btn_Mold_insert_initial_temperature.png", ProcessAppPath + r"\Pro_CoolingAdvancedSetting.png")
    Process.InsetValueSetting(ProcessAppPath, "\mold_insert_initial_temp", "50")
    Process.Click_Icon(ProcessAppPath + r"\Btn_OK.png", ProcessAppPath + r"\Pro_Tab_Cooling.png")
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath + "\\Pro_Tab_Summary.png", ProcessAppPath)
    Process.ProcessWizard_Summary_Finish(ProcessAppPath)
    Log.write_log(ProjectName, "Info: Process Wizard Setting is Finished")

    #Analyze Setting
    
    Analyzelist = [StudioAppPath + "\\Analysis_CFPCtW.png", StudioAppPath + "\\Analysis_CoolingCycle2.png", StudioAppPath + "\\Analysis_Filling_2.png", StudioAppPath + "\\Analysis_Packing2.png", StudioAppPath + "\\Analysis_CoolingTransient_2.png", StudioAppPath + "\\Analysis_Warpage.png"]
    Studio.AnalysisSetting(Analyzelist, StudioAppPath)
    Log.write_log(ProjectName, "Info: Analyze Setting is Finished")
    #Computation Parameter Wizard Setting
    #CMX Tab Flow/Pack Setting
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\ComputationLogo_2023.png")

    #CMX Tab Cool Setting
    CMX.CMX_Tab_Change(CMXAppPath + "\\CMX_Tab_Cool.png")
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\CMX_Btn_OK.png")
    Log.write_log(ProjectName, "Info: Computation Parameter Wizard Setting is Finished")
    
    
    wait(1)
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

    #Process Wizard Setting
    Process.Home_Process("New", ProcessAppPath)
    Process.ProcessWizard_Project_SettingMethod("CAE", ProcessAppPath) 
    #Process Tab Filling/Packing Setting
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_ProjectSetting.png", ProcessAppPath + "\\Pro_Tab_FillingPacking.png", ProcessAppPath)
    #Process Tab Cooling Setting
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_FillingPacking.png", ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath)  

    Process.Click_Icon(ProcessAppPath + r"\Btn_Setting.png", ProcessAppPath + r"\Pro_MoldPreheatSetting.png")
    Process.InsetValueSetting(ProcessAppPath, "\inset_temp", "50")
    Process.Click_Icon(ProcessAppPath + r"\Btn_ApplyCurrentSettingToAll.png", ProcessAppPath + r"\Pro_MoldPreheatSetting.png")
    Process.Click_Icon(ProcessAppPath + r"\Btn_OK.png", ProcessAppPath + r"\Pro_Tab_Cooling.png")
    Process.Click_Icon(ProcessAppPath + r"\Btn_CoolingHeating.png", ProcessAppPath + r"\Pro_CoolingAdvancedSetting.png")
    Process.InsetValueSetting(ProcessAppPath, "\inset_temp", "50")
    Process.Click_Icon(ProcessAppPath + r"\Btn_ApplyCurrentSettingToAll.png", ProcessAppPath + r"\Pro_Tab_Cooling.png")
    Process.Click_Icon(ProcessAppPath + r"\Btn_OK.png", ProcessAppPath + r"\Pro_Tab_Cooling.png")
    Process.Click_Icon(ProcessAppPath + r"\Btn_Mold_insert_initial_temperature.png", ProcessAppPath + r"\Pro_CoolingAdvancedSetting.png")
    Process.InsetValueSetting(ProcessAppPath, "\mold_insert_initial_temp", "50")
    Process.Click_Icon(ProcessAppPath + r"\Btn_OK.png", ProcessAppPath + r"\Pro_Tab_Cooling.png")
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath + "\\Pro_Tab_Summary.png", ProcessAppPath)
    Process.ProcessWizard_Summary_Finish(ProcessAppPath)
    Log.write_log(ProjectName, "Info: Process Wizard Setting is Finished")

    #Computation Parameter Wizard Setting
    #CMX Tab Flow/Pack Setting
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\ComputationLogo_2023.png")

    #CMX Tab Cool Setting
    CMX.CMX_Tab_Change(CMXAppPath + "\\CMX_Tab_Cool.png")
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\CMX_Btn_OK.png")
    Log.write_log(ProjectName, "Info: Computation Parameter Wizard Setting is Finished")
    
    #New Project
    click(StudioAppPath+r"\Studio_NewRun2.png")
    Log.write_log(ProjectName, "Info: New Project Setting is Finished")
    #Studio Pre Process Setting
    Studio.MeshType("Solid", StudioAppPath)
    Studio.Home_MoldingType(0, -105, StudioAppPath)
    Studio.Home_Model("ImportGeometry", StudioAppPath)
    Studio.ImportGeometry(IMDSourcePath, StudioAppPath)
   
    Studio.SwitchTab(StudioAppPath + r"\Studio_Tab_Mesh.png", StudioAppPath + r"\Studio_Tab_Meshing.png")
    Studio.Meshing_Generate(StudioAppPath)
    Studio.Meshing_GenerateBLM("None", StudioAppPath)
    Studio.Wait_Dialog(StudioAppPath, r"\Studio_FinalCheck.png")
    Studio.Click_Icon(StudioAppPath, "\\Studio_Model_tree3.png",0)
    Studio.Click_Icon(StudioAppPath, "\\Studio_Tree_Cooling_Channel.png",-65)
    Studio.Click_Icon(StudioAppPath, "\\Studio_Tree_Moldbase.png",-60)
   
    Studio.SwitchTab(StudioAppPath + r"\BC_tab.png", StudioAppPath + r"\Studio_Tab_B.C_Selected.png")
    Studio.SetView("Top",StudioAppPath)
    Studio.Click_Icon(StudioAppPath, "\\Fit_to_Window.png",0)
    Studio.Click_Icon(StudioAppPath, "\\Btn_ShowModeSelected_FeatureShaded2.png", 40)
    a=['45']
    Studio.SetIMD('0.3', Pattern(StudioAppPath + r"\Studio_S9_model.png").similar(0.90),StudioAppPath,*a)
    Studio.SwitchTab(StudioAppPath + r"\Studio_Tab_Mesh.png", StudioAppPath + r"\Studio_Tab_Meshing.png")
    Studio.Final_Check(StudioAppPath)
    Log.write_log(ProjectName, "Info: Studio Pre Process Setting is Finished")
    
    #Material Wizard Setting
    sMatlist = [MaterialAppPath + r"\MaterialPC+ABS_2023.png", MaterialAppPath + r"\MaterialSABIC.png",  MaterialAppPath + r"\Mateiral_CYCOLOY_C1200HF.png"]
    Material.OpenMaterialWizard(MaterialAppPath + "\\Studio_EM1.png", 200, 0, MaterialAppPath)
    Material.ClickMDXBank(MaterialAppPath)
    Material.SelectPartMaterial(sMatlist)
    Material.MaterialNotAddToUserBank(MaterialAppPath)
    Material.CloseMaterialWizard(MaterialAppPath)
    Log.write_log(ProjectName, "Info: Material Wizard Setting is Finished")

    sMatlist = [MaterialAppPath + r"\MaterialPC.png", MaterialAppPath + r"\MaterialSABIC.png",  MaterialAppPath + r"\CYCOLOY_EFX810ME.png"]
    Material.OpenMaterialWizard(MaterialAppPath + "\\Studio_IMD.png", 200, 0, MaterialAppPath)
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
    #Process Tab Cooling Setting
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_FillingPacking.png", ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath)  

    Process.Click_Icon(ProcessAppPath + r"\Btn_Setting.png", ProcessAppPath + r"\Pro_MoldPreheatSetting.png")
    Process.InsetValueSetting(ProcessAppPath, "\inset_temp", "80")
    Process.Click_Icon(ProcessAppPath + r"\Btn_ApplyCurrentSettingToAll.png", ProcessAppPath + r"\Pro_MoldPreheatSetting.png")
    Process.Click_Icon(ProcessAppPath + r"\Btn_OK.png", ProcessAppPath + r"\Pro_Tab_Cooling.png")
    Process.Click_Icon(ProcessAppPath + r"\Btn_CoolingHeating.png", ProcessAppPath + r"\Pro_CoolingAdvancedSetting.png")
    Process.InsetValueSetting(ProcessAppPath, "\inset_temp", "80")
    Process.Click_Icon(ProcessAppPath + r"\Btn_ApplyCurrentSettingToAll.png", ProcessAppPath + r"\Pro_Tab_Cooling.png")
    Process.Click_Icon(ProcessAppPath + r"\Btn_OK.png", ProcessAppPath + r"\Pro_Tab_Cooling.png")
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath + "\\Pro_Tab_Summary.png", ProcessAppPath)
    Process.ProcessWizard_Summary_Finish(ProcessAppPath)
    Log.write_log(ProjectName, "Info: Process Wizard Setting is Finished")
   
    #Analyze Setting    
    Analyzelist = [StudioAppPath + "\\Analysis_CFPCtW.png", StudioAppPath + "\\Analysis_CoolingCycle2.png", StudioAppPath + "\\Analysis_Filling_2.png", StudioAppPath + "\\Analysis_Packing2.png", StudioAppPath + "\\Analysis_CoolingTransient_2.png", StudioAppPath + "\\Analysis_Warpage.png"]
    Studio.AnalysisSetting(Analyzelist, StudioAppPath)
    Log.write_log(ProjectName, "Info: Analyze Setting is Finished")
    #Computation Parameter Wizard Setting
    #CMX Tab Flow/Pack Setting
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\ComputationLogo_2023.png")

    #CMX Tab Cool Setting
    CMX.CMX_Tab_Change(CMXAppPath + "\\CMX_Tab_Cool.png")
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\CMX_Cooling_AccurancyLevel_Standard.png")
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\CMX_Btn_OK.png")
    Log.write_log(ProjectName, "Info: Computation Parameter Wizard Setting is Finished")
    #Change Remark Name
    Studio.Click_Icon(StudioAppPath, r"\Studio_Tree_Run.png", 0)
    wait(1)
    Remark_name = ["SC(MP)","FC(MP)","IMD"]
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
