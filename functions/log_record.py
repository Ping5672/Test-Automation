import os, sys
import logging

#import time
#from datetime import date

sikuliShareAppPath = r"..\..\sikuli_Share"
if os.path.isdir(sikuliShareAppPath):
    cwd = r"..\.."
else:
    cwd = os.getcwd()
sikuliShareAppPath = cwd + r"\sikuli_Share"
sys.path.append(sikuliShareAppPath)

def write_log(log_name, message):
    try:
        dev_logger = logging.getLogger(name = log_name)
        
        if not dev_logger.handlers:
            dev_logger.setLevel(logging.DEBUG)

            handler = logging.FileHandler("{}.txt".format(log_name), mode='w')
            formatter = logging.Formatter(
                "[%(asctime)s][%(levelname)s] %(message)s",
                datefmt = "%Y-%m-%d %H:%M:%S",
            )
            handler.setFormatter(formatter)
            dev_logger.addHandler(handler)
        
            #handler1 = logging.StreamHandler()    #test
            #handler1.setFormatter(formatter)    #test
            #dev_logger.addHandler(handler1)    #test

        if "Debug" in message:
            dev_logger.debug(message.replace("Debug: ", ""))
        if "Info" in message:
            dev_logger.info(message.replace("Info: ", ""))
        if "Warning" in message:
            dev_logger.warning(message.replace("Warning: ", ""))
        if "Error" in message:
            dev_logger.error(message.replace("Error: ", "")) 
        if "Critical" in message:            
            dev_logger.critical(message.replace("Critical: ", ""))
        
        print("Write log is done!")
        return True
    
    except:
        print("Write log is failed!")
        return False
        
   
def write_log2(log_name, log2_name):
    try:
        Debug_list = []
        Info_list = []
        Warning_list = []
        Error_list = []
        Critical_list = []
        message_dict = {"Debug":[], "Info":[], "Warning":[], "Error":[], "Critical":[]}
        
        with open("{}.txt".format(log_name)) as fd:
            AllMessage = fd.readlines()
            FinalMessage = AllMessage[-1]
            for line in AllMessage:       
                #print(line)
                if "DEBUG" in line:
                    Debug_list.append(line.replace("\n", ""))
                if "INFO" in line:
                    Info_list.append(line.replace("\n", ""))
                if "WARNING" in line:
                    Warning_list.append(line.replace("\n", ""))
                if "ERROR" in line:
                    Error_list.append(line.replace("\n", ""))
                if "CRITICAL" in line:            
                    Critical_list.append(line.replace("\n", ""))
        message_dict["Debug"] = Debug_list
        message_dict["Info"] = Info_list
        message_dict["Warning"] = Warning_list
        message_dict["Error"] = Error_list
        message_dict["Critical"] = Critical_list

        #print(message_dict)        
        
        with open("{}.txt".format(log2_name), "w+") as f:        
            f.write("[Critical]" + "\n" +
                    "\n".join(message_dict["Critical"]) + "\n" + "\n" +
                    "[Error]" + "\n" +
                    "\n".join(message_dict["Error"]) + "\n" + "\n" +
                    "[Warning]" + "\n" +
                    "\n".join(message_dict["Warning"]) + "\n" + "\n" +
                    "[Info]" + "\n" +
                    "\n".join(message_dict["Info"]) + "\n" + "\n" +
                    "[Debug]" + "\n" +
                    "\n".join(message_dict["Debug"]))
        
        SummaryLog(FinalMessage)
        
        print("Write log2 is done!")
        return True
        
    except:
        SummaryLog(FinalMessage)
        print("Write log2 is failed!")
        return False

def SummaryLog(FinalMessage):
    try:
        logfile = os.path.dirname(sikuliShareAppPath) + r"/SummaryLog.txt"
        with open(logfile, "a+") as f:
            f.write("{}".format(FinalMessage))
            print("SummaryLog is done!")
        return True            
    except:
        print("SummaryLog is failed!")
        return False
   
"""
    logging.basicConfig(
        filename=os.path.join(os.getcwd(),"Log.log"),
        level=logging.DEBUG,
        format="[%(asctime)s] %(message)s",  
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    logging.debug(message)
"""

if __name__ == "__main__": 
    write_log("Studio", "Info: 123")
    write_log("Material", "Info: 456")
    write_log("CMX", "Error: 789")

