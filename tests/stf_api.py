import requests
import json
import random
import time


class StfDevices:

    def __init__(self, ip):
        self.ip = ip
        self.prefix = "http://"
        self.device_suffix = "/api/v1/devices"
        self.user_device_suffix = "/api/v1/user/devices"
        self.token = "951cfcdf4bc045849f55e810d863fbecaf01b07b54cf49879b573a77a8c389f4"
        self.device_url = self.prefix + self.ip + self.device_suffix
        self.user_device_url = self.prefix + self.ip + self.user_device_suffix

    def __get_all_devices_info(self):
        headers = {"Authorization": "Bearer " + self.token}
        result = requests.get(self.device_url, headers=headers)
        return result

    def __get_user_device(self):
        headers = {"Authorization": "Bearer " + self.token}
        result = requests.get(self.user_device_url, headers=headers)
        return result

    def count_all_devices(self):
        all_devices = self.__get_all_devices_info()
        if all_devices.status_code == 200:
            devices_json = json.loads(all_devices.text)
            if devices_json["success"]:
                print("total %d devices" % len(devices_json["devices"]))
                return len(devices_json["devices"])
            else:
                print("failed to get devices info")
        else:
            print("wrong status: %d" % all_devices.status_code)

    def count_available_devices(self):
        all_devices = self.__get_all_devices_info()
        available_devices = []
        if all_devices.status_code == 200:
            devices_json = json.loads(all_devices.text)
            if devices_json["success"]:
                for d in devices_json["devices"]:
                    if d["present"] == True and d["using"] == False:
                        available_devices.append(d)
                print("%d devices available for you to use" % len(available_devices))
                return len(available_devices), available_devices
            else:
                print("failed to get devices info")
        else:
            print("wrong status: %d" % all_devices.status_code)

    def get_single_device(self):
        count, available_devices = self.count_available_devices()
        if count > 0:
            # get random available device
            random.shuffle(available_devices)
            return available_devices[0]
        else:
            timeout = 600
            print("no device to use, wait until %s min timeout" % str(round(timeout/60, 1)))
            while timeout:
                time.sleep(10)
                timeout -= 10
                count, available_devices = self.count_available_devices()
                if count > 0:
                    random.shuffle(available_devices)
                    return available_devices[0]
            print("no available device now, please check the stf device pool")
            return []

    def get_single_device_info(self, serial):
        single_device_url = "/".join([self.device_url, serial])
        headers = {"Authorization": "Bearer " + self.token}
        result = requests.get(single_device_url, headers=headers)
        return result

    def rent_single_device(self, serial):
        headers = {"Authorization": "Bearer " + self.token, "Content-Type": "application/json"}
        data = {"serial": serial}
        result = requests.post(self.user_device_url, headers=headers, json=data)
        if json.loads(result.text)["success"] != True:
            print("rent device fail, rent again")
            time.sleep(10)
            result = requests.post(self.user_device_url, headers=headers, json=data)
        return result

    def return_rented_device(self, serial):
        return_url = "/".join([self.user_device_url, serial])
        headers = {"Authorization": "Bearer " + self.token}
        result = requests.delete(return_url, headers=headers)
        return result

    def get_user_device_remote_connect_url(self, serial):
        my_devices = self.__get_user_device()
        if my_devices.status_code == 200:
            devices_json = json.loads(my_devices.text)
            if devices_json["success"]:
                for d in devices_json["devices"]:
                    if d["serial"] == serial:
                        return d["remoteConnectUrl"]
            else:
                print("failed to get user devices info")
        else:
            print("wrong status: %d" % my_devices.status_code)

