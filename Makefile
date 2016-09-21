
PARTS = abstract.tex \
				acknowledgements.tex \
				tableofcontents.tex \
				chapter-intro.tex \
				chapter-darkmatter.tex \
				chapter-gammarays.tex \
				chapter-veritas.tex \
				chapter-reconstruction.tex \
				chapter-analysis.tex \
				chapter-conclusion.tex \
				bibliography.tex \
				citelist.bib \
				appendix.tex \
				
	

pdf : thesis.tex $(PARTS)
	if [ ! -d "tmp" ]; then mkdir tmp ; fi
	latexmk -f -dvi- -pdf -jobname=tmp/thesis thesis.tex -pdflatex='pdflatex -synctex=1 -interaction=nonstopmode --src-specials -shell-escape'

