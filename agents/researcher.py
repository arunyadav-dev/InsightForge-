from crewai import Agent, Task, Crew
from crewai.tools import BaseTool
from crewai_tools import SerperDevTool
import os
import requests
from dotenv import load_dotenv
from crewai import LLM
import os

llm = LLM(
    model="gemini/gemini-2.5-flash",  # ✅ Use this - latest & best
    api_key=os.getenv("GEMINI_API_KEY")
)
load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# 🔧 YouTube Tool
class YouTubeSearchTool(BaseTool):
    name: str = "YouTube Search Tool"
    description: str = "Fetch trending YouTube videos based on keyword"

    def _run(self, keyword: str):
        url = "https://www.googleapis.com/youtube/v3/search"

        params = {
            "part": "snippet",
            "q": keyword,
            "type": "video",
            "maxResults": 5,
            "order": "viewCount",
            "key": YOUTUBE_API_KEY
        }

        response = requests.get(url, params=params)
        data = response.json()

        videos = []

        for item in data.get("items", []):
            videos.append({
                "platform": "youtube",
                "title": item["snippet"]["title"],
                "channel": item["snippet"]["channelTitle"],
                "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                "published_at": item["snippet"]["publishedAt"],
                "keyword": keyword
            })

        return videos


# 🔍 Tools
youtube_tool = YouTubeSearchTool()
google_tool = SerperDevTool()

# 🤖 Researcher Agent
researcher = Agent(
    role="Multi-platform Content Researcher",
    goal="Fetch raw trending content data from YouTube and Google",
    backstory=(
        "You collect trending content ideas from multiple platforms. "
        "You do NOT analyze, only gather structured data."
    ),
    tools=[youtube_tool, google_tool],
    llm=llm,   # ✅ THIS FIXES YOUR ERROR
    verbose=True
)

# 📌 Task
def create_research_task(keyword):
    return Task(
        description=(
            f"For keyword '{keyword}', fetch:\n"
            "1. YouTube trending videos\n"
            "2. Google search trends\n\n"
            "Return combined data in JSON format.\n"
            "Do NOT analyze."
        ),
        agent=researcher,
        expected_output="Structured JSON with youtube + google results"
    )

# 🚀 Run
def run_research(keyword):
    task = create_research_task(keyword)

    crew = Crew(
        agents=[researcher],
        tasks=[task],
        verbose=True
    )

    return crew.kickoff()


# Test
if __name__ == "__main__":
    keyword = input("Enter keyword: ")
    result = run_research(keyword)

    print("\n🔥 Result:\n")
    print(result)