# Copyright 2012 Midokura Japan KK

from resource import ResourceBase

class Port(ResourceBase):

    class RouterPort(ResourceBase):

        def _ports_uri(self, tenant_id, router_uuid):
            response, routers =  self.cl.get(self.cl.routers_uri + "?tenant_id=" + tenant_id)
            router_uri =  self._find_resource(routers, router_uuid)
            response, router =  self.cl.get(router_uri)
            return  router['ports']

        def _port_uri(self, tenant_id, router_uuid, port_uuid):
            ports_uri = self._ports_uri(tenant_id, router_uuid)
            response, ports =  self.cl.get(ports_uri)
            return self._find_resource(ports, port_uuid)

        # create a port
        def create(self, tenant_id, router_uuid, type_,
                   networkAddress, networkLength, portAddress,
                   localNetworkAddress=None, localNetworkLength=None,
                   inbound_filter_id=None, outbound_filter_id=None,
                   vif_id=None):

            uri = self._ports_uri(tenant_id, router_uuid)
            data = { "type": type_,
                     "networkAddress": networkAddress,
                     "networkLength": networkLength, #int
                     "portAddress": portAddress,
                     "localNetworkAddress": localNetworkAddress,
                     "localNetworkLength": localNetworkLength,  #int
                     "inboundFilterId": inbound_filter_id,
                     "outboundFilterId": outbound_filter_id,
                     "vifId": vif_id}
            return self.cl.post(uri, data)

        def list(self, tenant_id, router_uuid):
            uri = self._ports_uri(tenant_id, router_uuid)
            return self.cl.get(uri)

        def get(self, tenant_id, router_uuid, port_uuid):
            port_uri = self._port_uri(tenant_id, router_uuid, port_uuid)
            return self.cl.get(port_uri)

        def update(self, tenant_id, router_uuid, port_uuid, data):
            port_uri = self._port_uri(tenant_id, router_uuid, port_uuid)
            return self.cl.put(port_uri, data)

        def delete(self, tenant_id, router_uuid, port_uuid):
            port_uri = self._port_uri(tenant_id, router_uuid, port_uuid)
            return self.cl.delete(port_uri)

        def link(self, tenant_id, router_uuid, port_uuid, peer_id):
            response, port = self.get(tenant_id, router_uuid, port_uuid)
            link_uri = port['link']
            data = {'peerId': peer_id}
            return self.cl.post(link_uri, data)

        def unlink(self, tenant_id, router_uuid, port_uuid):
            response, port = self.get(tenant_id, router_uuid, port_uuid)
            link_uri = port['link']
            data = {'peerId': None}
            return self.cl.post(link_uri, data)

        def bgp_create(self, tenant_id, router_uuid, port_uuid, local_as,
                       peer_as, peer_addr):
            response, port = self.get(tenant_id, router_uuid, port_uuid)
            bgp_uri = port['bgps']
            data = {'localAS':local_as,
                    'peerAS': peer_as,
                    'peerAddr': peer_addr}
            return self.cl.post(bgp_uri, data)

        def bgp_list(self, tenant_id, router_uuid, port_uuid):
            response, port = self.get(tenant_id, router_uuid, port_uuid)
            return self.cl.get(port['bgps'])

        def bgp_get(self, tenant_id, router_uuid, port_uuid, bgp_uuid):
            response, port = self.get(tenant_id, router_uuid, port_uuid)
            response, bgps =  self.cl.get(port['bgps'])
            bgp_uri = self._find_resource(bgps, bgp_uuid)
            return self.cl.get(bgp_uri)

        def bgp_delete(self, tenant_id, router_uuid, port_uuid, bgp_uuid):
            response, port = self.get(tenant_id, router_uuid, port_uuid)
            response, bgps =  self.cl.get(port['bgps'])
            bgp_uri = self._find_resource(bgps, bgp_uuid)
            return self.cl.get(bgp_uri)

        def bgp_ad_route(self, tenant_id, router_uuid, port_uuid, bgp_uuid,
                       nw_prefix, prefix_length):
            response, bgp = self.bgp_get(tenant_id, router_uuid, port_uuid,
                                         bgp_uuid)
            ad_route_uri = bgp['adRoutes']
            data = {'nwPrefix': nw_prefix,
                    'prefixLength': prefix_length}

            return self.cl.post(ad_route_uri, data)

        def bgp_ad_route_list(self, tenant_id, router_uuid, port_uuid,
                              bgp_uuid):

            response, bgp = self.bgp_get(tenant_id, router_uuid, port_uuid,
                                         bgp_uuid)
            ad_route_uri = bgp['adRoutes']
            return self.cl.get(ad_route_uri)


        def bgp_ad_route_get(self, tenant_id, router_uuid, port_uuid,
                              bgp_uuid, ad_route_uuid):

            response, ad_routes = self.bgp_ad_route_list(tenant_id,
                                                         router_uuid, port_uuid,
                                                         bgp_uuid)
            ad_route_uri = self._find_resource(ad_routes, ad_route_uuid)
            return self.cl.get(ad_route_uri)

        def bgp_ad_route_delete(self, tenant_id, router_uuid, port_uuid,
                              bgp_uuid, ad_route_uuid):

            response, ad_routes = self.bgp_ad_route_list(tenant_id,
                                                         router_uuid, port_uuid,
                                                         bgp_uuid)
            ad_route_uri = self._find_resource(ad_routes, ad_route_uuid)
            return self.cl.delete(ad_route_uri)


    class BridgePort(ResourceBase):

        def _ports_uri(self, tenant_id, bridge_uuid):
            response, bridges =  self.cl.get(self.cl.bridges_uri + "?tenant_id=" + tenant_id)
            bridge_uri =  self._find_resource(bridges, bridge_uuid)
            response, bridge =  self.cl.get(bridge_uri)
            return  bridge['ports']

        def _port_uri(self, tenant_id, bridge_uuid, port_uuid):
            ports_uri = self._ports_uri(tenant_id, bridge_uuid)
            response, ports =  self.cl.get(ports_uri)
            return self._find_resource(ports, port_uuid)


        def create(self, tenant_id, bridge_uuid, type_, inbound_filter_id=None,
                   outbound_filter_id=None, port_group_ids=None):
            uri = self._ports_uri(tenant_id, bridge_uuid)
            data = { 'type': type_,
                     'inboundFilterId': inbound_filter_id,
                     'outboundFilterId': outbound_filter_id,
                     'portGroupIDs': port_group_ids
                     }
            return self.cl.post(uri, data)

        def list(self, tenant_id, bridge_uuid):
            uri = self._ports_uri(tenant_id, bridge_uuid)
            return self.cl.get(uri)

        def get(self, tenant_id, bridge_uuid, port_uuid):
            port_uri = self._port_uri(tenant_id, bridge_uuid, port_uuid)
            return self.cl.get(port_uri)

        def update(self, tenant_id, bridge_uuid, port_uuid, data):
            port_uri = self._port_uri(tenant_id, bridge_uuid, port_uuid)
            return self.cl.put(port_uri, data)

        def delete(self, tenant_id, bridge_uuid, port_uuid):
            port_uri = self._port_uri(tenant_id, bridge_uuid, port_uuid)
            return self.cl.delete(port_uri)

        def link(self, tenant_id, bridge_uuid, port_uuid, peer_id):
            response, port = self.get(tenant_id, bridge_uuid, port_uuid)
            link_uri = port['link']
            data = {'peerId': peer_id}
            return self.cl.post(link_uri, data)

        def unlink(self, tenant_id, bridge_uuid, port_uuid):
            response, port = self.get(tenant_id, bridge_uuid, port_uuid)
            link_uri = port['link']
            data = {'peerId': None}
            return self.cl.post(link_uri, data)
