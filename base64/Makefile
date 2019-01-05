all: clean update

update: update-wpt update-generated

clean: clean-wpt clean-generated

GENERATED_FILES = \
    decode-generated.json encode-generated.json \
    decodeu-generated.json encodeu-generated.json

update-generated: $(GENERATED_FILES)
clean-generated:
	rm -fr $(GENERATED_FILES)

PERL = ../perl

decode-generated.json: generate-decode.pl
	$(PERL) $< > $@
encode-generated.json: generate-encode.pl
	$(PERL) $< > $@
decodeu-generated.json: generate-decode.pl
	$(PERL) $< base64url > $@
encodeu-generated.json: generate-encode.pl
	$(PERL) $< base64url > $@

update-wpt: LICENSE.wpt decode-wpt.json
clean-wpt:
	rm -fr LICENSE.wpt decode-wpt.json

LICENSE.wpt:
	wget -O $@ https://raw.githubusercontent.com/w3c/web-platform-tests/master/LICENSE.md
decode-wpt.json:
	wget -O $@ https://raw.githubusercontent.com/w3c/web-platform-tests/master/fetch/data-urls/resources/base64.json

## License: Public Domain.
