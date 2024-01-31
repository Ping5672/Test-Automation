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


ProjectName = "CFM-S2-P2"
username = "moldex3dqa"
password = "123456"
SVNPath = r"svn://192.168.3.4/QARepository/AutoTest/Moldex3D/2023Series/Moldex3D/CaseReference/ENT/" + ProjectName + r"/Geometry"
Filename= SVNPath.split('/')[-2]
localpath = os.path.normpath((cwd + r"\\" +Filename))
MainInstallPath ,ver = Common.getregkeyvalue(r"HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\CoreTechSystem\MDX_ParallelComputing", "INSTALLDIR")
WorkingFolder = Common.getregkeyvalue(r"HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\CoreTechSystem\MDX_ParallelComputing", "WorkingFolder")
StudioPath = MainInstallPath + r"\Bin\MDXStudio.exe"

CaseReferncePath = Common.gototargetpath('MDX_ENT') + "\\" + ProjectName
SourcePath =CaseReferncePath+ r"\CFM_Rotate_B.mdg"
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
    Studio.Home_MoldingType_New("Module_CFM", StudioAppPath)
    Studio.Home_Model("ImportGeometry", StudioAppPath)
    Studio.ImportGeometry(SourcePath, StudioAppPath)
    Studio.SwitchTab(StudioAppPath + "\\Studio_Tab_Mesh.png", StudioAppPath + "\\Studio_Tab_Meshing.png")
    Studio.Meshing_Generate(StudioAppPath)
    Studio.Meshing_GenerateBLM("None", StudioAppPath)
    Studio.Wait_Dialog(StudioAppPath, "\\Studio_FinalCheck.png")
    
    #Set Oberflow Attribute
    Studio.Click_Icon(StudioAppPath, "\\Btn_Angle_Front_Seletected.png", 40)
    Studio.Click_Icon(StudioAppPath, "\\Btn_Fit_To_Window.png", -24)
    Studio.Click_Icon(StudioAppPath, "\\Btn_ShowModeSelected_FeatureShaded2.png", 40)
    Studio.WindowSelect(StudioAppPath, "\\CFM_S2_P2_Overflow.png", 800, -100, -800, 100)
    rightClick(StudioAppPath + "\\CFM_S2_P2_Overflow_Selected.png")
    Studio.Click_IconEx(StudioAppPath + "\\Studio_Edit_Attribute.png")
    wait(StudioAppPath + "\\Studio_AttributeWizard_Attibute.png", 5)
    Studio.Click_IconEx(StudioAppPath + "\\Studio_AttributeWizard_Attibute.png", **{'similar':0.95, 'offsetx':80, 'offsety':20})
    Studio.Click_IconEx(StudioAppPath + "\\Studio_Attribute_Overflow.png")
    Studio.Click_IconEx(StudioAppPath + "\\Btn_Close.png")
    Studio.Click_Icon(StudioAppPath, "\\Btn_Angle_Perspective_Seletected.png", 40)
    Studio.Click_Icon(StudioAppPath, "\\Btn_Fit_To_Window.png", -24)
    Studio.Click_Icon(StudioAppPath, "\\Btn_ShowModeSelected_FeatureShaded2.png", 40)
    Studio.Final_Check(StudioAppPath)
    Log.write_log(ProjectName, "Info: Studio Pre Process Setting is Finished")

    #Material Wizard Setting
    sMatlist = [MaterialAppPath + "\\MaterialPU.png", MaterialAppPath + "\\MaterialCAE.png",MaterialAppPath + "\\MaterialPU2.png"]
    Material.OpenMaterialWizard(MaterialAppPath + "\\Studio_EM1.png", 200, 0, MaterialAppPath)
    Material.ClickMDXBank(MaterialAppPath)
    Material.SelectPartMaterial(sMatlist)
    Material.MaterialNotAddToUserBank(MaterialAppPath)
    Material.CloseMaterialWizard(MaterialAppPath)
    Log.write_log(ProjectName, "Info: Material Wizard Setting is Finished")
    
    #Process Wizard Setting
    Process.Home_Process("New", ProcessAppPath)
    #Process Tab Filling Setting  
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_ProjectSetting.png", ProcessAppPath + "\\Pro_Tab_Filling.png", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_Filling_FillingTime.png", 60, 0, "3", ProcessAppPath)
    #Process Filling/Packing - Flow Rate Profile Setting
    Process.Click_Icon(ProcessAppPath + "\\Btn_Pro_Flow_rate_profile.png", ProcessAppPath + "\\Pro_Filling_FlowRateProFile.png")
    Process.ProcessWizard_FillingPacking_Profile_Type_Switch("\\Pro_Type_FlowRate%Time%.png", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_SectionNo.png", 60, 0, "1", ProcessAppPath)
    Profilelist = [ProcessAppPath + "\\Pro_Filling_FlowRateProFile.png", "50"]
    Process.ProcessWizard_FillingPacking_Profile_Section_Value(Profilelist, ProcessAppPath)
    Process.Click_Icon(ProcessAppPath + "\\Btn_OK.png", ProcessAppPath + "\\Pro_Tab_Filling.png")
    #Process Tab Foaming Setting
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_Filling.png", ProcessAppPath + "\\Pro_Tab_Foaming.png", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_Foaming_VolumePercentage.png", 180, 0, "40", ProcessAppPath)
    #Process Tab Rotating Setting
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_Foaming.png", ProcessAppPath + "\\Pro_Tab_Rotating.png", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_Rotating_Origin.png", 5, 30, "0", ProcessAppPath) # X
    Process.ValueSetting(ProcessAppPath + "\\Pro_Rotating_Origin.png", 125, 30, "0", ProcessAppPath) # Y
    Process.ValueSetting(ProcessAppPath + "\\Pro_Rotating_Origin.png", 245, 30, "103", ProcessAppPath) # X
    Process.ValueSetting(ProcessAppPath + "\\Pro_Rotating_Axis.png", 5, 30, "1", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_Rotating_Axis.png", 125, 30, "0", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_Rotating_Axis.png", 245, 30, "0", ProcessAppPath)
    Process.ValueSetting(ProcessAppPath + "\\Pro_Rotating_MaxAngularSpeed.png", 100, 0, "0.15", ProcessAppPath)
    Process.Click_Icon(ProcessAppPath + "\\Btn_Pro_Angular_speed_profile.png", ProcessAppPath + "\\Btn_Pro_AngularSpeedProfile.png")
    Process.ValueSetting(ProcessAppPath + "\\Pro_SectionNo.png", 60, 0, "6", ProcessAppPath)
    Profilelist = [ProcessAppPath + "\\Btn_Pro_AngularSpeedProfile.png", "2", "0", "5", "0.15", "8", "-0.15", "11", "0.15", "14", "-0.15", "25", "0"]
    Process.ProcessWizard_Rotating_Angularspeed_Profile_Section_Value(Profilelist, ProcessAppPath)
    Process.Click_Icon(ProcessAppPath + "\\Btn_OK.png", ProcessAppPath + "\\Pro_Tab_Filling.png")
    
    #Process Tab Cooling Setting
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_Rotating.png", ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath)
    #Process Tab Summary
    Process.ProcessWizard_Tab_Next(ProcessAppPath + "\\Pro_Tab_Cooling.png", ProcessAppPath + "\\Pro_Tab_Summary.png", ProcessAppPath)
    Process.ProcessWizard_Summary_Finish(ProcessAppPath)
    Log.write_log(ProjectName, "Info: Process Wizard Setting is Finished")
    
    #Computation Parameter Wizard Setting
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\ComputationLogo.png")    
    #CMX Tab Flow/Pack Setting
    Studio.Click_Icon(CMXAppPath, r"\CMX_Flow_Customize.png", -36)
    CMX.ValueSetting(CMXAppPath + r"\CMX_Flow_Direction_Z.png", 20, 0, "-980")
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\CMX_Btn_OK.png")
    Log.write_log(ProjectName, "Info: Computation Parameter Wizard Setting is Finished")
    
    #Run 02
    #Copy Run
    Studio.Click_Icon(StudioAppPath, r"\Studio_Tree_Run.png", 0)
    CRfM.Copy_Run(Pattern(Copypath + r"\Run01.png").similar(0.92), "RunInputDataOnly", "None", "default", Copypath)
    Log.write_log(ProjectName, "Info: Copy Run1 to Run2 is Finished")
    
    #Computation Parameter Wizard Setting
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\ComputationLogo.png")    
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\Studio_Default.png")
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\CMX_Btn_OK.png")
    Log.write_log(ProjectName, "Info: Computation Parameter Wizard Setting is Finished")
    
    #Change Remark Name
    Studio.Click_Icon(StudioAppPath, "\\Studio_Tree_Run.png", 0)
    wait(1)
    Remark_name = ["Gravity", "No Gravity"]
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