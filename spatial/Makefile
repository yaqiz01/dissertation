PAPER = main
TEX = $(wildcard *.tex text/*.tex)
BIB = references.bib
FIGS = $(wildcard figs/*.pdf figs/*.png graphs/*.pdf graphs/*.png)

.PHONY: all export clean lunch

$(PAPER).pdf: $(TEX) $(BIB) $(FIGS) jpaper.cls
	echo $(FIGS)
	pdflatex $(PAPER)
	bibtex $(PAPER)
	pdflatex $(PAPER)
	pdflatex $(PAPER)
	bash publish.sh $(PAPER).pdf

lunch: $(PAPER).pdf
	bash publish.sh $(PAPER).pdf

test: $(TEX) $(BIB) $(FIGS) jpaper.cls
	echo $(FIGS)
	pdflatex $(PAPER)
	bibtex $(PAPER)
	pdflatex $(PAPER)
	pdflatex $(PAPER)

# figs/speedupbars.tex: figs/speedupbars.gp figs/speedupbars.dat
# 	cd figs && gnuplot speedupbars.gp
# 	cd figs && sed -i.bak 's/speedupbars/figs\/speedupbars/' speedupbars.tex

clean:
	rm -f *.aux *.bbl *.blg *.log *.out $(PAPER).pdf

