import os,re,sys
#import tex
#import oct
#import spec
def createFile(fPath,ReportSettings):
    TexFile = open('Test_Report.tex','w')

    TexFile.write(
    r"""
    \documentclass[6pt]{article}
    \usepackage{TestStyle}
    \usepackage{scrextend}
    \usepackage{changepage}
    \usepackage{alltt}

    \usepackage{bookmark,tocloft}
    \bookmarksetup{
      numbered,
      open
    }
    \renewcommand*{\thesection}{\arabic{section}}
    \definecolor{gray}{rgb}{0.8,0.8,0.8}


    \renewcommand{\cftsecfont}{\color{gray}}
    \renewcommand{\cftsubsecfont}{\color{gray}}
    \renewcommand{\cftsubsubsecfont}{\color{gray}}
    %\renewcommand{\cftsubsubsubsecfont}{\color{gray}}
    \renewcommand{\cftsubsecleader}{\color{gray}\cftdotfill{\cftsubsecdotsep}}
    \renewcommand{\cftsubsubsecleader}{\color{gray}\cftdotfill{\cftsubsubsecdotsep}}
    %\renewcommand{\cftsubsubsubsecleader}{\color{gray}\cftdotfill{\cftsubsubsubsecdotsep}}

    %----------------------------------------------------------------------------------------
    %	Load Document name Info
    %----------------------------------------------------------------------------------------
    """)

    TexFile.write("\\newcommand{\\reportTitle}{%s}"%ReportSettings["Report_Title"])
    TexFile.write("\\newcommand{\\subtitle}{%s}"%ReportSettings["Report_Subtitle"])
    TexFile.write("\\newcommand{\\reportrevision}{%s}"%ReportSettings["Report_Revision"])
    TexFile.write("\\newcommand{\\nameone}{}")
    TexFile.write("\\newcommand{\\nametwo}{}")
    TexFile.write("\\newcommand{\\leftfooterone}{%s}"%ReportSettings["Report_footer_1"])
    TexFile.write("\\newcommand{\\leftfooterthree}{%s}"%ReportSettings["Report_footer_3"])
    TexFile.write("\\newcommand{\\leftfootertwo}{%s}"%ReportSettings["Report_footer_2"])


    TexFile.write(
        r"""
    %\input{TitleInfo.tex}
    \setpythontexcontext{path=\MyPath}


    %----------------------------------------------------------------------------------------
    %	TITLE PAGE
    %----------------------------------------------------------------------------------------
    \begin{document}

    \maketitle

    %----------------------------------------------------------------------------------------
    %	TABLE OF CONTENTS
    %----------------------------------------------------------------------------------------
    \newpage
    \addtocontents{toc}{\protect\hypertarget{toc}{}}
    \tableofcontents
    \newpage

    %----------------------------------------------------------------------------------------
    %	Document Contents
    %----------------------------------------------------------------------------------------

    """)



    sectionnumber = 0
    specfilepath = str(fPath)
    filepath = os.path.join(str(fPath),"data")
    TexFile.write(r'\newcommand*{\MyPath}{' + filepath + "}" + os.linesep)
    directories = [ name for name in os.listdir(filepath) if os.path.isdir(os.path.join(filepath, name)) ]
    directoriesStripedName = [ re.sub('\(.*?\)','',name).strip() for name in os.listdir(filepath) if os.path.isdir(os.path.join(filepath, name)) ]
    files = [ name for name in os.listdir(specfilepath) if not os.path.isdir(os.path.join(specfilepath, name)) ]
    for f in files:
     if "TOC.tex" in f:
      with open(specfilepath + '/' + f, encoding='utf-8') as fp:
       for line in fp:
        sectionName=re.findall('{([^"]*)}', line)[0]
        if sectionName in directoriesStripedName:
         data = directories[directoriesStripedName.index(sectionName)]
         filesInDirectory = os.listdir(filepath + '/' + data)
        else:
         filesInDirectory = []
        if not ("section{" in line and "%" not in line and sectionName in directoriesStripedName and filesInDirectory != []):
         if "section{" in line:
          TexFile.write(r"\phantomsection" + os.linesep)
          level  = re.findall('\\\\([^"]*){', line)[0]
          if level == 'section':
           TexFile.write(r"\refstepcounter{section}" + os.linesep)
           TexFile.write(r"\addtocontents{toc}{\protect\contentsline{section}{\protect\numberline{\thesection}\color{gray}{"+sectionName+"}}{}{}}" + os.linesep)
           TexFile.write(r"\setcounter{subsection}{0}" + os.linesep)
           TexFile.write(r"\setcounter{subsubsection}{0}" + os.linesep)
           TexFile.write(r"\setcounter{subsubsubsection}{0}" + os.linesep)
          elif level == 'subsection':
           TexFile.write(r"\refstepcounter{subsection}" + os.linesep)
           TexFile.write(r"\addtocontents{toc}{\protect\contentsline{subsection}{\protect\numberline{\thesubsection}\color{gray}{"+sectionName+"}}{}{}}" + os.linesep)
           TexFile.write(r"\setcounter{subsubsection}{0}" + os.linesep)
           TexFile.write(r"\setcounter{subsubsubsection}{0}" + os.linesep)
          elif level == 'subsubsection':
           TexFile.write(r"\refstepcounter{subsubsection}" + os.linesep)
           TexFile.write(r"\addtocontents{toc}{\protect\contentsline{subsubsection}{\protect\numberline{\thesubsubsection}\color{gray}{"+sectionName+"}}{}{}}" + os.linesep)
           TexFile.write(r"\setcounter{subsubsubsection}{0}" + os.linesep)
          elif level == 'subsubsubsection':
           TexFile.write(r"\refstepcounter{subsubsubsection}" + os.linesep)
           TexFile.write(r"\addtocontents{toc}{\protect\contentsline{subsubsubsection}{\protect\numberline{\thesubsubsubsection}\color{gray}{"+sectionName+"}}{}{}}" + os.linesep)
         # TexFile.write(line.replace('section{','section*{'))
         # level  = re.findall('\\\\([^"]*){', line)[0]
          #TexFile.write(r"\addtocounter{"+level+"}{1}")
         # TexFile.write(r"\phantomsectiontotoc{"+level+"}{"+sectionName+"}")
        else:
         TexFile.write(line.replace("}\n",""))
         a = 0
         b = 0
         for data in directories:
          datawithoutbrackets = re.sub('\(.*?\)','',data).strip()
          if sectionName == datawithoutbrackets:  #returns data with (fail) or (pass) removed
           b=1
           beta = os.listdir(filepath + '/' + data)
           if beta == []:
            pass
           else:
            # TexFile.write(line.replace("}\n",""), end="",flush=True)
     # Pre-Process Folder
            for alpha in beta:
             if ".xls" in alpha or ".xlsx" in alpha:
              fullpath = os.path.join(filepath,data,alpha)
              path = os.path.join(filepath,data)
              os.chdir(path)
              equipment.Excel2CSV(fullpath)
              os.chdir(os.path.join(specfilepath,'pythontex-files-test-report'))
             if ".docx" in alpha:
              if ".docx.pdf" not in alpha:
               fullpath = os.path.join(filepath,data,alpha)
               tex.TexFile.writeWordDocument(fullpath.replace(r'/',r'\\'))
             if ".m" in alpha:
              fullpath = os.path.join(filepath,data,alpha)
              oct.RunOctave(fullpath)
     # Section Title pass fail
            if "(pass)" in data or "pass" in beta:
             TexFile.write(r" \textcolor{green}{(Pass)}}" + os.linesep)
            elif "(Pass)" in data or "pass" in beta:
             TexFile.write(r" \textcolor{green}{(Pass)}}" + os.linesep)
            elif "(fail)" in data or "fail" in beta:
             TexFile.write(r" \textcolor{red}{(Fail)}}" + os.linesep)
            elif "(Fail)" in data or "fail" in beta:
             TexFile.write(r" \textcolor{red}{(Fail)}}" + os.linesep)
            elif "(checked)" in data:
             TexFile.write(r" \textcolor{BurntOrange}{(Checked)}}" + os.linesep)
            elif "(Checked)" in data:
             TexFile.write(r" \textcolor{BurntOrange}{(Checked)}}" + os.linesep)
            else:
             TexFile.write("}" + os.linesep)
            TexFile.write(r"\label{sec:"+str(sectionnumber)+"}" + os.linesep)
            TexFile.write(r"\hyperlink{toc}{\small{Link back to \color{blue}Table of Contents}}\\\\" + os.linesep)
     # Fill with data
            beta = os.listdir(filepath + '/' + data)
            for alpha in beta:
             if ".tex" in alpha:
              a=1
              with open(filepath + '/' + data + '/' + alpha,'r', encoding='utf-8', errors='ignore') as file:
               filedata = file.read()
              TexFile.write(filedata)
             # TexFile.write( '\input{"\MyPath/' + data.replace(" ","\space ") + '/' + alpha.replace(" ","\space ") + '"}')
             if ".txt" in alpha and alpha != 'ReportInput-dont_edit-.txt':
              a=1
              with open(filepath + '/' + data + '/' + alpha,'r') as file:
               filedata = file.read()
              filedata = filedata.replace("\\", r"\textbackslash ")
              filedata = filedata.replace(r'_', r'\_')
              filedata = filedata.replace(r'#', r'\#')
              filedata = filedata.replace(r'%', r'\%')
              filedata = filedata.replace(r'$', r'\$')
              filedata = filedata.replace(r'{', r'\{')
              filedata = filedata.replace(r'}', r'\}')
              filedata = filedata.replace(r'&', r'\&')
              filedata = filedata.replace(r'>', r'\textgreater')
              filedata = filedata.replace(r'<', r'\textless')
              filedata = filedata.replace(r'~', r'\texttt{\~{}}')
              filedata = filedata.replace(r'^', r'\^{}')
              #with open(filepath + '/' + data + '/ReportInput-dont_edit-.txt', 'w') as file:
               #file.write(filedata)
              TexFile.write(filedata)
              #TexFile.write( '\input{"\MyPath/' + data.replace(" ","\space ") + '/ReportInput-dont_edit-.txt"}')
             if ".pdf" in alpha:
              a=1
              if ".docx.pdf" in alpha:
               TexFile.write( r'\includepdf[pages=-,scale=0.8,pagecommand={\pagestyle{fancy}}]{\MyPath/' + data + '/' + alpha + '}' + os.linesep)
              elif ".small.pdf" in alpha:
               TexFile.write(r"\begin{center}" + os.linesep)
               TexFile.write( '\includeCroppedPdf[width=.8\paperwidth,height=.3\paperheight,keepaspectratio]{\MyPath/' + data + '/' + alpha + '}' + os.linesep)
               TexFile.write(r"\end{center}" + os.linesep)
              elif ".smallest.pdf" in alpha:
               TexFile.write(r"\begin{center}" + os.linesep)
               TexFile.write( '\includeCroppedPdf[width=.8\paperwidth,height=.2\paperheight,keepaspectratio]{\MyPath/' + data + '/' + alpha + '}' + os.linesep)
               TexFile.write(r"\end{center}" + os.linesep)
              else:
               TexFile.write(r"\begin{center}" + os.linesep)
               TexFile.write( '\includeCroppedPdf[width=.8\paperwidth,height=.7\paperheight,keepaspectratio]{\MyPath/' + data + '/' + alpha + '}' + os.linesep)
               TexFile.write(r"\end{center}" + os.linesep)
             if ".png" in alpha:
              a=1
              TexFile.write(r"\begin{figure}[H]" + os.linesep)
              TexFile.write(r"\centering" + os.linesep)
              TexFile.write( '\includegraphics[width=.5\paperwidth]{\MyPath/' + data + '/' + alpha + '}' + os.linesep)
              TexFile.write( "\caption{" + alpha.replace(".png","") + "}" + os.linesep)
              TexFile.write( "\label{fig:" + alpha.replace(".png","") + "}" + os.linesep)
              TexFile.write(r"\end{figure}" + os.linesep)
             if ".jpg" in alpha:
              a=1
              TexFile.write(r"\begin{figure}[H]" + os.linesep)
              TexFile.write(r"\centering" + os.linesep)
              TexFile.write( '\includegraphics[width=.5\paperwidth]{\MyPath/' + data + '/' + alpha + '}' + os.linesep)
              TexFile.write( "\caption{" + alpha.replace(".jpg","") + "}" + os.linesep)
              TexFile.write( "\label{fig:" + alpha.replace(".jpg","") + "}" + os.linesep)
              TexFile.write(r"\end{figure}" + os.linesep)
             if ".csv" in alpha and 'statetable.csv' not in alpha:
              a=1
              TexFile.write( '\csv{\MyPath/' + data + '/' + alpha + '}{' + alpha.replace(".csv","") + '}' + os.linesep)
             if 'statetable.csv' in alpha:
              a=1
              TexFile.write( '\statetablecsv{\MyPath/' + data + '/' + alpha + '}{' + alpha.replace("statetable.csv","") + '}' + os.linesep)
             if ".dat" in alpha:
              a=1
              TexFile.write( '\plotfile{\MyPath/' + data + '/' + alpha + '}{' + alpha.replace(".dat","") + '}' + os.linesep)
             if ".pmbus" in alpha:
              a=1
              TexFile.write( '\PMBusSequence{\MyPath/' + data + '/' + alpha + '}')
            if os.path.isdir(filepath + '/' + data + "/embed"):
             beta = os.listdir(filepath + '/' + data + "/embed")
             TexFile.write(r"\noindent" + os.linesep)
             TexFile.write('Embedded Files'+r"\\" + os.linesep)
             TexFile.write(r"\noindent\rule{0.5\linewidth}{0.4pt}" + os.linesep)
             TexFile.write(r"\begin{adjustwidth}{1cm}{}" + os.linesep)
             for alpha in beta:
              TexFile.write(alpha + r'\attachfile{\MyPath/' + data + '/embed/' + alpha + '}' + os.linesep)
             TexFile.write(r"\end{adjustwidth}" + os.linesep)
             TexFile.write(r"\noindent" + os.linesep)
            if os.path.isdir(filepath + '/' + data + "/plots"):
             beta = os.listdir(filepath + '/' + data + "/plots")
             TexFile.write(r"\twocolumn" + os.linesep)
             for alpha in beta:
              if ".pdf" in alpha:
               a=1
               TexFile.write( '\smallpic{\MyPath/' + data + '/plots/' + alpha + '}{' + alpha.replace(".pdf","") + '}' + os.linesep)
               TexFile.write(r"\hyperref[sec:"+str(sectionnumber)+"]{\color{blue}Back}" + os.linesep)
              if ".png" in alpha:
               a=1
               TexFile.write( '\smallpic{\MyPath/' + data + '/plots/' + alpha + '}{' + alpha.replace(".png","") + '}' + os.linesep)
               TexFile.write(r"\hyperref[sec:"+str(sectionnumber)+"]{\color{blue}Back}" + os.linesep)
               TexFile.write(r" " + os.linesep)
               for aaa in beta:
                if (alpha.replace(".png",".csv")) in aaa:
                 TexFile.write( '\smallcsv{\MyPath/' + data + '/plots/' + alpha.replace(".png",".csv") + '}{}' + os.linesep)
             TexFile.write(r"\onecolumn" + os.linesep)
            if os.path.isdir(filepath + '/' + data + "/labelplots"):
             beta = os.listdir(filepath + '/' + data + "/labelplots")
             TexFile.write(r"\begin{longtable}{ll}" + os.linesep)
            # TexFile.write(r"\centering" + os.linesep)
             TexFile.write(r"\toprule" + os.linesep)
             TexFile.write(r"name  & link \\" + os.linesep)
             TexFile.write(r"\midrule" + os.linesep)
             for alpha in beta:
              if ".pdf" in alpha or ".png" in alpha:
               TexFile.write(alpha.replace(".png","") + " & \hyperref[fig:"+alpha.replace(".png","") + r"]{\color{blue}fig \ref*{fig:"+alpha.replace(".png","")+ r"}} \\" + os.linesep)
             TexFile.write(r"\bottomrule" + os.linesep)
             TexFile.write(r"\end{longtable}" + os.linesep)
             TexFile.write(r"\twocolumn" + os.linesep)
             for alpha in beta:
              if ".pdf" in alpha:
               a=1
               TexFile.write( '\smallpic{\MyPath/' + data + '/labelplots/' + alpha + '}{' + alpha.replace(".pdf","") + '}' + os.linesep)
               TexFile.write(r"\hyperref[sec:"+str(sectionnumber)+"]{\color{blue}Back}" + os.linesep)
              if ".png" in alpha:
               a=1
               TexFile.write( '\smallpic{\MyPath/' + data + '/labelplots/' + alpha + '}{' + alpha.replace(".png","") + '}' + os.linesep)
               TexFile.write(r"\hyperref[sec:"+str(sectionnumber)+"]{\color{blue}Back}" + os.linesep)
             TexFile.write(r"\onecolumn" + os.linesep)
          if b == 0:
           pass
           #TexFile.write("}")
          if a == 0:
           pass
          # TexFile.write('NA')
          sectionnumber = sectionnumber + 1

    TexFile.write(
    r"""

    %----------------------------------------------------------------------------------------
    %	End Document
    %----------------------------------------------------------------------------------------
    \end{document}
    """)

    TexFile.close()
