# py-wordstress

Wordstress is an opensource whitebox security scanner for wordpress powered websites. T

## Description

Wordstress plugin: https://wordpress.org/plugins/wordstress/

This is a fork of the original wordstress project:
https://github.com/thesp0nge/wordstress

The primary goal of this python module was to help those who are struggling to inventory their wordpress sites, and to correlate the results with wpvulndb to make an indexable json output. I created this python module because I found most of the wordstress ruby gems weren't being updated anymore, and I know python better than ruby. Also the existing ruby gem versions were lacking a verbose indexable output, as well as a full inventory of all plugins, themes, and core versions.

`wordstress.py` will run against whatever you define in `./conf/sites.conf` and POST those results to your splunk HTTP Event Collector

## Installation
### Plugin install:
To install the [wordstress plugin for
wordpress](https://wordpress.org/plugins/wordstress/) you must:

* download wordstress.zip and unpack the content to your `/wp-content/plugins/` directory
* activate the plugin through the `Plugins` menu in WordPress
* navigate the `Settings->Wordstress` admin page
* every time you enter wordstress setting page, a new key is automagically
  generated, to increase entropy you may want to reload the page a couple of
  times. When you're comfortable with the generated key, press the "Save Changes"
  button.
  The virtual page is now available at the url http://youblogurl/wordstress?wordstress-key=the_key

### wordstress Install

Clone this repo and install all of the prereqs. Written for python2.7+ 
```

pip install requests
pip install BeautifulSoup4
```


## Future Roadmap 

Todo developement items:
* Integrate wpvulndb vulnerability lookups for themes.
* Writing json output to a flat file for indexing into other logging solutions.
* GELF Forwarder for Graylog
* packaging for `pip` ?
