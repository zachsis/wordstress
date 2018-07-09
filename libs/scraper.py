try:
    import requests
except:
    print "[!] please install 'requests' python module: (pip install requests)"
try:
    import bs4
except:
    print "[!] please install 'requests' python module: (pip install beautifulsoup4)"

import re


class WordstressScraper(object):
    def __init__(self, _wordstresskey, _url):
        self.wordstresskey = _wordstresskey
        self.url = _url
        self.site = re.sub(r'http(s)?://', '', self.url)
        self.pluginlist = []
        self.pluginname = None
        self.pluginversion = None
        self.pluginmajorver = None
        self.pluginminorver = None
        self.pluginpath = None
        self.pluginstatus = None
        self.wpcoreversion = None
        self.wpcoremajorver = None
        self.wpcoreminorver = None
        self.wpcorepatchver = None
        self.themelist = None
        self.themename = None
        self.themeversion = None
        self.themepath = None
        self.themestatus = None
        self.fullurl = "{}/wordstress/?wordstress-key={}".format(self.url, self.wordstresskey)
        self.r = None
        self.soup = None
        self.page = None
        self.jsonout = {}
        self.jsonout["site"] = self.site
        self.jsonout["wp_version"] = {}
        self.jsonout["plugins"] = {}
        self.jsonout["themes"] = {}

    def getpage(self):
        """
        :returns the full wordstress plugin page output unparsed
        """
        retries = 0
        while retries < 10:
            try:
                self.r = requests.get(url=self.fullurl, verify=False)
            except requests.exceptions.RequestException as e:
                if isinstance(e, requests.exceptions.SSLError):
                    print e
                    break
                else:
                    retries += 1
                    print str(e)
                    continue
            break
        try:
            self.page = self.r.text
        except AttributeError as E:
            print '{}: wasnt able to pull the wordstress page from {}'.format(E, self.fullurl)
        return self.page

    def ifpage(self):
        """ We don't need to pull the content of the page more than once."""
        if self.page is None:
            self.getpage()

    def getwpversion(self):
        """
        :returns: wordpress version string object
        """
        self.ifpage()
        self.soup = bs4.BeautifulSoup(self.page, "html.parser")
        self.wpcoreversion = self.soup.find(id="wp_version").text
        self.jsonout["wp_version"]["version"] = self.wpcoreversion
        return self.wpcoreversion

    def getplugins(self):
        """
        :returns plugin list object 
        """
        self.ifpage()
        self.soup = bs4.BeautifulSoup(self.page, "html.parser")
        self.pluginlist = self.soup.findAll(id='all_plugin')
        for plugin in self.pluginlist:
            perpluginlist = plugin.contents[0].split(',')
            self.pluginname = ''.join(perpluginlist[:-3])  # this handles pluginnames with commas
            self.pluginversion = perpluginlist[-3]
            self.pluginpath = perpluginlist[-2]
            self.pluginstatus = perpluginlist[-1]
            self.jsonout["plugins"][self.pluginname] = {}
            self.jsonout["plugins"][self.pluginname]["version"] = self.pluginversion
            self.jsonout["plugins"][self.pluginname]["pluginpath"] = self.pluginpath
            self.jsonout["plugins"][self.pluginname]["pluginstatus"] = self.pluginstatus
        return self.pluginlist

    def getthemes(self):
        """
        :returns theme list object 
        """
        self.ifpage()
        self.soup = bs4.BeautifulSoup(self.page, "html.parser")
        self.themelist = self.soup.findAll(id='all_theme')
        for theme in self.themelist:
            perthemelist = theme.contents[0].split(',')
            self.themename = ''.join(perthemelist[:-3])
            self.themeversion = perthemelist[-3]
            self.themepath = perthemelist[-2]
            self.themestatus = perthemelist[-1]
            self.jsonout["themes"][self.themename] = {}
            self.jsonout["themes"][self.themename]["version"] = self.themeversion
            self.jsonout["themes"][self.themename]["themepath"] = self.themepath
            self.jsonout["themes"][self.themename]["themestatus"] = self.themestatus
        return self.themelist

    def fullinventory(self):
        """
        :returns full inventory as dictionary object 
        """
        self.getwpversion()
        self.getplugins()
        self.getthemes()
        return self.jsonout