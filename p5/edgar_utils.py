import re
import pandas as pd
import netaddr
from bisect import bisect

ips = pd.read_csv("ip2location.csv")

def lookup_region(ip):
    ip_re = re.sub(r"[a-z]", r"0", ip)
    ip_int = int(netaddr.IPAddress(ip_re))
    idx = bisect(ips["low"], ip_int)
    return ips.iloc[idx-1]["region"]


class Filing:
    def __init__(self, html):
        
        dates = []
        for date in re.findall(r"\d{4}-\d{2}-\d{2}", html):
            if date[0:2] == '19' or date[0:2] == '20':
                dates.append(date)
            
        self.dates =  dates
        
        if len(re.findall(r"SIC.(\d+)", html)) == 0:
            self.sic = None  
        else:
            self.sic = int(re.findall(r"SIC.(\d+)", html)[0])
            
        addresses = []
        for addr_html in re.findall(r'<div class="mailer">([\s\S]+?)</div>', html):
            lines = []           
            address = re.findall(r'<span class="mailerAddress">([\s\S]+?)</span>',                                         addr_html)
            
            if len(address) > 0:
                for line in address:
                    lines.append(line.strip())
                addresses.append("\n".join(lines))

        self.addresses = addresses

    def state(self):
        for addr in self.addresses:
            state_abr = len(re.findall(r'([A-Z]{2}) \d{5}', addr))
            if state_abr > 0:
                return re.findall(r'([A-Z]{2}) \d{5}', addr)[0] 
        return None
        
            
        
    
    
    
    
    