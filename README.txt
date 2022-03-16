MANUAL:
The script accepts valid sreality search result urls - i.e. the first url that loads after adjusting 
search filters on the sreality search page and hitting Enter. It should look something like:
https://www.sreality.cz/hledani/pronajem/komercni/sklady,vyrobni-prostory,ordinace/moravskoslezsky-kraj?plocha-od=1000&plocha-do=10000000000
If given invalid url, the script returns a warning and lets the user enter an url again.


BUGFIXES:
20.1.2022 - fixed a bug where the first results page didnt load correctly (due to some internal sreality magic, adding '&strana=1' to the end of url seems to break the filtering a bit, while '&strana=n' for n>1 works.