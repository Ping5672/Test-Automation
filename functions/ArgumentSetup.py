# -*- coding: UTF-8 -*-
import os, sys

StudioAppPath = r"..\..\sikuli_Share\Studio.sikuli"
if os.path.isdir(StudioAppPath):
    cwd = r"..\.."
else:
    cwd = os.getcwd()

StudioAppPath = cwd + r"\sikuli_Share\Studio.sikuli"
CMAppPath = cwd + r"\sikuli_Share\CM.sikuli"
CommonAppPath = cwd + r"\sikuli_Share\Common.sikuli"
MaterialAppPath = cwd + r"\sikuli_Share\Material.sikuli"
ProcessAppPath = cwd + r"\sikuli_Share\Process.sikuli"
CMXAppPath = cwd + r"\sikuli_Share\CMX.sikuli"
RhinoAppPath = cwd + r"\sikuli_Share/Rhino_Mesh.sikuli"
BCAppPath = cwd + r"\sikuli_Share\Studio.sikuli\Add_BC.sikuli"
CRNAppPath = r"..\..\sikuli_Share\Studio.sikuli\Change_Remark_Name.sikuli"
Copypath = r"..\..\sikuli_Share\Studio.sikuli\Copy_Run_for_MCM.sikuli"
exceptprocedureApp = cwd + r"\sikuli_Share\exceptprocedure\exceptprocedure.py"

sys.path.append(StudioAppPath)
sys.path.append(CMAppPath)
sys.path.append(CommonAppPath)
sys.path.append(MaterialAppPath)
sys.path.append(ProcessAppPath)
sys.path.append(CMXAppPath)
sys.path.append(RhinoAppPath)
sys.path.append(BCAppPath)
sys.path.append(CRNAppPath)
sys.path.append(exceptprocedureApp)

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
