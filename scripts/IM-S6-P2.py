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


ProjectName = "IM-S6-P2"
username = "moldex3dqa"
password = "123456"
SVNPath = r"svn://192.168.3.4/QARepository/AutoTest/Moldex3D/2023Series/Moldex3D/CaseReference/ENT/" + ProjectName + r"/Geometry"
localpath = os.path.normpath((cwd + r"\\" +ProjectName))

MainInstallPath ,ver = Common.getregkeyvalue(r"HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\CoreTechSystem\MDX_ParallelComputing", "INSTALLDIR")
WorkingFolder = Common.getregkeyvalue(r"HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\CoreTechSystem\MDX_ParallelComputing", "WorkingFolder")
StudioPath = MainInstallPath + r"\Bin\MDXStudio.exe"
CaseReferncePath = Common.gototargetpath('MDX_ENT') + "\\" + ProjectName
SourcePath = CaseReferncePath + r"\HRS_SC.mdg"
CMPath = MainInstallPath + r'\Bin\MDXComputingManager' + ver + r'.exe'
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
    Studio.Home_Model("ImportGeometry", StudioAppPath)
    Studio.ImportGeometry(SourcePath, StudioAppPath)
    Studio.SwitchTab(StudioAppPath + r"\Studio_Tab_Mesh.png", StudioAppPath + r"\Studio_Tab_Meshing.png")
    Studio.Meshing_Generate(StudioAppPath)
    Studio.Meshing_GenerateBLM("None", StudioAppPath)
    Studio.Wait_Dialog(StudioAppPath, r"\Studio_FinalCheck.png")
    Studio.Final_Check(StudioAppPath)
    Log.write_log(ProjectName, "Info: Studio Pre Process Setting is Finished")
    
    #Material Wizard Setting
    sMatlist = [MaterialAppPath + r"\MaterialPS_2023.png", MaterialAppPath + r"\MaterialPS_L2.png", MaterialAppPath + r"\MaterialCAE_2023.png", MaterialAppPath + r"\Material_A7.png"]
    Material.OpenMaterialWizard(MaterialAppPath + "\\Studio_EM1.png", 200, 0, MaterialAppPath)
    Material.ClickMDXBank(MaterialAppPath)
    Material.SelectPartMaterial(sMatlist)
    Material.MaterialNotAddToUserBank(MaterialAppPath)
    Material.CloseMaterialWizard(MaterialAppPath)
    Log.write_log(ProjectName, "Info: Material Wizard Setting is Finished")
    #Process Wizard Setting
    Process.Home_Process("Default", ProcessAppPath)
    Log.write_log(ProjectName, "Info: Process Wizard Setting is Finished")
    
    #Analyze Setting
    Analyzelist = [StudioAppPath + "\\Analysis_CHRSFPCtW.png", StudioAppPath + "\\Analysis_CoolingCycle4.png", StudioAppPath + "\\Analysis_HRS.png", StudioAppPath + "\\Analysis_Filling_2.png", StudioAppPath + "\\Analysis_Packing2.png", StudioAppPath + "\\Analysis_CoolingTransient_2.png", StudioAppPath + "\\Analysis_Warpage.png"]
    Studio.AnalysisSetting(Analyzelist, StudioAppPath)
    Log.write_log(ProjectName, "Info: Analyze Setting is Finished")
    
    #CMX Tab Flow/Pack Setting
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\ComputationLogo_2023.png")
    CMX.CMX_Tab_Change(CMXAppPath +"\\Tab_HRS.png")
    CMX.sethotrunnerpressure()
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\CMX_Btn_OK.png")
    Log.write_log(ProjectName, "Info: Computation Parameter Wizard Setting is Finished")
   

    wait(1)
    #Change Remark Name
    Studio.Click_Icon(StudioAppPath, r"\Studio_Tree_Run.png", 0)
    wait(1)
    Remark_name = ["HRS"]
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
