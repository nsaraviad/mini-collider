OBJECTS=anexo_codigo.pdf

all: anexo_codigo.pdf

anexo_codigo.pdf: anexo_codigo.tex
	pdflatex -shell-escape anexo_codigo.tex
	makeindex anexo_codigo.tex
	pdflatex -shell-escape anexo_codigo.tex
	rm -f *.aux *.log *.toc  *.out *.bbl *.blg *.lof *.ind *.ilg

clean:
	rm -f *.aux *.log *.toc  *.out *.bbl *.blg *.lof *.ind *.ilg
	
borrar:
	rm -f *.aux *.log *.toc  *.out *.bbl *.blg *.lof *.ind *.ilg anexo_codigo.pdf
