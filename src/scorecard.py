import pandas as pd
import re

def generate_vendor_scorecard(df):
    vendor_stats = {}

    for _, row in df.iterrows():
        vendor = row['channel']
        if vendor not in vendor_stats:
            vendor_stats[vendor] = {
                "posts": [],
                "prices": []
            }
        vendor_stats[vendor]["posts"].append(row['cleaned_text'])
        vendor_stats[vendor]["prices"].extend([int(s) for s in re.findall(r'\d+', row['cleaned_text'])])

    final_scores = {}
    for vendor, data in vendor_stats.items():
        avg_price = sum(data["prices"]) / len(data["prices"]) if data["prices"] else 0
        post_freq = len(data["posts"])
        score = 0.5 * post_freq + 0.5 * avg_price
        final_scores[vendor] = {
            "Posts": post_freq,
            "Avg Price (ETB)": avg_price,
            "Lending Score": score
        }

    score_df = pd.DataFrame(final_scores).T
    score_df.to_csv("results/vendor_scorecard.csv")
    print("✅ Saved vendor scorecard to results/vendor_scorecard.csv")
