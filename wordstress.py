from libs import WPVulnDBLookup
from libs import SplunkHTTPEventCollector
import ConfigParser
import os


def main():
    ConfigParser.SafeConfigParser()
    settings = ConfigParser.SafeConfigParser()
    settings.read('{}/conf/settings.conf'.format(os.getcwd()))
    sites = ConfigParser.SafeConfigParser()
    sites.read('{}/conf/sites.conf'.format(os.getcwd()))

    hecurl = settings.get(section="splunk", option="splunkurl")
    hectoken = settings.get(section="splunk", option="token")
    sourcetype = settings.get(section="splunk", option="sourcetype")

    for s in sites.sections():
        configdict = dict(sites.items(s))
        print configdict['url']
        site = WPVulnDBLookup(_url=configdict['url'], _wordstresskey=configdict['key'])

        print site.fullurl
        myevent = site.fullvulnlookup()
        print SplunkHTTPEventCollector.eventpost(splunkurl=hecurl,
                                                 token=hectoken,
                                                 sourcetype=sourcetype,
                                                 event=myevent)


main()
