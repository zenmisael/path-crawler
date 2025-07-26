#!/usr/bin/env python3

import requests
import argparse
import re
from urllib.parse import urljoin, urlparse
import os

visited_links = set()
log_file = None

def get_arguments():
    parser = argparse.ArgumentParser(description="Simple recursive web crawler with logging")
    parser.add_argument("-u", "--url", dest="url", required=True, help="Target URL to crawl")
    return parser.parse_args()

def extract_all_hrefs(url):
    try:
        response = requests.get(url, timeout=5)
        content_type = response.headers.get('Content-Type', '')
        if 'text/html' not in content_type:
            return []
        html = response.text
        return re.findall(r'href=[\'"]?([^\'" >]+)', html)
    except requests.RequestException as e:
        print(f"[!] Error fetching {url}: {e}")
        return []

def log_to_file(link):
    with open(log_file, "a") as f:
        f.write(link + "\n")

def crawl(url, base_domain):
    if url in visited_links:
        return

    visited_links.add(url)
    print(f"[+] Link found: {url}")
    log_to_file(url)

    for href in extract_all_hrefs(url):
        absolute_link = urljoin(url, href)
        parsed_link = urlparse(absolute_link)

        # Skip external domains
        if base_domain not in parsed_link.netloc:
            continue

        clean_url = absolute_link.split("#")[0]
        if clean_url not in visited_links:
            crawl(clean_url, base_domain)

def main():
    global log_file

    print("""
######################################################################
#--> Dir Crawler                                                  <--#
#--> by BORG                                                      <--#
######################################################################
""")

    args = get_arguments()
    target_url = args.url
    parsed = urlparse(target_url)
    base_domain = parsed.netloc

    # Safe filename for logging
    log_file = f"{base_domain.replace(':', '_')}.txt"

    # Clear file if it exists
    open(log_file, "w").close()

    crawl(target_url, base_domain)
    print(f"\n[+] Crawling completed. Results saved to: {log_file}")

if __name__ == "__main__":
    main()
