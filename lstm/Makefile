PAPER = main
TEX = $(wildcard *.tex text/*.tex)
BIB = references.bib
FIGS = $(wildcard figs/*.pdf figs/*.png graphs/*.pdf graphs/*.png)
CODE = $(wildcard code/*)

.PHONY: all export clean

$(PAPER).pdf: $(TEX) $(BIB) $(FIGS) $(CODE)
	echo $(FIGS)
	pdflatex $(PAPER)
	bibtex $(PAPER)
	pdflatex $(PAPER)
	pdflatex $(PAPER)
	#cp main.pdf ~/Dropbox/SYSML_RNN_DRAFT/

lunch: $(PAPER).pdf
	bash publish.sh $(PAPER).pdf

test: $(TEX) $(BIB) $(FIGS)
	echo $(FIGS)
	pdflatex $(PAPER)
	bibtex $(PAPER)
	pdflatex $(PAPER)
	pdflatex $(PAPER)

continuous:
	latexmk -pdf -pvc -halt-on-error main

# figs/speedupbars.tex: figs/speedupbars.gp figs/speedupbars.dat
# 	cd figs && gnuplot speedupbars.gp
# 	cd figs && sed -i.bak 's/speedupbars/figs\/speedupbars/' speedupbars.tex

clean:
	rm -f *.aux *.bbl *.blg *.log *.out $(PAPER).pdf

