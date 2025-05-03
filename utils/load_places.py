from api.get_cities import get_places
from models.rl_agent import RLAgent
import pandas as pd
import concurrent.futures
import time

def fetch_places_with_delay(location, category, fetch_limit=10):
    print(f"Fetching {fetch_limit} places for {category} in {location}...")
    data = get_places(location, category=category, limit=fetch_limit)
    time.sleep(1)
    return category, data

def load_places(state):
    """Fetch places for a given state using multithreading with rate limiting."""
    location = f"{state}, India"
    
    category_counts = [5, 4, 3, 3, 2, 1]  
    
    agent = RLAgent()
    categories = agent.recommend_categories(state)
    all_places = []
    seen_names = set()
    print(categories)
    
    # Use ThreadPoolExecutor with controlled execution
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        future_to_category = {
            executor.submit(fetch_places_with_delay, location, category): category
            for category in categories
        }

        for future in concurrent.futures.as_completed(future_to_category):
            category, data = future.result()

            if "features" not in data or not data["features"]:
                print(f"No data found for category: {category}")
                continue

            # Flatten and create DataFrame
            places = [item["properties"] for item in data["features"]]
            df = pd.DataFrame(places)

            # Select and rename relevant columns
            selected_columns = {
                "name": "name",
                "state_district": "district",
                "city": "city",
                "formatted": "address"
            }
            df = df.reindex(columns=selected_columns.keys(), fill_value="N/A")
            df = df.rename(columns=selected_columns)
            df["category"] = category.capitalize()

            # Drop already seen names (optional but recommended)
            df = df[~df["name"].isin(seen_names)]

            # Sample required number
            required_count = category_counts[categories.index(category)]
            df = df.sample(n=min(required_count, len(df)), random_state=42)

            # Track seen names
            seen_names.update(df["name"].tolist())

            all_places.append(df)

    # Final merge
    if all_places:
        final_df = pd.concat(all_places, ignore_index=True)
    else:
        final_df = pd.DataFrame(columns=["name", "district", "city", "address", "category"])
    
    return final_df