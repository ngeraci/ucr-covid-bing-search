""" Use Bing Web Search API v7 to retrieve result URLs for search term.
    Write list of URLs to .txt file
"""
import re
import configparser
import time
import requests


def main():
    """ read config file
        call get_results() function with config and search term
    """
    config = configparser.ConfigParser()
    config.read("config.ini")
    bing_config = config["bing-search-api"]

    search_term = "site:ucr.edu covid-19"

    outfile_name = re.sub(
        r"[:\.\s\\\/]", "_",
        search_term) + "-" + time.strftime("%Y%m%dT%H%M%SZ") + ".txt"

    for page in get_results(bing_config, search_term):
        with open(outfile_name, "a") as outfile:
            for site in page["webPages"]["value"]:
                outfile.write("\n{}".format(site["url"]))


def get_results(bing_config, search_term, count=50):
    """ Generator function to return paged JSON results from Bing Web Search API v7.

            bing_config: configparser object or dictionary
                         required values: "endpoint", "key"

            search_term: search query string

            count: results per page (50 maximum)
    """

    offset = 0

    first_page = requests.get(bing_config["endpoint"],
                              headers={
                                  "Ocp-Apim-Subscription-Key":
                                  bing_config["key"]
                              },
                              params={
                                  "q": search_term,
                                  "count": count,
                              }).json()

    total_estimated_matches = first_page["webPages"]["totalEstimatedMatches"]
    offset += count

    yield first_page

    while offset < (total_estimated_matches - count):
        next_page = requests.get(bing_config["endpoint"],
                                 headers={
                                     "Ocp-Apim-Subscription-Key":
                                     bing_config["key"]
                                 },
                                 params={
                                     "q": search_term,
                                     "count": count,
                                     "offset": offset
                                 }).json()
        offset += count
        yield next_page


if __name__ == '__main__':
    main()
