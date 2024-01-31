from sikuli import *
import sys, os
#import _winreg
LogAppPath = r"../sikuli_Share/Common.sikuli"
sys.path.append(LogAppPath)
import log_record as Log

"""
def RhinoRegistrySetting():
    try:
        key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\McNeel\Rhinoceros\6.0\License Manager", 0, _winreg.KEY_WRITE | _winreg.KEY_WOW64_64KEY)
        print("OpenKey is Done!")
        Log.write_log("Registry Setting", "Info: OpenKey is Done!")
        _winreg.SetValueEx(key, "Server", 0, _winreg.REG_SZ, "192.168.130.51")
        print("Set License Manager Value is Done!")
        Log.write_log("Registry Setting", "Info: Set License Manager Value is Done!")
    except:
        print("RhinoRegistrySetting is Failed!")
        Log.write_log("Registry Setting", "Error: RhinoRegistrySetting is Failed!")
    finally:
        _winreg.CloseKey(key)
        print("CloseKey is Done!")
        Log.write_log("Registry Setting", "Info: CloseKey is Done!")
    try:
        key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\McNeel\McNeelUpdate", 0, _winreg.KEY_WRITE | _winreg.KEY_WOW64_64KEY)
        print("OpenKey is Done!")
        Log.write_log("Registry Setting", "Info: OpenKey is Done!")
        _winreg.SetValueEx(key, "Enabled", 0, _winreg.REG_SZ, "0")
        print("Set McNeelUpdate Value is Done!")
        Log.write_log("Registry Setting", "Info: Set McNeelUpdate Value is Done!")
    except:
        print("RhinoRegistrySetting is Failed!")
        Log.write_log("Registry Setting", "Error: RhinoRegistrySetting is Failed!")
    finally:
        _winreg.CloseKey(key)
        print("CloseKey is Done!")
        Log.write_log("Registry Setting", "Info: CloseKey is Done!")
    try:
        key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\McNeel\Rhinoceros\7.0\Install", 0, _winreg.KEY_WRITE | _winreg.KEY_WOW64_64KEY)
        print("OpenKey is Done!")
        Log.write_log("Registry Setting", "Info: OpenKey is Done!")
        _winreg.SetValueEx(key, "enable_automatic_updates", 0, _winreg.REG_SZ, "0")
        _winreg.SetValueEx(key, "send_statistics", 0, _winreg.REG_SZ, "0")
        print("Set Install Value is Done!")
        Log.write_log("Registry Setting", "Info: Set Install Value is Done!")
    except:
        print("RhinoRegistrySetting is Failed!")
        Log.write_log("Registry Setting", "Error: RhinoRegistrySetting is Failed!")
    finally:
        _winreg.CloseKey(key)
        print("CloseKey is Done!")
        Log.write_log("Registry Setting", "Info: CloseKey is Done!")

def ProjectRegistrySetting():
    try:
        key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, r"SOFTWARE\CoreTechSystem\Moldex3D 2022", 0, _winreg.KEY_WRITE | _winreg.KEY_WOW64_64KEY)
        print("OpenKey is Done!")
        Log.write_log("Registry Setting", "Info: OpenKey is Done!")
        _winreg.SetValueEx(key, "ShowStartPage", 0, _winreg.REG_SZ, "0")
        print("Set ShowStartPage Value is Done!")
        Log.write_log("Registry Setting", "Info: Set ShowStartPage Value is Done!")
        _winreg.SetValueEx(key, "UEPEMail", 0, _winreg.REG_SZ, "0")
        print("Set UEPEMail Value is Done!")
        Log.write_log("Registry Setting", "Info: Set UEPEMail Value is Done!")
        _winreg.SetValueEx(key, "UEPSendLogFile", 0, _winreg.REG_SZ, "0")
        print("Set UEPSendLogFile Value is Done!")
        Log.write_log("Registry Setting", "Info: Set UEPSendLogFile Value is Done!")
        _winreg.SetValueEx(key, "UEPSendMDGFile", 0, _winreg.REG_SZ, "0")
        print("Set UEPSendMDGFile Value is Done!")
        Log.write_log("Registry Setting", "Info: Set UEPSendMDGFile Value is Done!")
    except:
        print("ProjectRegistrySetting is Failed!")
        Log.write_log("Registry Setting", "Error: ProjectRegistrySetting is Failed!")
    finally:
        _winreg.CloseKey(key)
        print("CloseKey is Done!")
        Log.write_log("Registry Setting", "Info: CloseKey is Done!")
"""

def RhinoRegSetting():
    try:
        os.popen(('reg add {} /v {} /d {} /f'.format("\"HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\McNeel\Rhinoceros\{}\License Manager\"".format("6.0"), "\"Server\"", "\"192.168.130.51\"")))
        print("Set License Value is Done!")
        Log.write_log("Reg", "Info: Set License Value is Done!")
    except:
        print("Set License Value is Failed!")
        Log.write_log("Reg", "Error: Set License Value is Failed!")
    try:
        os.popen(('reg add {} /v {} /d {} /f'.format("\"HKEY_LOCAL_MACHINE\SOFTWARE\McNeel\McNeelUpdate\"", "Enabled", 0)))
        print("Set McNeelUpdate Value is Done!")
        Log.write_log("Reg", "Info: Set McNeelUpdate Value is Done!")
    except:
        print("Set McNeelUpdate Value is Failed!")
        Log.write_log("Reg", "Error: Set McNeelUpdate Value is Failed!")
    try:
        os.popen(('reg add {} /v {} /d {} /f'.format("\"HKEY_CURRENT_USER\SOFTWARE\McNeel\Rhinoceros\{}\Global Options\Privacy\"".format("5.0"), "\"RhinoSplash.UsageStatsEnabledDialog Shown\"", "0")))
        print("Set Privacy Value is Done!")
        Log.write_log("Reg", "Info: Set Privacy Value is Done!")
    except:
        print("Set Privacy Value is Failed!")
        Log.write_log("Reg", "Error: Set Privacy Value is Failed!")

def ProjectRegSetting():
    try:
        os.popen(('reg add {} /v {} /d {} /f'.format("\"HKEY_CURRENT_USER\SOFTWARE\CoreTechSystem\Moldex3D 2022\"", "\"ShowStartPage\"", 0)))
        print("Set ShowStartPage Value is Done!")
        Log.write_log("Reg", "Info: Set ShowStartPage Value is Done!")
        os.popen(('reg add {} /v {} /d {} /f'.format("\"HKEY_CURRENT_USER\SOFTWARE\CoreTechSystem\Moldex3D 2022\"", "\"UEPEMail\"", 0)))
        print("Set UEPEMail Value is Done!")
        Log.write_log("Reg", "Info: Set UEPEMail Value is Done!")
        os.popen(('reg add {} /v {} /d {} /f'.format("\"HKEY_CURRENT_USER\SOFTWARE\CoreTechSystem\Moldex3D 2022\"", "\"UEPSendLogFile\"", 0)))
        print("Set UEPSendLogFile Value is Done!")
        Log.write_log("Reg", "Info: Set UEPSendLogFile Value is Done!")
        os.popen(('reg add {} /v {} /d {} /f'.format("\"HKEY_CURRENT_USER\SOFTWARE\CoreTechSystem\Moldex3D 2022\"", "\"UEPSendMDGFile\"", 0)))
        print("Set UEPSendMDGFile Value is Done!")
        Log.write_log("Reg", "Info: Set UEPSendMDGFile Value is Done!")
    except:
        print("ProjectRegSetting is Failed!")
        Log.write_log("Reg", "Error: ProjectRegSetting is Failed!")