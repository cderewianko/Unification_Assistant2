import asyncio
import aiohttp
import os
import time

import pprint

pp = pprint.PrettyPrinter(indent=4)

print(os.getenv("EWELINK_PASSWORD")[0], os.getenv("EWELINK_EMAIL"))
#from ewelink import Client, DeviceOffline

from casper_home.src.devices.ewelink import Client


def get_client():
    async def inner_toggle():
        client = Client(os.getenv("EWELINK_PASSWORD"), os.getenv("EWELINK_EMAIL"))
        await client.login()
        return client
    
    asyncio.run(inner_toggle())


def toggle_device(device_name=None, device_id=None, state=True):
    # inner_toggle())
    # device_id = await find_device_id(device_name, the_info, client=client)
    async def inner_toggle():
        client = Client(os.getenv("EWELINK_PASSWORD"), os.getenv("EWELINK_EMAIL"))
        await client.login()
        
        # if device_name != None:
        #    result = find_device_id(device_name, client)
        #    print('result: ', result)
        
        device = client.get_device(device_id)
        await (device.on() if state else device.off())
    
    asyncio.run(inner_toggle())
    
async def sync_toggle_device(device_name=None, device_id=None, state=False):
    client = Client(os.getenv("EWELINK_PASSWORD"), os.getenv("EWELINK_EMAIL"))
    await client.login()
    
    # if device_name != None:
    #    result = find_device_id(device_name, client)
    #    print('result: ', result)
    
    device = client.get_device(device_id)
    await (device.on() if state else device.off())


def find_device_id(device_name: str) -> str:
    async def inner_check():
        client = Client(os.getenv("EWELINK_PASSWORD"), os.getenv("EWELINK_EMAIL"))
        await client.login()
        
        input_info = {}
        for device in client.devices:
            input_info[device.name] = {
                "device_id": device.id,
                "params": device.params
            }
        
        device_info = input_info.get(device_name)
        
        if device_info:
            return device_info.get("device_id")
        else:
            return ""
    
    return asyncio.run(inner_check())


def find_device_name(device_id: str) -> str:
    async def inner_check():
        client = Client(os.getenv("EWELINK_PASSWORD"), os.getenv("EWELINK_EMAIL"))
        await client.login()
        
        for device in client.devices:
            if str(device.id) == str(device_id):
                return device.name
    
    return asyncio.run(inner_check())


def get_device_list():
    #print('ping 2')
    async def inner_check():
        #print('os.getenv("EWELINK_EMAIL"): ', os.getenv("EWELINK_EMAIL"))
        client = Client(os.getenv("EWELINK_PASSWORD"), os.getenv("EWELINK_EMAIL"))
        await client.login()
        
        #print('client.devices: ', client.devices)

        devices_list = list()
        for device in client.devices:
            devices_list.append(vars(device).get("data"))
            #print('................................................')
            #pp.pprint(vars(device).get("data"))
            
        return devices_list
    
    #print('ping 3')
    #return asyncio.run(inner_check())
    # return await inner_check()
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        return asyncio.create_task(inner_check())
    
    else:
        return asyncio.run(inner_check())

def test_smart_switch(device_name, device_id):
    print(f"Turning On Using Name: {device_name}, {device_id}")
    toggle_device(device_name=device_name, device_id=device_id, state=True)
    time.sleep(2)
    print(f"Turning Off Using Name: {device_name}, {device_id}")
    toggle_device(device_name=device_name, device_id=device_id, state=False)


def test_get_devices():
    print('ping 1')
    the_list = get_device_list()
    for device in the_list:
        print('device: ', device)
        continue
        #print(f":Device: {item} ID: {value.get('device_id')}")


def test_get_id_from_name(device_name):
    # Get a device id from its name.
    result_id = find_device_id(device_name)
    print(f":Device Name: {device_name} - ID: {result_id}")


def test_get_name_from_id(device_id):
    # Get a device name from its id.
    result_name = find_device_name(device_id)
    print(f":Device ID: {device_id} - Name: {result_name}")


def test_set_of_test():
    smart_switch_name = "Christmas Cheer Tree"
    #smart_switch_name = "The chicken"
    smart_switch_id = "10003fbccc"
    #smart_switch_id = "100064b966"
    
    print('smart_switch_id: ', smart_switch_id)
    
    test_smart_switch(smart_switch_name, smart_switch_id)
    #test_get_devices()
    # test_get_id_from_name(smart_switch_name)
    # test_get_name_from_id(smart_switch_id)


if __name__ == "__main__":
    test_set_of_test()


