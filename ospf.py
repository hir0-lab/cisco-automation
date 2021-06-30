from genie.conf import Genie
from genie.conf.base import Testbed, Device, Link, Interface
from genie.conf.base.attributes import UnsupportedAttributeWarning
from genie.utils.config import Config
from genie.utils.diff import Diff
from genie.libs.conf.vrf import Vrf
from genie.libs.conf.interface import Interface
from genie.libs.conf.ospf import Ospf
from genie.libs.conf.ospf.gracefulrestart import GracefulRestart
from genie.libs.conf.ospf.stubrouter import StubRouter
from genie.libs.conf.ospf.areanetwork import AreaNetwork
from genie.libs.conf.ospf.arearange import AreaRange
from genie.libs.conf.ospf.interfacestaticneighbor import InterfaceStaticNeighbor

def ospf_setup():

    #device-information
    testbed = Genie.init('yaml/csrbed.yaml')
    device = testbed.devices['csr1']

    device.connect()
    ##before-config-get

    cfg1 = device.execute('show run')
    conf1 = Config(cfg1)
    conf1.tree()
    cfg1_result = conf1.config

    #config-make


    vrf1 = Vrf('default')
    ospf1 = Ospf()

    device.add_feature(ospf1)
    intf1 = Interface(device=device, name='GigabitEthernet2')

    #interface_configure
    intf1.description = 'pyats-ospf-conf' 
    intf1.ipv4 = '192.168.10.1'
    intf1.ipv4.netmask = '255.255.255.0'
    intf1.shutdown = False

    #ospf_configure
    ospf1.device_attr[device].vrf_attr[vrf1].instance = '1'
    ospf1.device_attr[device].vrf_attr[vrf1].enable = True
    ospf1.device_attr[device].vrf_attr[vrf1].router_id = '1.1.1.1'

    #area-setup
    an1 = AreaNetwork(device=device)
    an1.area_network = '192.168.10.0'
    an1.area_network_wildcard = '0.0.0.255'
    ospf1.device_attr[device].vrf_attr[vrf1].area_attr['2'].add_areanetwork_key(an1)


    #build
    print(ospf1.build_config(apply=False))

    #device.connect()
    intf1.build_config()
    ospf1.build_config()

    ##after-config-get
    cfg2 = device.execute('show run')
    conf2 = Config(cfg2)
    conf2.tree()
    cfg2_result = conf2.config

    ##diff-config

    dif = Diff(cfg1_result, cfg2_result)
    dif.findDiff()
    print(dif)   


if __name__ == "__main__":
    ospf_setup()
    
