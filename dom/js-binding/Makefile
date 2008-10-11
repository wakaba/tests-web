PERL = perl -I/home/httpd/html/www/markup/html/whatpm
WTTJS_PL = /home/httpd/html/www/webidl2tests/bin/wttjs.pl

all: webdomcore html xhr

webdomcore:
	$(PERL) $(WTTJS_PL) --idl-file-name idls/webdomcore-20081008.idl \
	    --instances-file-name idls/webdomcore.json \
	    --test-dir-name tests/ \
	    --testset-id webdomcore-20081008

html:
	$(PERL) $(WTTJS_PL) --idl-file-name idls/html5-r2321.idl \
	    --instances-file-name idls/html.json \
	    --test-dir-name tests/ \
	    --testset-id html5-r2321

xhr:
	$(PERL) $(WTTJS_PL) --idl-file-name idls/xhr2-20081006.idl \
	    --instances-file-name idls/xhr.json \
	    --test-dir-name tests/ \
	    --testset-id xhr2-20081006
