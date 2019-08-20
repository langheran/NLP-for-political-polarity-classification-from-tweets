#MaxThreads 1

;Haystack = \textless{}latex\textgreater{}\textbackslash{}cite\{Wen2015\}\textless{}/latex\textgreater{} Hello \textless{}latex\textgreater{}\textbackslash{}cite\{Wen2016\}\textless{}/latex\textgreater{}
Loop, 2
{
	FileRead, Haystack, % A_ScriptDir . "\paper.tex"
	Loop, 10
	{
		p := 1, m := ""
		while p := RegExMatch(Haystack, "is)(\\textless\{\}(latex|latexnb|bibliography)\\textgreater\{\}(.*?)\\textless\{\}\/(latex|latexnb|bibliography)\\textgreater\{\})", m, p + StrLen(m))
		{
			match%A_Index% := m1
			Callout(m1)
		}
	}
	FileDelete, % A_ScriptDir . "\paper.tex"
	file := FileOpen(A_ScriptDir . "\paper.tex", "w")
	file.Write(Haystack)
	file.Close()
	Sleep, 500
}

Callout(m) {
	global Haystack
	original:=m
	if(InStr(m, "\textless{}bibliography\textgreater{}"))
	{
		m:=RegExReplace(m, "is)(\\textless\{\}bibliography\\textgreater\{\})")
		m:=RegExReplace(m, "is)(\\textless\{\}\/bibliography\\textgreater\{\})")
		m:=RegExReplace(m, "\\\{","{")
		m:=RegExReplace(m, "\\\}","}")
		m:=RegExReplace(m, "\\\]","]")
		m:=RegExReplace(m, "\\\[","[")
		m:=RegExReplace(m, "\\\$","$")
		m:=RegExReplace(m, "\\\_","_")
		m:=RegExReplace(m, "\\\^","^")
		m:=RegExReplace(m, "\{\[\}","[")
		m:=RegExReplace(m, "\{\]\}","]")
		m:=RegExReplace(m, "\\textbackslash{}","\")
		new:=m
		Haystack:=StrReplace(Haystack, original)
		FileDelete, % A_ScriptDir . "\bib.bib"
		file := FileOpen(A_ScriptDir . "\bib.bib", "w")
		file.Write(new)
		file.Close()
	}
	else
	{
		nobreaks:=0
		if(InStr(m, "\textless{}latexnb\textgreater{}"))
		{
			m:=RegExReplace(m, "latexnb", "latex")
			nobreaks:=1
		}
		m:=RegExReplace(m, "is)(\\textless\{\}latex\\textgreater\{\})")
		m:=RegExReplace(m, "is)(\\textless\{\}\/latex\\textgreater\{\})")
		m:=RegExReplace(m, "\\\{","{")
		m:=RegExReplace(m, "\\\}","}")
		m:=RegExReplace(m, "\\\]","]")
		m:=RegExReplace(m, "\\\[","[")
		m:=RegExReplace(m, "\\\$","$")
		m:=RegExReplace(m, "\\\_","_")
		m:=RegExReplace(m, "\\\^","^")
		m:=RegExReplace(m, "\{\[\}","[")
		m:=RegExReplace(m, "\{\]\}","]")
		m:=RegExReplace(m, "\\textbackslash{}","\")
		if(nobreaks)
		{
			m:=RegExReplace(m, "is)\.[\n\r]+", "<br>")
			m:=RegExReplace(m, "is)[\n\r]+", " ")
			Loop, 15
				m:=RegExReplace(m, "is)[\s]+", " ")
			m:=RegExReplace(m, "is)[\n\r]+", " ")
			m:=RegExReplace(m, "\<br\>", "`r`n")
		}
		new:=m
		Haystack:=StrReplace(Haystack, original, new)
	}
}