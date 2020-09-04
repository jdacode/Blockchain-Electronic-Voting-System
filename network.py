from ipaddress import ip_address


class Network:
    def __init__(self, ip):
        self.ip = ip

    @staticmethod
    def is_a_valid_ip(ip):
        try:
                ip_add, port = ip.split(":")
                if int(port) < 0 or ' ' in port: return False
                if ip_add == 'localhost' or ip_address(ip_add): return True
        except ValueError:
            return False





