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

ProjectName = "IM-S3-P1"
username = "moldex3dqa"
password = "123456"
SVNPath = r"svn://192.168.3.4/QARepository/AutoTest/Moldex3D/2023Series/Moldex3D/CaseReference/ENT/" + ProjectName + r"/Geometry"
Filename= SVNPath.split('/')[-2]
localpath = os.path.normpath((cwd + r"\\" +Filename))

MainInstallPath ,ver = Common.getregkeyvalue(r"HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\CoreTechSystem\MDX_ParallelComputing", "INSTALLDIR")
WorkingFolder = Common.getregkeyvalue(r"HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\CoreTechSystem\MDX_ParallelComputing", "WorkingFolder")
StudioPath = MainInstallPath + r"\Bin\MDXStudio.exe"
CaseReferncePath = Common.gototargetpath('MDX_ENT') + "\\" + ProjectName
PartPath = CaseReferncePath + r"\Part.stp"
RunnerPath = CaseReferncePath + r"\Runner.stp"
CoolingChannelPath = CaseReferncePath + r"\Cooling_Channel.stp"
MoldbasePath = CaseReferncePath + r"\Moldbase.stp"
CompressionzonePath = CaseReferncePath + r"\CompressionZone.stl"
ChargePath = CaseReferncePath + r"\charge.stp"
CMPath = MainInstallPath + r"\Bin\MDXComputingManager" + ver + ".exe"
hostname, local_ip = Common.getcuriphostname()


