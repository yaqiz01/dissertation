MAIN=text/thesis
SIG=text/signature

all:
	latexmk -pdf -f $(MAIN).tex
	latexmk -c

sig:
	latexmk -pdf -f $(SIG).tex
	latexmk -c

clean:
	latexmk -c

