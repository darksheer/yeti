from datetime import timedelta
import logging

from core.observables import Ip
from core.feed import Feed
from core.errors import ObservableValidationError


class SysctlCameleonAddserverDomains(Feed):
    default_values = {
        'frequency': timedelta(hours=1),
        'source': 'http://sysctl.org/cameleon/hosts',
        'name': 'SysctlCameleonAddserverDomains',
        'description': 'sysctl.org project Cameleon addserver domain block list (not identified as malicious, but serving adds.).'
    }

    def update(self):
        for line in self.update_lines():
            self.analyze(line)

    def analyze(self, line):
        if line.startswith('#'):
            return

        try:
            parts = line.split()
            ip = str(parts[0]).strip()
            context = {
                'source': self.name
            }

            try:
                ip = Ip.get_or_create(value=ip)
                ip.add_context(context)
                ip.add_source('feed')
                ip.tag(['addserver'])
            except ObservableValidationError as e:
                logging.error(e)
        except Exception as e:
            logging.debug(e)