try:
    #svn execution
    Common.SVNLogin(username, password)   
    Common.SVNDownload(SVNPath, localpath)
    print ("Info: SVN download is Finished")
    Log.write_log("Pre_Setting", "Info: SVN download is Finished")
    
    Studio.OpenApp(StudioPath, StudioAppPath + "\\Studio_UI.png")
    Log.write_log(ProjectName, "Info: Open Studio is Finished")
    #New Project
    Studio.NewProject(ProjectName, StudioAppPath)
    Log.write_log(ProjectName, "Info: New Project Setting is Finished")

    #Studio Pre Process Setting
    Studio.MeshType("Solid", StudioAppPath)
    Studio.Home_MoldingType(0, -105, StudioAppPath)
    Studio.Click_Icon(StudioAppPath, "\\Studio_Tree_Model.png",0)
   
    Studio.Click_Icon(StudioAppPath, "\\Studio_Import_icon.png", 0)
    Studio.ImportGeometry(RunnerPath, StudioAppPath)
    
    Studio.SetAttribute("ColdRunner","Geoemetry", StudioAppPath)
    
    Studio.Click_Icon(StudioAppPath, "\\Studio_Import_icon.png", 0)
    Studio.ImportGeometry(PartPath, StudioAppPath)
    Studio.SetAttribute("Part","Geoemetry", StudioAppPath)
    #set part attribute
    Studio.Click_Icon(StudioAppPath, "\\Studio_Import_icon.png", 0)
    Studio.ImportGeometry(CoolingChannelPath, StudioAppPath)
    cc = {'D':'8'}
    Studio.SetAttribute("Coolingchannel","Line", StudioAppPath,**cc)
    
    Studio.Click_Icon(StudioAppPath, "\\Studio_Import_icon.png", 0)
    Studio.ImportGeometry(MoldbasePath, StudioAppPath)
    Studio.SetAttribute("Moldbase","Geoemetry", StudioAppPath)
    
    wait(2)
    #set moldbase attribute 
    Studio.Click_Icon(StudioAppPath, "\\Studio_MeltEntrance_Icon.png", 0)
    
    #add melt entrance
    Studio.Inletoutlet_wizard(StudioAppPath)
    
    Studio.SwitchTab(StudioAppPath + "\\Studio_Tab_Mesh.png", StudioAppPath + "\\Studio_Tab_Meshing.png")
    partmesh={'Part':'0.8'}
    Coldrunnermesh={'ColdRunner':'0.8'}
    Studio.Node_Seeding(StudioAppPath,**partmesh)
    Studio.Node_Seeding(StudioAppPath,**Coldrunnermesh)
    wait(3)
    Studio.Meshing_Generate(StudioAppPath)
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
        if exists(StudioAppPath + r"\Btn_Yes.png", 1):
            click(StudioAppPath + r"\Btn_Yes.png")
        i += 1
    if exists(StudioAppPath + r"\Btn_OK.png", 10):
        click(StudioAppPath + r"\Btn_OK.png") 
    Log.write_log(ProjectName, "Info: Studio Pre Process Setting is Finished")

    #Material Wizard Setting
    sMatlist = [MaterialAppPath + r"\MaterialPC_2023.png", MaterialAppPath + r"\MaterialCAE_2023.png", MaterialAppPath + r"\MaterialYung_SU_CGF003_2023.png"]
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
    Analyzelist = [StudioAppPath + "\\Analysis_CtFPCtWO.png", StudioAppPath + "\\Analysis_CoolingTransient_2.png", StudioAppPath + "\\Analysis_Filling.png", StudioAppPath + "\\Analysis_Packing2.png", StudioAppPath + "\\Analysis_CoolingTransient_2.png", StudioAppPath + "\\Analysis_Warpage.png",StudioAppPath + "\\Analysis_Optics2.png"]
    Studio.AnalysisSetting(Analyzelist, StudioAppPath)
    Log.write_log(ProjectName, "Info: Analyze Setting is Finished")
    #Computation Parameter Wizard Setting
    #CMX Tab Flow/Pack Setting
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\ComputationLogo_2023.png")
    CMX.FPSolverTypeChange(CMXAppPath + "\\CMX_Flow_Solver.png", "Enhanced")
    CMX.Checkbox(CMXAppPath + "\\CMX_Flow_PredictGateFreezeTime.png", -100, 0, CMXAppPath)
    CMX.Checkbox(CMXAppPath + "\\CMX_Flow_ExtenPackingCalculationToCoolingPhase.png", -120, 0, CMXAppPath)
    CMX.Checkbox(CMXAppPath + "\\CMX_Flow_UseSolidStatePropertiesForShrinkage.png", -105, 0, CMXAppPath)
    #CMX Tab Cool Setting
    CMX.CMX_Tab_Change(CMXAppPath + "\\CMX_Tab_Cool.png")
    #CMX Tab VE/Optics Setting
    CMX.CMX_Tab_Change(CMXAppPath + "\\CMX_Tab_VEOptics.png")
    CMX.Checkbox(CMXAppPath + "\\CMX_VEOptics_EstimateFillingPackingStage.png", -90, 0, CMXAppPath)
    CMX.Checkbox(CMXAppPath + "\\CMX_VEOptics_EstimateCoolingStage.png", -73, 0, CMXAppPath)
    CMX.Checkbox(CMXAppPath + "\\CMX_VEOptics_EstimateOpticsProperties.png", -73, 0, CMXAppPath)
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\CMX_Btn_Add.png")
    CMX.ValueSetting(CMXAppPath + "\\CMX_Direction_X.png", 0, 20, "0.00")
    CMX.ValueSetting(CMXAppPath + "\\CMX_Direction_Y.png", 0, 20, "-1.00")
    CMX.ValueSetting(CMXAppPath + "\\CMX_Direction_Z.png", 0, 20, "0.00")
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\CMX_Btn_OK.png")
    Log.write_log(ProjectName, "Info: Computation Parameter Wizard Setting is Finished")
    wait(1)
    
    Studio.Click_Icon(StudioAppPath, "\\Studio_Tree_Run.png", 0)
    CRfM.Copy_Run(Pattern(Copypath + "\\Run01.png").similar(0.92), "RunInputDataOnly", "None", "default", Copypath)
    Log.write_log(ProjectName, "Info: Copy IM to ICM  is Finished")
    #copy run to ICM
    Studio.MeshType("eDesign", StudioAppPath)
    Studio.MeshType("Solid", StudioAppPath)
    Studio.Home_MoldingType(0, -30, StudioAppPath)
    Studio.Click_Icon(StudioAppPath, "\\Studio_Tree_Model.png",0)
    Studio.Click_Icon(StudioAppPath, "\\Studio_Model_Tree.png", -95)
    Studio.Click_Icon(StudioAppPath, "\\Studio_Tree_Model_part_unselected.png", -20)
    Studio.Click_Icon(StudioAppPath, "\\Studio_Tree_Model_ColdRunner_unselected.png", -45)
    
    Studio.Click_Icon(StudioAppPath, "\\Studio_Import_icon.png", 0)
    Studio.ImportGeometry(CompressionzonePath, StudioAppPath)
    
    
    Studio.SetAttribute("Compressionzone","Geometry", StudioAppPath)
    wait(1)
    Studio.SetView("Perspective",StudioAppPath)
    Studio.Click_Icon(StudioAppPath, "\\Btn_Fit_To_Window.png", -24)
    Studio.SwitchTab(StudioAppPath +"\\Studio_Tab_B.C_NonSelected.png", StudioAppPath + "\\Studio_Tab_B.C_Selected.png")
    Studio.SetMovingSurface(StudioAppPath + r"\Studio_OPT_SET_BC.png","0,1,0",StudioAppPath)
    
    Studio.SwitchTab(StudioAppPath +"\\Studio_Tab_Mesh.png", StudioAppPath + "\\Studio_Tab_Meshing.png")
    Studio.SetMeshParameter('Hybrid','CompressionZone','BLM',StudioAppPath)
    wait(1)
    
    Studio.Node_Seeding(StudioAppPath)
    wait(1)
    Studio.Meshing_Generate(StudioAppPath)
    Studio.Meshing_GenerateBLM("None", StudioAppPath)
    Studio.Wait_Dialog(StudioAppPath, "\\Studio_FinalCheck.png")
    Studio.Click_Icon(StudioAppPath, "\\Btn_Angle_Perspective_Seletected.png", 40)
    Studio.Click_Icon(StudioAppPath, "\\Btn_Fit_To_Window.png", -24)
    Studio.Click_Icon(StudioAppPath, "\\Btn_ShowModeSelected_FeatureShaded2.png", 40)
    Studio.Final_Check(StudioAppPath)
    wait(3)
    #Process Wizard Setting
    Process.Home_Process("New", ProcessAppPath)
    Process.ProcessWizard_Project_SettingMethod("CAE", ProcessAppPath) 
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_ProjectSetting.png", ProcessAppPath + "\\Pro_Tab_FillingPacking.png", ProcessAppPath)
   
    #Process Tab Compression Setting
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_FillingPacking.png", ProcessAppPath + "\\Pro_Tab_Compression.png", ProcessAppPath)  
    #Process Tab Compression Setting
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_Compression.png", ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath)  
    #Process Tab Summary
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath + "\\Pro_Tab_Summary.png", ProcessAppPath)
    Process.ProcessWizard_Summary_Finish(ProcessAppPath)
    Log.write_log(ProjectName, "Info: Process Wizard Setting is Finished")
   
    wait(2)
      
    
    #Analyze Setting
    Analyzelist = [StudioAppPath + "\\Analysis_CtFPCtWO.png", StudioAppPath + "\\Analysis_CoolingTransient_2.png", StudioAppPath + "\\Analysis_FillingAndPacking_2.png", StudioAppPath + "\\Analysis_CoolingTransient_2.png", StudioAppPath + "\\Analysis_Warpage.png", StudioAppPath + "\\Analysis_Optics2.png"]
    Studio.AnalysisSetting(Analyzelist, StudioAppPath)
    Log.write_log(ProjectName, "Info: Analyze Setting is Finished")
    
    wait(3)
    #Computation Parameter Wizard Setting
    #CMX Tab VE/Optics Setting
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\ComputationLogo_2023.png")
    CMX.CMX_Tab_Change(CMXAppPath + "\\CMX_Tab_VEOptics.png")
    CMX.Checkbox(CMXAppPath + "\\CMX_VEOptics_EstimateFillingPackingStage.png", -90, 0, CMXAppPath)
    CMX.Checkbox(CMXAppPath + "\\CMX_VEOptics_EstimateCoolingStage.png", -73, 0, CMXAppPath)
    CMX.Checkbox(CMXAppPath + "\\CMX_VEOptics_EstimateOpticsProperties.png", -73, 0, CMXAppPath)
    CMX.ValueSetting(CMXAppPath + "\\CMX_Direction_X.png", 0, 20, "0.00")
    CMX.ValueSetting(CMXAppPath + "\\CMX_Direction_Y.png", 0, 20, "-1.00")
    CMX.ValueSetting(CMXAppPath + "\\CMX_Direction_Z.png", 0, 20, "0.00")
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\CMX_Btn_OK.png")
    
    #Create CM Run
    wait(1)
    Studio.Click_Icon(StudioAppPath, "\\Studio_NewRun2.png", 0)
    Studio.MeshType("Solid", StudioAppPath)
    Studio.Home_MoldingType(0, -10, StudioAppPath)
    Studio.Click_Icon(StudioAppPath, "\\Studio_Tree_Model.png",0)
       
    Studio.Click_Icon(StudioAppPath, "\\Studio_Import_icon.png", 0)
    Studio.ImportGeometry(PartPath, StudioAppPath)
    Studio.SetAttribute("Part","Geoemetry", StudioAppPath)
    #set part attribute
    Studio.Click_Icon(StudioAppPath, "\\Studio_Import_icon.png", 0)
    Studio.ImportGeometry(CoolingChannelPath, StudioAppPath)
    cc = {'D':'8'}
    Studio.SetAttribute("Coolingchannel","Line", StudioAppPath,**cc)
    
    Studio.Click_Icon(StudioAppPath, "\\Studio_Import_icon.png", 0)
    Studio.ImportGeometry(MoldbasePath, StudioAppPath)
    Studio.SetAttribute("Moldbase","Geoemetry", StudioAppPath)
   
    
    wait(2)
    #set in/oulet 
    Studio.Inletoutlet_wizard(StudioAppPath)
    Studio.Compression_wizard("0,-1,0","15", StudioAppPath)
    
    Studio.SwitchTab(StudioAppPath + "\\Studio_Tab_Mesh.png", StudioAppPath + "\\Studio_Tab_Meshing.png")
    partmesh={'Part':'1.5'}
    Studio.Node_Seeding(StudioAppPath,**partmesh)
    
    wait(3)
    Studio.Meshing_Generate(StudioAppPath)
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
        if exists(StudioAppPath + r"\Btn_Yes.png", 1):
            click(StudioAppPath + r"\Btn_Yes.png")
        i += 1
    if exists(StudioAppPath + r"\Btn_OK.png", 10):
        click(StudioAppPath + r"\Btn_OK.png") 
    Log.write_log(ProjectName, "Info: Studio Pre Process Setting is Finished")
    wait(2)
    Studio.Click_Icon(StudioAppPath, "\\Studio_Import_icon.png", 0)
    Studio.ImportGeometry(ChargePath, StudioAppPath)
    wait(2)
    Studio.SwitchTab(StudioAppPath + "\\Home_tab.png", StudioAppPath + "\\Home_tab_2.png")
    Studio.SetCharge(StudioAppPath)
    
    Log.write_log(ProjectName, "Info: Studio Pre Process Setting is Finished")
    
    
    #Material Wizard Setting
    sMatlist = [MaterialAppPath + r"\MaterialPC_2023.png", MaterialAppPath + r"\MaterialCAE_2023.png", MaterialAppPath + r"\MaterialYung_SU_CGF003_2023.png"]
    Material.OpenMaterialWizard(MaterialAppPath + "\\Studio_Charge.png", 270, 0, MaterialAppPath)
    Material.ClickMDXBank(MaterialAppPath)
    Material.SelectPartMaterial(sMatlist)
    Material.MaterialNotAddToUserBank(MaterialAppPath)
    Material.CloseMaterialWizard(MaterialAppPath)

    
    #Process Wizard Setting
    Process.Home_Process("New", ProcessAppPath)
    Process.ProcessWizard_Project_SettingMethod("CAE", ProcessAppPath) 
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_ProjectSetting.png", ProcessAppPath + "\\Pro_Tab_Compression.png", ProcessAppPath) 
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_Compression.png", ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath)  
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath + "\\Pro_Tab_Summary.png", ProcessAppPath)
    Process.ProcessWizard_Summary_Finish(ProcessAppPath)
    Log.write_log(ProjectName, "Info: Process Wizard Setting is Finished")
    wait(5)
      
    #Analyze Setting
    Analyzelist = [StudioAppPath + "\\Analysis_CtFPCtWO.png", StudioAppPath + "\\Analysis_CoolingTransient_2.png", StudioAppPath + "\\Analysis_FillingAndPacking_2.png", StudioAppPath + "\\Analysis_CoolingTransient_2.png", StudioAppPath + "\\Analysis_Warpage.png", StudioAppPath + "\\Analysis_Optics2.png"]
    Studio.AnalysisSetting(Analyzelist, StudioAppPath)
    Log.write_log(ProjectName, "Info: Analyze Setting is Finished")
    wait(5)
    
    #Computation Parameter Wizard Setting
    #CMX Tab VE/Optics Setting
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\ComputationLogo_2023.png")
    CMX.CMX_Tab_Change(CMXAppPath + "\\CMX_Tab_VEOptics.png")
    CMX.Checkbox(CMXAppPath + "\\CMX_VEOptics_EstimateFillingPackingStage.png", -90, 0, CMXAppPath)
    CMX.Checkbox(CMXAppPath + "\\CMX_VEOptics_EstimateCoolingStage.png", -73, 0, CMXAppPath)
    CMX.Checkbox(CMXAppPath + "\\CMX_VEOptics_EstimateOpticsProperties.png", -73, 0, CMXAppPath)
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\CMX_Btn_Add.png")
    CMX.ValueSetting(CMXAppPath + "\\CMX_Direction_X.png", 0, 20, "0.00")
    CMX.ValueSetting(CMXAppPath + "\\CMX_Direction_Y.png", 0, 20, "-1.00")
    CMX.ValueSetting(CMXAppPath + "\\CMX_Direction_Z.png", 0, 20, "0.00")
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\CMX_Btn_OK.png")
    wait(2)
    
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
    print( "ENT-IM-S3-P1 Test is Failed!")
    Log.write_log(ProjectName, "Error: %s Test is Failed!" % ProjectName)
Log.write_log2(ProjectName, "Summary")

