# import dearpygui.dearpygui as dpg
# import requests
# import base64
# import re

# def clean_markdown(text):
#     # Basic markdown cleaning (same as previous)
#     text = re.sub(r"#+\s*", "", text)
#     text = re.sub(r"\*+\s?", "", text)
#     text = re.sub(r"\[.*?\]\(.*?\)", "", text)
#     return text.strip()

# def fetch_readme(sender, app_data):
#     repo_url = dpg.get_value("input_url")
#     try:
#         # Show loading indicator
#         dpg.show_item("loading_tag")
#         dpg.disable_item("fetch_btn")
        
#         # Extract repo parts
#         parts = repo_url.strip("/").split("/")
#         if len(parts) < 2 or "github.com" not in repo_url:
#             raise ValueError("Invalid GitHub URL")
            
#         owner, repo = parts[-2], parts[-1]
#         api_url = f"https://api.github.com/repos/{owner}/{repo}/readme"
        
#         # Fetch from GitHub API
#         response = requests.get(api_url, headers={"Accept": "application/vnd.github.v3+json"})
#         response.raise_for_status()
        
#         content = base64.b64decode(response.json()["content"]).decode("utf-8")
#         cleaned_content = clean_markdown(content)
        
#         # Update output
#         dpg.set_value("output_text", cleaned_content)
        
#     except Exception as e:
#         dpg.set_value("output_text", f"Error: {str(e)}")
#     finally:
#         dpg.hide_item("loading_tag")
#         dpg.enable_item("fetch_btn")

# def create_gui():
#     dpg.create_context()
#     dpg.create_viewport(title='GitHub README Viewer', width=800, height=600)
    
#     with dpg.window(label="Main Window", tag="main_window"):
#         # Input Section
#         dpg.add_text("Enter GitHub Repository URL:")
#         dpg.add_input_text(tag="input_url", width=600)
#         dpg.add_spacer(height=5)
        
#         # Fetch Button with Loading Indicator
#         with dpg.group(horizontal=True):
#             dpg.add_button(label="Fetch README", tag="fetch_btn", callback=fetch_readme)
#             dpg.add_loading_indicator(tag="loading_tag", show=False)
        
#         # Output Display
#         dpg.add_spacer(height=10)
#         dpg.add_separator()
#         dpg.add_spacer(height=10)
#         dpg.add_text("README Contents:", color=(0, 255, 0))
#         dpg.add_input_text(
#             tag="output_text", 
#             multiline=True, 
#             width=760, 
#             height=400, 
#             readonly=True
#         )
    
#     dpg.setup_dearpygui()
#     dpg.show_viewport()
#     dpg.set_primary_window("main_window", True)
#     dpg.start_dearpygui()
#     dpg.destroy_context()

# if __name__ == "__main__":
#     create_gui()


# CODE -1 


# import dearpygui.dearpygui as dpg
# import requests
# import base64
# import re

# def clean_markdown(text):
#     text = re.sub(r"#+\s*", "", text)
#     text = re.sub(r"\*+\s?", "", text)
#     text = re.sub(r"\[.*?\]\(.*?\)", "", text)
#     return text.strip()

# def is_direct_readme_url(url):
#     """Check if the URL is a direct link to a README file"""
#     patterns = [
#         r"github\.com/.*/blob/.*README\.md$",
#         r"github\.com/.*/README\.md$",
#         r"raw\.githubusercontent\.com/.*/.*/README\.md$"
#     ]
#     return any(re.search(pattern, url) for pattern in patterns)

# def process_direct_readme(url):
#     """Convert GitHub README URL to raw content URL"""
#     if "raw.githubusercontent.com" in url:
#         return url
    
#     # Convert regular GitHub URL to raw URL
#     url = url.replace("github.com", "raw.githubusercontent.com")
#     url = url.replace("/blob/", "/")
#     return url

# def fetch_readme(sender, app_data):
#     input_url = dpg.get_value("input_url")
#     try:
#         dpg.show_item("loading_tag")
#         dpg.disable_item("fetch_btn")
        
