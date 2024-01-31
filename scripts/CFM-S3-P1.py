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
import Copy_Run_for_MCM as CRfM
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
Copypath = ArgS.Copypath
exceptprocedureApp = ArgS.exceptprocedureApp


ProjectName = "CFM-S3-P1"
username = "moldex3dqa"
password = "123456"
SVNPath = r"svn://192.168.3.4/QARepository/AutoTest/Moldex3D/2023Series/Moldex3D/CaseReference/ENT/" + ProjectName + r"/Geometry"
Filename= SVNPath.split('/')[-2]
localpath = os.path.normpath((cwd + r"\\" +Filename))
MainInstallPath ,ver = Common.getregkeyvalue(r"HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\CoreTechSystem\MDX_ParallelComputing", "INSTALLDIR")
WorkingFolder = Common.getregkeyvalue(r"HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\CoreTechSystem\MDX_ParallelComputing", "WorkingFolder")
StudioPath = MainInstallPath + r"\Bin\MDXStudio.exe"

CaseReferncePath = Common.gototargetpath('MDX_ENT') + "\\" + ProjectName
Run01_Part_SourcePath =CaseReferncePath+ r"\Part.stp"
Run01_Runner_SourcePath =CaseReferncePath+ r"\Runner.stp"
Run01_CompressionZone_SourcePath =CaseReferncePath+ r"\CompressionZone.stp"
Run01_Moldbase_SourcePath =CaseReferncePath+ r"\Moldbase.stp"
Run01_HeatingRod_SourcePath =CaseReferncePath+ r"\HeatingRod.igs"
Run01_Charge_SourcePath =CaseReferncePath+ r"\Charge.stp"
Run01_Venting_SourcePath =CaseReferncePath+ r"\Venting.igs"
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
    Studio.Home_MoldingType_New("Module_CFM", StudioAppPath)
    Studio.Click_IconEx(StudioAppPath + "\\Studio_Tree_Model.png")
    Studio.Home_Model("ImportGeometry", StudioAppPath)
    Studio.ImportGeometry(Run01_Part_SourcePath, StudioAppPath)
    Studio.SetAttribute("Part","Geoemetry", StudioAppPath)
    Studio.Click_IconEx(StudioAppPath + "\\Studio_Import_icon.png")
    Studio.ImportGeometry(Run01_Runner_SourcePath, StudioAppPath)
    Studio.SetAttribute("ColdRunner","Geoemetry", StudioAppPath)
    """
    Studio.Click_IconEx(StudioAppPath + "\\Studio_Import_icon.png")
    Studio.ImportGeometry(Run01_CompressionZone_SourcePath, StudioAppPath)
    Studio.SetAttribute("CompressionZone","Geoemetry", StudioAppPath)
    Studio.Click_IconEx(StudioAppPath + "\\Studio_AttributeIcon.png")
    Studio.Click_IconEx(StudioAppPath + "\\Studio_Attribute_SelectBC.png")
    doubleClick(StudioAppPath + "\\Studio_Attribute_CFM-S3-P1_MovingSurface.png")
    Studio.Click_IconEx(StudioAppPath + "\\Btn_Close.png")
    """
    Studio.Compression_Setting_Zone("ColdRunner", "0,0,-1","20", StudioAppPath)
    Studio.Compression_Setting_Region("Remove", "All", StudioAppPath)
    Studio.Compression_Setting_Region("Add", "Rectangle", StudioAppPath)
    Studio.WindowSelect(StudioAppPath, "\\CFM_S3_P1_Compression.png", 30, -20, -30, 20)
    Studio.Click_IconEx(StudioAppPath + "\\Btn_OK.png")
    
    Studio.Click_IconEx(StudioAppPath + "\\Studio_Import_icon.png")
    Studio.ImportGeometry(Run01_Moldbase_SourcePath, StudioAppPath)
    Studio.SetAttribute("Moldbase","Geoemetry", StudioAppPath)
    Studio.Click_IconEx(StudioAppPath + "\\Studio_Import_icon.png")
    Studio.ImportGeometry(Run01_HeatingRod_SourcePath, StudioAppPath)
    Studio.SetAttribute("HeatingRod","Line", StudioAppPath, **{"D":"4"})
    
    Studio.SwitchTab(StudioAppPath + "\\Studio_Tab_Mesh.png", StudioAppPath + "\\Studio_Tab_Meshing.png")
    #SeedingSize={"Part":"2", "ColdRunner":"1.5", "CompressionZone":"3"}
    SeedingSize={"Part":"2", "ColdRunner":"1.5"}
    Studio.Node_Seeding(StudioAppPath,**SeedingSize)
    Studio.SetMeshParameter("Hybrid","CompressionZone","Prism",StudioAppPath)
    #Studio.SetMeshParameter("Hybrid","CompressionZone","PureTetra",StudioAppPath)
    
    Studio.Meshing_Generate(StudioAppPath)
    Studio.Meshing_GenerateBLM("CompressionZone", StudioAppPath)
    Studio.Wait_Dialog(StudioAppPath, "\\Studio_CompressionZone_Check.png")
    
    #Studio.Click_Icon(StudioAppPath, "\\Studio_Tree_Model.png", 0)
    Studio.Click_Icon(StudioAppPath, "\\Studio_Check.png", 0)
    Studio.Click_Icon(StudioAppPath, "\\Studio_Tree_HeatingRod.png", -53)
    Studio.Click_Icon(StudioAppPath, "\\Btn_Angle_Perspective_Seletected.png", 40)
    Studio.Click_Icon(StudioAppPath, "\\Btn_Fit_To_Window.png", -24)
    Studio.Click_Icon(StudioAppPath, "\\Btn_ShowModeSelected_FeatureShaded2.png", 40)
    Studio.Final_Check(StudioAppPath)
    Log.write_log(ProjectName, "Info: Studio Pre Process Setting is Finished")
    
    #Charge Setting
    Studio.Home_Model("ImportGeometry", StudioAppPath)
    Studio.ImportGeometry(Run01_Charge_SourcePath, StudioAppPath)
    Studio.SwitchTab(StudioAppPath + "\\Studio_Tab_Home_Blue.png", StudioAppPath + "\\Studio_Tab_Home.png")
    Studio.SetCharge(StudioAppPath)
    Log.write_log(ProjectName, "Info: Studio Charge Setting is Finished")
    
    #Material Wizard Setting
    sMatlist = [MaterialAppPath + "\\MaterialRubber.png", MaterialAppPath + "\\MaterialGeneric.png",MaterialAppPath + "\\MaterialRubber3.png"]
    Material.OpenMaterialWizard(MaterialAppPath + "\\Studio_Charge1.png", 200, 0, MaterialAppPath)
    Material.ClickMDXBank(MaterialAppPath)
    Material.SelectPartMaterial(sMatlist)
    Material.MaterialNotAddToUserBank(MaterialAppPath)
    Material.CloseMaterialWizard(MaterialAppPath)
    Log.write_log(ProjectName, "Info: Material Wizard Setting is Finished")
    
    #Process Wizard Setting
    #Process Tab Project Setting 
    Process.Home_Process("New", ProcessAppPath)
    if not exists(Pattern(ProcessAppPath + "\\Pro_Project_TransferType.png").similar(0.95)):
        Process.Click_IconEx(ProcessAppPath + "\\Pro_Project_Type.png", **{"similar":"0.95", "offsetx":"100", "offsety":"0"})
        Process.Click_IconEx(ProcessAppPath + "\\Pro_Project_TransferType.png", **{"similar":"0.95"})
    
    #Process Tab Transfer Setting  
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_ProjectSetting.png", ProcessAppPath + "\\Pro_Tab_Transfer.png", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_Transfer_TransferTime.png", 100, 0, "20", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_Transfer_MaxTransferForce.png", 100, 0, "30", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_Filling_ResinTemp.png", 120, 0, "80", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_Filling_MoldTemp3.png", 120, 0, "200", ProcessAppPath)
    Process.Click_IconEx(ProcessAppPath + "\\Pro_Filling_RetractionSetting.png", **{"similar":"0.9", "offsetx":"-63", "offsety":"-2"})
    Process.ValueSetting(ProcessAppPath + "\\Pro_Filling_RetractionStartTime.png", 120, 0, "6", ProcessAppPath)
    
    #Process Tab Foaming Setting
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_Transfer.png", ProcessAppPath + "\\Pro_Tab_Foaming.png", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_Foaming_CBADosageAmount.png", 160, 0, "5", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_Foaming_ProducedGasAmount.png", 160, 0, "350", ProcessAppPath)
    
    #Process Tab Cooling Setting
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_Foaming.png", ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath)
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
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\CMX_Cooling_AccurancyLevel_Standard.png")
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\CMX_Btn_OK.png")
    Log.write_log(ProjectName, "Info: Computation Parameter Wizard Setting is Finished")
    
    #Venting Setting
    Studio.Home_Model("ImportGeometry", StudioAppPath)
    Studio.ImportGeometry(Run01_Venting_SourcePath, StudioAppPath)
    Studio.SwitchTab(StudioAppPath + "\\Studio_Tab_Home_Blue.png", StudioAppPath + "\\Studio_Tab_Home.png")
    Studio.SetVenting(StudioAppPath)
    Log.write_log(ProjectName, "Info: Studio Venting Setting is Finished")
    
    #Set RC Task Number
    Studio.TaskNumberSetting("4", StudioAppPath)
    click(StudioAppPath + "\\Btn_OK.png")
    Studio.SwitchTab(StudioAppPath + "\\Studio_Tab_Home_Blue.png", StudioAppPath + "\\Studio_Tab_Home.png")
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
    print("%s Test is Failed!") % ProjectName
    Log.write_log(ProjectName, "Error: %s Test is Failed!" % ProjectName)
Log.write_log2(ProjectName, "Summary")