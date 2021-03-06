
PARTS = abstract.tex \
				acknowledgements.tex \
				tableofcontents.tex \
				chapter-1intro.tex \
				chapter-2darkmatter.tex \
				chapter-3gammarays.tex \
				chapter-4veritas.tex \
				chapter-5reconstruction.tex \
				chapter-6analysis.tex \
				chapter-7conclusion.tex \
				chapter-8bibliography.tex \
				citelist.bib \
				chapter-9appendix.tex \
				
	

pdf : thesis.tex $(PARTS)
	if [ ! -d "tmp" ]; then mkdir tmp ; fi
	latexmk -f -dvi- -pdf -jobname=tmp/thesis thesis.tex -pdflatex='pdflatex -synctex=1 -interaction=nonstopmode --src-specials -shell-escape' ; cp tmp/thesis.pdf tmp/thesis_duplicate.pdf ; cp tmp/thesis.pdf tmp/dissertation_kelley-hoskins_nathan.pdf

