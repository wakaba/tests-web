
_WITH_CHARSET_SUFFIX = BASENAME \
  BASENAME.sjis \
  BASENAME.cp932 \
  BASENAME.euc \
  BASENAME.jis \
  BASENAME.utf8 \
  BASENAME.cp1252 \
  BASENAME.iso88591

JS_FILES = $(subst BASENAME,script-1.js,$(_WITH_CHARSET_SUFFIX))
HTML_FILES = \
  $(subst BASENAME,nocharset-1-nocharset.html,$(_WITH_CHARSET_SUFFIX)) \
  $(subst BASENAME,nocharset-1-sjis.html,$(_WITH_CHARSET_SUFFIX)) \
  $(subst BASENAME,nocharset-1-iso88591.html,$(_WITH_CHARSET_SUFFIX)) \
  $(subst BASENAME,sjis-1-nocharset.html,$(_WITH_CHARSET_SUFFIX)) \
  $(subst BASENAME,sjis-1-sjis.html,$(_WITH_CHARSET_SUFFIX)) \
  $(subst BASENAME,sjis-1-utf8.html,$(_WITH_CHARSET_SUFFIX)) \
  $(subst BASENAME,sjis-1-iso88591.html,$(_WITH_CHARSET_SUFFIX))

SRC2BIN_PL = src2bin.pl
SRC2BIN = perl $(SRC2BIN_PL)

all: $(HTML_FILES) $(JS_FILES)

%.js: %.jssrc $(SRC2BIN_PL)
	$(SRC2BIN) $< > $@

%.sjis: %
	cp $< $@
%.cp932: %
	cp $< $@
%.euc: %
	cp $< $@
%.jis: %
	cp $< $@
%.utf8: %
	cp $< $@
%.cp1252: %
	cp $< $@
%.iso88591: %
	cp $< $@
