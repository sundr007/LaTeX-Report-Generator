import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os

from ReportGenerator import report

scriptPath = os.path.dirname(os.path.abspath(__file__))
os.chdir(scriptPath)

report = report()
print(report.getPath(),flush=True)

def setTitle():
    title = os.path.basename(report.getPath())
    window.title(title)

def open():
    path = filedialog.askdirectory(initialdir = report.getPath())
    report.setPath(path)
    setTitle()
    updateTreeWithTOC()

def new():
    open()
    report.new()
    setTitle()

def quit():
    report.saveSettings()
    window.quit()

def hello():
    print ("hello!")

def updateTreeWithTOC():
    TOC = report.getTOC()
    tree = ttk.Treeview(window)

    tree["columns"]=("one","two")
    tree.column("#0", width=270, minwidth=270, stretch=tk.NO)
    tree.column("one", width=150, minwidth=150, stretch=tk.NO)
    tree.column("two", width=400, minwidth=200)
    tree.heading("#0",text="Section",anchor=tk.W)
    tree.heading("one", text="Folder?",anchor=tk.W)
    tree.heading("two", text="# files",anchor=tk.W)

    for section in TOC:
        if section["level"] == 0:
            level0 = tree.insert("", "end", None, text=section["name"], values=("",""))
        elif section["level"] == 1:
            level1 = tree.insert(level0, "end", None, text=section["name"], values=("",""))
        elif section["level"] == 2:
            level2 = tree.insert(level1, "end", None, text=section["name"], values=("",""))
        elif section["level"] == 3:
            tree.insert(level2, "end", None, text=section["name"], values=("",""))

    tree.pack(side=tk.TOP,fill=tk.X)

window = tk.Tk()
window.geometry("500x400")

class MyDialog:

    def __init__(self, parent,ReportSettings):
        top = self.top = tk.Toplevel(parent)
        self.myLabel1 = tk.Label(top, text='Title')
        self.myLabel1.pack()
        self.myEntryBox1 = tk.Entry(top)
        self.myEntryBox1.insert(0, ReportSettings["Report_Title"])
        self.myEntryBox1.pack()

        self.myLabel2 = tk.Label(top, text='SubTitle')
        self.myLabel2.pack()
        self.myEntryBox2 = tk.Entry(top)
        self.myEntryBox2.insert(0, ReportSettings["Report_Subtitle"])
        self.myEntryBox2.pack()

        self.myLabel3 = tk.Label(top, text='Revision')
        self.myLabel3.pack()
        self.myEntryBox3 = tk.Entry(top)
        self.myEntryBox3.insert(0, ReportSettings["Report_Revision"])
        self.myEntryBox3.pack()

        self.myLabel4 = tk.Label(top, text='Footer1')
        self.myLabel4.pack()
        self.myEntryBox4 = tk.Entry(top)
        self.myEntryBox4.insert(0, ReportSettings["Report_footer_1"])
        self.myEntryBox4.pack()

        self.myLabel5 = tk.Label(top, text='Footer2')
        self.myLabel5.pack()
        self.myEntryBox5 = tk.Entry(top)
        self.myEntryBox5.insert(0, ReportSettings["Report_footer_2"])
        self.myEntryBox5.pack()

        self.myLabel6 = tk.Label(top, text='Footer3')
        self.myLabel6.pack()
        self.myEntryBox6 = tk.Entry(top)
        self.myEntryBox6.insert(0, ReportSettings["Report_footer_3"])
        self.myEntryBox6.pack()

        self.mySubmitButton = tk.Button(top, text='Submit', command=self.send)
        self.mySubmitButton.pack()

    def send(self):
        self.Title      = self.myEntryBox1.get()
        self.SubTitle   = self.myEntryBox2.get()
        self.Revision   = self.myEntryBox3.get()
        self.Footer1    = self.myEntryBox4.get()
        self.Footer2    = self.myEntryBox5.get()
        self.Footer3    = self.myEntryBox6.get()

        self.top.destroy()

def onClick():
    inputDialog = MyDialog(window,report.getReportSettings())
    window.wait_window(inputDialog.top)
    report.loadReportSettings(
            inputDialog.Title      ,
            inputDialog.SubTitle   ,
            inputDialog.Revision   ,
            inputDialog.Footer1    ,
            inputDialog.Footer2    ,
            inputDialog.Footer3    ,
    )
    # print(report.getReportSettings())

# create a toplevel menu
menubar = tk.Menu(window)

# create a pulldown menu, and add it to the menu bar
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=new)
filemenu.add_command(label="Open", command=open)
filemenu.add_command(label="Save", command=report.saveSettings)
filemenu.add_separator()
filemenu.add_command(label="Create Folders from TOC", command=report.createFoldersFromTOC)
filemenu.add_command(label="Cleanup Folders", command=report.DeleteUnusedFolders)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=quit)
menubar.add_cascade(label="File", menu=filemenu)

reportmenu = tk.Menu(menubar, tearoff=0)
reportmenu.add_command(label="Create Report", command=report.CreateReport)
reportmenu.add_separator()
reportmenu.add_command(label="Settings", command=onClick)
menubar.add_cascade(label="Report", menu=reportmenu)


# display the menu
window.config(menu=menubar)


window.mainloop()
