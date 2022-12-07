import cinderlib as cl
import sys,os
import importlib
import sys
import configparser
print("Load driver module")
MODULE_PATH = os.path.abspath("./driver/ixsystems/__init__.py")
MODULE_NAME = "cinder.volume.drivers.ixsystems"
spec = importlib.util.spec_from_file_location(MODULE_NAME, MODULE_PATH)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module 
spec.loader.exec_module(module)
print("Load config: ./test/truenas22.cfg") 
config = configparser.ConfigParser()
config.read("./test/truenas22.cfg") 
configdict = dict(config.items('ixsystems-iscsi'))
print(config.items('ixsystems-iscsi'))

# Initialize the ixsystem-iscsi driver
print("Load driver") 
driver = cl.Backend(volume_backend_name='ixsystems-iscsi',**configdict)

def test_create_delete_volume():
    print("Start test_create_delete_volume") 
    vol = driver.create_volume(1,name="vol-1")
    assert vol.name == "vol-1"
    print("Volume create: "+ vol.name_in_storage)     
    print("Volume id: "+ vol.name_in_storage)
    vol.delete()
    print("Volume deleted: "+ vol.name_in_storage)     
def test_attach_read_write_volume():   
    print("Start test_attach_read_write_volume")          
    vol = driver.create_volume(1,name="vol-2")
    assert vol.name == "vol-2"    
    print("Volume create: "+ vol.name)     
    print("Volume id: "+ vol.name_in_storage)    
    avol = vol.attach()
    print("Volume attached: "+ avol.device['path'])         
    print("Writing data to volume: "+ avol.device['path'])             
    data = b"xxxxxxxxxxxxxxxx"
    dev = os.open(avol.device['path'], os.O_RDWR)
    os.write(dev,data)
    print("Reading data from volume: "+ avol.device['path'])                 
    os.lseek(dev,0,os.SEEK_SET)
    assert os.read(dev,16) == data
    print("Detach volume: "+ avol.device['path'])    
    vol.detach()
    vol.delete()
    print("Delete volume: "+ vol.name_in_storage)                         