import cinderlib as cl
import sys,os
MODULE_PATH = os.path.abspath("./driver/ixsystems/__init__.py")
MODULE_NAME = "cinder.volume.drivers.ixsystems"
import importlib
import sys
import configparser

spec = importlib.util.spec_from_file_location(MODULE_NAME, MODULE_PATH)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module 
spec.loader.exec_module(module)

config = configparser.ConfigParser()
config.read("./test/truenas22.cfg") 
print(config.items('ixsystems-iscsi'))
configdict = dict(config.items('ixsystems-iscsi'))

print(os.getcwd())

def test_fun():
    
    # Initialize the ixsystem-iscsi driver
    driver = cl.Backend(volume_backend_name='ixsystems-iscsi',**configdict)
    vol = driver.create_volume(1,name="vol-1")
    assert vol.name == "vol-1"
    avol = vol.attach()
    avol.device['path']

    data = b"xxxxxxxxxxxxxxxx"
    dev = os.open(avol.device['path'], os.O_RDWR)
    os.write(dev,data)
    os.lseek(dev,0,os.SEEK_SET)
    assert os.read(dev,16) == data
    vol.detach()
    vol.delete()