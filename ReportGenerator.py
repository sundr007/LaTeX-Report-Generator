import pickle
import traceback
import os,re, shutil
import CreateTexFile
import subprocess
from datetime import datetime

class report:
    def __init__(self):
        #set name from variable name. http://stackoverflow.com/questions/1690400/getting-an-instance-name-inside-class-init
        (filename,line_number,function_name,text)=traceback.extract_stack()[-2]
        def_name = text[:text.find('=')].strip()
        self.name = def_name

        try:
            self.load()
        except:
            ##############
            #to demonstrate
            self.path = 'notSet'
            self.TOC = []
            self.Report_Title       = ""
            self.Report_Subtitle    = ""
            self.Report_Revision    = ""
            self.Report_footer_1    = ""
            self.Report_footer_2    = ""
            self.Report_footer_3    = ""
            ##############

            self.saveSettings()
    def load(self):
        """try load self.name.txt"""
        file = open(self.name+'.txt','rb')
        dataPickle = file.read()
        file.close()

        self.__dict__ = pickle.loads(dataPickle)
    def saveSettings(self):
        """save class as self.name.txt"""
        file = open(self.name+'.txt','wb')
        file.write(pickle.dumps(self.__dict__))
        file.close()
    def setPath(self,path):
        self.path = path
    def getPath(self):
        return self.path

    def new(self):
        dataFolder = os.path.join(self.path,'data')
        TOCfile = os.path.join(self.path,'TOC.tex')
        if not os.path.exists(TOCfile):
            file = open(TOCfile,'w')
            file.write(r"\begin{document}"+'\n')
            file.write(r"\section{Section 1}"+'\n')
            file.write(r"\end{document}"+'\n')
            file.close()
        if not os.path.exists(dataFolder):
            os.makedirs(dataFolder)

    def loadReportSettings(self,
                                Report_Title,
                                Report_Subtitle,
                                Report_Revision,
                                Report_footer_1,
                                Report_footer_2,
                                Report_footer_3):
        self.Report_Title = Report_Title
        self.Report_Subtitle = Report_Subtitle
        self.Report_Revision = Report_Revision
        self.Report_footer_1 = Report_footer_1
        self.Report_footer_2 = Report_footer_2
        self.Report_footer_3 = Report_footer_3

    def getReportSettings(self):
        return {    "Report_Title":self.Report_Title,
                    "Report_Subtitle":self.Report_Subtitle,
                    "Report_Revision":self.Report_Revision,
                    "Report_footer_1":self.Report_footer_1,
                    "Report_footer_2":self.Report_footer_2,
                    "Report_footer_3":self.Report_footer_3}

    def loadTOC(self):
        TOCfile = os.path.join(self.path,'TOC.tex')
        if os.path.exists(TOCfile):
            self.TOC = []
            file = open(TOCfile,'r')
            for line in file:
                if "section{" in line:
                    name  = re.findall('{([^"]*)}', line)[0]
                    level = line.count("sub")
                    filepath = os.path.join(self.path,"data",name)
                    if os.path.exists(filepath):
                        exists="Y"
                        nFiles=  len(os.listdir(filepath))
                    else:
                        exists=""
                        nFiles=  0
                    self.TOC.append({"name":name,"level":level,"nFiles":nFiles,"exists":exists})

    def createFoldersFromTOC(self):
        self.loadTOC()
        for section in self.TOC:
            folderName = os.path.join(self.path,"data",section["name"])
            if not os.path.exists(folderName):
                os.makedirs(folderName)

    def getTOC(self):
        self.loadTOC()
        return self.TOC

    def DeleteUnusedFolders(self):
        filepath = os.path.join(self.path,"data")
        files = os.listdir(filepath)
        for file in files:
            path = os.path.join(filepath,file)
            try:
                os.rmdir(path)
            except:
                print(path + " not empty")
    def CreateReport(self):
        title = "%s-%s-%s-%s" % ( datetime.today().strftime('%Y-%m-%d'),
                            self.getReportSettings()["Report_Title"],
                            self.getReportSettings()["Report_Subtitle"],
                            self.getReportSettings()["Report_Revision"],
                            )
        CreateTexFile.createFile(self.path,self.getReportSettings())
        destinationPath = os.path.join(os.getcwd(),"Standard_Test_Report","Test_Report.tex")
        outputFile = os.path.join(os.getcwd(),"Standard_Test_Report","Test_Report.pdf")
        shutil.move("Test_Report.tex",destinationPath)
        for i in range(2):
            subprocess.call(['pdflatex','-interaction', 'nonstopmode',destinationPath],cwd=os.path.join(os.getcwd(),"Standard_Test_Report"),timeout=30)
        shutil.move(outputFile,os.path.join(self.path,"%s.pdf"%title))
