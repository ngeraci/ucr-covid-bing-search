# UCR COVID-19 Bing search results

This is a quick example script that uses the [Bing Web Search API v7](https://azure.microsoft.com/en-us/services/cognitive-services/bing-web-search-api/) to retrieve search result URLs and write them to a text file.

## Use case
UCR Library uses [Archive-It](https://archive-it.org/) for web archiving of campus websites. During the COVID-19 pandemic, the University Archivist is creating an Archive-It collection specifically documenting campus websites related to COVID-19. Archive-It needs to be seeded with specific URLs to crawl. So this script was written to use the Bing Web Search API to search for sites with the keyword "covid-19" on the "ucr.edu" domain, and write the URLs to a text file (one URL per line) that can be used to populate Archive-It.

## Account configuration
These are my rough notes from the setup process.

1. Sign up for Azure free account
2. Log in at portal.azure.com
3. "Cognitive Services" -> "Create Cognitive Services" -> "Bing Search". Pricing tier F1 (free).
4. Resource -> "Keys and Endpoint"
	* create "config.ini" file in same directory as script
	* copy and paste the provided "Endpoint" and "Key 1" values into config file
	* append "/search" to endpoint URL
	```
	[bing-search-api]
	endpoint = https://(YOUR RESOURCE NAME).cognitiveservices.azure.com/bing/v7.0/search
	key = (YOUR KEY)
	```


## Notes
* Search term is set as a string on line 18. Our search is "site:ucr.edu covid-19"
* Took about 11 minutes to run - retrived 48947 URLs
* Free tier is 1000 transactions/month -- each transaction with this script gets 50 search results, so 50,000 results/month.
	* [More pricing info](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/search-api/) 
	* Azure free account gives $200 credit on signup
	* UCR initial query fell just under 1 month free tier usage. Not sure yet how often we will re-run to pick up new URLs.
* Getting large proportion of duplicate URLs so far -- seems to be an [issue other people have also had](https://stackoverflow.com/questions/39216665/when-using-bing-search-api-how-do-you-omit-duplicate-results) with this API. So far I have separately deduplicated URLs before sending to University Archivist to load in Archive-It, but will look into tweaking search parameters and/or deduping as part of this script.
* Other potential features to add: command-line interface with search term as argument, option to download full JSON from Bing (not just URL), option to set outfile location (currently writes to same directory as script).
* [Google Custom Search API](https://developers.google.com/custom-search/v1/overview) was another option I researched for this use case, but had daily limits on free tier query counts that seemed more challenging to work with (i.e. spreading out queries over multiple days)