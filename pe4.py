import wikipedia
import time
import re
from concurrent.futures import ThreadPoolExecutor

def clean_filename(title, suffix=""):
  
    safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '_', '-')).rstrip()
    return f"{safe_title}{suffix}.txt"


def section_a():
    print("--- Section A: Sequential Download ---")
    
    search_term = 'generative artificial intelligence'
    topics = wikipedia.search(search_term)
    print(f"Found {len(topics)} topics for '{search_term}'.")

    start_time_a = time.perf_counter()

    for topic in topics:
        try:
          
            page = wikipedia.page(topic, auto_suggest=False)
            
            title = page.title
            
            references = page.references
            
            filename = clean_filename(title)
            
            with open(filename, 'w', encoding='utf-8') as f:
            
                f.write('\n'.join(references))
                
            print(f"  [A] Successfully saved references for: {title} to {filename}")
            
        except wikipedia.exceptions.PageError:
            print(f"  [A] Could not find Wikipedia page for topic: {topic}")
        except wikipedia.exceptions.DisambiguationError as e:
            print(f"  [A] Disambiguation error for topic: {topic}. Options: {e.options}")
        except Exception as e:
            print(f"  [A] An unexpected error occurred for topic {topic}: {e}")

    end_time_a = time.perf_counter()

    print(f"\nSection A (Sequential) execution time: {end_time_a - start_time_a:.4f} seconds\n")
    return topics


def wiki_dl_and_save(topic):
    """Retrieves Wikipedia page references for a topic and saves them to a .txt file."""
    try:
        page = wikipedia.page(topic, auto_suggest=False)
        
        title = page.title
        references = page.references
        
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
    
    topics_b = topics
    print(f"Processing {len(topics_b)} topics concurrently.")

    start_time_b = time.perf_counter()

    with ThreadPoolExecutor() as executor:
        executor.map(wiki_dl_and_save, topics_b)

    end_time_b = time.perf_counter()

    print(f"\nSection B (Concurrent) execution time: {end_time_b - start_time_b:.4f} seconds\n")

if __name__ == "__main__":
    topics_list = section_a()
    
    section_b(topics_list)
    
    print("Assignment execution complete. Check the generated .txt files.")

