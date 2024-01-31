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
Copypath=ArgS.Copypath

ProjectName = "IM-S5-P1"
username = "moldex3dqa"
password = "123456"
SVNPath = r"svn://192.168.3.4/QARepository/AutoTest/Moldex3D/2023Series/Moldex3D/CaseReference/ENT/" + ProjectName + r"/Geometry"
localpath = os.path.normpath((cwd + r"\\" +ProjectName))

MainInstallPath ,ver = Common.getregkeyvalue(r"HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\CoreTechSystem\MDX_ParallelComputing", "INSTALLDIR")
WorkingFolder = Common.getregkeyvalue(r"HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\CoreTechSystem\MDX_ParallelComputing", "WorkingFolder")
StudioPath = MainInstallPath + r"\Bin\MDXStudio.exe"
CaseReferncePath = Common.gototargetpath('MDX_ENT') + "\\" + ProjectName
PartPath = CaseReferncePath + r"\Part.stp"
MoldInsertPath = CaseReferncePath + r"\MoldInsert.stp"
RunnerPath1 = CaseReferncePath + r"\hotrunner1.igs"
RunnerPath2 = CaseReferncePath + r"\hotrunner2.igs"
RunnerPath3 = CaseReferncePath + r"\hotrunner3.igs"
HotRunnerMetalPath = CaseReferncePath + r"\HotRunner_Metal.stp"
CoolingchannelPath = CaseReferncePath + r"\coolingchannel.igs"
MoldbasePath = CaseReferncePath + r"\MoldBase.stp"
HeatingrodPath = CaseReferncePath + r"\Heating_Rod.stp"
CMPath = MainInstallPath + r'\Bin\MDXComputingManager' + ver + r'.exe'
SourcePath = CaseReferncePath + r"\AHR-FC.mdg"
SourcePath2 = CaseReferncePath + r"\AHR-eDn.mdg"
hostname, local_ip = Common.getcuriphostname()


