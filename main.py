from app.search.search import search_companies
from app.utils.url_filters import filter_company_urls

def main():
    query = input("Enter your lead search query: ")
    results = search_companies(query, max_results=30)

    filtered_results = filter_company_urls(results)
    print("\nFiltered Company Websites:\n")

    for index, item in enumerate(filtered_results, start=1):
        print(f"{index}, {item['title']}")
        print(item['url'])
        print()

if __name__ == "__main__":
    main()