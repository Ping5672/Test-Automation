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

ProjectName = "IM-S4-P2"
username = "moldex3dqa"
password = "123456"
SVNPath = r"svn://192.168.3.4/QARepository/AutoTest/Moldex3D/2023Series/Moldex3D/CaseReference/ENT/" + ProjectName + r"/Geometry"
localpath = os.path.normpath((cwd + r"\\" +ProjectName))
MainInstallPath ,ver = Common.getregkeyvalue(r"HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\CoreTechSystem\MDX_ParallelComputing", "INSTALLDIR")
WorkingFolder = Common.getregkeyvalue(r"HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\CoreTechSystem\MDX_ParallelComputing", "WorkingFolder")
StudioPath = MainInstallPath + r"\Bin\MDXStudio.exe"
#CaseReferncePath = os.path.join(Common.gototargetpath('MDX_ENT'), r'/NEW-MDX-ENT/IM-S1-P1/Geometry')
CaseReferncePath = Common.gototargetpath('MDX_ENT') + "\\" + ProjectName + r"\Source"
SourcePath = CaseReferncePath + r"\Part_73855.mdg"
SourcePath2 = CaseReferncePath + r"\Annealing.mdg"
CMPath = MainInstallPath + r"\Bin\MDXComputingManager" + ver + ".exe"
hostname, local_ip = Common.getcuriphostname()





