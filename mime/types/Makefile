all: clean update

update: update-wpt
clean: clean-wpt

update-wpt: LICENSE.wpt \
    canon-wpt-mime-types.json canon-wpt-generated-mime-types.json
clean-wpt:
	rm -fr LICENSE.wpt
	rm -fr canon-wpt-mime-types.json canon-wpt-generated-mime-types.json

LICENSE.wpt:
	wget -O $@ https://raw.githubusercontent.com/w3c/web-platform-tests/master/LICENSE.md
canon-wpt-mime-types.json:
	wget -O $@ https://raw.githubusercontent.com/w3c/web-platform-tests/master/mimesniff/mime-types/resources/mime-types.json
canon-wpt-generated-mime-types.json:
	wget -O $@ https://raw.githubusercontent.com/w3c/web-platform-tests/master/mimesniff/mime-types/resources/generated-mime-types.json

## License: Public Domain.
