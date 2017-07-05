NAME=Masterarbeit
COMPILE=pdflatex -halt-on-error
COMPILE_SYNC=$(COMPILE) -synctex=15 -undump=pdflatex
#COMPILE=tectonic --keep-intermediates --print --reruns 2

all: build

open: all
	open $(NAME).pdf &> /dev/null || xdg-open $(NAME).pdf

prepare: clean
	python3 prepare.py

build: prepare
	python3 bibarchive.py
	$(COMPILE) $(NAME).tex
	biber $(NAME)
	texindy $(NAME).idx
	makeglossaries $(NAME)
	$(COMPILE) $(NAME).tex
	$(COMPILE) $(NAME).tex
	$(COMPILE_SYNC) $(NAME).tex

deploy:
	scp $(NAME).pdf hetzner:

clean:
	git clean -f -X

