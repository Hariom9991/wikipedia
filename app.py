from fastapi import FastAPI
import wikipedia

app = FastAPI()

@app.get("/")
async def get_wikipedia_url(topic: str):
    try:
        # Search for the topic
        search_results = wikipedia.search(topic, results=1)
        
        if search_results:
            # Get the page using the first search result
            page = wikipedia.page(search_results[0])
            # Return the actual Wikipedia URL
            return {"topic": topic, "url": page.url}
        else:
            # If no results found, try to get the page directly
            page = wikipedia.page(topic)
            return {"topic": topic, "url": page.url}
            
    except wikipedia.exceptions.DisambiguationError as e:
        # If there's ambiguity, try the first option
        try:
            page = wikipedia.page(e.options[0])
            return {"topic": topic, "url": page.url}
        except:
            return {"topic": topic, "url": "https://en.wikipedia.org/wiki/Main_Page"}
    except wikipedia.exceptions.PageError:
        # If page doesn't exist, return main page
        return {"topic": topic, "url": "https://en.wikipedia.org/wiki/Main_Page"}
    except:
        # For any other error, return main page
        return {"topic": topic, "url": "https://en.wikipedia.org/wiki/Main_Page"}
