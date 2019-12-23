import json

from providers.a4kScrapers.en import get_torrent, get_hosters
from providerModules.a4kScrapers.third_party.source_utils import control

def optimize_requests(cancel=lambda: False, results=[]):
    def optimize(scrapers, type, ctor_fn):
        for scraper in scrapers:
            if cancel():
                return

            scraper_module = __import__('providers.a4kScrapers.en.%s.%s' % (type, scraper), fromlist=[''])
            scraper_results = ctor_fn(scraper_module).optimize_requests()
            results.append(scraper_results)

            control.log('a4kScrapers.optimize.%s:\n%s' % (scraper, json.dumps(scraper_results, sort_keys=True, indent=4)), 'notice')

    optimize(get_torrent(), 'torrent', lambda mod: mod.sources())
    optimize(get_hosters(), 'hosters', lambda mod: mod.source())
