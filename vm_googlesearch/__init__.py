from bs4 import BeautifulSoup
from requests import get
from WebSearcher import locations

def fetch_results(search_term, location, number_results, language_code, proxy=None):
        escaped_search_term = search_term.replace(' ', '+')
        loc_id = locations.get_location_id(location)
        usr_agent = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/61.0.3163.100 Safari/537.36'}
        google_url = 'https://www.google.com/search?q={}&uule={}&num={}&hl={}'.format(escaped_search_term, loc_id, number_results+1,
                                                                              language_code)
        print("URL: %s"%google_url)
        proxies = None
        if proxy:
            if proxy[:5]=="https":
                proxies = {"https":proxy} 
            else:
                proxies = {"http":proxy}
        
        response = get(google_url, headers=usr_agent, proxies=proxies)    
        response.raise_for_status()

        return response.text

def parse_results(raw_html):
    soup = BeautifulSoup(raw_html, 'html.parser')
    result_block = soup.find_all('div', attrs={'class': 'g'})
    for result in result_block:
        link = result.find('a', href=True)
        title = result.find('h3')
        if link and title:
            yield link['href']

def search(term, num_results=10, lang="en", location="", proxy=None):
    

    html = fetch_results(term, location, num_results, lang)
    return list(parse_results(html))