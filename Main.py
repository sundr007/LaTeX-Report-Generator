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
            level0 = tree.insert("", 0, None, text=section["name"], values=("",""))
        elif section["level"] == 1:
            level1 = tree.insert(level0, "end", None, text=section["name"], values=("",""))
        elif section["level"] == 2:
            level2 = tree.insert(level1, "end", None, text=section["name"], values=("",""))
        elif section["level"] == 3:
            tree.insert(level2, "end", None, text=section["name"], values=("",""))

    tree.pack(side=tk.TOP,fill=tk.X)

window = tk.Tk()
window.geometry("500x400")

# greeting = tk.Label(text="Hello, Tkinter")
# greeting.pack()

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
filemenu.add_command(label="Create Report", command=report.CreateReport)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=quit)
menubar.add_cascade(label="File", menu=filemenu)

# create more pulldown menus
editmenu = tk.Menu(menubar, tearoff=0)
editmenu.add_command(label="Cut", command=hello)
editmenu.add_command(label="Copy", command=hello)
editmenu.add_command(label="Paste", command=hello)
menubar.add_cascade(label="Edit", menu=editmenu)

helpmenu = tk.Menu(menubar, tearoff=0)
helpmenu.add_command(label="About", command=hello)
menubar.add_cascade(label="Preferences", menu=helpmenu)

# display the menu
window.config(menu=menubar)

# test




window.mainloop()
