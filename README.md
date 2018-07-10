# wordstress

Wordstress is an opensource whitebox security scanner for wordpress powered websites. 

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

Clone this repo and install all of the prereqs. Configure settings in `./conf/`  Written for python2.7+ 
```
pip install requests
pip install BeautifulSoup4
```

### Sample output

```
{
	"themes": {
		"sometheme": {
			"version": "1.0",
			"themestatus": "inactive",
			"themepath": "sometheme"
		}
	},
	"confirmed_vulns": {
		"coreversion": [{
			"title": "WordPress <= x.x.x - Application Denial of Service (DoS) (unpatched)",
			"created_at": "2018-02-05T16:50:40.000Z",
			"updated_at": "2018-02-08T08:18:56.000Z",
			"vuln_type": "DOS",
			"references": {
				"url": [
					"https://thehackernews.com/..."
				],
				"cve": [
					"2018-6389"
				]
			},
			"published_date": "2017-02-05T00:00:00.000Z",
			"fixed_in": null,
			"id": 1111
		}]
	},
	"published_date": "2018-06-27T00:00:00.000Z",
	"fixed_in": "1.2.3",
	"id": 1111,
	"site": "www.yoursite.com/blog/",
	"wp_version": {
		"vulnerabilities": [{
			"title": "Vuln Title Here",
			"created_at": "2018-02-05T16:50:40.000Z",
			"updated_at": "2018-02-08T08:18:56.000Z",
			"vuln_type": "DOS",
			"references": {
				"url": [
					"https://linktoinfoonyourvuln.thanksto.wpvulndbdotcom"
				],
				"cve": [
					"2018-1234"
				]
			},
			"published_date": "2018-02-05T00:00:00.000Z",
			"fixed_in": null,
			"id": 9021
		}]
	}
	"plugins": {
		"Megaplugin For Extra Frop": {
			"pluginstatus": "inactive",
			"wpvulndb": {
				"popular": true,
				"vulnerabilities": [{
					"vulnerablestatus": false,
					"title": "Some Plugin (XSS)",
					"created_at": "2015-10-13T21:22:12.000Z",
					"updated_at": "2015-10-15T13:58:43.000Z",
					"vuln_type": "XSS",
					"references": {
						"url": [
							"http://blog.asdf.com/asdf/"
						]
					},
					"published_date": "2015-10-13T00:00:00.000Z",
					"fixed_in": "1.2.4",
					"id": 8215
				}],
				"last_updated": "2018-06-19T18:18:00.000Z",
				"latest_version": "4.5.6"
			},
			"version": "1.2.3",
			"pluginpath": "path/file.php"
		}
	}
}
```




## Future Roadmap 

Todo developement items:
* Integrate wpvulndb vulnerability lookups for themes.
* Writing json output to a flat file for indexing into other logging solutions.
* GELF Forwarder for Graylog
* packaging for `pip` ?
