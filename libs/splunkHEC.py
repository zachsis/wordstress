import requests
import json


class SplunkHTTPEventCollector(object):
    """
    method for leveraging the splunk HTTP Event Collector. 
    """

    @classmethod
    def eventpost(cls, splunkurl, event, sourcetype, token):
        cls.token = token
        cls.event = event
        cls.sourcetype = sourcetype
        cls.splunkurl = '{}/services/collector/event'.format(splunkurl)
        cls.headers = {'Authorization': 'Splunk {}'.format(cls.token)}
        splunkjsontemplate = {}
        splunkjsontemplate["sourcetype"] = cls.sourcetype
        splunkjsontemplate["event"] = cls.event
        splunkjsontemplate = json.dumps(splunkjsontemplate)
        r = requests.post(url=cls.splunkurl, verify=False, headers=cls.headers, data=splunkjsontemplate)
        return r.text
