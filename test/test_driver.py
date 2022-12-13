import pytest
import cinderlib
import sys
import os
import importlib
import configparser


@pytest.fixture()
def cinderdriver(configfile):
    print("Load driver module")
    MODULE_PATH = os.path.abspath("./driver/ixsystems/__init__.py")
    MODULE_NAME = "cinder.volume.drivers.ixsystems"
    spec = importlib.util.spec_from_file_location(MODULE_NAME, MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    print("Load config: " + configfile)
    config = configparser.ConfigParser()
    config.read(configfile)
    configdict = dict(config.items('ixsystems-iscsi'))
    print(config.items('ixsystems-iscsi'))

    # Initialize the ixsystem-iscsi driver
    print("Load driver")
    driver = cinderlib.Backend(volume_backend_name='ixsystems-iscsi', **configdict)
    return driver


def test_create_delete_volume(cinderdriver):
    print("Start test_create_delete_volume")
    vol = cinderdriver.create_volume(1, name="vol-1")
    assert vol.name == "vol-1"
    print("Volume create: " + vol.name_in_storage)
    print("Volume id: " + vol.name_in_storage)
    vol.delete()
    print("Volume deleted: " + vol.name_in_storage)


def test_attach_read_write_volume(cinderdriver):
    print("Start test_attach_read_write_volume")
    vol = cinderdriver.create_volume(1, name="vol-2")
    assert vol.name == "vol-2"
    print("Volume create: " + vol.name)
    print("Volume id: " + vol.name_in_storage)
    avol = vol.attach()
    print("Volume attached: " + avol.device['path'])
    print("Writing data to volume: " + avol.device['path'])
    data = b"xxxxxxxxxxxxxxxx"
    dev = os.open(avol.device['path'], os.O_RDWR)
    os.write(dev, data)
    print("Reading data from volume: " + avol.device['path'])
    os.lseek(dev, 0, os.SEEK_SET)
    assert os.read(dev, 16) == data
    print("Detach volume: " + avol.device['path'])
    vol.detach()
    vol.delete()
    print("Delete volume: " + vol.name_in_storage)


def test_attach_multiple_volumes(cinderdriver):
    print("Start test_attach_multiple_volumes")
    for i in range(0, 2):
        vol = cinderdriver.create_volume(1, name="vol-" + str(i))
        print("Volume create: " + vol.name)
        print("Volume id: " + vol.name_in_storage)
    print("Volume attach")        
    cinderdriver.volumes[0].attach()
    cinderdriver.volumes[1].attach()
    print("Volume detach")            
    cinderdriver.volumes[0].detach()
    cinderdriver.volumes[1].detach()
    print("Volume delete: " + cinderdriver.volumes[0].name_in_storage)
    cinderdriver.volumes[0].delete()
    print("Volume delete: " + cinderdriver.volumes[0].name_in_storage)    
    cinderdriver.volumes[0].delete()