#         content = ""
#         if is_direct_readme_url(input_url):
#             # Handle direct README URL
#             raw_url = process_direct_readme(input_url)
#             response = requests.get(raw_url)
#             response.raise_for_status()
#             content = response.text
#         else:
#             # Handle repository URL
#             parts = input_url.strip("/").split("/")
#             if len(parts) < 2 or "github.com" not in input_url:
#                 raise ValueError("Invalid GitHub URL")
            
#             owner, repo = parts[-2], parts[-1]
#             api_url = f"https://api.github.com/repos/{owner}/{repo}/readme"
#             response = requests.get(api_url, headers={"Accept": "application/vnd.github.v3+json"})
#             response.raise_for_status()
            
#             content = base64.b64decode(response.json()["content"]).decode("utf-8")
        
#         cleaned_content = clean_markdown(content)
#         dpg.set_value("output_text", cleaned_content)
        
#     except Exception as e:
#         error_msg = f"Error: {str(e)}"
#         if "404" in str(e):
#             error_msg += "\nREADME might not exist in this repository"
#         dpg.set_value("output_text", error_msg)
#     finally:
#         dpg.hide_item("loading_tag")
#         dpg.enable_item("fetch_btn")

# def create_gui():
#     dpg.create_context()
#     dpg.create_viewport(title='GitHub README Viewer', width=800, height=600)
    
#     with dpg.window(label="Main Window", tag="main_window"):
#         dpg.add_text("Enter GitHub Repository or Direct README URL:")
#         dpg.add_input_text(tag="input_url", width=600, hint="e.g., https://github.com/user/repo or https://github.com/user/repo/blob/main/README.md")
#         dpg.add_spacer(height=5)
        
#         with dpg.group(horizontal=True):
#             dpg.add_button(label="Fetch README", tag="fetch_btn", callback=fetch_readme)
#             dpg.add_loading_indicator(tag="loading_tag", show=False)
        
#         dpg.add_spacer(height=10)
#         dpg.add_separator()
#         dpg.add_spacer(height=10)
#         dpg.add_text("README Contents:", color=(0, 255, 0))
#         dpg.add_input_text(
#             tag="output_text", 
#             multiline=True, 
#             width=760, 
#             height=400, 
#             readonly=True
#         )
    
#     dpg.setup_dearpygui()
#     dpg.show_viewport()
#     dpg.set_primary_window("main_window", True)
#     dpg.start_dearpygui()
#     dpg.destroy_context()

# if __name__ == "__main__":
#     create_gui()




# CODE _3

import dearpygui.dearpygui as dpg
import requests
import base64
import re
from textblob import TextBlob  # Lightweight NLP library

# Predefined technology list (expand as needed)
TECH_STACK_KEYWORDS = {
    'python', 'javascript', 'react', 'nodejs', 'django', 'flask',
    'tensorflow', 'pytorch', 'docker', 'kubernetes', 'aws',
    'mongodb', 'postgresql', 'graphql', 'typescript', 'java',
    'c++', 'rust', 'go', 'vue', 'angular', 'svelte', 'fastapi'
}

def analyze_readme(content):
    """Perform lightweight NLP analysis on README content"""
    analysis = {}
    
    # Basic statistics
    analysis['word_count'] = len(content.split())
    analysis['paragraph_count'] = len(content.split('\n\n'))
    
    # Sentiment analysis
    blob = TextBlob(content)
    analysis['sentiment'] = blob.sentiment.polarity  # Range: -1 to 1
    
    # Readability metrics
    analysis['readability'] = blob.sentiment.subjectivity  # Range: 0 to 1
    analysis['flesch_score'] = textstat.flesch_reading_ease(content)
    
    # Technology detection
    found_tech = []
    content_lower = content.lower()
    for tech in TECH_STACK_KEYWORDS:
        if re.search(rf'\b{tech}\b', content_lower):
            found_tech.append(tech.title())
    analysis['technologies'] = found_tech
    
    # Project title detection
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    analysis['title'] = title_match.group(1).strip() if title_match else "Untitled Project"
    
    # Complexity rating (simple heuristic)
    tech_density = len(found_tech) / (len(content.split())/100)  # Tech terms per 100 words
    analysis['complexity'] = min(10, round(tech_density * 2, 1))  # Scale to 0-10
    
    # Overall rating calculation
    analysis['rating'] = round(
        (analysis['flesch_score'] * 0.3) + 
        (analysis['sentiment'] * 2 + 1) * 2.5 +  # Convert -1-1 to 0-5
        (len(found_tech) * 0.5) +
        (analysis['complexity'] * 0.4),
        1
    )
    
    return analysis

