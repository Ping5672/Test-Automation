from sikuli import *
import sys, os
LogAppPath = r"..\..\sikuli_Share\Common.sikuli"

if os.path.isdir(LogAppPath):
    cwd = r"..\.."
else:
    cwd = (str(os.getcwd())).split('MDX_')[0] + r'MDX_' + (str(os.getcwd())).split('MDX_')[1].split('\\')[0]
    
LogAppPath = cwd + r"\sikuli_Share\Common.sikuli"
sys.path.append(LogAppPath)
import log_record as Log

def Setting(Format, Layout, Template):
    #*arg = Format, Layout, Template
    if not exists("{}.png".format(Format)):
        click(Pattern("Format.png").exact().targetOffset(100,0))
        click("{}.png".format(Format))
    if exists("Layout.png"):
        if not exists("{}.png".format(Layout)):
            click(Pattern("Layout.png").exact().targetOffset(100,0))
            click("{}.png".format(Layout))
    type(Pattern("Template.png").exact().targetOffset(100,0), "a",Key.CTRL)
    paste(Template)

def Preferences(ImageFormat, Resolution_Image, VideoFormat, Resolution_Video, Duration, FrameSec, ColorLegend):
    if not exists("{}.png".format(ImageFormat)):
        click("ImageFormat.png")
        click("{}.png".format(ImageFormat))
    if not exists("{}.png".format(Resolution_Image)):
        click("Resolution_Image.png")
        click("{}.png".format(Resolution_Image))
    if not exists("{}.png".format(VideoFormat)):
        click("VideoFormat.png")
        click("{}.png".format(VideoFormat))
    if not exists("{}.png".format(Resolution_Video)):
        click("Resolution_Video.png")
        click("{}.png".format(Resolution_Video))
    if not exists("{}.png".format(Duration)):
        click("Duration.png")
        click("{}.png".format(Duration))
    if not exists("{}.png".format(FrameSec)):
        click("FrameSec.png")
        click("{}.png".format(FrameSec))
    if not exists("{}.png".format(ColorLegend)):
        click("ColorLegend.png")
        click("{}.png".format(ColorLegend))
    
def RunInfo(BaseRun, Compare1, Compare2, Compare3):
    if not exists("{}.png".format(BaseRun)):
        click("BaseRun.png")
        click("{}.png".format(BaseRun))
    if not exists("{}.png".format(Compare1)):
        click("Compare_1.png")
        click("{}.png".format(Compare1))
    if not exists("{}.png".format(Compare2)):
        click("Compare_2.png")
        click("{}.png".format(Compare2))
    if not exists("{}.png".format(Compare3)):
        click("Compare_3.png")
        click("{}.png".format(Compare3))

def SaveAs(ExportRPTPath, **arg):
    #**arg: Name = Name, Location = Location
    try:
        Filepath = []
        if arg:
            if arg.get("Name") == "":
                type(Pattern(ExportRPTPath + "\\Location.png").similar(0.90).targetOffset(100,0), "a",Key.CTRL)
                paste(arg.get("Location"))
                type(Key.ENTER)
                
                type(Pattern(ExportRPTPath + "\\Name.png").similar(0.90).targetOffset(100,0), "a", Key.CTRL)
                type("c", Key.CTRL)
                N = os.popen(r"python" + " " + cwd + r"/sikuli_Share/ExportRPT.sikuli/Clipboard.py", "r") 
                Name = N.read()
                N.close()
                Filepath = [Name.replace("\n", ""), arg.get("Location")]
                
            if arg.get("Location") == "":
                type(Pattern(ExportRPTPath + "\\Name.png").similar(0.90).targetOffset(100,0), "a", Key.CTRL)
                paste(arg.get("Name"))
                type(Key.ENTER)
                
                type(Pattern(ExportRPTPath + "\\Location.png").similar(0.90).targetOffset(100,0), "a", Key.CTRL)
                type("c", Key.CTRL)
                L = os.popen(r"python" + " " + cwd + r"/sikuli_Share/ExportRPT.sikuli/Clipboard.py", "r")
                Location = L.read()
                L.close()    
                Filepath = [arg.get("Name"), Location.replace("\n", "")]
                
            if (arg.get("Name") and arg.get("Location")) != "":
                type(Pattern(ExportRPTPath + "\\Name.png").similar(0.90).targetOffset(100,0), "a", Key.CTRL)
                paste(arg.get("Name"))
                type(Key.ENTER)
                type(Pattern(ExportRPTPath + "\\Location.png").similar(0.90).targetOffset(100,0), "a",Key.CTRL)
                paste(arg.get("Location"))
                type(Key.ENTER)
                Filepath = [arg.get("Name"), arg.get("Location")]

        else:
            type(Pattern(ExportRPTPath + "\\Name.png").similar(0.90).targetOffset(100,0), "a", Key.CTRL)
            type("c", Key.CTRL)
            N = os.popen(r"python" + " " + cwd + r"/sikuli_Share/ExportRPT.sikuli/Clipboard.py", "r") 
            Name = N.read()
            #print(Name.replace("\n", ""))
            N.close()
            Filepath.append(Name.replace("\n", ""))
            #print(Filepath)
            type(Pattern(ExportRPTPath + "\\Location.png").similar(0.90).targetOffset(100,0), "a", Key.CTRL)
            type("c", Key.CTRL)
            L = os.popen(r"python" + " " + cwd + r"/sikuli_Share/ExportRPT.sikuli/Clipboard.py", "r")
            Location = L.read()
            #print(Location.replace("\n", ""))
            L.close()
            Filepath.append(Location.replace("\n", ""))
            #print(Filepath)
        print("def SaveAs has been done")
        Log.write_log("Report", "Info: def SaveAs has been done")
        return Filepath
    except:
        print("def SaveAs has been failed")
        Log.write_log("Report", "Error: def SaveAs has been failed")
        return False
            
