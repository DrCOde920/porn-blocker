import time

# Define the list of websites you want to block permanently
sites_to_block = ["www.xnxx.com", "www.fuckcams.com", "www.pornhub.com", "www.redtube.com", "www.youporn.com", "www.spankbang.com", "www.tube8.com", "www.homemade-tube.com", "www.porn.com", "www.brazzers.com", "www.nuvid.com", "www.yuvutu.com", "www.eporner.com", "www.tnaflix.com", "www.pornhd.com", "www.fapdu.com", "www.slutload.com", "www.porn300.com", "www.pornhat.com", "www.pornmd.com", "www.xvideos.com", "www.redtube.com", "www.youjizz.com", "www.spankwire.com", "www.tube8.com", "www.homemade-tube.com", "www.porn.com", "www.brazzers.com", "www.nuvid.com", "www.yuvutu.com", "www.eporner.com", "www.tnaflix.com", "www.pornhd.com", "www.fapdu.com", "www.slutload.com", "www.porn300.com", "www.pornhat.com", "www.pornmd.com", "www.xhamster.com", "www.pornhubpremium.com", "www.onlyfans.com", "www.patreon.com", "www.fetlife.com", "www.adultfriendfinder.com", "www.cam4.com", "www.chaturbate.com", "www.myfreecams.com", "www.streamate.com", "www.bongaCams.com", "www.imlive.com", "www.flirt4free.com", "www.livejasmin.com", "www.cams.com", "www.stripchat.com", "www.camster.com", "www.sexier.com", "www.iwantclips.com", "www.clips4sale.com",  "www.fleshlight.com", "www.povd.com", "www.eroprofile.com", "www.sex.com", "www.sexsearch.com", "www.adultsearch.com", "www.backpage.com", "www.craigslist.org", "www.loveawake.com", "www.mature.nl", "www.mature.nl", "www.mature.nl"] #

# The location of the hosts file on Linux (Kali)
hosts_path = "/etc/hosts" #
# The IP address to redirect blocked sites to (localhost)
redirect = "127.0.0.1" #

def add_sites_to_hosts():
    print("Attempting to add blocked sites to hosts file...")
    try:
        with open(hosts_path, 'r+') as hostfile: # Open in read/write mode
            hosts_content = hostfile.read()
            for site in sites_to_block:
                if site not in hosts_content:
                    # Add the site to the hosts file if not already present
                    hostfile.write(redirect + " " + site + "\n")
                    print(f"Blocked: {site}")
                else:
                    print(f"Site already blocked: {site}")
        print("Website blocking complete. You can now close this script.")
    except PermissionError:
        print(f"Error: Permission denied. Please run this script with sudo.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    add_sites_to_hosts()
