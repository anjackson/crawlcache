from mitmproxy import http, ctx
import typing
import requests
from requests.adapters import HTTPAdapter
import urlcanon

#
# Based on https://github.com/mitmproxy/mitmproxy/blob/master/examples/complex/change_upstream_proxy.py
#

# This scripts demonstrates how mitmproxy can switch to a second/different upstream proxy
# in upstream proxy mode.
#
# Usage: mitmdump --mode upstream:http://default-upstream-proxy.local:8080/ -s change_upstream_proxy.py
#
# If you want to change the target server, you should modify flow.request.host and flow.request.port

class CrawlCache():

    def __init__(self):
        self.recrawl_period = 60*60*24*365
        # Set up a large pool for connections to OutbackCDX:
        self.s = requests.Session()
        self.s.mount('http://', HTTPAdapter(pool_connections=1000, pool_maxsize=1000))


    def request(self, flow: http.HTTPFlow) -> None:
        if flow.request.method == "CONNECT":
            # If the decision is done by domain, one could also modify the server address here.
            # We do it after CONNECT here to have the request data available as well.
            return
        address = self.proxy_address(flow)
        if flow.live:
            flow.live.change_upstream_proxy_server(address)  # type: ignore

    def proxy_address(self, flow: http.HTTPFlow) -> typing.Tuple[str, int]:
        # Check if the URL is known to the CDX server
        playback = False
        
        # Use the canonicalised URL
        r_url = str(urlcanon.whatwg(urlcanon.parse_url(flow.request.url)))
        
        # Query the CDX service for this URL:
        ctx.log.info("checking %s..." % r_url)
        r = self.s.get('http://cdxserver:8080/fc', params = {
            'url': r_url,
            'sort': 'reverse',
            'limit': 10
        })

        # Loop through response CDX lines:
        for cdxline in r.iter_lines(decode_unicode=True):
            cdx = cdxline.split(" ")
            # Compare canonicalised URLs (in case an intermediary e.g. adds a default :80 port)
            cdx_url = str(urlcanon.whatwg(urlcanon.parse_url(cdx[2])))
            if r_url == cdx_url:
                ctx.log.info("MATCH")
                playback = True
                break
            else:
                ctx.log.info("NO MATCH '%s' '%s'" % (r_url, cdx_url))

        # Either playback or record, depending on the outcome:
        if playback:
            ctx.log.info("PYWB")
            return ("pywb", 8080)
        else:
            ctx.log.info("WARCPROX")
            return ("warcprox", 8000)



addons = [
    CrawlCache()
]


