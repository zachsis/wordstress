import configparser
import logging
import os


class GetConfig(object):
    def __init__(self):
        try:
            self.settings = configparser.ConfigParser()
            self.settings.read('{}/conf/settings.conf'.format(os.getcwd()))
            self.hecurl = self.settings.get(section="splunk", option="splunkurl")
            self.hectoken = self.settings.get(section="splunk", option="token")
            self.sourcetype = self.settings.get(section="splunk", option="sourcetype")
            logging.basicConfig(filename=self.settings.get(section="debuglogging",
                                                           option="logpath"),
                                level=self.settings.get(section="debuglogging",
                                                        option="verbosity"),
                                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                datefmt='%a, %d %b %Y %H:%M:%S')
            self.log = logging.getLogger(name="py-wordstress")

        except Exception as E:
            print('! Something went wrong with opening settings.conf')
            print(E)
            exit(1)

        try:
            self.sites = configparser.ConfigParser()
            self.sites.read('{}/conf/sites.conf'.format(os.getcwd()))

        except Exception as E:
            print('! Something went wrong with opening sites.conf')
            print(E)
            exit(1)
