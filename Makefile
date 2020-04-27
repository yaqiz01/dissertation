
MAIN=text/thesis
SIG=text/signature

thesis.pdf: text/*
	latexmk -pdf $(MAIN).tex
	latexmk -c thesis.pdf

sig:
	latexmk -pdf $(SIG).tex
	latexmk -c

clean:
	latexmk -c

