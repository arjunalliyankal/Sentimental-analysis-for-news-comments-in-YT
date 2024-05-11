

# FOR SCRAPE AND CLEAN THE DATA

import os
import sys
import csv
import demoji
import unicodedata
import re
import time  # For implementing rate limiting
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# YouTube Data API key
API_KEY = "AIzaSyAwCOQt2tGyBbVlrMWla85JsGYPoUJBRZk"

def get_comments(client, video_id, token=None):
    try:
        response = (
            client.commentThreads()
            .list(
                part="snippet",
                videoId=video_id,
                textFormat="plainText",
                maxResults=100,
                pageToken=token,
            )
            .execute()
        )
        return response
    except HttpError as e:
        print("HTTP Error:", e)
        return None
    except Exception as e:
        print("Error:", e)
        return None

def get_reply_comments(client, comment_id, token=None):
    try:
        response = (
            client.comments()
            .list(
                part="snippet",
                parentId=comment_id,
                textFormat="plainText",
                maxResults=100,
                pageToken=token,
            )
            .execute()
        )
        return response
    except HttpError as e:
        print("HTTP Error:", e)
        return None
    except Exception as e:
        print("Error:", e)
        return None

def remove_emoji(inputString):
    dem = demoji.findall(inputString)
    for item in dem.keys():
        inputString = inputString.replace(item, '')
    return inputString
    # return demoji.get_emoji_regexp().sub(u'', inputString)

def remove_non_english(inputString):
    return ''.join(c for c in unicodedata.normalize('NFKD', inputString) if c.isalnum() and c.isalpha() and c.islower() or c.isupper() or c.isspace())

def remove_long_white_spaces(inputString):
    return re.sub(r'\s+', ' ', inputString)

def process_csv(input_file, csv_writer):
    cleaned_comments = set()  # Store comments to remove duplicates
    with open(input_file, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader, None)  # Get the header if it exists, or None
        if header:
            csv_writer.writerow(header)  # Write the header to the output file
        for row in csv_reader:
            cleaned_comment = remove_emoji(row[0])
            cleaned_comment = remove_non_english(cleaned_comment)
            cleaned_comment = remove_long_white_spaces(cleaned_comment)
            if cleaned_comment.strip():  # Check if comment is not empty after cleaning
                if cleaned_comment not in cleaned_comments:  # Check for duplicates
                    csv_writer.writerow([cleaned_comment])
                    cleaned_comments.add(cleaned_comment)  # Add to set to mark as seen

def main(text):
    #if len(sys.argv) != 2:
     #   print("Usage: python cmntrply.py video_ID")
      #  sys.exit(1)
    
    # vid_id =text
    # output_file = f"{vid_id}_comments.csv"
    

# ... (other parts of your code)

    video_id =text 
    output_folder = "comments_csv"
    reply_output_file = f"{video_id}_reply_comments.csv"
    cleaned_output_file = 'cleaned_comments.csv'

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    output_file = os.path.join(output_folder, f"{video_id}_comments.csv")

    with open(output_file, "w", newline="", encoding="utf-8") as file:
        # ... (rest of your code)
     yt_client = build(
        "youtube", "v3", developerKey=API_KEY
    )

    comments = []
    next_page_token = None

    while True:
        resp = get_comments(yt_client, video_id, next_page_token)

        if not resp:
            break

        comments += resp.get("items", [])
        next_page_token = resp.get("nextPageToken")

        if not next_page_token:
            break

        time.sleep(1)  # Adding a delay to avoid hitting rate limits

    print(f"Total comments fetched: {len(comments)}")

    reply_comments = []

    for comment in comments:
        reply_token = None
        while True:
            resp = get_reply_comments(yt_client, comment["id"], reply_token)

            if not resp:
                break

            reply_comments += resp.get("items", [])
            reply_token = resp.get("nextPageToken")

            if not reply_token:
                break

            time.sleep(1)  # Adding a delay to avoid hitting rate limits

    print(f"Total reply comments fetched: {len(reply_comments)}")

    with open(output_file, "w", newline="", encoding="utf-8") as file:
        csv_writer = csv.writer(file)
        for i in comments:
            row = [i["snippet"]["topLevelComment"]["snippet"]["textDisplay"]]
            csv_writer.writerow(row)

    with open(reply_output_file, "w", newline="", encoding="utf-8") as file:
        csv_writer = csv.writer(file)
        for i in reply_comments:
            row = [i["snippet"]["textDisplay"]]
            csv_writer.writerow(row)

    with open(cleaned_output_file, 'w', encoding='utf-8', newline='') as new_csv:
        csv_writer = csv.writer(new_csv)
        csv_writer.writerow(['comment'])

        process_csv(output_file, csv_writer)
        process_csv(reply_output_file, csv_writer)

    print("Cleaning process completed. Output saved to", cleaned_output_file)

if __name__ == "__main__":
    main()
