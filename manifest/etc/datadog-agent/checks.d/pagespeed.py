'''
Inspired by https://docs.datadoghq.com/developers/agent_checks/
'''
import requests
import time

from checks import AgentCheck

class PageSpeedCheck(AgentCheck):
    def check(self, instance):
        google_api_key = self.init_config.get('google_api_key')
        timeout = self.init_config.get('timeout', 20)

        url = instance['url']
        tags = instance['tags']

        self.log.info('Running pagespeed check for %s' % (url))
        for strategy in ['desktop', 'mobile']:
            try:
                api_url = 'https://www.googleapis.com/pagespeedonline/v4/runPagespeed?url=%s&strategy=%s&key=%s' % (url, strategy, google_api_key)

                response = requests.get(api_url, timeout=timeout)
                if response.status_code != 200:
                    self.log.error('Pagespeed API call returned status code %d' % (response.status_code))
                    continue

                try:
                    pagespeed_result = response.json()
                except ValueError as e:
                    self.log.error('Error while decoding JSON response: ' + str(e))
                    continue

                loaded_url = pagespeed_result['id']
                score = pagespeed_result['ruleGroups']['SPEED']['score']
                median_fcp = pagespeed_result['loadingExperience']['metrics']['FIRST_CONTENTFUL_PAINT_MS']['median']
                median_dcl = pagespeed_result['loadingExperience']['metrics']['DOM_CONTENT_LOADED_EVENT_FIRED_MS']['median']

                metric_tags = ['strategy:' + strategy, 'url:' + loaded_url] + tags
                self.gauge('pagespeed.score', score, tags=metric_tags, hostname=None, device_name=None)
                self.gauge('pagespeed.median_fcp', median_fcp, tags=metric_tags, hostname=None, device_name=None)
                self.gauge('pagespeed.median_dcl', median_dcl, tags=metric_tags, hostname=None, device_name=None)

                self.log.info('Url: %s strategy: %s page score: %d FCP: %d DCL %d' % (loaded_url, strategy, score, median_fcp, median_dcl))

                pageStats = pagespeed_result['pageStats']
                for metric, value in pageStats.iteritems():
                    self.gauge('pagespeed.' + metric, value, tags=metric_tags, hostname=None, device_name=None)

            except requests.exceptions.Timeout:
                self.log.error('Pagespeed API call timed out')
