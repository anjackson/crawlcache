Squid
=====

This does not appear to work. 

The 'SSL Bumping' works fine, i.e. it will mint certificates for hosts and run as a MITM. But we want to chain this server with upstream proxies that also do SSL Bumping, and Squid does not seem to support forwarding the request like that. e.g. I can defer to a parent cache\_peer for plain HTTP but HTTPS connections do not get passed to the parent cache\_peer when they've been Bumped.

See 

- http://squid-web-proxy-cache.1019090.n4.nabble.com/SSL-Bump-with-HTTP-Cache-Peer-Parent-td4687034.html
- http://squid-web-proxy-cache.1019090.n4.nabble.com/ssl-bump-with-cache-peer-problem-Handshake-fail-after-Client-Hello-td4672064.html




