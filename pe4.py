import wikipedia
import time
import re
from concurrent.futures import ThreadPoolExecutor

# Function to clean up the title for a valid filename
def clean_filename(title, suffix=""):
    # Remove characters that are invalid in filenames and replace spaces with underscores
    # The assignment example "Music and artificial intelligence" -> "Music and artificial intelligence.txt"
    # suggests a simple cleanup is sufficient, but we'll be safe.
    # We'll allow alphanumeric, spaces, and underscores.
    safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '_', '-')).rstrip()
    return f"{safe_title}{suffix}.txt"

# --- Section A: Sequentially download wikipedia content ---
def section_a():
    print("--- Section A: Sequential Download ---")
    
    # 1. Use the wikipedia.search method to return a list of topics related to 'generative artificial intelligence'.
    search_term = 'generative artificial intelligence'
    topics = wikipedia.search(search_term)
    print(f"Found {len(topics)} topics for '{search_term}'.")

    # 3. Print to the console the amount of time it took the above code to execute
    start_time_a = time.perf_counter()

    # 2. Iterate over the topics returned in #1 above using a for loop.
    for topic in topics:
        try:
            # assign the page contents to a variable named page using the wikipedia.page method. 
            # Be sure to use auto_suggest=False when using this method
            page = wikipedia.page(topic, auto_suggest=False)
            
            # assign the page title to a variable (using page.title)
            title = page.title
            
            # retrieve the references for that page (using page.references)
            references = page.references
            
            # write the references (with each reference on its own line) to a .txt file 
            # where the name of the file is the title of the topic.
            filename = clean_filename(title)
            
            with open(filename, 'w', encoding='utf-8') as f:
                # page.references returns a list of strings (URLs). 
                # We join them with a newline character to ensure each link is on its own line.
                f.write('\n'.join(references))
                
            print(f"  [A] Successfully saved references for: {title} to {filename}")
            
        except wikipedia.exceptions.PageError:
            print(f"  [A] Could not find Wikipedia page for topic: {topic}")
        except wikipedia.exceptions.DisambiguationError as e:
            print(f"  [A] Disambiguation error for topic: {topic}. Options: {e.options}")
        except Exception as e:
            print(f"  [A] An unexpected error occurred for topic {topic}: {e}")

    end_time_a = time.perf_counter()

    # 3. Print execution time
    print(f"\nSection A (Sequential) execution time: {end_time_a - start_time_a:.4f} seconds\n")
    return topics

# --- Section B: Concurrently download wikipedia content ---

# 2. Create a function def wiki_dl_and_save(topic):
def wiki_dl_and_save(topic):
    """Retrieves Wikipedia page references for a topic and saves them to a .txt file."""
    try:
        # retrieves the wikipedia page for the topic
        page = wikipedia.page(topic, auto_suggest=False)
        
        # gets the title and the references for the topic
        title = page.title
        references = page.references
        
        # creates a .txt file where the name of the file is the title of the topic
        # writes the references to the file created in the preceding step (each reference should be on its own line)
        filename = clean_filename(title, suffix="_concurrent")
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(references))
            
        print(f"  [B] Successfully saved references for: {title} to {filename}")
        
    except wikipedia.exceptions.PageError:
        print(f"  [B] Could not find Wikipedia page for topic: {topic}")
    except wikipedia.exceptions.DisambiguationError as e:
        print(f"  [B] Disambiguation error for topic: {topic}. Options: {e.options}")
    except Exception as e:
        print(f"  [B] An unexpected error occurred for topic {topic}: {e}")

def section_b(topics):
    print("--- Section B: Concurrent Download ---")
    
    # 1. Use the wikipedia.search method to return a list of topics related to 'generative artificial intelligence'.
    # We will reuse the list from Section A to ensure a fair comparison.
    topics_b = topics
    print(f"Processing {len(topics_b)} topics concurrently.")

    # 4. Print to the console the amount of time it took the above code to execute
    start_time_b = time.perf_counter()

    # 3. Use the ThreadPoolExecutor from the concurrent.futures library to execute concurrently the function defined in step 2.
    with ThreadPoolExecutor() as executor:
        # you can call the .map() method of the ThreadPoolExecutor object with the function name and list of topics
        executor.map(wiki_dl_and_save, topics_b)

    end_time_b = time.perf_counter()

    # 4. Print execution time
    print(f"\nSection B (Concurrent) execution time: {end_time_b - start_time_b:.4f} seconds\n")

if __name__ == "__main__":
    # Run Section A first, and pass the topics list to Section B
    topics_list = section_a()
    
    # Run Section B
    section_b(topics_list)
    
    print("Assignment execution complete. Check the generated .txt files.")

