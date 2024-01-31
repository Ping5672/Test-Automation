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


ProjectName = "FIM-S2-P1"
username = "rex"
password = "123456"
SVNPath = r"svn://192.168.3.4/QARepository/AutoTest/Moldex3D/2023Series/Moldex3D/CaseReference/ENT/" + ProjectName + r"/Geometry"
Filename= SVNPath.split('/')[-2]
localpath = os.path.normpath((cwd + r"\\" +Filename))
MainInstallPath ,ver = Common.getregkeyvalue(r"HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\CoreTechSystem\MDX_ParallelComputing", "INSTALLDIR")
WorkingFolder = Common.getregkeyvalue(r"HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\CoreTechSystem\MDX_ParallelComputing", "WorkingFolder")
StudioPath = MainInstallPath + r"\Bin\MDXStudio.exe"

CaseReferncePath = Common.gototargetpath('MDX_ENT') + "\\" + ProjectName
Run01_SourcePath =CaseReferncePath+ r"\FIM_SC.mdg"
Run02_SourcePath =CaseReferncePath+ r"\FIM_FC.mdg"
Run03_SourcePath =CaseReferncePath+ r"\FIM_eDesign.mdg"
CMPath = MainInstallPath + r"\Bin\MDXComputingManager" + ver + ".exe"
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
    Studio.Home_MoldingType_New("Module_IM2", StudioAppPath)
    Studio.MeshType("Solid", StudioAppPath)
    Studio.Home_MoldingType_New("Module_FIM", StudioAppPath)
    Studio.Home_Model("ImportGeometry", StudioAppPath)
    Studio.ImportGeometry(Run01_SourcePath, StudioAppPath)
    Studio.SwitchTab(StudioAppPath + "\\Studio_Tab_Mesh.png", StudioAppPath + "\\Studio_Tab_Meshing.png")
    Studio.Final_Check(StudioAppPath)
    Log.write_log(ProjectName, "Info: Studio Pre Process Setting is Finished")

    #Material Wizard Setting
    sMatlist = [MaterialAppPath + "\\MaterialRubber.png", MaterialAppPath + "\\MaterialGeneric.png",MaterialAppPath + "\\MaterialRubber1.png"]
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
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_FillingPacking.png", ProcessAppPath + "\\Pro_Tab_Foaming.png", ProcessAppPath)  
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_Foaming.png", ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath)  
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath + "\\Pro_Tab_Summary.png", ProcessAppPath)
    Process.ProcessWizard_Summary_Finish(ProcessAppPath)
    Log.write_log(ProjectName, "Info: Process Wizard Setting is Finished")

    #Analyze Setting
    Analyzelist = [StudioAppPath + "\\Analysis_CFAndPCtW.png", StudioAppPath + "\\Analysis_CoolingCycle2.png", StudioAppPath + "\\Analysis_FillingAndPacking_2.png", StudioAppPath + "\\Analysis_CoolingTransient_2.png", StudioAppPath + "\\Analysis_Warpage.png"]
    Studio.AnalysisSetting(Analyzelist, StudioAppPath)
    Log.write_log(ProjectName, "Info: Analyze Setting is Finished")
    
    #Computation Parameter Wizard Setting
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\ComputationLogo.png")    
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
    Studio.ImportGeometry(Run02_SourcePath, StudioAppPath)
    Studio.SwitchTab(StudioAppPath + "\\Studio_Tab_Mesh.png", StudioAppPath + "\\Studio_Tab_Meshing.png")
    Studio.Meshing_Generate(StudioAppPath)
    Studio.Meshing_GenerateBLM("Runner", StudioAppPath)
    Studio.Wait_Dialog(StudioAppPath, "\\Studio_Runner_Check.png")
    Studio.Click_Icon(StudioAppPath, "\\Btn_Angle_Front_Seletected.png", 20)
    Studio.Click_Icon(StudioAppPath, "\\Btn_Fit_To_Window.png", -24)
    Studio.Final_Check(StudioAppPath)
    Log.write_log(ProjectName, "Info: Studio Pre Process Setting is Finished")
    
    #Material Wizard Setting
    sMatlist = [MaterialAppPath + "\\MaterialRubber.png", MaterialAppPath + "\\MaterialGeneric.png",MaterialAppPath + "\\MaterialRubber1.png"]
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
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_FillingPacking.png", ProcessAppPath + "\\Pro_Tab_Foaming.png", ProcessAppPath)  
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_Foaming.png", ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath)  
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath + "\\Pro_Tab_Summary.png", ProcessAppPath)
    Process.ProcessWizard_Summary_Finish(ProcessAppPath)
    Log.write_log(ProjectName, "Info: Process Wizard Setting is Finished")

    #Analyze Setting
    Analyzelist = [StudioAppPath + "\\Analysis_CFAndPCtW.png", StudioAppPath + "\\Analysis_CoolingCycle2.png", StudioAppPath + "\\Analysis_FillingAndPacking_2.png", StudioAppPath + "\\Analysis_CoolingTransient_2.png", StudioAppPath + "\\Analysis_Warpage.png"]
    Studio.AnalysisSetting(Analyzelist, StudioAppPath)
    Log.write_log(ProjectName, "Info: Analyze Setting is Finished")
    
    #Computation Parameter Wizard Setting
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\ComputationLogo.png")    
    CMX.CMX_Tab_Change(CMXAppPath + "\\CMX_Tab_Cool.png")
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\CMX_Cooling_AccurancyLevel_Standard.png")
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\CMX_Btn_OK.png")
    Log.write_log(ProjectName, "Info: Computation Parameter Wizard Setting is Finished")

    
    #Run 03
    #New Run (eDesign)
    Studio.Click_Icon(StudioAppPath, "\\Studio_NewRun2.png", 0)
    Log.write_log(ProjectName, "Info: New Run Setting is Finished")
    Studio.MeshType("eDesign", StudioAppPath)
    #Studio Pre Process Setting
    Studio.Home_Model("ImportGeometry", StudioAppPath)
    Studio.ImportGeometry(Run03_SourcePath, StudioAppPath)
    Studio.SwitchTab(StudioAppPath + "\\Studio_Tab_Mesh.png", StudioAppPath + "\\Studio_Tab_Meshing.png")
    Studio.Meshing_Generate(StudioAppPath)
    Studio.Meshing_GenerateeDesign(StudioAppPath)
    Studio.Wait_Dialog(StudioAppPath, "\\Log_Generate_Solid_Mesh_Done.png")
    Studio.Final_Check(StudioAppPath)
    wait(3)
    Log.write_log(ProjectName, "Info: Studio Pre Process Setting is Finished")
    

    #Material Wizard Setting
    sMatlist = [MaterialAppPath + "\\MaterialRubber.png", MaterialAppPath + "\\MaterialGeneric.png",MaterialAppPath + "\\MaterialRubber1.png"]
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
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_FillingPacking.png", ProcessAppPath + "\\Pro_Tab_Foaming.png", ProcessAppPath)  
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_Foaming.png", ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath)  
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath + "\\Pro_Tab_Summary.png", ProcessAppPath)
    Process.ProcessWizard_Summary_Finish(ProcessAppPath)
    Log.write_log(ProjectName, "Info: Process Wizard Setting is Finished")

    #Analyze Setting
    Analyzelist = [StudioAppPath + "\\Analysis_CFAndPCtW.png", StudioAppPath + "\\Analysis_CoolingCycle2.png", StudioAppPath + "\\Analysis_FillingAndPacking_2.png", StudioAppPath + "\\Analysis_CoolingTransient_2.png", StudioAppPath + "\\Analysis_Warpage.png"]
    Studio.AnalysisSetting(Analyzelist, StudioAppPath)
    Log.write_log(ProjectName, "Info: Analyze Setting is Finished")
    
    #Computation Parameter Wizard Setting
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\ComputationLogo.png")    
    CMX.CMX_Tab_Change(CMXAppPath + "\\CMX_Tab_Cool.png")
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\CMX_Cooling_AccurancyLevel_Standard.png")
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\CMX_Btn_OK.png")
    Log.write_log(ProjectName, "Info: Computation Parameter Wizard Setting is Finished")

    #Change Remark Name
    Studio.Click_Icon(StudioAppPath, "\\Studio_Tree_Run.png", 0)
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
    print( "ENT-FIM-S2-P1 Test is Failed!")
    Log.write_log(ProjectName, "Error: %s Test is Failed!" % ProjectName)
Log.write_log2(ProjectName, "Summary")
