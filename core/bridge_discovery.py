from zeroconf import ServiceBrowser, ServiceListener, Zeroconf
import json
import codecs
import socket


class MyListener(ServiceListener):

    def update_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        print(f"Service {name} updated")

    def remove_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        print(f"Service {name} removed")

    def add_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        info = zc.get_service_info(type_, name)
        print(f"Service {name} added, service info: {info}")
        if len(info.addresses) != 1:
            print(f"Aborting, unexpected info.addresses length: {len(info.addresses)}")
            return
        data = {
            "Bridge ID": codecs.decode(info.properties.get(codecs.encode("bridgeid"))).upper(),
            'Model ID': codecs.decode(info.properties.get(codecs.encode("modelid"))).upper(),
            "IP": socket.inet_ntoa(info.addresses[0])
        }
        with open("data/bridge.json", "w") as json_file:
            json.dump(data, json_file, indent=4)


zeroconf = Zeroconf()
listener = MyListener()
browser = ServiceBrowser(zeroconf, "_hue._tcp.local.", listener)
try:
    input("Press enter to exit...\n\n")
finally:
    zeroconf.close()
    print("finally done")
