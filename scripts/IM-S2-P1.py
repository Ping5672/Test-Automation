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

ProjectName = "IM-S2-P1"
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
PartInsertPath = CaseReferncePath + r"\Partinsert.stp"
RunnerPath1 = CaseReferncePath + r"\runner1.igs"
RunnerPath2 = CaseReferncePath + r"\runner2.igs"
RunnerPath3 = CaseReferncePath + r"\runner3.igs"
GatePath = CaseReferncePath + r"\gate.igs"
HeatingrodPath = CaseReferncePath + r"\HeatingRod.igs"
MoldbasePath = CaseReferncePath + r"\Moldbase.stp"
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
    Log.write_log(ProjectName, "Info: Open Studio is Finished")
    #New Project
    Studio.NewProject(ProjectName, StudioAppPath)
    Log.write_log(ProjectName, "Info: New Project Setting is Finished")

    #Studio Pre Process Setting
    Studio.MeshType("Solid", StudioAppPath)
    Studio.Home_MoldingType(0, -105, StudioAppPath)

    Studio.Click_Icon(StudioAppPath, "\\Studio_Import_icon.png", 0)
    Studio.ImportGeometry(GatePath, StudioAppPath)
    Studio.Click_Icon(StudioAppPath, "\\Studio_Tree_Model.png",0)
    g = {'Gate':'PinGate','D1red':'2','D1green':'6','L':'6'}
    Studio.SetAttribute("ColdRunnerGate","Line", StudioAppPath,**g)
    #set gate attribute 
    Studio.Click_Icon(StudioAppPath, "\\Studio_Import_icon.png", 0)
    Studio.ImportGeometry(RunnerPath3, StudioAppPath)
    r1 = {'Type':'Circular','D1red':'6','D1green':'4',}
    Studio.SetAttribute("ColdRunner","Line", StudioAppPath,**r1)
    Studio.Click_Icon(StudioAppPath, "\\Studio_Import_icon.png", 0)
    Studio.ImportGeometry(RunnerPath1, StudioAppPath)
    r_2 = {'Type':'Circular','D1red':'6','D1green':'6'}
    Studio.SetAttribute("ColdRunner","Line", StudioAppPath,**r_2)
    Studio.Click_Icon(StudioAppPath, "\\Studio_Import_icon.png", 0)
    Studio.ImportGeometry(RunnerPath2, StudioAppPath)
    r_3 = {'Type':'Circular','D1red':'6','D1green':'6'}
    Studio.SetAttribute("ColdRunner","Line", StudioAppPath,**r_3)

    #set runner attribute
    Studio.Click_Icon(StudioAppPath, "\\Studio_Import_icon.png", 0)
    Studio.ImportGeometry(HeatingrodPath, StudioAppPath)
    hr = {'D':'4'}
    Studio.SetAttribute("Heatingrod","Line", StudioAppPath,**hr)
    #set heating rod attribute
    Studio.Click_Icon(StudioAppPath, "\\Studio_Import_icon.png", 0)
    Studio.ImportGeometry(PartPath, StudioAppPath)
    Studio.SetAttribute("Part","Geoemetry", StudioAppPath)
    #set part attribute
    Studio.Click_Icon(StudioAppPath, "\\Studio_Import_icon.png", 0)
    Studio.ImportGeometry(PartInsertPath, StudioAppPath)
    Studio.SetAttribute("PartInsert","Geoemetry", StudioAppPath)
    #set part insert attribute
    
    Studio.Click_Icon(StudioAppPath, "\\Studio_Import_icon.png", 0)
    Studio.ImportGeometry(MoldbasePath, StudioAppPath)
    Studio.SetAttribute("Moldbase","Geoemetry", StudioAppPath)
    
    
    #set moldbase attribute 
    Studio.Click_Icon(StudioAppPath, "\\Studio_MeltEntrance_Icon.png", 0)
    Studio.Symmetry_wizard(StudioAppPath,'0.5')
    #add melt entrance

    Studio.SwitchTab(StudioAppPath + "\\Studio_Tab_Mesh.png", StudioAppPath + "\\Studio_Tab_Meshing.png")
    partmesh={'Part':'0.8'}
    partinsertmesh={'Partinsert':'0.8'}
    Studio.Node_Seeding(StudioAppPath,**partmesh)
    Studio.Node_Seeding(StudioAppPath,**partinsertmesh)
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
    sMatlist = [MaterialAppPath + r"\MaterialBMC_2023.png", MaterialAppPath + r"\MaterialWAHHONG_2023.png", MaterialAppPath + r"\Material033171141X_2023.png"]
    sMatlist2 =[MaterialAppPath + r"\MaterialABS_2023.png", MaterialAppPath + r"\MaterialASchulman_2023.png", MaterialAppPath + r"\MaterialRABS9000UV5_2023.png"]
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
    Log.write_log("ENT-IM-S2-P1", "Info: Material Wizard Setting is Finished")
    
    #Process Wizard Setting
    Process.Home_Process("New_Injection", ProcessAppPath)
    Process.ProcessWizard_Project_SettingMethod("CAE", ProcessAppPath) 
    #Process Tab Filling/Packing Setting
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_ProjectSetting.png", ProcessAppPath + "\\Pro_Tab_FillingCuring.png", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_Filling_CuringTime.png", 60, 0, "4.57", ProcessAppPath)
    #Process Filling/Packing - Flow Rate Profile Setting
    Process.Click_Icon(ProcessAppPath + "\\Btn_Pro_Flow_rate_profile.png", ProcessAppPath + "\\Pro_Filling_FlowRateProFile.png")
    Process.ProcessWizard_FillingPacking_Profile_Type_Switch("\\Pro_Type_FlowRate%Time%.png", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_SectionNo.png", 60, 0, "1", ProcessAppPath)
    Process.Click_Icon(ProcessAppPath + "\\Btn_OK.png", ProcessAppPath + "\\Pro_Tab_FillingCuring.png")
    #Process Filling/Packing - Injection Pressure Profile Setting
    Process.Click_Icon(ProcessAppPath + "\\Btn_Pro_Inject_pressure_profile.png", ProcessAppPath + "\\Pro_Filling_Injectionpressureprofile.png")
    Process.ProcessWizard_FillingPacking_Profile_Type_Switch("\\Pro_Type_InjectionPressure%Time%.png", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_SectionNo.png", 60, 0, "1", ProcessAppPath)
    Process.Click_Icon(ProcessAppPath + "\\Btn_OK.png", ProcessAppPath + "\\Pro_Tab_FillingCuring.png")
    #Process Filling/Packing - Packing Pressure Profile Setting
    Process.Click_Icon(ProcessAppPath + "\\Btn_Pro_Cure_pressure_profile.png", ProcessAppPath + "\\Btn_Pro_Cure_pressure_profile.png")
    Process.ProcessWizard_FillingPacking_Profile_Type_Switch("\\Pro_Type_CuringPressure%TimeSec.png", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_SectionNo.png", 60, 0, "3", ProcessAppPath)
    Process.Click_Icon(ProcessAppPath + "\\Btn_OK.png", ProcessAppPath + "\\Pro_Tab_FillingCuring.png")
    #Process Tab Cooling Setting
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_FillingCuring.png", ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath)  

    #Process Tab Summary
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath + "\\Pro_Tab_Summary.png", ProcessAppPath)
    Process.ProcessWizard_Summary_Finish(ProcessAppPath)
    Log.write_log("TS", "Info: Process Wizard Setting is Finished")
    #Analyze Setting
    Analyzelist = [StudioAppPath + "\\Analysis_CtFCCtW.png", StudioAppPath + "\\Analysis_CoolingTransient.png", StudioAppPath + "\\Analysis_Filling.png", StudioAppPath + "\\Analysis_Curing.png", StudioAppPath + "\\Analysis_CoolingTransient.png", StudioAppPath + "\\Analysis_Warpage.png"]
    Studio.AnalysisSetting(Analyzelist, StudioAppPath)
    Log.write_log("TS", "Info: Analyze Setting is Finished")
    #Computation Parameter Wizard Setting
    #CMX Tab Flow/Pack Setting
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\ComputationLogo_2023.png")
    CMX.FPSolverTypeChange(CMXAppPath + "\\CMX_Flow_Solver.png", "Enhanced")

    #CMX Tab Cool Setting
    CMX.CMX_Tab_Change(CMXAppPath + "\\CMX_Tab_Cool.png")
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\CMX_Btn_OK.png")
    Log.write_log(ProjectName, "Info: Computation Parameter Wizard Setting is Finished")



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
    Process.Home_Process("New_Injection", ProcessAppPath)
    Process.ProcessWizard_Project_SettingMethod("CAE", ProcessAppPath) 
    #Process Tab Filling/Packing Setting
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_ProjectSetting.png", ProcessAppPath + "\\Pro_Tab_FillingCuring.png", ProcessAppPath)

    Process.ValueSetting(ProcessAppPath + "\\Pro_Filling_CuringTime.png", 60, 0, "4.57", ProcessAppPath)
    #Process Filling/Packing - Flow Rate Profile Setting
    Process.Click_Icon(ProcessAppPath + "\\Btn_Pro_Flow_rate_profile.png", ProcessAppPath + "\\Pro_Filling_FlowRateProFile.png")
    Process.ProcessWizard_FillingPacking_Profile_Type_Switch("\\Pro_Type_FlowRate%Time%.png", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_SectionNo.png", 60, 0, "1", ProcessAppPath)
    Process.Click_Icon(ProcessAppPath + "\\Btn_OK.png", ProcessAppPath + "\\Pro_Tab_FillingCuring.png")
    #Process Filling/Packing - Injection Pressure Profile Setting
    Process.Click_Icon(ProcessAppPath + "\\Btn_Pro_Inject_pressure_profile.png", ProcessAppPath + "\\Pro_Filling_Injectionpressureprofile.png")
    Process.ProcessWizard_FillingPacking_Profile_Type_Switch("\\Pro_Type_InjectionPressure%Time%.png", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_SectionNo.png", 60, 0, "1", ProcessAppPath)
    Process.Click_Icon(ProcessAppPath + "\\Btn_OK.png", ProcessAppPath + "\\Pro_Tab_FillingCuring.png")
    #Process Filling/Packing - Packing Pressure Profile Setting
    Process.Click_Icon(ProcessAppPath + "\\Btn_Pro_Cure_pressure_profile.png", ProcessAppPath + "\\Btn_Pro_Cure_pressure_profile.png")
    Process.ProcessWizard_FillingPacking_Profile_Type_Switch("\\Pro_Type_CuringPressure%TimeSec.png", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_SectionNo.png", 60, 0, "3", ProcessAppPath)
    Process.Click_Icon(ProcessAppPath + "\\Btn_OK.png", ProcessAppPath + "\\Pro_Tab_FillingCuring.png")
    #Process Tab Cooling Setting
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_FillingCuring.png", ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath)  

    #Process Tab Summary
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath + "\\Pro_Tab_Summary.png", ProcessAppPath)
    Process.ProcessWizard_Summary_Finish(ProcessAppPath)
    Log.write_log(ProjectName, "Info: Process Wizard Setting is Finished")

    wait(5)
    #Computation Parameter Wizard Setting
    #CMX Tab Flow/Pack Setting
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\ComputationLogo_2023.png")
    CMX.FPSolverTypeChange(CMXAppPath + "\\CMX_Flow_Solver.png", "Enhanced")


    #CMX Tab Cool Setting
    CMX.CMX_Tab_Change(CMXAppPath + "\\CMX_Tab_Cool.png")
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
    Process.Home_Process("New_Transfer", ProcessAppPath)
    Process.ProcessWizard_Project_SettingMethod("CAE", ProcessAppPath) 
     #Process Tab Cooling Setting
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_ProjectSetting.png", ProcessAppPath + "\\Pro_Tab_RIM.png", ProcessAppPath)  
    click(Pattern(ProcessAppPath + r"\Process_transfer_time.png").similar(0.90).targetOffset(170,0))
    type("7")
    #Process Tab Summary
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_RIM.png", ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath)
    Process.ProcessWizard_Summary_Finish(ProcessAppPath)
    Log.write_log(ProjectName, "Info: Process Wizard Setting is Finished")
    
    #Analyze Setting
    Analyzelist = [StudioAppPath + "\\Analysis_CtFCCtW.png", StudioAppPath + "\\Analysis_CoolingTransient.png", StudioAppPath + "\\Analysis_Filling.png", StudioAppPath + "\\Analysis_Curing.png", StudioAppPath + "\\Analysis_CoolingTransient.png", StudioAppPath + "\\Analysis_Warpage.png"]
    Studio.AnalysisSetting(Analyzelist, StudioAppPath)
    Log.write_log(ProjectName, "Info: Analyze Setting is Finished")
    
    
    #Computation Parameter Wizard Setting
    #CMX Tab Flow/Pack Setting
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\ComputationLogo_2023.png")
    CMX.FPSolverTypeChange(CMXAppPath + "\\CMX_Flow_Solver.png", "Enhanced")

    #CMX Tab Cool Setting
    CMX.CMX_Tab_Change(CMXAppPath + "\\CMX_Tab_Cool.png")
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\CMX_Btn_OK.png")
    Log.write_log(ProjectName, "Info: Computation Parameter Wizard Setting is Finished")
    
    wait(1)
    Studio.Click_Icon(StudioAppPath, "\\Studio_Tree_Run.png", 0)
    CRfM.Copy_Run(Pattern(Copypath + "\\Run03.png").similar(0.92), "RunInputDataOnly", "None", "default", Copypath)
    Log.write_log(ProjectName, "Info: Copy FC to eDesign  is Finished(Transfer)")
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
    Process.Home_Process("New_Transfer", ProcessAppPath)
    Process.ProcessWizard_Project_SettingMethod("CAE", ProcessAppPath) 
    #Process Tab Cooling Setting
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_ProjectSetting.png", ProcessAppPath + "\\Pro_Tab_RIM.png", ProcessAppPath)  
    click(Pattern(ProcessAppPath + r"\Process_transfer_time.png").similar(0.90).targetOffset(170,0))
    wait(1)
    type("a",Key.CTRL)
    wait(1)
    type("7")
    #Process Tab Summary
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_RIM.png", ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath)
    Process.ProcessWizard_Summary_Finish(ProcessAppPath)
    Log.write_log(ProjectName, "Info: Process Wizard Setting is Finished")
    #Analyze Setting
    Analyzelist = [StudioAppPath + "\\Analysis_CtFCCtW.png", StudioAppPath + "\\Analysis_CoolingTransient.png", StudioAppPath + "\\Analysis_Filling.png", StudioAppPath + "\\Analysis_Curing.png", StudioAppPath + "\\Analysis_CoolingTransient.png", StudioAppPath + "\\Analysis_Warpage.png"]
    Studio.AnalysisSetting(Analyzelist, StudioAppPath)
    Log.write_log(ProjectName, "Info: Analyze Setting is Finished")
    
    
    #Computation Parameter Wizard Setting
    #CMX Tab Flow/Pack Setting
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\ComputationLogo_2023.png")
    CMX.FPSolverTypeChange(CMXAppPath + "\\CMX_Flow_Solver.png", "Enhanced")

    #CMX Tab Cool Setting
    CMX.CMX_Tab_Change(CMXAppPath + "\\CMX_Tab_Cool.png")
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\CMX_Btn_OK.png")
    Log.write_log(ProjectName, "Info: Computation Parameter Wizard Setting is Finished")
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
    Log.write_log("Initial", "Info: %s Test is Finished!" % ProjectName)
    wait(1)
    Studio.ClickRun(30, StudioAppPath)
    Studio.Submit_Batch_Run(2,StudioAppPath)
    wait(2)
      
    #Close Studio UI
    Studio.CloseApp(StudioPath)  
    Log.write_log(ProjectName, "Info: %s Test is Finished!" % ProjectName)

    
except:
    os.popen(("python {}").format(exceptprocedureApp))
    print( "ENT-IM-S2-P1 Test is Failed!")
    Log.write_log(ProjectName, "Error: TP Test is Failed!")
Log.write_log2(ProjectName, "Summary")
