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

ProjectName = "PIM-S1-P1"
username = "moldex3dqa"
password = "123456"
SVNPath = r"svn://192.168.3.4/QARepository/AutoTest/Moldex3D/2023Series/Moldex3D/CaseReference/ENT/" + ProjectName + r"/Geometry"
Filename= SVNPath.split('/')[-2]
localpath = os.path.normpath((cwd + r"\\" +Filename))

MainInstallPath ,ver = Common.getregkeyvalue(r"HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\CoreTechSystem\MDX_ParallelComputing", "INSTALLDIR")
WorkingFolder = Common.getregkeyvalue(r"HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\CoreTechSystem\MDX_ParallelComputing", "WorkingFolder")
StudioPath = MainInstallPath + r"\Bin\MDXStudio.exe"
CaseReferncePath = Common.gototargetpath('MDX_ENT') + "\\" + ProjectName

SC_SourcePath=CaseReferncePath+r"\PIM_SC.mdg"
FC_SourcePath=CaseReferncePath+r"\PIM_FC.mdg"
eDesign_SourcePath=CaseReferncePath+r"\PIM_eDesign.mdg"
PartPath = CaseReferncePath+ r"\part.stp"
RunnerPath1 = CaseReferncePath + r"\runner.igs"
MoldbasePath = CaseReferncePath + r"\moldbase.stp"
CoolingChannelPath = CaseReferncePath +r"\coolingchannel.igs"
PartPath2 = CaseReferncePath + r"\eDesign\part.stp"
PartInsertPath2 = CaseReferncePath + r"\eDesign\partinsert.stp"
RunnerPath2 = CaseReferncePath + r"\eDdesign\runner.igs"
MoldbasePath2 = CaseReferncePath + r"\eDesign\moldbase.stp"
CoolingChannelPath2 = CaseReferncePath + r"\eDeisgn\coolingchannel.igs"
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
    Log.write_log(ProjectName,"Info: Open Studio is Finished")
    #New Project
    Studio.NewProject(ProjectName, StudioAppPath)
    Log.write_log(ProjectName, "Info: New Project Setting is Finished")
    #Studio Pre Process Setting
    Studio.MeshType("Solid", StudioAppPath)
    Studio.Home_MoldingType(0, -85, StudioAppPath)
    Studio.Click_Icon(StudioAppPath, "\\Studio_Tree_Model.png",0)
    Studio.Click_Icon(StudioAppPath, "\\Studio_Import_icon.png", 0)
    Studio.ImportGeometry(SC_SourcePath, StudioAppPath)
    Studio.SwitchTab(StudioAppPath + "\\Studio_Tab_Mesh.png", StudioAppPath + "\\Studio_Tab_Meshing.png")

    nodesize1={'Part':'0.2'}
    Studio.Node_Seeding(StudioAppPath,**nodesize1)
    
    Studio.Meshing_Generate(StudioAppPath)
    Studio.Meshing_GenerateBLM("None", StudioAppPath)
    Studio.Wait_Dialog(StudioAppPath, "\\Studio_FinalCheck.png")
    Studio.Click_Icon(StudioAppPath, "\\Btn_Angle_Perspective_Seletected.png", 40)
    Studio.Click_Icon(StudioAppPath, "\\Btn_Fit_To_Window.png", -24)
    Studio.Click_Icon(StudioAppPath, "\\Btn_ShowModeSelected_FeatureShaded2.png", 40)
    Studio.Final_Check(StudioAppPath)

 
    Log.write_log(ProjectName, "Info: Studio Pre Process Setting is Finished")
    #Material Wizard Setting
    sMatlist = [MaterialAppPath + r"\MaterialSPECIAL_2023.png", MaterialAppPath + r"\MaterialPIM_2023.png",MaterialAppPath + "\\MaterialCAE_2023.png", MaterialAppPath + r"\MaterialCAEMIM002_2023.png"]
    Material.OpenMaterialWizard(MaterialAppPath + "\\Studio_EM1.png", 200, 0, MaterialAppPath)
    Material.ClickMDXBank(MaterialAppPath)
    Material.SelectPartMaterial(sMatlist)
    Material.MaterialNotAddToUserBank(MaterialAppPath)
    Material.CloseMaterialWizard(MaterialAppPath)
    Log.write_log(ProjectName, "Info: Material Wizard Setting is Finished")
    
    #Process Wizard Setting

    Process.Home_Process("Default", ProcessAppPath)
    #Analyze Setting
    Analyzelist = [StudioAppPath + "\\Analysis_CtFPCtW.png", StudioAppPath + "\\Analysis_CoolingTransient_2.png", StudioAppPath + "\\Analysis_Filling.png", StudioAppPath + "\\Analysis_Packing2.png", StudioAppPath + "\\Analysis_CoolingTransient_2.png", StudioAppPath + "\\Analysis_Warpage.png"]
    Studio.AnalysisSetting(Analyzelist, StudioAppPath)
    Log.write_log(ProjectName, "Info: Analyze Setting is Finished")
    #Computation Parameter Wizard Setting
    #CMX Tab Flow/Pack Setting
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\ComputationLogo_2023.png")
    CMX.Checkbox(CMXAppPath + "\\CMX_Flow_Weldline_particle.png", -55, 0, CMXAppPath)
    CMX.Checkbox(CMXAppPath + "\\CMX_Flow_ParticleTrackingFrom.png", -60, 0, CMXAppPath)
    #CMX Tab Cool Setting
    CMX.CMX_Tab_Change(CMXAppPath + "\\CMX_Tab_Cool.png")
    CMX.Checkbox(CMXAppPath + "\\CMX_Cool_CoolingChannelAnalysisBy2.png", -82, 0, CMXAppPath)
    CMX.SelectDropDownMenu(CMXAppPath + "\\CMX_Cool_CoolingChannelAnalysisBy2.png", -10, 30, CMXAppPath + "\\CMX_Cool_Run3DSolidCoolingChannelAnalysis2.png", 0, 0)
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\CMX_Btn_OK.png")
    Log.write_log(ProjectName, "Info: Computation Parameter Wizard Setting is Finished")
    
    #New Run (Fc)
    Studio.Click_Icon(StudioAppPath, "\\Studio_NewRun2.png", 0)
    Studio.MeshType("Solid", StudioAppPath)
    Studio.Home_MoldingType(0, -85, StudioAppPath)
    Studio.Click_Icon(StudioAppPath, "\\Studio_Tree_Model.png",0)
    Studio.Click_Icon(StudioAppPath, "\\Studio_Import_icon.png", 0)
    Studio.ImportGeometry(FC_SourcePath, StudioAppPath)
    wait(1)
    Studio.SwitchTab(StudioAppPath + "\\Studio_Tab_Mesh.png", StudioAppPath + "\\Studio_Tab_Meshing.png")

    nodesize1={'Part':'3'}
    Studio.Node_Seeding(StudioAppPath,**nodesize1)
    nodesize2={'Partinsert':'5'}
    Studio.Node_Seeding(StudioAppPath,**nodesize2)
    
    Studio.Meshing_Generate(StudioAppPath)
    Studio.Meshing_GenerateBLM("Runner", StudioAppPath)
    Studio.Wait_Dialog(StudioAppPath, "\\Studio_Runner_Check.png")
    Studio.Click_Icon(StudioAppPath, "\\Btn_Angle_Perspective_Seletected.png", 40)
    Studio.Click_Icon(StudioAppPath, "\\Btn_Fit_To_Window.png", -24)
    Studio.Click_Icon(StudioAppPath, "\\Btn_ShowModeSelected_FeatureShaded2.png", 40)
    Studio.Final_Check(StudioAppPath)

 
    Log.write_log(ProjectName, "Info: Studio Pre Process Setting is Finished")
    #Material Wizard Setting
    sMatlist = [MaterialAppPath + r"\MaterialSPECIAL_2023.png", MaterialAppPath + r"\MaterialPIM_2023.png",MaterialAppPath + "\\MaterialCAE_2023.png", MaterialAppPath + r"\MaterialCAECIM001_2023.png"]
    Material.OpenMaterialWizard(MaterialAppPath + "\\Studio_EM1.png", 200, 0, MaterialAppPath)
    Material.ClickMDXBank(MaterialAppPath)
    Material.SelectPartMaterial(sMatlist)
    Material.MaterialNotAddToUserBank(MaterialAppPath)
    Material.CloseMaterialWizard(MaterialAppPath)
    Log.write_log(ProjectName, "Info: Material Wizard Setting is Finished")
    #Part Insert
    sMatlist2 = [MaterialAppPath + r"\MaterialMetal_2023.png", MaterialAppPath + r"\Material_Generic_2023.png", MaterialAppPath + r"\Materia_Iron_FE_2023.png"]
    Material.OpenMaterialWizard(MaterialAppPath + "\\StudioPartInsert1.png", 200, 0, MaterialAppPath)
    Material.ClickMDXBank(MaterialAppPath)
    Material.SelectPartMaterial(sMatlist2)
    Material.MaterialNotAddToUserBank(MaterialAppPath)
    Material.CloseMaterialWizard(MaterialAppPath)
    Log.write_log(ProjectName, "Info: Material Wizard Setting is Finished")

    #Process Wizard Setting

    Process.Home_Process("Default", ProcessAppPath)
    #Analyze Setting
    Analyzelist = [StudioAppPath + "\\Analysis_CtFPCtW.png", StudioAppPath + "\\Analysis_CoolingTransient_2.png", StudioAppPath + "\\Analysis_Filling.png", StudioAppPath + "\\Analysis_Packing2.png", StudioAppPath + "\\Analysis_CoolingTransient_2.png", StudioAppPath + "\\Analysis_Warpage.png"]
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
     
    #New Run(eD)
    Studio.Click_Icon(StudioAppPath, "\\Studio_NewRun2.png", 0)
    Log.write_log(ProjectName, "Info: New Run(eD) Setting is Finished")
    Studio.MeshType("eDesign", StudioAppPath)
    Studio.Home_MoldingType(0, -85, StudioAppPath)
    Studio.Click_Icon(StudioAppPath, "\\Studio_Tree_Model.png",0)
    Studio.Home_Model("ImportGeometry", StudioAppPath)
    Studio.ImportGeometry(eDesign_SourcePath, StudioAppPath)
    wait(1)
    Studio.SwitchTab(StudioAppPath +"\\Studio_Tab_Mesh.png", StudioAppPath + "\\Studio_Tab_Meshing.png")
    Studio.Meshing_Generate(StudioAppPath)
    Studio.Meshing_GenerateeDesign(StudioAppPath)
    Studio.Wait_Dialog(StudioAppPath, "\\Log_Generate_Solid_Mesh_Done.png")
    Studio.Final_Check(StudioAppPath)

    #Material Wizard Setting
    sMatlist = [MaterialAppPath + r"\MaterialSPECIAL_2023.png", MaterialAppPath + r"\MaterialPIM_2023.png",MaterialAppPath + "\\MaterialCAE_2023.png", MaterialAppPath + r"\MaterialCAECIM001_2023.png"]
    Material.OpenMaterialWizard(MaterialAppPath + "\\Studio_EM1.png", 200, 0, MaterialAppPath)
    Material.ClickMDXBank(MaterialAppPath)
    Material.SelectPartMaterial(sMatlist)
    Material.MaterialNotAddToUserBank(MaterialAppPath)
    Material.CloseMaterialWizard(MaterialAppPath)
    Log.write_log(ProjectName, "Info: Material Wizard Setting is Finished")
    Material.Wait_Dialog(StudioAppPath, "\\Logo_NonFiber_UnSelected.png", "\\Logo_NonFiber_UnSelected_Blue.png")
    Material.Click_Icon(MaterialAppPath + "\\StudioPartInsert1.png", 200) 
    Material.MCM2ndRunInsertSelection(MaterialAppPath + "\\StudioPartInsertSelection.png", MaterialAppPath + "\\Studio_Metal_Iron.png", MaterialAppPath)
    Log.write_log(ProjectName, "Info: Material Wizard Setting is Finished")
    

   #Process Wizard Setting
    Process.Home_Process("Default", ProcessAppPath)
    #Analyze Setting
    Analyzelist = [StudioAppPath + "\\Analysis_CtFPCtW.png", StudioAppPath + "\\Analysis_CoolingTransient.png", StudioAppPath + "\\Analysis_Filling.png", StudioAppPath + "\\Analysis_Packing2.png", StudioAppPath + "\\Analysis_CoolingTransient.png", StudioAppPath + "\\Analysis_Warpage.png"]
    Studio.AnalysisSetting(Analyzelist, StudioAppPath)
    Log.write_log(ProjectName,"Info: Analyze Setting is Finished")
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
    print( "ENT-PIM-S1-P1 Test is Failed!")
    Log.write_log(ProjectName,"Error: %s Test is Failed!" % ProjectName)
Log.write_log2(ProjectName, "Summary")

