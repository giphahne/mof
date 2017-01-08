import time
import os
import sys
from lxml import html
import requests
import zipfile
import re
from datetime import datetime


TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S.%fZ'

class LogPrinter(object):
    """
    A class implementing a 'log like' interface toward 
    printing.
    """

    @classmethod
    def _format_log_message(cls, log_message):
        timestamp = datetime.strftime(datetime.now(), TIMESTAMP_FORMAT)
        return ("{timestamp}: {log_message}"
                .format(timestamp=timestamp,
                        log_message=log_message))

    @classmethod
    def _print_log_message(cls, log_message):
        print (cls._format_log_message(log_message))

    @classmethod
    def _print_err_message(cls, log_message):
        print (cls._format_log_message(log_message), file=sys.stderr)
        
    @classmethod
    def info(cls, log_message):
        cls._print_log_message(log_message)
        return log_message

    @classmethod
    def error(cls, log_message):
        cls._print_err_message(log_message)


class FlushingLogPrinter(LogPrinter):
    """
    """
    @classmethod
    def info(cls, log_message):
        cls._print_log_message(log_message)
        sys.stdout.flush()
        return log_message

    @classmethod
    def error(cls, log_message):
        cls._print_err_message(log_message)
        sys.stderr.flush()
        
lg = FlushingLogPrinter


# def download_and_extract_zip_file_to_directory(file_url, data_dir, dest_filename):

#     destination_path = os.path.join(data_dir, dest_filename)
    
#     lg.info("getting: {}".format(file_url))
#     lg.info("saving to: {}".format(destination_path))
    
#     response = requests.get(
#         file_url,
#         stream=True
#     )

#     with open(destination_path, 'wb') as destination_file:
#         for file_chunk in response.iter_content(chunk_size=1024):
#             if file_chunk:
#                 destination_file.write(file_chunk)

#     if zipfile.is_zipfile(destination_path):
#         lg.info("yes, is zip")
#     else:
#         lg.info("no, not zip")

#     zipped_data = zipfile.ZipFile(destination_path, mode='r')

#     lg.info("zipfile contains: {}".format(zipped_data.namelist()))

#     zipped_data.extractall(path=data_dir)


def extract_file_url_from_page_text(page_text):
    
    #element_url_pattern = "https[^ ]*ROCKWELL[0-9][0-9][0-9][0-9]\.zip"
    file_url_pattern = "https[^ ]*ROCKWELL[0-9][0-9][0-9][0-9]\.zip"

    urls = re.findall(file_url_pattern, page_text)

    if len(urls) == 0:
        lg.info("no URLs found matching pattern: {0}".format(file_url_pattern))
        return None
    
    elif not all(urls[0] == r for r in urls):
        # raise <something>
        lg.info("multiple, distinct URLs found!: {0}".format(urls))
        return None

    else:
        # they're all the same, so just return the first:
        return urls[0]

    
if __name__ == "__main__":

    current_dir = sys.path[0]
    data_dir = os.path.join(current_dir, "cycle_databases")
    
    
    with requests.Session() as s:
    

        lg.info("fetching 'Downloads' page...")
        page_response = s.get(
            'https://www.nysenate.gov/legislation'
        )
        lg.info("'Downloads' page response: {0}".format(page_response))

        page_text = page_response.text

        lg.info("Attempting to extract file URL from page text...")
        file_url = extract_file_url_from_page_text(page_text)
        lg.info("found file URL: {0}".format(file_url))

        current_filename = file_url.split("/")[-1]
        lg.info("current filename: {0}".format(current_filename))

        if current_filename in os.listdir(data_dir):
            lg.info("current file already exists in data dir, exiting.")
        else:            
            local_filepath = download_and_extract_zip_file_to_directory(
                file_url, data_dir, dest_filename=current_filename
            )
    

    
