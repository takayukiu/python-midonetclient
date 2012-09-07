# Copyright 2012 Midokura Japan KK

import os
import sys
import unittest
import uuid
from webob import exc

TOPDIR = os.path.normpath(os.path.join(os.path.abspath(sys.argv[0]),
                                   os.pardir,
                                   os.pardir,
                                   os.pardir))
sys.path.insert(0, TOPDIR)

from midonet.client import MidonetClient
from midonet import utils


class TestRule(unittest.TestCase):

    tenent = None
    router = None
    test_tenant_name = "TEST_TENANT"
    test_router_name = "TEST_ROUTER"

    @classmethod
    def setUpClass(cls):
        mc = MidonetClient()
        cls.router = mc.routers()
        cls.chain = mc.chains()
        cls.rule = mc.rules()

    @classmethod
    def tearDownClass(cls):
        pass

    def test_create_get_delete(self):
        r, c = self.router.create(self.test_tenant_name, self.test_router_name)
        router_uuid = utils.get_uuid(r)

        r, c = self.chain.create(self.test_tenant_name, 'dnat')
        chain_dnat_uuid = utils.get_uuid(r)

        r, c = self.chain.create(self.test_tenant_name, 'snat')
        chain_snat_uuid = utils.get_uuid(r)

        r, c = self.rule.create(self.test_tenant_name, chain_dnat_uuid,
                                 type_='drop', properties={'key': 'val'})

        r0, c = self.rule.create_dnat_rule(
            self.test_tenant_name, chain_dnat_uuid, '123.10.10.3',
            '192.168.10.3')

        r0, c = self.rule.create_dnat_rule(
            self.test_tenant_name, chain_dnat_uuid, '123.10.10.3',
            '192.168.10.3',[str(uuid.uuid4()), str(uuid.uuid4())])

        r1, c = self.rule.create_snat_rule(
            self.test_tenant_name, chain_snat_uuid, '123.10.10.3',
            '192.168.10.3', [str(uuid.uuid4())])

        r1, c = self.rule.create_snat_rule(
            self.test_tenant_name, chain_snat_uuid, '123.10.10.3',
            '192.168.10.3', [str(uuid.uuid4())])

        r, c = self.rule.list(self.test_tenant_name, chain_dnat_uuid)
        r, c = self.rule.list(self.test_tenant_name, chain_snat_uuid)

        dnat_rule_uuid = utils.get_uuid(r0)
        snat_rule_uuid = utils.get_uuid(r1)

        r, c = self.rule.get(
            self.test_tenant_name, chain_dnat_uuid, dnat_rule_uuid)
        self.rule.delete(self.test_tenant_name, chain_dnat_uuid, dnat_rule_uuid)
        self.chain.delete(self.test_tenant_name, chain_dnat_uuid)

        r, c =self.rule.get(
            self.test_tenant_name, chain_snat_uuid, snat_rule_uuid)
        self.rule.delete(self.test_tenant_name, chain_snat_uuid, snat_rule_uuid)
        self.chain.delete(self.test_tenant_name, chain_snat_uuid)

        self.router.delete(self.test_tenant_name, router_uuid)
if __name__ == '__main__':
    unittest.main()
