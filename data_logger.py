import datetime
import device
import asyncio
import os


class DataLogger:
    def __init__(self):
        self.interval = 5 # seconds
        self.device = device.Device()

    def get_state_file_prefix(self):
        dt = datetime.datetime.now()
        prefix = "logs/" + datetime.datetime.strftime(dt, "%Y-%m-%d")
        return prefix

    def ensure_file(self, file, type):
        if os.path.exists(file):
            return True
        else:
            if type == "internet":
                with open(file, 'w+') as f:
                    f.write("timestamp,EARFCN/ARFCN,Frequency_Band,Downlink_Bandwidth,TZTRANSMODE,RSRP,RSRQ,SINR,TZTXPOWER,Serving_CellID,Physical_CellID,RSSI,DL_MCS,CQI")
            elif type == "device":
                with open(file, 'w+') as f:
                    f.write("timestamp,device_name,mac,ip,expire_time")
            return True

    def log_device_stats(self):
        stats = self.device.get_device_stats()
        file_name = self.get_state_file_prefix() + "_device_stats.csv"
        if self.ensure_file(file_name, "device"):
            record = ""
            for each in stats:
                timestamp = str(datetime.datetime.now())
                record = record + "\n" + timestamp
                for key, value in each.items():
                    record = record + "," + str(value)
            with open(file_name, 'a') as f:
                f.write(record)
        return stats

    def log_internet_stats(self):
        stats = self.device.get_internet_stats()
        file_name = self.get_state_file_prefix() + "_internet_stats.csv"
        timestamp = str(datetime.datetime.now())
        record = "\n" + timestamp
        if self.ensure_file(file_name, "internet"):
            for key, value in stats.items():
                record = record + "," + str(value)
            with open(file_name, 'a') as f:
                f.write(record)
        return stats

    async def loop_internet_stats(self):
        while True:
            try:
                stats = self.log_internet_stats()
                print("Added log: " + str(stats))
                await asyncio.sleep(self.interval)
            except Exception as e:
                await asyncio.sleep(self.interval * 5)

    async def loop_device_stats(self):
        while True:
            try:
                stats = self.log_device_stats()
                print("Added log: " + str(stats))
                await asyncio.sleep(self.interval)
            except Exception as e:
                await asyncio.sleep(self.interval * 5)

    async def loop(self):
        a = await asyncio.gather(
            self.loop_internet_stats(),
            self.loop_device_stats())
        print(a)


def main():
    dl = DataLogger()
    asyncio.run(dl.loop())


if __name__ == '__main__':
    main()
