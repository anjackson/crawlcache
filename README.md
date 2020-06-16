# crawlcache
Experimental crawler proxy using a WARC-based cache.

The [Chronicrawl](https://github.com/nla/chronicrawl) project prompted me to prototype my idea of a caching crawler proxy, powered by WARCs. The basic idea is the same, in that we design a crawler that will crawl the live web, archiving as it goes, but when revisiting a URL, can play back the response from the archive rather than visit the original server every time.

The difference is that rather than closely integrating with the browser, we implement this as a HTTP proxy. This means any existing crawler or HTTP client can be used with it.

We build on [mitmproxy](https://mitmproxy.org/), which does most of the hard work. We simply use it's [addons](https://docs.mitmproxy.org/stable/addons-overview/) system to intercept calls to the proxy. We look each URL up in our CDX service, then redirect to the appropriate upstream proxy. If we want to capture the request from the live web, we redirect to a WARC-writing archiving proxy (currently [warcprox](https://github.com/internetarchive/warcprox)) which has been extended to update our [OutbackCDX](https://github.com/nla/outbackcdx) index as it goes.  If we already have an archive copy that is 'fresh' enough, we redirect the client request to a [pywb](https://github.com/webrecorder/pywb/) playback service running in proxy mode. 

## Running it

Build and start up the services:

```
docker-compose build
docker-compose up
```
Now, in another terminal, call it like e.g.

```
curl -k -x localhost:8000 https://example.org/
```

The first time it's called, the warcprox service will be used to archive the request and response. But if you call it again, the reponse will come from pywb instead.


## To Do

- Only use pywb for plain GET requests.
- Support an `Accept-Datetime`/`CrawlCache-Datetime` header to allow the client to say 'The resource must be recrawled from the live web if it's older than this'.
- Support a watchdog-reloadable pygtrie-based SURT map of recrawl periods/timestamps. 
- Support needed WARC file-naming conventions.
- Support using pywb in recording mode as an alternative to warcprox (needs to integrate with OutbackCDX & Kafka as per the UKWA warcprox modules).
- Consider interpretation of standard `Cache-Control` headers.
- Check it works!
- ...at actual scale!


