import pandas as pd
import requests
import time
from os import getenv
import json

API_KEY = getenv("GOOGLE_BOOKS_API_KEY")
CSV_FILE = "Summaries.csv"
SAVE_EVERY = 10  # Save progress after every N requests

# Load CSV
df = pd.read_csv(CSV_FILE, sep=",") 

# Ensure "Google-Book-ID" column exists
if "Google-Book-ID" not in df.columns:
    df["Google-Book-ID"] = None

errored = []
update_count = 0  # Counter to track how many requests have been made

def fetch_google_books_data(title, author):
    """Fetches book summary, image, keywords, and Google Book ID from Google Books API."""
    query = f"{title} {author}"
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}&key={API_KEY}"

    try:
        response = requests.get(url)
        
        # If rate limit is exceeded, exit immediately
        if response.status_code == 429:
            df.to_csv(CSV_FILE, sep=",", index=False)
            print("🚨 Rate limit exceeded. Exiting...")
            exit(1)

        data = response.json()

        # Print full response in case of errors
        if "error" in data and data["error"].get("code") == 429:
            print(json.dumps(data, indent=4))

        book_item = data.get("items", [])[0]
        book = book_item["volumeInfo"]

        google_book_id = book_item.get("id", None)  # Extract Google Book ID
        summary = book.get("description", -1)
        image_url = book.get("imageLinks", {}).get("thumbnail", None)
        categories = book.get("categories", None)
        keywords = ", ".join(categories) if categories else None

        return summary, image_url, keywords, google_book_id
    except IndexError:
        # Some Titles don't return any results, return -1 for those
        print(f"Index Error in {title}")
        return -1, None, None, None
    except Exception as e:
        print(f"Error fetching {title}: {e}")
        errored.append({"title": title, "author": author})
        return None, None, None, None

def check_processed(element):
    """Check if the element is already processed, int -1 is assigned for processed rows"""
    if pd.isna(element):
        return True
    if element == "-1":
        return False
    return False
        
# Process books that need summaries
for index, row in df.iterrows():
    if check_processed(row["Summary"]): 
        title, author = row["Book-Title"], row["Book-Author"]
        
        summary, image_url, keywords, google_book_id = fetch_google_books_data(title, author)
        
        if summary:
            df.at[index, "Summary"] = summary
            df.at[index, "Image-From-Google"] = image_url
            df.at[index, "Keywords"] = keywords
            df.at[index, "Google-Book-ID"] = google_book_id  # Store Google Book ID
            update_count += 1

            # Save progress every `SAVE_EVERY` requests
            if update_count % SAVE_EVERY == 0:
                df.to_csv(CSV_FILE, sep=",", index=False)
                print(f"✅ Saved progress after {update_count} updates.")

# Final save in case there are unsaved changes
df.to_csv(CSV_FILE, sep=",", index=False)
print("Processed: ", update_count)
print("🎉 All missing summaries fetched!")

with open('error.json', 'w') as err_file:
    json.dump(errored, err_file, indent=4)

