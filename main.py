from app.search.search import search_companies
from app.utils.url_filters import filter_company_urls
from app.classifier.url_classifier import classify_results

def main():
    query = input("Enter your lead search query: ")
    results = search_companies(query, max_results=30)

    filtered_results = filter_company_urls(results)
    classified_results = classify_results(filtered_results)
    print("\nClassified Company Websites:\n")

    for index, item in enumerate(classified_results, start=1):
        if item["type"]=="company":
            action = "scrape_company"
        elif item["type"] in ["directory", "article"]:
            action = "extract_company_links"
        else:
            action = "ignore"
        print(f"{index}, {item['title']}")
        print(item['url'])
        print(f"Type: {item['type']}")
        print(f"Confidence: {item['confidence']}")
        print(f"Action: {action}")
        print(f"Scores: {item['scores']}")
        print("---------------")

if __name__ == "__main__":
    main()