"""
Notify device connections and disconnections
"""
import device
import asyncio
import telegram_notifier


class Notifier:
    def __init__(self):
        self.dev = device.Device()
        self.device_list = {}
        self.first_run = True
        self.tele_notifier = telegram_notifier.Bot("<Bot Token>")

    async def run(self):
        active_device_list = {}
        all_device_list = {}

        while True:
            try:
                all_devices = self.dev.get_device_stats()

                for each in all_devices:
                    all_device_list[each["mac"]] = each["device_name"]

                active_devices = self.dev.get_active_device_stats()

                # Check newly connected devices
                active_devs = []
                for each in active_devices:
                    if each[1] not in active_device_list:
                        active_device_list[each[1]] = all_device_list[each[1]]
                        if not self.first_run:
                            message = "Device connected: " + all_device_list[each[1]] + ":" + each[1]
                            print(message)
                            self.tele_notifier.send_message(chat_id="<user_id>", text=message)
                    active_devs.append(each[1])

                # Check offline devices
                delete_list = []
                for each in active_device_list:
                    if each not in active_devs:
                        delete_list.append(each)
                        message = "Device disconnected: " + all_device_list[each] + ":" + each
                        print(message)
                        self.tele_notifier.send_message(chat_id="<user_id>", text=message)

                # Delete the offline devices
                for each in delete_list:
                    del active_device_list[each]

                self.first_run = False

            except Exception as e:
                print("Error" + str(e))

            await asyncio.sleep(5)


if __name__ == '__main__':
    notif = Notifier()
    asyncio.run(notif.run())