def update_analysis_display(analysis):
    """Update UI elements with analysis results"""
    dpg.set_value("tech_stack", ", ".join(analysis['technologies']) or "None detected")
    dpg.set_value("project_title", analysis['title'])
    dpg.set_value("readability_score", f"{analysis['flesch_score']:.1f} (0-100 scale)")
    dpg.set_value("complexity_score", f"{analysis['complexity']:.1f}/10")
    dpg.set_value("overall_rating", f"{analysis['rating']:.1f}/10")
    
    # Set color based on rating
    rating_color = (0, 1, 0) if analysis['rating'] > 6 else (1, 1, 0) if analysis['rating'] > 4 else (1, 0, 0)
    dpg.configure_item("rating_value", color=rating_color)

def fetch_readme(sender, app_data):
    input_url = dpg.get_value("input_url")
    try:
        dpg.show_item("loading_tag")
        dpg.disable_item("fetch_btn")
        
        content = ""
        if is_direct_readme_url(input_url):
            raw_url = process_direct_readme(input_url)
            response = requests.get(raw_url)
            response.raise_for_status()
            content = response.text
        else:
            parts = input_url.strip("/").split("/")
            if len(parts) < 2 or "github.com" not in input_url:
                raise ValueError("Invalid GitHub URL")
            
            owner, repo = parts[-2], parts[-1]
            api_url = f"https://api.github.com/repos/{owner}/{repo}/readme"
            response = requests.get(api_url, headers={"Accept": "application/vnd.github.v3+json"})
            response.raise_for_status()
            
            content = base64.b64decode(response.json()["content"]).decode("utf-8")
        
        cleaned_content = clean_markdown(content)
        dpg.set_value("output_text", cleaned_content)
        
        # Perform analysis
        analysis = analyze_readme(cleaned_content)
        update_analysis_display(analysis)
        
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        if "404" in str(e):
            error_msg += "\nREADME might not exist in this repository"
        dpg.set_value("output_text", error_msg)
    finally:
        dpg.hide_item("loading_tag")
        dpg.enable_item("fetch_btn")

def create_gui():
    dpg.create_context()
    dpg.create_viewport(title='GitHub README Analyzer', width=1000, height=800)
    
    with dpg.window(label="Main Window", tag="main_window"):
        with dpg.group(horizontal=True):
            # Left Panel - Input and Analysis
            with dpg.child_window(width=300):
                dpg.add_text("Enter GitHub URL:")
                dpg.add_input_text(tag="input_url", width=280, hint="Repository or README.md URL")
                dpg.add_button(label="Analyze README", tag="fetch_btn", callback=fetch_readme)
                dpg.add_loading_indicator(tag="loading_tag", show=False)
                
                dpg.add_spacer(height=20)
                dpg.add_separator()
                dpg.add_spacer(height=10)
                
                dpg.add_text("Project Analysis", color=(0, 200, 255))
                dpg.add_text("Title:")
                dpg.add_text(tag="project_title", default_value="N/A")
                dpg.add_spacer(height=5)
                
                dpg.add_text("Detected Tech Stack:")
                dpg.add_text(tag="tech_stack", default_value="Analyzing...")
                dpg.add_spacer(height=5)
                
                dpg.add_text("Readability Score:")
                dpg.add_text(tag="readability_score", default_value="N/A")
                dpg.add_spacer(height=5)
                
                dpg.add_text("Technical Complexity:")
                dpg.add_text(tag="complexity_score", default_value="N/A")
                dpg.add_spacer(height=5)
                
                dpg.add_text("Overall Rating:")
                dpg.add_text(tag="overall_rating", default_value="N/A", color=(0, 1, 0), tag="rating_value")
            
            # Right Panel - README Display
            with dpg.child_window():
                dpg.add_text("README Contents:", color=(0, 255, 0))
                dpg.add_input_text(
                    tag="output_text", 
                    multiline=True, 
                    width=680, 
                    height=700, 
                    readonly=True
                )
    
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("main_window", True)
    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == "__main__":
    create_gui()