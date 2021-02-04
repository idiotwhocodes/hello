from requests.sessions import session
from bs4 import BeautifulSoup as bs 
from requests_html import HTMLSession
import pandas as pd
# from googleapiclient.discovery import build
# from pprint import pprint

# Enter Your video url here
video_url = "https://www.youtube.com/watch?v=4aWMGUF5RMw"

session = HTMLSession()

# response = session.get(video_url)
# response.html.render(sleep=1)
# soup = bs(response.html.html, "html.parser")
API_KEY = "AIzaSyDLHZt0LlS4ZybFCJKZOnJSoPJQJlRRg28"
API_NAME = 'youtube'
API_VERSION = 'v3'


def get_details(url):
    response = session.get(url)
    response.html.render(sleep=1)
    soup = bs(response.html.html, "html.parser")

    # open("video.html", "w", encoding="utf8").write(output.html.html)  
    output = {}

    # Retriving Video title
    output["title"] = soup.find('h1').text.strip()
    
    # Number of views
    output["views"] = int(''.join([x for x in soup.find("span", attrs={"class": "view-count"}).text if x.isdigit()]))
    
    # Publising date
    output["date_published"] = soup.find("div", {"id": "date"}).text[1:]

    # video description
    output["description"] = soup.find("yt-formatted-string", {"class": "content"}).text

    # Duration
    output["duration"] = soup.find("span", {"class": "ytp-time-duration"}).text

    # Video Tags For video classfication
    output["tags"] = ', '.join([ meta.attrs.get("content") for meta in soup.find_all("meta", {"property": "og:video:tag"}) ])

    # Likes
    text_yt_formatted_strings = soup.find_all("yt-formatted-string", {"id": "text", "class": "ytd-toggle-button-renderer"})
    # print(text_yt_formatted_strings)
    output["likes"] = text_yt_formatted_strings[0].text

    # DisLikes
    output["dislikes"] = text_yt_formatted_strings[1].text

    # Channel_Info
    channel_tag = soup.find("yt-formatted-string", {"class": "ytd-channel-name"}).find("a")

    # channel name
    channel_name = channel_tag.text
    
    # channel URL
    channel_url = f"https://www.youtube.com{channel_tag['href']}"
    
    # number of subscribers as str
    channel_subscribers = soup.find("yt-formatted-string", {"id": "owner-sub-count"}).text.strip()
    output["channel_name"] = channel_name
    output["channel_url"] = channel_url
    output["subscribers"] = channel_subscribers
    # output['channel'] = {'name': channel_name, 'url': channel_url, 'subscribers': channel_subscribers}

    # # Number of commnets
    # output["comments"] = int(''.join([x for x in soup.find("yt-fomatted-string", attrs={"class": "count-text"}).text if x.isdigit()]))

    # output["comments"] = 

    return output


if __name__ == "__main__":
    # import argparse
    # parser = argparse.ArgumentParser(description="YouTube Video Data Extractor")
    # parser.add_argument("url", help="URL of the YouTube video")
    # args = parser.parse_args()
    # url = args.url

    # Direct Entered URL
    url = video_url

    # get the data
    data_file = get_details(url)
    # # print in nice format
    # print(data_file)
    # print(f"Title: {data['title']}")
    # print(f"Views: {data['views']}")
    # print(f"Published at: {data['date_published']}")
    # print(f"Video Duration: {data['duration']}")
    # print(f"Video tags: {data['tags']}")
    # print(f"Likes: {data['likes']}")
    # print(f"Dislikes: {data['dislikes']}")
    # print(f"\nDescription: {data['description']}\n")
    # print(f"\nTags: {data['channel']['info']}")
    # print(f"\nChannel Name: {data['channel']['name']}")
    # print(f"Channel URL: {data['channel']['url']}")
    # print(f"Channel Subscribers: {data['channel']['subscribers']}")

    df = pd.DataFrame(data=data_file, index=[1])
    df = (df.T)
    print(df)
    df.to_excel('data_file.xlsx')