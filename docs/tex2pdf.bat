::start doc2tex.bat
call del paper.aux
call del paper.bcf
call del paper.log
call del paper.out
call del paper.run.xml
call del paper.synctex.gz
call del paper.bbl
call del paper.blg
call compile.bat
call bibtex.exe "paper"
call compile.bat
call compile.bat