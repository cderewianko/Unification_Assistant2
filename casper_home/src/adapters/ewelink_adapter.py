
import uuid

from casper_home.src.devices import ewelink_device


class EWeLinkAdapter:
    async def discover(self) -> list[dict]:
        devices = []
        #print('pure')
        #device_list = await ewelink_device.test_get_devices()
        device_list = await ewelink_device.get_device_list()
        #print('device_list: ', device_list)
        for ewelink_data in device_list:
            print('EWElink mac: ', ewelink_data["extra"]["extra"]["mac"])
            #print('new ------------------------------------------------------')
            #print('ewelink_data: ', ewelink_data)
            #print("casper_uuid:", str(uuid.uuid4()))
            #print("name:", ewelink_data.get("name", "NO_ALIAS"))
            #print("manufacturer:", ewelink_data.get("brandName", "NO_MANUFACTURER"))
            #print("model:", ewelink_data["extra"]["extra"]["model"])
            #print("type:", ewelink_data.get("type", "NO_TYPE"))
            #print("ip:", ewelink_data.get("ip", "NO_IP"))
            #print("mac:", ewelink_data["extra"]["extra"]["mac"])
            #print("device_id:", ewelink_data.get("deviceid", "NO_DEVICE_ID"))
            #print("api_name:", ewelink_data.get("apikey", "NO_APIKEY"))
            #print("status:", ewelink_data["params"]["switch"])
            #print('"connection": {"protocol": "local_http", "status": kasa_data.get("relay_state")},')
            #print("capabilities:", ["on_off"])
            #print("metadata:", ewelink_data)
            #continue
            
            #data =
            #ewelink_data = ewelink_device.get_device_data(ip)
            devices.append({
                "casper_uuid": str(uuid.uuid4()),
                "name": ewelink_data.get("name", "NO_ALIAS"),
                "manufacturer": ewelink_data.get("brandName", "NO_MANUFACTURER"),
                "model": ewelink_data["extra"]["extra"]["model"],
                "type": ewelink_data.get("type", "NO_TYPE"),
                "identifiers": {
                    "ip": ewelink_data.get("ip", "NO_IP"),
                    "mac": ewelink_data["extra"]["extra"]["mac"],
                    "device_id": ewelink_data.get("deviceid", "NO_DEVICE_ID"),
                    "api_name": ewelink_data.get("apikey", "NO_APIKEY")
                },
                "status": ewelink_data["params"]["switch"],
                # "connection": {"protocol": "local_http", "status": kasa_data.get("relay_state")},
                "capabilities": ["on_off"],
                "metadata": ewelink_data
            })
        
        return devices
