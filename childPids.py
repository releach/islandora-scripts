from islandora_config import Islandora  # Custom
from argparse import RawTextHelpFormatter
import argparse
import logging
import requests
import os


description = """
Generates a list of child pids for book objects and writes them to a txt file. 
Takes a single book pid, or if --list argument supplied, iterates through a txt file of book pids.  

You must be on the Hampshire VPN to use this script. 


Example:
$ python3 childPids.py mtholyoke:58118 pidout.txt
or
$ python3 childPids.py --list pidlist.txt pidout.txt

Attribution: 
- Adapted from Tristan Chambers' book2PDF.py script. 

"""

logging.basicConfig(level=logging.INFO)


class childPids(Islandora):

    def build_child_pids(self, book_pid, pidout):
        logging.info("Generating page pids for %s" % book_pid)
        mode = 'a' if os.path.exists(pidout) else 'w'
        with open(pidout, mode) as a:
            try:
                solr_request = requests.get(
                    f"{self.solr_url}/select?q=RELS_EXT_isPageOf_uri_s%3A%22info%3Afedora%2F{book_pid}%22&rows=1000&fl=PID%2CRELS_EXT_isSequenceNumber_literal_s%2Cfgs_label_s&wt=json&indent=true")
            except:
                logging.error("Failed to connect to Solr. Are you on the VPN?")
            page_pids = solr_request.json()['response']['docs']
            num_pages = len(page_pids)
            if num_pages < 1:
                logging.error(f"No pages found for {book_pid}. Skipping.")
                return
            for page_pid in page_pids:
                page_pid = page_pid['PID']
                a.write(f'{page_pid}\n')

    def build_child_pids_list(self, pidlist, pidout):
        logging.info("Generating page pids for %s" % pidlist)
        mode = 'a' if os.path.exists(pidout) else 'w'
        with open(pid, 'r') as r, open(pidout, mode) as a:
            for book_pid in r:
                book_pid = book_pid.strip()
                try:
                    solr_request = requests.get(
                        f"{self.solr_url}/select?q=RELS_EXT_isPageOf_uri_s%3A%22info%3Afedora%2F{book_pid}%22&rows=1000&fl=PID%2CRELS_EXT_isSequenceNumber_literal_s%2Cfgs_label_s&wt=json&indent=true")
                except:
                    logging.error(
                        "Failed to connect to Solr. Are you on the VPN?")

                page_pids = solr_request.json()['response']['docs']

                num_pages = len(page_pids)
                if num_pages < 1:
                    logging.error(f"No pages found for {book_pid}. Skipping.")
                    return
                for page_pid in page_pids:
                    page_pid = page_pid['PID'].strip()
                    a.write(f'{page_pid}\n')


if __name__ == "__main__":

    childPids = childPids()
    childPids.load_home_config('prod')

    argparser = argparse.ArgumentParser(
        description=description, formatter_class=RawTextHelpFormatter)
    argparser.add_argument(
        'PID', help="PID of the book you want child pids for")
    argparser.add_argument(
        'PIDOUT', help="Provide a filename for pidout file")
    argparser.add_argument(
        "--list", help="Provide path to a list of book pids", action="store_true")
    cliargs = argparser.parse_args()
    pid = cliargs.PID
    pidout = cliargs.PIDOUT
    if cliargs.list is True:
        childPids.build_child_pids_list(pid, pidout)
    else:
        childPids.build_child_pids(pid, pidout)
