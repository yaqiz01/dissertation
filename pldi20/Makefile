TARGET=supplement
#TARGET=paper
all: pdf

pdf:
	latexmk -pdf -f $(TARGET).tex
	latexmk -c

pvc:
	latexmk -pdf -pvc $(TARGET).tex

clean:
	latexmk -c
	rm -f paper.tdo

cleanall:
	latexmk -C
	rm -f paper.tdo

# ps:
# 	 latexmk -pdfps $(TARGET).tex

proof:
	echo "weasel words: "
	sh helpers/weasel-words.sh *.tex
	echo
	echo "passive voice: "
	sh helpers/passive.sh *.tex
	echo
	echo "duplicates: "
	perl helpers/dups.pl *.tex

PAPER:=paper
lunch: $(PAPER).pdf
	#bash publish.sh $(PAPER).pdf
#ifeq ($(USER),Yaqi)
	#cp main.pdf ~/Dropbox/Plasticine
#endif
	echo "Publishing $(PAPER).pdf to group lunch website"
	scp $(PAPER).pdf root@ppl.stanford.edu:/root/drafts/pldi20_pir.pdf