try:
   
    #svn execution
    Common.SVNLogin(username, password)
    Common.SVNDownload(SVNPath, localpath)
    #Open Studio UI 
    
    Studio.OpenApp(StudioPath, StudioAppPath + "\\Studio_UI.png")
    Log.write_log(ProjectName, "Info: Open Studio is Finished")
    #New Project
    Studio.NewProject("ENT-IM-S5-P1", StudioAppPath)
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
    Studio.ImportGeometry(RunnerPath2, StudioAppPath)
    #Studio.Click_Icon(StudioAppPath, "\\Studio_Tree_Model.png",0)
    r0 = {'Type':'Circular','D1red':'3','D1green':'10'}
    Studio.SetAttribute("HotRunner","Line", StudioAppPath,**r0) 
    Studio.Click_Icon(StudioAppPath, "\\Studio_Import_icon.png", 0)
    Studio.ImportGeometry(RunnerPath1, StudioAppPath)
    r1 = {'Type':'Circular','D1red':'10','D1green':'10',}
    Studio.SetAttribute("HotRunner","Line", StudioAppPath,**r1)
    Studio.Click_Icon(StudioAppPath, "\\Studio_Import_icon.png", 0)
    Studio.ImportGeometry(RunnerPath3, StudioAppPath)
    r_2 = {'Type':'Circular','D1red':'3','D1green':'3'}
    Studio.SetAttribute("HotRunner","Line", StudioAppPath,**r_2)
    
    #set runner attribute
    Studio.Click_Icon(StudioAppPath, "\\Studio_Import_icon.png", 0)
    Studio.ImportGeometry(HeatingrodPath, StudioAppPath)
    Studio.SetAttribute("Heatingrod","Geometry", StudioAppPath)
    #set heating rod attribute
    Studio.Click_Icon(StudioAppPath, "\\Studio_Import_icon.png", 0)
    Studio.ImportGeometry(HotRunnerMetalPath, StudioAppPath)
    Studio.SetAttribute("HotRunnerMetal","Geoemetry", StudioAppPath)
    #set hot runner metal attribute
    Studio.Click_Icon(StudioAppPath, "\\Studio_Import_icon.png", 0)
    Studio.ImportGeometry(MoldInsertPath, StudioAppPath)
    Studio.SetAttribute("Moldinsert","Geoemetry", StudioAppPath)
    #set moldinsert attribute 
    
    Studio.Click_Icon(StudioAppPath, "\\Studio_Import_icon.png", 0)
    Studio.ImportGeometry(MoldbasePath, StudioAppPath)
    Studio.SetAttribute("Moldbase","Geoemetry", StudioAppPath)
    #set moldbase attribute 
    Studio.Click_Icon(StudioAppPath, "\\Studio_Import_icon.png", 0)
    Studio.ImportGeometry(CoolingchannelPath, StudioAppPath)
    c = {'D':'8'}
    Studio.SetAttribute("Coolingchannel","Line", StudioAppPath,**c)
    #set cooling channel attribute 
    Studio.Click_Icon(StudioAppPath, "\\Studio_MeltEntrance_Icon.png", 0)
    Studio.Inletoutlet_wizard(StudioAppPath)
    Studio.Click_Icon(StudioAppPath, "\\Studio_Tree_Cooling_Channel.png", -80)
    #add melt entrance
    Studio.SwitchTab(StudioAppPath + "\\Studio_Tab_Mesh.png", StudioAppPath + "\\Studio_Tab_Meshing.png")
   
    partmesh={'Part':'5'}
    moldinsertmesh={'Moldinsert':'5'}
    hotrunnermetalmesh={'HotRunnerMetal':'3'}
    heatingrodmesh={'HeatingRod':'2'}
    Studio.Node_Seeding(StudioAppPath,**heatingrodmesh)
    Studio.Node_Seeding(StudioAppPath,**hotrunnermetalmesh)
    Studio.Node_Seeding(StudioAppPath,**partmesh)
    Studio.Node_Seeding(StudioAppPath,**moldinsertmesh)
   
    
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
    Process.Click_Icon(ProcessAppPath + r"\Btn_MoldMetalMaterial.png", ProcessAppPath + r"\Pro_CoolingAdvancedSetting.png")
    Process.SelectMoldMetalMaterial(ProcessAppPath + r"\Pro_Cooling_Hot_Runner_Metal_1.png", 280, 0, ProcessAppPath + r"\Pro_MaterialAir.png")
    Process.Click_Icon(ProcessAppPath + r"\Btn_OK.png", ProcessAppPath + r"\Pro_Tab_Cooling.png")
    #Process Tab Summary
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath + "\\Pro_Tab_Summary.png", ProcessAppPath)
    Process.ProcessWizard_Summary_Finish(ProcessAppPath)
    Log.write_log(ProjectName, "Info: Process Wizard Setting is Finished")
    #Analyze Setting
    Analyzelist = [StudioAppPath + "\\Analysis_CtFPCtW.png", StudioAppPath + "\\Analysis_CoolingTransient.png", StudioAppPath + "\\Analysis_Filling.png", StudioAppPath + "\\Analysis_Packing2.png", StudioAppPath + "\\Analysis_CoolingTransient.png", StudioAppPath + "\\Analysis_Warpage.png"]
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
    click(StudioAppPath+r"\Studio_NewRun2.png")
    #new run  FC
    Studio.MeshType("Solid", StudioAppPath)
    Studio.Home_MoldingType(0, -105, StudioAppPath)
    Studio.Click_Icon(StudioAppPath, "\\Studio_Import_icon.png", 0)
    wait(2)
    Studio.ImportGeometry(PartPath, StudioAppPath)
    Studio.Click_Icon(StudioAppPath, "\\Studio_Tree_Model.png",0)
    Studio.SetAttribute("Part","Geoemetry", StudioAppPath)
    #set part attribute
    Studio.Click_Icon(StudioAppPath, "\\Studio_Import_icon.png", 0)
    Studio.ImportGeometry(RunnerPath2, StudioAppPath)
    #Studio.Click_Icon(StudioAppPath, "\\Studio_Tree_Model.png",0)
    r0 = {'Type':'Circular','D1red':'3','D1green':'10'}
    Studio.SetAttribute("HotRunner","Line", StudioAppPath,**r0) 
    Studio.Click_Icon(StudioAppPath, "\\Studio_Import_icon.png", 0)
    Studio.ImportGeometry(RunnerPath1, StudioAppPath)
    r1 = {'Type':'Circular','D1red':'10','D1green':'10',}
    Studio.SetAttribute("HotRunner","Line", StudioAppPath,**r1)
    Studio.Click_Icon(StudioAppPath, "\\Studio_Import_icon.png", 0)
    Studio.ImportGeometry(RunnerPath3, StudioAppPath)
    r_2 = {'Type':'Circular','D1red':'3','D1green':'3'}
    Studio.SetAttribute("HotRunner","Line", StudioAppPath,**r_2)
    #set runner attribute
    Studio.Click_Icon(StudioAppPath, "\\Studio_Import_icon.png", 0)
    Studio.ImportGeometry(HeatingrodPath, StudioAppPath)
    Studio.SetAttribute("Heatingrod","Geometry", StudioAppPath)
    Studio.Click_Icon(StudioAppPath, "\\Studio_Tree_Model_Object.png", -38)
    
    #set heating rod attribute
    Studio.Click_Icon(StudioAppPath, "\\Studio_Import_icon.png", 0)
    Studio.ImportGeometry(HotRunnerMetalPath, StudioAppPath)
    Studio.SetView("Bottom",StudioAppPath)
    Studio.Click_Icon(StudioAppPath, "\\Fit_to_Window.png",0)
    r0 = {'HCF': StudioAppPath + r"\HCF1.png"}
    Studio.SetAttribute("HotRunnerMetal","Geoemetry", StudioAppPath,**r0)
    Studio.SwitchTab(StudioAppPath + r"\BC_tab.png", StudioAppPath + r"\Studio_Tab_B.C_Selected.png")
    Studio.SetHeatConduction(StudioAppPath + r"\HCF2.png",StudioAppPath + r"\Studio_HotRunnerHeatBC.png",StudioAppPath)
    #set hot runner metal attribute
    Studio.SwitchTab(StudioAppPath + r"\Tab_home_blue.png", StudioAppPath + r"\Tab_home_white.png")
    wait(2)
    Studio.Click_Icon(StudioAppPath, "\\Studio_Import_icon.png", 0)
    Studio.ImportGeometry(MoldbasePath, StudioAppPath)
    Studio.SetAttribute("Moldbase","Geoemetry", StudioAppPath)
    #set moldbase attribute 
    Studio.Click_Icon(StudioAppPath, "\\Studio_Import_icon.png", 0)
    Studio.ImportGeometry(CoolingchannelPath, StudioAppPath)
    c = {'D':'8'}
    Studio.SetAttribute("Coolingchannel","Line", StudioAppPath,**c)
    #set cooling channel attribute 
    Studio.Click_Icon(StudioAppPath, "\\Studio_MeltEntrance_Icon.png", 0)
    Studio.Inletoutlet_wizard(StudioAppPath)
    Studio.Click_Icon(StudioAppPath, "\\Studio_Tree_Cooling_Channel.png", -80)
    #add melt entrance
    
    Studio.SwitchTab(StudioAppPath + "\\Studio_Tab_Mesh.png", StudioAppPath + "\\Studio_Tab_Meshing.png")
    Studio.Click_Icon(StudioAppPath, "\\Studio_Tree_Model_Object.png", -38)
    Studio.Click_Icon(StudioAppPath, "\\Studio_Tree_Model_Object.png", -38)
    click(StudioAppPath + r"\Studio_logo.png")
    partmesh={'Part':'5'}
    hotrunnermetalmesh={'HotRunnerMetal':'3'}
    heatingrodmesh={'HeatingRod':'2'}
    Studio.Node_Seeding(StudioAppPath,**heatingrodmesh)
    Studio.Node_Seeding(StudioAppPath,**hotrunnermetalmesh)
    Studio.Node_Seeding(StudioAppPath,**partmesh)
   

    wait(3)
    
    click(StudioAppPath + r"\Studio_Generate.png")
    if exists(StudioAppPath + r"\Btn_Yes.png", 5):
        click(StudioAppPath + r"\Btn_Yes.png")
    Studio.Wait_Dialog(StudioAppPath, r"\Studio_Mesh_Process.png")
    Studio.Meshing_GenerateBLM("Runner", StudioAppPath)
   
    Studio.Click_Icon(StudioAppPath, "\\Btn_Fit_To_Window.png", -24)
    Studio.Click_Icon(StudioAppPath, "\\Btn_ShowModeSelected_FeatureShaded2.png", 40)
    if exists(StudioAppPath + r"\Studio_FinalCheck2.png"):
        click(StudioAppPath + r"\Studio_FinalCheck2.png")  
    if exists(Pattern(StudioAppPath + r"\Studio_setpartingdirection.png").similar(0.85), 10):
        click(StudioAppPath + r"\Btn_Check.png")
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
    #Process Tab Summary
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath + "\\Pro_Tab_Summary.png", ProcessAppPath)
    Process.ProcessWizard_Summary_Finish(ProcessAppPath)
    Log.write_log(ProjectName, "Info: Process Wizard Setting is Finished")
    #Analyze Setting
    Analyzelist = [StudioAppPath + "\\Analysis_CtFPCtW.png", StudioAppPath + "\\Analysis_CoolingTransient.png", StudioAppPath + "\\Analysis_Filling.png", StudioAppPath + "\\Analysis_Packing2.png", StudioAppPath + "\\Analysis_CoolingTransient.png", StudioAppPath + "\\Analysis_Warpage.png"]
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
    #copy run to edesign
    Studio.Click_Icon(StudioAppPath, "\\Studio_Tree_Run.png", 0)
    CRfM.Copy_Run(Pattern(Copypath + "\\Run02.png").similar(0.92), "RunInputDataOnly", "None", "default", Copypath)
    Studio.MeshType("eDesign", StudioAppPath)
   
    Studio.SwitchTab(StudioAppPath +"\\Studio_Tab_Mesh.png", StudioAppPath + "\\Studio_Tab_Meshing.png")
    Studio.Meshing_Generate(StudioAppPath)
    Studio.Meshing_GenerateeDesign(StudioAppPath)
    Studio.Wait_Dialog(StudioAppPath, "\\Log_Generate_Solid_Mesh_Done.png")
    Studio.Final_Check(StudioAppPath)
    #Process Wizard Setting
    Process.Home_Process("New", ProcessAppPath)
    Process.ProcessWizard_Project_SettingMethod("CAE", ProcessAppPath) 
    #Process Tab Filling/Packing Setting
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_ProjectSetting.png", ProcessAppPath + "\\Pro_Tab_FillingPacking.png", ProcessAppPath)
    #Process Tab Cooling Setting
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_FillingPacking.png", ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath)  
    #Process Tab Summary
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath + "\\Pro_Tab_Summary.png", ProcessAppPath)
    Process.ProcessWizard_Summary_Finish(ProcessAppPath)
    Log.write_log(ProjectName, "Info: Process Wizard Setting is Finished")
    #Analyze Setting
    Analyzelist = [StudioAppPath + "\\Analysis_CtFPCtW.png", StudioAppPath + "\\Analysis_CoolingTransient.png", StudioAppPath + "\\Analysis_Filling.png", StudioAppPath + "\\Analysis_Packing2.png", StudioAppPath + "\\Analysis_CoolingTransient.png", StudioAppPath + "\\Analysis_Warpage.png"]
    Studio.AnalysisSetting(Analyzelist, StudioAppPath)
    Log.write_log(ProjectName, "Info: Analyze Setting is Finished")
    #Computation Parameter Wizard Setting
    #CMX Tab Flow/Pack Setting
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\ComputationLogo_2023.png")
    #CMX Tab Cool Setting
    CMX.CMX_Tab_Change(CMXAppPath + "\\CMX_Tab_Cool.png")
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\CMX_Btn_OK.png")
    Log.write_log(ProjectName, "Info: Computation Parameter Wizard Setting is Finished")
    
     #Change Remark Name
    Studio.Click_Icon(StudioAppPath, r"\Studio_Tree_Run.png", 0)
    wait(1)
    Remark_name = ["SC","FC","eDesign"]
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
    Log.write_log(ProjectName, "Info: Computing Manager Add Server Setting is Finished")
    wait(1)
    Studio.ClickRun(30, StudioAppPath)
    Studio.Submit_Batch_Run(2,StudioAppPath)
    wait(2)
      
    #Close Studio UI
    Studio.CloseApp(StudioPath)  
    print (ProjectName+" Test is Finished!")
    Log.write_log(ProjectName, "Info: STR Test is Finished!")
    
except:
    os.popen(("python {}").format(exceptprocedureApp))
    print(ProjectName+" Test is Failed!")
    Log.write_log(ProjectName,"Error: %s Test is Failed!" % ProjectName)
Log.write_log2(ProjectName, "Summary")
   