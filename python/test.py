import bluetooth

service_matches = bluetooth.find_service(address="00:20:12:08:A1:2B")

if(not len(service_matches)==0):
    print("cnm")
    print(service_matches[0]['host'])
    print(service_matches[0]['name'])
    print(service_matches[0]['port'])