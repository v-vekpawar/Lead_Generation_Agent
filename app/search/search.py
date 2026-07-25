from ddgs import DDGS

def search_companies(query:str, max_results: int = 10):
    """
    Search the web and return company-related results.

    Args:
        query: Search phrase
        max_results: Number of results to return

    Returns:
        List of dictionaries containing search results
    """
    results=[]
    with DDGS() as ddgs:
        search_results = ddgs.text(query, max_results=max_results)
        for result in search_results:
            results.append({
                "title":result.get("title"),
                "url":result.get("href"),
                "snippet":result.get("body")
            })

    return results

if __name__ == "__main__":
    query = "digital marketing compaines in Mumbai"
    companies = search_companies(query, max_results=10)

    for company in companies:
        print("\n-------------------")
        print(f"Company: {company["title"]}")
        print(f"Website: {company["url"]}")
        print(f"Description: {company["snippet"]}")