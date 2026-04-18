#A it is not using crew AI , but it is providing faster result . I(Arun) tested it 

import os
import requests
from dotenv import load_dotenv
import json
from datetime import datetime

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

def fetch_youtube_videos(keyword):
    """Fetch YouTube videos directly"""
    try:
        url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "part": "snippet",
            "q": keyword,
            "type": "video",
            "maxResults": 5,
            "order": "viewCount",
            "key": YOUTUBE_API_KEY
        }
        
        print(f"📺 Fetching YouTube videos...")
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if "error" in data:
            print(f"❌ YouTube Error: {data['error']['message']}")
            return []
        
        videos = []
        for item in data.get("items", []):
            videos.append({
                "title": item["snippet"]["title"],
                "channel": item["snippet"]["channelTitle"],
                "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                "published_at": item["snippet"]["publishedAt"][:10],
                "description": item["snippet"]["description"][:100]
            })
        
        print(f"✅ Found {len(videos)} YouTube videos\n")
        return videos
    
    except Exception as e:
        print(f"❌ YouTube Error: {e}\n")
        return []


def fetch_google_trends(keyword):
    """Fetch Google search trends directly"""
    try:
        url = "https://google.serper.dev/search"
        headers = {
            "X-API-KEY": SERPER_API_KEY,
            "Content-Type": "application/json"
        }
        payload = {
            "q": keyword,
            "num": 10
        }
        
        print(f"🔍 Fetching Google trends...")
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        data = response.json()
        
        results = []
        for item in data.get("organic", []):
            results.append({
                "title": item.get("title"),
                "link": item.get("link"),
                "snippet": item.get("snippet", "")[:100]
            })
        
        print(f"✅ Found {len(results)} Google results\n")
        return results
    
    except Exception as e:
        print(f"❌ Google Error: {e}\n")
        return []


def display_results(keyword, youtube_videos, google_results):
    """Display formatted results"""
    
    print("\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + f" RESEARCH RESULTS - {keyword.upper()} ".center(78) + "║")
    print("╚" + "═" * 78 + "╝")
    
    # YouTube Section
    if youtube_videos:
        print("\n📺 YOUTUBE TRENDING VIDEOS")
        print("─" * 78)
        
        for idx, video in enumerate(youtube_videos, 1):
            print(f"\n#{idx}. {video['title'][:65]}")
            print(f"   Channel  : {video['channel']}")
            print(f"   Posted   : {video['published_at']}")
            print(f"   Link     : {video['url']}")
    else:
        print("\n📺 YOUTUBE TRENDING VIDEOS")
        print("─" * 78)
        print("❌ No results found")
    
    # Google Section
    if google_results:
        print("\n\n🔍 GOOGLE SEARCH RESULTS")
        print("─" * 78)
        
        for idx, result in enumerate(google_results[:5], 1):
            print(f"\n#{idx}. {result['title'][:65]}")
            print(f"   Summary  : {result['snippet']}")
            print(f"   Link     : {result['link']}")
    else:
        print("\n\n🔍 GOOGLE SEARCH RESULTS")
        print("─" * 78)
        print("❌ No results found")
    
    print("\n\n" + "╔" + "═" * 78 + "╗")
    print("║" + f" ✅ COMPLETE - {datetime.now().strftime('%H:%M:%S')} ".center(78) + "║")
    print("╚" + "═" * 78 + "╝\n")


def main():
    print("\n" + "=" * 78)
    print("🚀 CONTENT RESEARCH TOOL (FAST VERSION - NO CREWAI)".center(78))
    print("=" * 78)
    
    keyword = input("\n🔍 Enter keyword to research: ").strip()
    
    if not keyword:
        print("❌ Keyword cannot be empty!")
        return
    
    print(f"\n⏳ Searching for '{keyword}'...\n")
    
    # Fetch data
    youtube_videos = fetch_youtube_videos(keyword)
    google_results = fetch_google_trends(keyword)
    
    # Display results
    display_results(keyword, youtube_videos, google_results)


if __name__ == "__main__":
    main()