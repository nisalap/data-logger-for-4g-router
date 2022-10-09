import requests
import json

DEVICE_1 = "ZLT_P11X"


class Device:
    def __init__(self):
        self.device = DEVICE_1

    def get_device_stats(self):
        endpoint = "http://192.168.8.1/cgi-bin/http.cgi"
        body = {"cmd": 122, "method": "GET", "language": "EN", "sessionId": ""}
        response = requests.post(url=endpoint, json=body)
        json_response = json.loads(response.content.decode("utf-8"))
        dev_list = self.decode_device_stats(json_response)
        # print(dev_list)
        return dev_list

    def get_active_device_stats(self):
        endpoint = "http://192.168.8.1/cgi-bin/http.cgi"
        body = {"cmd": 120, "method": "GET", "language": "EN", "sessionId": ""}
        response = requests.post(url=endpoint, json=body)
        json_response = json.loads(response.content.decode("utf-8"))
        dev_list = json_response["data"]
        # print(dev_list)
        return dev_list

    def get_internet_stats(self):
        endpoint = "http://192.168.8.1/cgi-bin/http.cgi"
        body = {"method": "POST", "cmd": 82,"language": "EN", "sessionId": ""}
        response = requests.post(url=endpoint, json=body)
        json_response = json.loads(response.content.decode("utf-8"))
        int_stats = self.decode_internet_stats(json_response)
        # print(int_stats)
        return int_stats

    def decode_internet_stats(self, json_message):
        # data =  {"success":true,"cmd":82,"message":"EARFCN/ARFCN@1$Frequency Band@1$Downlink Bandwidth@1$TZTRANSMODE@1$RSRP@1$RSRQ@1$SINR@13$TZTXPOWER@8$Serving CellID@324352$Physical CellID@408$RSSI@-51$RRCState@Connected$DL_MCS@27$CQI@11","other":""}
        message = json_message["message"]
        categories = message.split('$')
        stats = {}
        for each in categories:
            spl = each.split('@')
            if "RRCState" in spl[0]:
                continue
            else:
                key = spl[0].replace(" ", "_")
                stats[key] = int(spl[1])
        return stats

    def decode_device_stats(self, json_message):
        # dd = {"success": true, "cmd": 122, "data":[["1665393747","mac","ip","name","0"],["1665393747","mac","ip","name","0"]]}
        # Format timestamp device_name, mac, ip, expire_time
        devices = []
        for each in json_message["data"]:
            device = {"device_name": each[3], "mac": each[1], "ip": each[2], "expire_time": int(each[0])}
            devices.append(device)
        return devices
