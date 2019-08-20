cd git_overleaf
git pull
xcopy /y ..\media .\media
copy ..\paper.tex paper.tex
copy ..\packages.tex packages.tex
copy ..\institute.tex institute.tex
copy ..\authors.tex authors.tex
copy ..\abstract.tex abstract.tex
copy ..\bib.bib bib.bib
git add .
git rm -f commit.bat
git commit -a -m "commit"
git push origin master