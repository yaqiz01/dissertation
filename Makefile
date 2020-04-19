
MAIN=text/thesis
SIG=text/signature

thesis.pdf: text/*
	latexmk -pdf $(MAIN).tex
	latexmk -c

sig:
	latexmk -pdf $(SIG).tex
	latexmk -c

clean:
	latexmk -c

