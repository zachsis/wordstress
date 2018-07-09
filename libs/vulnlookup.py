from libs import WordstressScraper
from pkg_resources import parse_version
import requests
import json


class WPVulnDBLookup(WordstressScraper):
    def __init__(self, *args, **kwargs):
        super(WPVulnDBLookup, self).__init__(*args, **kwargs)
        self.fullinventory()
        self.wpvulndbbaseurl = 'https://wpvulndb.com/api/v2'
        self.vulndbjson = None
        self.jsonout["wp_version"]["vulnerabilities"] = []
        self.jsonout["confirmed_vulns"] = {}
        self.jsonout["confirmed_vulns"]["coreversion"] = []
        self.jsonout["confirmed_vulns"]["plugins"] = []
        self.vulnmajver = None
        self.vulnminver = None
        self.pluginfilename = None
        self.plugindirname = None

    def corelookup(self):
        """
        :return: dictionary
        """
        version = self.wpcoreversion.split('.')
        self.wpcoremajorver = version[0]
        self.wpcoreminorver = version[1]
        self.wpcorepatchver = version[2]
        self.fullurl = '{}/wordpresses/{}{}{}'.format(self.wpvulndbbaseurl, self.wpcoremajorver, self.wpcoreminorver,
                                                      self.wpcorepatchver)
        self.pullvulndata()
        try:
            self.vulndbjson = json.loads(self.r.text)

            for vuln in self.vulndbjson[self.wpcoreversion]["vulnerabilities"]:
                try:
                    if WPVulnDBLookup.versioncheck(_curver=self.wpcoreversion, _fixed_in=vuln["fixed_in"]):
                        self.jsonout["wp_version"]["vulnerabilities"].append(vuln)
                        self.jsonout["confirmed_vulns"]["coreversion"].append(vuln)
                except Exception as E:
                    print E
                    # self.jsonout["wp_version"]["vulnerror"] = vuln
                    # self.jsonout["wp_version"]["vulnerror"]["errors"] = str(E)
                    continue
        except Exception as E:
            print E
            pass
        return self.jsonout["wp_version"]

    def pluginlookup(self):
        """
        Notes: wpvulndb is not consistent in how it archives plugin names. 
        Sometimes the folder of the plugin should be the api request. 
        Other times it is the plugin file name sans .php. 
        Some plugins that have 'premium' or 'pro' on them dont seem to return.
        
        Anomaly: https://wpvulndb.com/api/v2/plugins/wordpress-varnish 
        vs 
        https://wpvulndb.com/api/v2/plugins/wp-varnish
        
        ^ The wp-varnish output has 'latest_version':null where the other has the
        actual version. Need to check for 'null' in current_version output. Also we'll need
        to test both the folder name and the filename.
        
        If wpvulndb wont return anything for the plugin, it will throw status 404
        :return: 
        """

        for inventory_key, inventory_val in self.jsonout["plugins"].iteritems():
            self.jsonout["plugins"][inventory_key]["wpvulndb"] = {}
            plg = inventory_val["pluginpath"].split("/")
            if len(plg) == 2:
                self.plugindirname = plg[0]
                self.pluginfilename = plg[1]
            self.fullurl = '{}/plugins/{}'.format(self.wpvulndbbaseurl, self.plugindirname)
            self.pullvulndata()
            try:
                for wpvdb_key, wpvdb_val in json.loads(self.r.text).iteritems():
                    self.jsonout["plugins"][inventory_key]["wpvulndb"] = wpvdb_val
                    if wpvdb_val["vulnerabilities"]:
                        for vuln in self.jsonout["plugins"][inventory_key]["wpvulndb"]["vulnerabilities"]:
                            if WPVulnDBLookup.versioncheck(_curver=inventory_val["version"],
                                                           _fixed_in=vuln["fixed_in"]):
                                vuln["vulnerablestatus"] = True
                                self.jsonout['confirmed_vulns']['plugins'].append(vuln)
                            else:
                                vuln["vulnerablestatus"] = False
                    else:
                        self.jsonout["plugins"][inventory_key]["wpvulndb"] = wpvdb_val
            except Exception as E:
                # self.jsonout["plugins"][inventory_key]["wpvulndb"]["exception"] = str(E)
                # self.jsonout["plugins"][inventory_key]["wpvulndb"]["url"] = self.r.url
                # self.jsonout["plugins"][inventory_key]["wpvulndb"]["status_code"] = self.r.status_code
                print "{} : {}".format(self.jsonout["plugins"][inventory_key], str(E))
                continue
            if self.r.status_code == 404:
                try:
                    self.fullurl = '{}/plugins/{}'.format(self.wpvulndbbaseurl, self.pluginfilename[:-4])
                    self.pullvulndata()
                    for wpvdb_key, wpvdb_val in json.loads(self.r.text).iteritems():
                        self.jsonout["plugins"][inventory_key]["wpvulndb"] = wpvdb_val
                except Exception as E:
                    # self.jsonout["plugins"][inventory_key]["wpvulndb"]["exception"] = str(E)
                    # self.jsonout["plugins"][inventory_key]["wpvulndb"]["url"] = self.r.url
                    # self.jsonout["plugins"][inventory_key]["wpvulndb"]["status_code"] = self.r.status_code
                    print "{} : {}".format(self.jsonout["plugins"][inventory_key], str(E))
                    continue

        return self.jsonout["plugins"]

    @classmethod
    def versioncheck(cls, _curver, _fixed_in):
        if _fixed_in is None:
            # version is vulnerable
            return True
        if parse_version(_curver) < parse_version(_fixed_in):
            # version is vulnerable
            return True
        else:
            # version is not vulnerable
            return False

    def themelookup(self):
        """
        To be implemented
        :return: 
        """
        return

    def pullvulndata(self):
        """
        we need to make sure that the response from wpvulndb is either a 200 or 404 when looking up vulns.
        If its anything else, its likely you've been blocked by their CDN firewall.         
        """
        try:
            count = 0
            self.r = requests.get(url=self.fullurl, verify=False)
            while self.r.status_code == 429 and count < 10:
                self.r = requests.get(url=self.fullurl, verify=False)
                count += 1
                from time import sleep
                sleep(5)
            if self.r.status_code != 200 and self.r.status_code != 404:
                print self.r.status_code
                print self.r.content
            if count == 10:
                print 'something is funky with wpvulndb. tried 10 times'
        except requests.HTTPError as e:
            print "{}: something went wrong pulling vulndata from wpvulndb".format(str(e))
            pass

    def fullvulnlookup(self):
        self.corelookup()
        self.pluginlookup()
        self.themelookup()
        return self.jsonout
