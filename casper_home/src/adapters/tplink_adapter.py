
import uuid

from casper_home.src.devices import tplink_device


class TPLinkAdapter:
    async def discover(self) -> list[dict]:
        devices = []
        device_info = tplink_device.get_devices()
        #print('__________________-----------device_info: ', device_info)
        for mac, ip in device_info.items():  # from arp or kasa lib
            print('TP Link mac: ', mac)
            #print('iprrrrrrr: ', ip.get("device_ip"))
            kasa_data = await tplink_device.get_device_data(ip.get("device_ip"))
            #print('kasa_data: ', kasa_data)
            #continue
            devices.append({
                "casper_uuid": str(uuid.uuid4()),
                "name": kasa_data.get("alias", "NO_ALIAS"),
                "manufacturer": kasa_data.get("dev_name", "NO_MANUFACTURER"), #"TP-Link",
                "model": kasa_data.get("model", "NO_MODEL"),
                "type": kasa_data.get("type", "NO_TYPE"),
                "identifiers": {
                    "ip": ip,
                    "mac": mac, #kasa_data.get("mac"),
                    "device_id": kasa_data.get("deviceId", "NO_DEVICE_ID"),
                    "api_name": None
                },
                "status": kasa_data.get("relay_state", 0),
                #"connection": {"protocol": "local_http", "status": kasa_data.get("relay_state")},
                "capabilities": ["on_off"],
                "metadata": kasa_data
            })
        #print('DEVICES: ', devices)
        return devices
