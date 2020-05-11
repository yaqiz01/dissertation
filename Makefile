
MAIN=text/thesis
SIG=text/signature

thesis.pdf: text/* figs/*
	latexmk -pdf $(MAIN).tex
	latexmk -c thesis.pdf

sig:
	latexmk -pdf $(SIG).tex
	latexmk -c

env: requirements.txt
ifeq ("$(wildcard env/)","")
	virtualenv -p python3.7 env
endif
	env/bin/pip install -r requirements.txt

clean:
	latexmk -c

