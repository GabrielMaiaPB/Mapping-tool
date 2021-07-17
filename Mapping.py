import os
import threading

mapped_addresses = []
threads = []

ipconfig = os.popen("ipconfig").read()
with open("ip.txt", "w+") as ip:
    ip.write(ipconfig)
    ip.seek(0)
    for line_file1 in ip.readlines():
        if "IPv4" in line_file1:
            line_file1 = line_file1[line_file1.rfind(":")+2:]
            ip_address = line_file1
            break

ip_range = ip_address[:ip_address.rfind(".")+1]


def pinger(counter: int) -> None:
    machine = ip_range + str(counter)
    command = os.popen(f"ping {machine} -n 1").read()
    with open("results.txt", "a+") as results1:
        results1.write(command)


for i in range(1, 255):
    t = threading.Thread(target=pinger, args=(i,))
    threads.append(t)
    t.start()

for thread in threads:
    thread.join()

with open("results.txt", "r+") as results:
    for line_file2 in results.readlines():
        if "TTL" in line_file2:
            mapped_addresses.append(line_file2[:line_file2.find(":")])
    results.seek(0)
    results.truncate(0)

auxiliar_impressao = 0
for mapped_address in mapped_addresses:
    auxiliar_impressao += 1
    print(f"[{auxiliar_impressao}]: {mapped_address}")
