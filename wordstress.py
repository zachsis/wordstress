from libs import GetConfig
from libs import SplunkHTTPEventCollector
from libs import WPVulnDBLookup


class Run(GetConfig):
    def __init__(self):
        super(Run, self).__init__()

    def main(self):
        for s in self.sites.sections():
            try:
                configdict = dict(self.sites.items(s))
                site = WPVulnDBLookup(_url=configdict['url'], _wordstresskey=configdict['key'])
                print(site.fullurl)
                myevent = site.fullvulnlookup()
            except Exception as E:
                self.log.critical(
                    'ERROR WITH SITE {}/wordstress/?wordstress-key={}'.format(configdict['url'], configdict['key']))
                pass

            try:
                splunkresponse = (SplunkHTTPEventCollector.eventpost(splunkurl=self.hecurl,
                                                                     token=self.hectoken,
                                                                     event=myevent,
                                                                     sourcetype=self.sourcetype))
                self.log.info("Splunk HEC Response: {}".format(splunkresponse))
            except Exception as E:
                self.log.critical('Unable to POST to splunk HEC!')
                pass


r = Run()

if __name__ == '__main__':
    r.main()
