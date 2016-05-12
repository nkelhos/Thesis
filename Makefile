# To get a pdf, type 'make'

# File Suffixes
.SUFFIXES: .tex .dvi .eps .ps .pdf .jpg .jpg.bb .gif .gif.bb

#
# Basic variables
RM       = rm
LATEX    = latex
BIBTEX   = bibtex
DVIPS    = dvips
DVIPDF   = dvipdf
PS2PDF   = ps2pdf
MAINFILE = thesis
#STYFILE  = mtustyle.sty
STYFILE  = citelist.sty

#
# List of files
TEXFILES = tableofcontents.tex        \
           abstract.tex               \
           chapter-intro.tex          \
           chapter-veritas.tex        \
           chapter-darkmatter.tex     \
           chapter-reconstruction.tex \
           chapter-analysis.tex       \
           chapter-conclusion.tex     \
           appendix.tex               \
           bibliography.tex           \
           citelist.bib

IMAGES = images/thesis.imageintersections.eps \
				 images/thesis.iactarray.eps \
				 images/mirror_polaris.eps

#Dedication.tex       \
#Acknowledgments.tex  \

#
# Different make options
# Default target
all: $(MAINFILE).pdf clean

images/thesis.imageintersections.eps : images/thesis.imageintersections.png
	convert $< $@

images/thesis.iactarray.eps : images/thesis.iactarray.png
	convert $< $@

images/mirror_polaris.eps : images/mirror_polaris.png
	convert $< $@

$(MAINFILE): $(MAINFILE).dvi

$(MAINFILE).aux:
	-if [ ! -f $(MAINFILE).aux ]; then touch $(MAINFILE).aux; fi

$(MAINFILE).dvi: $(MAINFILE).tex $(STYFILE) $(TEXFILES) $(IMAGES)
	@echo
	@echo "  Making DVI document"
	-$(LATEX) $(MAINFILE)
	-$(LATEX) $(MAINFILE)
	-$(BIBTEX) $(MAINFILE)
	-$(BIBTEX) $(MAINFILE)
	-$(LATEX) $(MAINFILE)
	-$(LATEX) $(MAINFILE)

$(MAINFILE).bbl: $(MAINFILE).bib
	-if [ ! -f $(MAINFILE).aux ]; then touch $(MAINFILE).aux; fi
	-$(BIBTEX) $(MAINFILE)

pdf: $(MAINFILE).pdf

$(MAINFILE).pdf: $(MAINFILE).ps
	@echo
	@echo "  Making PDF document (embedded fonts)"
	@echo
	$(PS2PDF) -dPDFSETTINGS=/prepress -dSubsetFonts=true -dEmbedAllFonts=true -dMaxSubsetPct=100 $< $@
	@echo
	@echo

ps: $(MAINFILE).ps

$(MAINFILE).ps:  $(MAINFILE).dvi
	@echo
	@echo "  Making PostScript document"
	@echo
	$(DVIPS) -R0 -Ppdf -G0 -t letter -o $@ $<
	@echo
	@echo

clean:
	@echo
	@echo "  Cleaning up files associated with $(MAINFILE).tex"
	@echo
	$(RM) -f *.aux
	$(RM) -f *.bbl
	$(RM) -f *.blg
	$(RM) -f *.dvi
	$(RM) -f *.ilg
	$(RM) -f *.lof
	$(RM) -f *.log
	$(RM) -f *.lot
	$(RM) -f *.mtc
	$(RM) -f *.out
	$(RM) -f *.ps
	$(RM) -f *.toc
	@echo
	@echo

