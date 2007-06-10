all: \
  shift-jis-1997-0.html \
  shift-jis-1997-8.html \
  shift-jis-1997-9.html \
  shift-jis-1997-A.html \
  shift-jis-1997-E.html \
  shift-jis-1997-F.html

shift-jis-1997.tbl:
	wget "http://suika.fam.cx/gate/cvs/*checkout*/char/table/sjis/shift-jis-1997.tbl"

shift-jis-1997-0.html: shift-jis-1997.tbl maketest.pl
	perl maketest.pl 0 $< > $@
shift-jis-1997-8.html: shift-jis-1997.tbl maketest.pl
	perl maketest.pl 8 $< > $@
shift-jis-1997-9.html: shift-jis-1997.tbl maketest.pl
	perl maketest.pl 9 $< > $@
shift-jis-1997-A.html: shift-jis-1997.tbl maketest.pl
	perl maketest.pl 10 $< > $@
shift-jis-1997-E.html: shift-jis-1997.tbl maketest.pl
	perl maketest.pl 14 $< > $@
shift-jis-1997-F.html: shift-jis-1997.tbl maketest.pl
	perl maketest.pl 15 $< > $@

clean:
	rm -fv *~
	rm -fv shift-jis-1997.tbl
