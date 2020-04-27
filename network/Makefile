PAPER = main
TEX = $(wildcard *.tex text/*.tex)
BIB = references.bib
FIGS = $(wildcard figs/*.pdf figs/*.png graphs/*.pdf graphs/*.png)

.PHONY: all export clean env

$(PAPER).pdf: $(TEX) $(BIB) $(FIGS) code/ jpaper.cls
	echo $(FIGS)
	pdflatex -shell-escape $(PAPER)
	bibtex $(PAPER)
	pdflatex -shell-escape $(PAPER)
	pdflatex -shell-escape $(PAPER)

lunch: $(PAPER).pdf
	#bash publish.sh $(PAPER).pdf
ifeq ($(USER),Yaqi)
	cp main.pdf ~/Dropbox/Plasticine
endif

test: $(TEX) $(BIB) $(FIGS) jpaper.cls
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

env:
	virtualenv -p python3 env3 
	env3/bin/pip install -r requirements3.txt

clean:
	rm -f *.aux *.bbl *.blg *.log *.out $(PAPER).pdf

