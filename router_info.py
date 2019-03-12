from iosxeapi.iosxerestapi import iosxerestapi
from pprint import pprint

router_call = iosxerestapi(host='ios-xe-mgmt.cisco.com', username='root', password='D_Vay!_10&', port=9443)
bgp = router_call.get_bgp()
pprint(bgp)

int = router_call.get_interfaces_oper()
pprint(int)