def ClickBottom(BtnPic):
    try:
        click(Pattern(BtnPic).similar(0.9))
        print("{} has been clicked".format(BtnPic))
        Log.write_log("Report", "Info: {} has been clicked".format(BtnPic))
        return True
    except:
        print("{} click failed".format(BtnPic))
        Log.write_log("Report", "Error: {} click failed".format(BtnPic))
        return False

def ProgressCheck(ExportRPTPath):
    try:
        if exists(Pattern(ExportRPTPath + "\\RPTGenCompleted.png").exact(), 1800):
            print("def ProgressCheck has been done")
            Log.write_log("Report", "Info: def ProgressCheck has been done")
        else:
            print("def ProgressCheck has been failed-1")
            Log.write_log("Report", "Error: def ProgressCheck has been failed-1")
        return True
    except:
        print("def ProgressCheck has been failed-2")
        Log.write_log("Report", "Error: def ProgressCheck has been failed-2")
        return False
        
def FileCheck(Filepath):
    #print(Filepath)
    try:
        print(Filepath)
        Log.write_log("Report", "{}".format(Filepath))       
        if os.path.isfile("{}\{}.ppt".format(Filepath[1], Filepath[0])):
            print("def FileCheck has been done")
            Log.write_log("Report", "Info: def FileCheck has been done")
            return True
    except:
        print("def FileCheck has been failed")
        Log.write_log("Report", "Error: def FileCheck has been failed")
        return False

def ExportRPT(ExportRPTPath, **arg):
    #**arg: Name = Name, Location = Location
    try:
        if arg:
            arg.setdefault("Name", "")
            arg.setdefault("Location", "")
            if len(arg) == 2:
                Filepath = SaveAs(ExportRPTPath, Name = arg.get("Name"), Location = arg.get("Location"))
            if len(arg) == 1:
                if arg.get("Name") == "":
                    Filepath = SaveAs(ExportRPTPath, Location = arg.get("Location"))
                if arg.get("Location") == "":
                    Filepath = SaveAs(ExportRPTPath, Name = arg.get("Name"))
        else:
            Filepath = SaveAs(ExportRPTPath)
        i = 0
        while (exists(Pattern(ExportRPTPath + "\\Btn_Start.png").exact(), 2) and i <= 2):
            ClickBottom(ExportRPTPath + "\\Btn_Start.png")
            if exists(Pattern(ExportRPTPath + "\\Btn_Yes.png").exact()):
                ClickBottom(ExportRPTPath + "\\Btn_Yes.png")
            wait(2)
            i = i + 1
        ProgressCheck(ExportRPTPath)
        FileCheck(Filepath)
        ClickBottom(ExportRPTPath + "\\Btn_Close.png")
        waitVanish(Pattern(ExportRPTPath + "\\Btn_Close.png").exact(), 10)
        print("Report has been exported")
        Log.write_log("Report", "Info: Report has been exported")
        return True
    except:
        print("Report export failed")
        Log.write_log("Report", "Error: Report export failed")
        return False
        
if __name__ == "__main__":
    ExportRPTPath = r"..\..\sikuli_Share\ExpReport.sikuli"
    if os.path.isdir(ExportRPTPath):
        cwd = r"..\.."
    else:
        cwd = (str(os.getcwd())).split('MDX_')[0] + r'MDX_' + (str(os.getcwd())).split('MDX_')[1].split('\\')[0]
    ExportRPTPath = cwd + r"\sikuli_Share\ExportRPT.sikuli"
    Name = "Test"
    Location = r"C:\Users\Administrator\Desktop\testfolder"
    ExportRPT(ExportRPTPath)
    #ExportRPT(ExportRPTPath, Name = Name, Location = Location)
    #ExportRPT(ExportRPTPath, Name = Name)
    #ExportRPT(ExportRPTPath, Location = Location)
