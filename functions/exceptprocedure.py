import os

exelist = ["Rhino.exe", "mdxmatwzd.exe", "MdxPro.exe", "MDXStudio.exe", "MDXProject.exe"]

for x in range(len(exelist)):
    s = os.system(("tasklist /FI ""\"IMAGENAME eq {}""\" 2>NUL | find /I /N ""\"{}""\">NUL").format(exelist[x], exelist[x])) #Check *.exe is running or not
    if (s==0): #if *.exe is running
        print (("taskkill /f /im {}").format(exelist[x]))
        os.system(("taskkill /f /im {}").format(exelist[x])) #task kill *.exe
