import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os,platform,subprocess

from ReportGenerator import report
from Dialog import MyDialog

class App:
    def __init__(self):
        scriptPath = os.path.dirname(os.path.abspath(__file__))
        os.chdir(scriptPath)
        self.report = report()

        print(self.report.getPath(),flush=True)
        self.window = tk.Tk()
        self.window.geometry("500x600")

        # create a toplevel menu
        menubar = tk.Menu(self.window)

        # create a pulldown menu, and add it to the menu bar
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=self.new)
        filemenu.add_command(label="Open", command=self.open)
        filemenu.add_command(label="Save", command=self.report.saveSettings)
        filemenu.add_separator()
        filemenu.add_command(label="Create Folders from TOC", command=self.report.createFoldersFromTOC)
        filemenu.add_command(label="Cleanup Folders", command=self.report.DeleteUnusedFolders)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        reportmenu = tk.Menu(menubar, tearoff=0)
        reportmenu.add_command(label="Create Report", command=self.report.CreateReport)
        reportmenu.add_separator()
        reportmenu.add_command(label="Settings", command=self.onClick)
        menubar.add_cascade(label="Report", menu=reportmenu)

        # display the menu
        self.window.config(menu=menubar)
        self.window.mainloop()

    def setTitle(self):
        title = os.path.basename(self.report.getPath())
        self.window.title(title)

    def open(self):
        path = filedialog.askdirectory(initialdir = self.report.getPath())
        self.report.setPath(path)
        self.setTitle()
        self.updateTreeWithTOC()

    def new(self):
        open()
        self.report.new()
        setTitle()

    def quit(self):
        self.report.saveSettings()
        self.window.quit()

    def hello(self):
        print ("hello!")

    def onClick(self):
        inputDialog = MyDialog(self.window,self.report.getReportSettings())
        self.window.wait_window(inputDialog.top)
        self.report.loadReportSettings(
                inputDialog.Title      ,
                inputDialog.SubTitle   ,
                inputDialog.Revision   ,
                inputDialog.Footer1    ,
                inputDialog.Footer2    ,
                inputDialog.Footer3    ,
        )

    def OnDoubleClick(self,event):
        item = self.tree.selection()[0]
        name = self.tree.item(item,"text")
        print("you clicked on", name)
        filepath = os.path.join(self.report.getPath(),"data",name)
        if os.path.exists(filepath):
            self.open_file(filepath)

    def open_file(self,path):
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])

    def updateTreeWithTOC(self):
        TOC = self.report.getTOC()
        self.tree = ttk.Treeview(self.window)

        self.tree["columns"]=("one","two")
        self.tree.column("#0", width=270, minwidth=270)
        self.tree.column("one", width=75, minwidth=75)
        self.tree.column("two", width=400, minwidth=200)
        self.tree.heading("#0",text="Section",anchor=tk.W)
        self.tree.heading("one", text="Folder?",anchor=tk.W)
        self.tree.heading("two", text="# files",anchor=tk.W)

        for section in TOC:
            if section["level"] == 0:
                level0 = self.tree.insert("", "end", None,open=True, text=section["name"], values=(section["exists"],section["nFiles"]))
            elif section["level"] == 1:
                level1 = self.tree.insert(level0, "end", None,open=True, text=section["name"], values=(section["exists"],section["nFiles"]))
            elif section["level"] == 2:
                level2 = self.tree.insert(level1, "end", None,open=True, text=section["name"], values=(section["exists"],section["nFiles"]))
            elif section["level"] == 3:
                self.tree.insert(level2, "end", None,open=True, text=section["name"], values=(section["exists"],section["nFiles"]))
        self.tree.bind("<Double-1>", self.OnDoubleClick)
        self.tree.pack(side=tk.TOP,fill=tk.X)

if __name__ == "__main__":
    app = App()
