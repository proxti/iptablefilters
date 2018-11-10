import sys
import subprocess

# proxti made me

def execute(command):
    subprocess.call(command, shell=True)


def filters(save):
    execute("/sbin/iptables -t mangle -A PREROUTING -m conntrack --ctstate INVALID -j DROP")
    execute("/sbin/iptables -t mangle -A PREROUTING -p tcp ! --syn -m conntrack --ctstate NEW -j DROP")
    execute(
        "/sbin/iptables -t mangle -A PREROUTING -p tcp -m conntrack --ctstate NEW -m tcpmss ! --mss 536:65535 -j DROP")
    execute("/sbin/iptables -t mangle -A PREROUTING -p tcp --tcp-flags FIN,SYN,RST,PSH,ACK,URG NONE -j DROP")
    execute("/sbin/iptables -t mangle -A PREROUTING -p tcp --tcp-flags FIN,SYN FIN,SYN -j DROP")
    execute("/sbin/iptables -t mangle -A PREROUTING -p tcp --tcp-flags SYN,RST SYN,RST -j DROP")
    execute("/sbin/iptables -t mangle -A PREROUTING -p tcp --tcp-flags ACK,URG URG -j DROP")
    execute("/sbin/iptables -t mangle -A PREROUTING -p tcp --tcp-flags ACK,FIN FIN -j DROP")
    execute("/sbin/iptables -t mangle -A PREROUTING -p tcp --tcp-flags ACK,PSH PSH -j DROP")
    execute("/sbin/iptables -t mangle -A PREROUTING -s 224.0.0.0/3 -j DROP")
    execute("/sbin/iptables -t mangle -A PREROUTING -s 169.254.0.0/16 -j DROP")
    execute("/sbin/iptables -t mangle -A PREROUTING -s 172.16.0.0/12 -j DROP")
    execute("/sbin/iptables -t mangle -A PREROUTING -s 0.0.0.0/8 -j DROP")
    execute("/sbin/iptables -t mangle -A PREROUTING -s 240.0.0.0/5 -j DROP")
    execute("/sbin/iptables -t mangle -A PREROUTING -s 127.0.0.0/8 ! -i lo -j DROP")
    execute("/sbin/iptables -t mangle -A PREROUTING -p icmp -j DROP")
    execute("/sbin/iptables -t mangle -A PREROUTING -f -j DROP")
    execute("/sbin/iptables -A INPUT -p tcp -m connlimit --connlimit-above 111 -j REJECT --reject-with tcp-reset")
    execute("/sbin/iptables -N port-scanning")
    execute(
        "/sbin/iptables -A port-scanning -p tcp --tcp-flags SYN,ACK,FIN,RST RST -m limit --limit 1/s --limit-burst 2 -j RETURN")
    execute("/sbin/iptables -A port-scanning -j DROP")

    if save == "y":
        answer = raw_input("Are You on centos or debian? c/d").strip()

        if answer.lower() == "c":
            execute("/sbin/service iptables save")
        else:
            execute("apt-get install iptables-persistent -y")
    else:
        sys.exit()


if __name__ == "__main__":
    while (len(sys.argv) < 2):
        sys.exit("Usage: python " + sys.argv[0] + " y/n (save rules)")
        sys.exit()
        break

    saveyn = sys.argv[1]

    if saveyn == "y":
        saveornot = "y"
        filters(saveornot)
    else:
        saveornot = "n"
        filters(saveornot)