try:
    
    #svn execution
    Common.SVNLogin(username, password)
    Common.SVNDownload(SVNPath, localpath)
    Studio.OpenApp(StudioPath, StudioAppPath + "\\Studio_UI.png")
    Log.write_log(ProjectName, "Info: Open Studio is Finished")
    #New Project
    Studio.NewProject("ENT-IM-S4-P2", StudioAppPath)
    Log.write_log(ProjectName, "Info: New Project Setting is Finished")
    #Studio Pre Process Setting
    Studio.MeshType("Solid", StudioAppPath)
    Studio.Home_MoldingType(0, -105, StudioAppPath)
    Studio.Home_Model("ImportGeometry", StudioAppPath)
    wait(3)
    Studio.ImportGeometry(SourcePath, StudioAppPath)
    Studio.SwitchTab(StudioAppPath + r"\Studio_Tab_Mesh.png", StudioAppPath + r"\Studio_Tab_Meshing.png")
    Studio.Meshing_Generate(StudioAppPath)
    Studio.Meshing_GenerateBLM("None", StudioAppPath)
    Studio.Wait_Dialog(StudioAppPath, r"\Studio_FinalCheck.png")
    Studio.Final_Check(StudioAppPath)
    Log.write_log(ProjectName, "Info: Studio Pre Process Setting is Finished")
    
    #Material Wizard Setting
    sMatlist = [MaterialAppPath + r"\MaterialPMMA_2023.png", MaterialAppPath + r"\MaterialSUMITOMO_2023.png", MaterialAppPath + r"\Material_SUMIPEXLW2_2023.png"]
    sMatlist2 =[MaterialAppPath + r"\MaterialPC_2023.png", MaterialAppPath + r"\MaterialCAE_2023.png", MaterialAppPath + r"\MaterialYung_SU_CGF003_2023.png"]
    Material.OpenMaterialWizard(MaterialAppPath + "\\Studio_EM1.png", 200, 0, MaterialAppPath)
    Material.ClickMDXBank(MaterialAppPath)
    Material.SelectPartMaterial(sMatlist)
    Material.MaterialNotAddToUserBank(MaterialAppPath)
    Material.CloseMaterialWizard(MaterialAppPath)
    #Part Insert
    Studio.Wait_Dialog(StudioAppPath, "\\Logo_NonFiber.png")
    Material.OpenMaterialWizard(MaterialAppPath + "\\StudioPartInsert1.png", 200, 0, MaterialAppPath)
    Material.ClickMDXBank(MaterialAppPath)
    Material.SelectPartMaterial(sMatlist2)
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
    Analyzelist = [StudioAppPath + "\\Analysis_CFPCtWS.png", StudioAppPath + "\\Analysis_CoolingCycle4.png", StudioAppPath + "\\Analysis_Filling_2.png", StudioAppPath + "\\Analysis_Packing2.png", StudioAppPath + "\\Analysis_CoolingCycle4.png", StudioAppPath + "\\Analysis_Warpage.png", StudioAppPath + "\\Analysis_Stress2.png"]
    Studio.AnalysisSetting(Analyzelist, StudioAppPath)
    Log.write_log(ProjectName, "Info: Analyze Setting is Finished")
   

    #CMX Tab Flow/Pack Setting
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\ComputationLogo_2023.png")
    #CMX Tab Stress Setting
    CMX.CMX_Tab_Change(CMXAppPath + r"\CMX_Tab_Stress_2.png")
    CMX.StressAnalysisType(CMXAppPath + r"\CMX_Stress_Analysis_Type.png", "Stress")
    Log.write_log(ProjectName, "Info: Computation Parameter Wizard Setting is Finished")
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\CMX_Btn_OK.png")
  
    Studio.SwitchTab(StudioAppPath + r"\BC_tab.png", StudioAppPath + r"\Studio_Tab_B.C_Selected.png")
    Studio.Click_Icon(StudioAppPath, "\\Studio_Tree_Model.png",0)
    Studio.Click_Icon(StudioAppPath, "\\Studio_Tree_Model_Object.png", -38)
    click(Pattern(StudioAppPath + r"\Studio_Tree_Model_part_unselected.png").similar(0.98).targetOffset(-20,0))
    dragDrop(StudioAppPath + r"\Studio_S4_bar.png",StudioAppPath + r"\Studio_S4_Bottom.png")
    click(Pattern(StudioAppPath + r"\Studio_Tree_NonAttribute.png").similar(0.92).targetOffset(-60,0))
    Studio.Click_Icon(StudioAppPath, "\\Fit_to_Window.png",0)
    Studio.SetView("Bottom",StudioAppPath)
    Studio.Click_Icon(StudioAppPath, "\\Fit_to_Window.png",0)
    
    Studio.SetPressure(StudioAppPath + r"\Studio_ENT_IM_S4_Model.png","0.1",StudioAppPath)
    Studio.SetPressure(StudioAppPath + r"\Studio_ENT_IM_S4_Model2.png","0.1",StudioAppPath)
    Studio.SetPressure(StudioAppPath + r"\Studio_ENT_IM_S4_Model3.png","0.1",StudioAppPath)
    #dragDrop(StudioAppPath + r"\Studio_ObjectBar.png",StudioAppPath + r"\Studio_ObjectBar_Bottom.png")
    Studio.SetView("Top",StudioAppPath)
    
    Studio.Click_Icon(StudioAppPath, "\\Btn_Fit_Window.png",0)
    Studio.SetFixConstraint("Stress",StudioAppPath + r"\Studio_ENT_IM_S4_Model4.png",StudioAppPath,"0")
    Studio.SetFixConstraint("Stress",StudioAppPath + r"\Studio_ENT_IM_S4_Model5.png",StudioAppPath,"0")
    Studio.SetFixConstraint("Stress",StudioAppPath + r"\Studio_ENT_IM_S4_Model6.png",StudioAppPath,"0")
    
    Studio.Click_Icon(StudioAppPath, "\\Studio_Tree_Run.png",0)
    #Copy run(2)
    wait(1)

    CRfM.Copy_Run(Pattern(Copypath + "\\Run01.png").similar(0.92), "RunInputDataOnly", "None", "default", Copypath)
    Log.write_log(ProjectName, "Info: Copy Stress to Annealing(Enhance)  is Finished")  
    Studio.Click_Icon(StudioAppPath, "\\Studio_Tree_Model.png",0)
   
    Studio.SetView("Perspective",StudioAppPath)
    Studio.Click_Icon(StudioAppPath, "\\Btn_Fit_Window.png",0)
    mouseMove(StudioAppPath + r"\Studio_ENT_IM_S4_Model9.png")
    Mouse.wheel(WHEEL_UP, 30)
    
    Studio.SetFixConstraint("Stress",StudioAppPath + r"\Studio_ENT_IM_S4_Model18_0.png",StudioAppPath,"0")
    Studio.SwitchTab(StudioAppPath + r"\Tab_home_blue.png", StudioAppPath + r"\Tab_home_white.png")
    

    #CMX Tab Warp Setting
    wait(2)
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\ComputationLogo_2023.png")
    CMX.CMX_Tab_Change(CMXAppPath + r"\CMX_Tab_Warp.png")
    CMX.WarpSolverTypeChange(CMXAppPath + r"\CMX_Warp_Solver.png", "Standard")
    #CMX Tab Stress Setting
    CMX.CMX_Tab_Change(CMXAppPath + r"\CMX_Tab_Stress_2.png")
    CMX.StressAnalysisType(CMXAppPath + r"\CMX_Stress_Analysis_Type.png", "Annealing")
    Log.write_log(ProjectName, "Info: Computation Parameter Wizard Setting is Finished")
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\CMX_Btn_OK.png")
   
   
    #Copy run(3)
    wait(1)
    Studio.Click_Icon(StudioAppPath, "\\Studio_Tree_Run.png", 0)
    CRfM.Copy_Run(Pattern(Copypath + "\\Run01.png").similar(0.92), "RunInputDataOnly", "None", "default", Copypath)
    Log.write_log(ProjectName, "Info: Copy Stress to Annealing(Standard)  is Finished")
    #CMX Tab Warp Setting
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\ComputationLogo_2023.png")
    CMX.CMX_Tab_Change(CMXAppPath + r"\CMX_Tab_Warp.png")
    CMX.WarpSolverTypeChange(CMXAppPath + r"\CMX_Warp_Solver.png", "Enhanced")
    #CMX Tab Stress Setting
    CMX.CMX_Tab_Change(CMXAppPath + r"\CMX_Tab_Stress_2.png")
    CMX.StressAnalysisType(CMXAppPath + r"\CMX_Stress_Analysis_Type.png", "Annealing")
    Log.write_log(ProjectName, "Info: Computation Parameter Wizard Setting is Finished")
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\CMX_Btn_OK.png")
    
    Studio.SwitchTab(StudioAppPath + r"\BC_tab.png", StudioAppPath + r"\Studio_Tab_B.C_Selected.png") 
     
    Studio.Click_Icon(StudioAppPath, "\\Studio_Tree_Model.png",0)
    click(StudioAppPath + r"\Result_Stress.png")
    type(Key.DELETE)
    Studio.SetView("Perspective",StudioAppPath)
    Studio.Click_Icon(StudioAppPath, "\\Btn_Fit_Window.png",0)
 
    Studio.SetFixConstraint("Stress",Pattern(StudioAppPath + r"\Studio_ENT_IM_S4_Model8.png").similar(0.90),StudioAppPath)
   
   
     #Create run(edesign)(4)
    wait(1)
    Studio.SwitchTab(StudioAppPath + r"\Tab_home_blue.png", StudioAppPath + r"\Tab_home_white.png")
    click(StudioAppPath+r"\Studio_NewRun2.png")
    Studio.MeshType("eDesign", StudioAppPath)
    Studio.Home_Model("ImportGeometry", StudioAppPath)
    Studio.ImportGeometry(SourcePath2, StudioAppPath)
    wait(2)
    
    Studio.SwitchTab(StudioAppPath +"\\Studio_Tab_Mesh.png", StudioAppPath + "\\Studio_Tab_Meshing.png")
    
    Studio.Meshing_Generate(StudioAppPath)
    Studio.Meshing_GenerateeDesign(StudioAppPath)
    Studio.Wait_Dialog(StudioAppPath, "\\Log_Generate_Solid_Mesh_Done.png")
    Studio.Final_Check(StudioAppPath)
    Log.write_log(ProjectName, "Info: Create eDesign  is Finished")
    wait(3)
    
    #Material Wizard Setting
    sMatlist = [MaterialAppPath + r"\MaterialPMMA_2023.png", MaterialAppPath + r"\MaterialSUMITOMO_2023.png", MaterialAppPath + r"\Material_SUMIPEXLW2_2023.png"]
    sMatlist2 =[MaterialAppPath + r"\MaterialPC_2023.png", MaterialAppPath + r"\MaterialCAE_2023.png", MaterialAppPath + r"\MaterialYung_SU_CGF003_2023.png"]
    
    Material.OpenMaterialWizard(MaterialAppPath + "\\Studio_EM1.png", 200, 0, MaterialAppPath)
    Material.ClickMDXBank(MaterialAppPath)
    Material.SelectPartMaterial(sMatlist)
    Material.MaterialNotAddToUserBank(MaterialAppPath)
    Material.CloseMaterialWizard(MaterialAppPath)
    #Part Insert
    Studio.Wait_Dialog(StudioAppPath, "\\Logo_NonFiber.png")
    Material.OpenMaterialWizard(MaterialAppPath + "\\StudioPartInsert1.png", 200, 0, MaterialAppPath)
    Material.ClickMDXBank(MaterialAppPath)
    Material.SelectPartMaterial(sMatlist2)
    Material.MaterialNotAddToUserBank(MaterialAppPath)
    Material.CloseMaterialWizard(MaterialAppPath)
    Log.write_log(ProjectName, "Info: Material Wizard Setting is Finished")
    wait(1)
    click(StudioAppPath + r"\Studio_logo.png")
    wait(1)
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
    #Analysis Setting
   
    Analyzelist = [StudioAppPath + "\\Analysis_FPWS.png", StudioAppPath + "\\Analysis_Filling3.png", StudioAppPath + "\\Analysis_Packing2.png", StudioAppPath + "\\Analysis_Warpage.png", StudioAppPath + "\\Analysis_Stress2.png"]
    Studio.AnalysisSetting(Analyzelist, StudioAppPath)
    Log.write_log(ProjectName, "Info: Analyze Setting is Finished")
    #CMX Tab Flow/Pack Setting
    
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\ComputationLogo_2023.png")
    CMX.CMX_Tab_Change(CMXAppPath + r"\CMX_Tab_Warp.png")
    CMX.WarpSolverTypeChange(CMXAppPath + r"\CMX_Warp_Solver.png", "Standard")
    #CMX Tab Stress Setting
    CMX.CMX_Tab_Change(CMXAppPath + r"\CMX_Tab_Stress_2.png")
    CMX.StressAnalysisType(CMXAppPath + r"\CMX_Stress_Analysis_Type.png", "Stress")
    Log.write_log(ProjectName, "Info: Computation Parameter Wizard Setting is Finished")
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\CMX_Btn_OK.png")
    
    Studio.SwitchTab(StudioAppPath + r"\BC_tab.png", StudioAppPath + r"\Studio_Tab_B.C_Selected.png")
    Studio.SetView("Bottom",StudioAppPath)
    Studio.Click_Icon(StudioAppPath, "\\Btn_Fit_Window.png",0)
    Studio.SetPressure(StudioAppPath + r"\Studio_ENT_IM_S4_Model26.png","0.1",StudioAppPath)
    Studio.Click_Icon(StudioAppPath, "\\Studio_Tree_Model.png",0)
    Studio.Click_Icon(StudioAppPath, "\\Studio_Tree_Model_Object.png", -38)
    click(Pattern(StudioAppPath + r"\Studio_Tree_Model_part_unselected.png").similar(0.92).targetOffset(-20,0))
    click(Pattern(StudioAppPath + r"\Studio_Tree_NonAttribute.png").similar(0.92).targetOffset(-60,0))
    
    Studio.SetView("Perspective",StudioAppPath)
    Studio.Click_Icon(StudioAppPath, "\\Fit_To_Window.png",0)
    
  
    Studio.SetFixConstraint("Stress", Pattern(StudioAppPath + r"\Studio_ENT_IM_S4_Model19.png").similar(0.90), StudioAppPath)
   
   
    #Copy run (5)
    wait(2)
    Studio.Click_Icon(StudioAppPath, r"\Studio_Tree_Run_2.png", 0)
    CRfM.Copy_Run(Pattern(Copypath + "\\Run04.png").similar(0.92), "RunInputDataOnly", "None", "default", Copypath)
    Log.write_log(ProjectName, "Info: Copy Stress to Annealing(Standard)  is Finished")
    Studio.SwitchTab(StudioAppPath + r"\Tab_home_blue.png", StudioAppPath + r"\Tab_home_white.png")
    #CMX Tab Flow/Pack Setting
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\ComputationLogo_2023.png")
    #CMX Tab Stress Setting
    CMX.CMX_Tab_Change(CMXAppPath + r"\CMX_Tab_Stress.png")
    CMX.StressAnalysisType(CMXAppPath + r"\CMX_Stress_Analysis_Type.png", "Annealing")
    Log.write_log(ProjectName, "Info: Computation Parameter Wizard Setting is Finished")
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\CMX_Btn_OK.png")
   
    #Copy run(6)
    wait(1)
    Studio.Click_Icon(StudioAppPath, "\\Project_tree_2.png", 0)
    CRfM.Copy_Run(Pattern(Copypath + "\\Run05.png").similar(0.92), "RunInputDataOnly", "None", "default", Copypath)
    Log.write_log(ProjectName, "Info: Copy Stress to Annealing(Standard)  is Finished")
    #CMX Tab Flow/Pack Setting
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\ComputationLogo_2023.png")
    wait(1)
    click(CMXAppPath + r"\CMX_Tab_Warp.png")
    CMX.WarpSolverTypeChange(CMXAppPath + r"\CMX_Warp_Solver.png", "Enhanced")
     #CMX Tab Stress Setting
    CMX.CMX_Tab_Change(CMXAppPath + r"\CMX_Tab_Stress.png")
    CMX.StressAnalysisType(CMXAppPath + r"\CMX_Stress_Analysis_Type.png", "Annealing")
    Log.write_log(ProjectName, "Info: Computation Parameter Wizard Setting is Finished")
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\CMX_Btn_OK.png")


    #Copy run
    wait(1)
    CRfM.Copy_Run(Pattern(Copypath + "\\Run01.png").similar(0.92), "RunInputDataOnly", "None", "default", Copypath)
    Log.write_log(ProjectName, "Info: Copy to only Stress   is Finished")
    #Analyze Setting
    Analyzelist = [StudioAppPath + "\\Analysis_S.png", StudioAppPath + "\\Analysis_Stress2.png"]
    Studio.AnalysisSetting(Analyzelist, StudioAppPath)
    Log.write_log(ProjectName, "Info: Analyze Setting is Finished")
    #CMX Tab Flow/Pack Setting
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\ComputationLogo_2023.png")
    #CMX Tab Stress Setting
    CMX.CMX_Tab_Change(CMXAppPath + r"\CMX_Tab_Stress_2.png")
    CMX.StressAnalysisType(CMXAppPath + r"\CMX_Stress_Analysis_Type.png", "Stress")
    Log.write_log(ProjectName, "Info: Computation Parameter Wizard Setting is Finished")
    CMX.ClickButton(CMXAppPath, CMXAppPath + "\\CMX_Btn_OK.png")
     
      
     #Change Remark Name
    Studio.Click_Icon(StudioAppPath, r"\Studio_Tree_Run.png", 0)
    wait(1)
    Remark_name = ["Stress","Annealing Standard","Annealing Enhanced","edesign Stress","edesign annealing standard","edesign annealing enhanced","Stress only"]
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
    print (ProjectName+" Test is Finished!")
    Log.write_log(ProjectName, "Info: STR Test is Finished!")
   
except:
    os.popen(("python {}").format(exceptprocedureApp))
    print(ProjectName+ "Test is Failed!")
    Log.write_log(ProjectName, "Error: STR Test is Failed!")
Log.write_log2(ProjectName, "Summary")
