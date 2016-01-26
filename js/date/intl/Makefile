all: jp-1.html

map-jp-filtered.txt:
	wget -O $@ https://raw.githubusercontent.com/manakai/data-locale/master/data/calendar/day-era/map-jp-filtered.txt

jp-1.html: map2test.pl
	perl map2test.pl < map-jp-filtered.txt > $@
