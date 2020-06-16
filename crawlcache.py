from mitmproxy import http
import typing

#
# Based on https://github.com/mitmproxy/mitmproxy/blob/master/examples/complex/change_upstream_proxy.py
#

# This scripts demonstrates how mitmproxy can switch to a second/different upstream proxy
# in upstream proxy mode.
#
# Usage: mitmdump -U http://default-upstream-proxy.local:8080/ -s change_upstream_proxy.py
#
# If you want to change the target server, you should modify flow.request.host and flow.request.port


def proxy_address(flow: http.HTTPFlow) -> typing.Tuple[str, int]:
    # Poor man's loadbalancing: route every second domain through the alternative proxy.
    if hash(flow.request.host) % 2 == 1:
        print("WARCPROX")
        return ("warcprox", 8000)
    else:
        print("PYWB")
        return ("pywb", 8000)


def request(flow: http.HTTPFlow) -> None:
    if flow.request.method == "CONNECT":
        # If the decision is done by domain, one could also modify the server address here.
        # We do it after CONNECT here to have the request data available as well.
        print("CONNECT")
        flow.live.change_upstream_proxy_server(("pywb",8000))  # type: ignore
        return
    address = proxy_address(flow)
    if flow.live:
        flow.live.change_upstream_proxy_server(address)  # type: ignore
