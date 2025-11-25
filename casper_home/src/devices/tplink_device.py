
import asyncio
import subprocess
import re

import kasa

from casper_home.src.devices.base_device import BaseDevice


class TpLinkDevice(BaseDevice):
    def __init__(self, device_id, name, manufacturer, ip_address):
        super().__init__(device_id, name, manufacturer)
        self.plug = kasa.iot.IotPlug(ip_address)

    async def turn_on(self):
        await self.plug.turn_on()
        return True

    async def turn_off(self):
        await self.plug.turn_off()
        return True
    
    async def dim(self):
        pass

    async def get_state(self):
        await self.plug.update()
        self.state = {
            "power": "on" if self.plug.is_on else "off",
            "current_power_w": self.plug.emeter_realtime.get("power", 0),
        }
        return self.state
    
    async def toggle(self):
        pass


#################################################
# Migrated from essential_assistant project


def get_devices2():
    # Returning a list of TP-Link devices based off of the company prefix, quickest
    # way I can figure out how to get all the devices on the network.
    result = subprocess.check_output("arp -a", shell=True).decode()
    pattern = re.compile(r"(\d+\.\d+\.\d+\.\d+)\s+([\da-f-]{17})", re.I)
    tplink_prefixes = (
        "b0-be-76",
        "50-c7-bf",
        "c0-06-c3",
        "74-da-38",
        "10-da-43",
        "68-ff-7b"
    )
    
    devices_info = {}
    for ip, mac in pattern.findall(result):
        mac_lower = mac.lower()
        #print('mac_lower: ', ip, mac_lower)
        if mac_lower.startswith(tplink_prefixes):
            # devices.append({"ip": ip, "mac": mac_lower})
            
            devices_info[str(mac_lower)] = {
                "direct_device_access": ip,
                "device_id": "",
                "device_mac": mac_lower,
                "device_ip": ip,
                "device_params": ""
                
                
            }
    
    #print('devices_info: ', devices_info)
    return devices_info


def get_devices():
    # Returning a list of TP-Link devices based off of the company prefix, quickest
    # way I can figure out how to get all the devices on the network.
    result = subprocess.check_output("arp -a", shell=True).decode()
    pattern = re.compile(r"(\d+\.\d+\.\d+\.\d+)\s+([\da-f-]{17})", re.I)
    tplink_prefixes = (
        "b0-be-76",
        "50-c7-bf",
        "c0-06-c3",
        "74-da-38",
        "10-da-43",
        "68-ff-7b"
    )
    
    devices_info = {}
    #print('get_devices - devices_info: ', devices_info)
    for ip, mac in pattern.findall(result):
        mac_lower = mac.lower()
        if mac_lower.startswith(tplink_prefixes):
            # devices.append({"ip": ip, "mac": mac_lower})
            
            devices_info[str(mac_lower)] = {
                "direct_device_access": ip,
                "device_id": "",
                "device_mac": mac_lower,
                "device_ip": ip,
                "device_params": ""
            }
    
    return devices_info


def toggle_device(device_ip: str):
    """Toggle a Smart Plug or Switch on or off."""
    
    async def inner_check():
        # plug = SmartPlug(device_ip)
        plug = kasa.iot.IotPlug(device_ip)
        
        await plug.update()  # Get current state #  DO NOT REMOVE
        
        # Show current status
        print(f"Device: {plug.alias} ({device_ip}) is currently {'ON' if plug.is_on else 'OFF'}")
        
        # Toggle the device
        if plug.is_on:
            await plug.turn_off()
        else:
            await plug.turn_on()
        
        # Recheck state
        await plug.update()  # DO NOT REMOVE
        new_state = "ON" if plug.is_on else "OFF"
        print(f"Device: {plug.alias} is now {new_state}")
        
        return plug.is_on
    
    return asyncio.run(inner_check())


async def get_device_data(device_ip: str):
    plug = kasa.iot.IotPlug(device_ip)
    #print('+++ plug: ', plug)
    await plug.update()
    #print('+++ plug: ', plug)
    return vars(plug).get("_sys_info")
    
def get_device_data2(device_ip: str):
    async def inner_check():
        plug = kasa.iot.IotPlug(device_ip)
        #print('+++ plug: ', plug)
        asyncio.run(plug.update())
        #print('+++ plug: ', plug)
        return vars(plug).get("_sys_info")
    
    return asyncio.run(inner_check())

def get_device_info_from_ip(device_ip):
    plug = kasa.iot.IotPlug(device_ip)
    asyncio.run(plug.update())
    return plug.alias, plug.params
    #async def inner_check():
    #    # plug = SmartPlug(device_ip)
    #    plug = kasa.iot.IotPlug(device_ip)
    #    asyncio.run(plug.update())
    #    return plug.alias
    #    #plug = kasa.iot.IotPlug(device_ip)
    #
    #    #await plug.update()  # Get current state #  DO NOT REMOVE
    #    #return plug.alias, plug.data
    #    ## Show current status
    #    #print(f"Device: {plug.alias} ({device_ip}) is currently {'ON' if plug.is_on else 'OFF'}")
    #    #return plug.is_on
    #    ## Toggle the device
    #    #if plug.is_on:
    #    #    await plug.turn_off()
    #    #else:
    #    #    await plug.turn_on()
    #    #
    #    ## Recheck state
    #    #await plug.update()  # DO NOT REMOVE
    #    #new_state = "ON" if plug.is_on else "OFF"
    #    #print(f"Device: {plug.alias} is now {new_state}")
    #    #return plug.is_on
    #
    #return asyncio.run(inner_check())

def testing():
    result_info = get_devices()
    print('result_info: ', result_info)
    #print('result_info; ', result_info)
    for device_mac, device_values in result_info.items():
        print('device_values.get("device_ip"): ', device_values.get("device_ip"))
        plug = kasa.iot.IotPlug(device_values.get("device_ip"))
        #plug = get_device_data
        asyncio.run(plug.update())
        print('plug.alias: ', plug.alias)
        
        #print('plug.alias: ', plug.alias)
        #plug.update()
        #print('plug: ', plug.is_on)
    #toggle_device("192.168.1.194")
    #toggle_device("192.168.1.127")

#testing()
#print('--', get_device_data("192.168.1.127"))
#print('--', get_device_data("192.168.1.194"))

#pp = pprint.PrettyPrinter(indent=4)
#device1 = get_device_data("192.168.1.127")
##device2 = get_device_data("192.168.1.194")
#
#print('DEVICE 1', '-'*50)
#pp.pprint(device1)#.get("_sys_info"))
#print('DEVICE 2', '-'*50)
#pp.pprint(device2)

#print('card--', get_device_info_from_ip("192.168.1.127"))
#print('card--', get_device_info_from_ip("192.168.1.194"))
