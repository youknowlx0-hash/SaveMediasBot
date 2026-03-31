import requests

def search_youtube(query):
    url = f"https://ytsearcher.vercel.app/api?query={query}"
    res = requests.get(url).json()
    return res[:5]
