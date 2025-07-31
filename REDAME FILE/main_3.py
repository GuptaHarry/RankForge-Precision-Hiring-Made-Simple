import dearpygui.dearpygui as dpg
import requests
import base64
import re
from textblob import TextBlob
import textstat


TECH_STACK_KEYWORDS = {
    'python', 'javascript', 'react', 'nodejs', 'django', 'flask',
    'tensorflow', 'pytorch', 'docker', 'kubernetes', 'aws',
    'mongodb', 'postgresql', 'graphql', 'typescript', 'java',
    'c++', 'rust', 'go', 'vue', 'angular', 'svelte', 'fastapi'
}

def clean_markdown(text):
    text = re.sub(r"#+\s*", "", text)
    text = re.sub(r"\*+\s?", "", text)
    text = re.sub(r"\[.*?\]\(.*?\)", "", text)
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    return text.strip()

def is_direct_readme_url(url):
    patterns = [
        r"github\.com/.*/blob/.*/README\.md$",
        r"github\.com/.*/README\.md$",
        r"raw\.githubusercontent\.com/.*/.*/README\.md$"
    ]
    return any(re.search(pattern, url) for pattern in patterns)

def process_direct_readme(url):
    if "raw.githubusercontent.com" in url:
        return url
    url = url.replace("github.com", "raw.githubusercontent.com")
    return url.replace("/blob/", "/")

def analyze_readme(content):
    analysis = {}
    
    analysis['word_count'] = len(content.split())
    analysis['paragraph_count'] = len(content.split('\n\n'))
    
    
    blob = TextBlob(content)
    analysis['sentiment'] = blob.sentiment.polarity
    
    analysis['flesch_score'] = textstat.flesch_reading_ease(content)
    
    found_tech = []
    content_lower = content.lower()
    for tech in TECH_STACK_KEYWORDS:
        if re.search(rf'\b{tech}\b', content_lower):
            found_tech.append(tech.title())
    analysis['technologies'] = found_tech

    tech_density = len(found_tech) / (len(content.split())/100)
    analysis['complexity'] = min(10, round(tech_density * 2, 1))
    
    analysis['rating'] = round(
        (analysis['flesch_score'] * 0.3) + 
        (analysis['sentiment'] * 2 + 1) * 2.5 + 
        (len(found_tech) * 0.5) +
        (analysis['complexity'] * 0.4),
        1
    )
    
    return analysis

def update_analysis_display(analysis):
    dpg.set_value("tech_stack", ", ".join(analysis['technologies']) or "None detected")
    dpg.set_value("readability_score", f"{analysis['flesch_score']:.1f} (0-100)")
    dpg.set_value("complexity_score", f"{analysis['complexity']:.1f}/10")
    dpg.set_value("rating_value", f"{analysis['rating']:.1f}")  


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
        
        analysis = analyze_readme(cleaned_content)
        update_analysis_display(analysis)
        
    except Exception as e:
        dpg.set_value("output_text", f"Error: {str(e)}")
    finally:
        dpg.hide_item("loading_tag")
        dpg.enable_item("fetch_btn")


def create_gui():
    dpg.create_context()
    
    # Custom theme for larger fonts and white background
    with dpg.theme() as global_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (255, 255, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 0, 0), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Button, (240, 240, 240), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (220, 220, 220), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (200, 200, 200), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (245, 245, 245), category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 10, 5, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 10, 10, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 20, 20, category=dpg.mvThemeCat_Core)
    
    # Theme for headings
    with dpg.theme() as heading_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_Text, (30, 30, 180), category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 5, 10, category=dpg.mvThemeCat_Core)
    
    # Theme for important values
    with dpg.theme() as value_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_Text, (200, 30, 30), category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 5, 10, category=dpg.mvThemeCat_Core)
    
    dpg.bind_theme(global_theme)
    
    dpg.create_viewport(title='GitHub README Analyzer', width=1000, height=800)

    with dpg.window(label="Main Window", tag="main_window"):
        # Title
        with dpg.group(horizontal=True):
            dpg.add_spacer(width=20)
            dpg.add_text("GitHub README Analyzer", color=(30, 30, 180))
        
        # Input section
        dpg.add_spacer(height=10)
        with dpg.group(horizontal=True):
            dpg.add_spacer(width=20)
            dpg.add_text("Enter GitHub Repository URL:", color=(0, 0, 139))
        with dpg.group(horizontal=True):
            dpg.add_spacer(width=20)
            dpg.add_input_text(tag="input_url", width=600, height=40, hint="https://github.com/username/repo", 
                             default_value="", tracked=True)
            dpg.add_button(label="Analyze README", tag="fetch_btn", callback=fetch_readme, height=40)
            dpg.add_loading_indicator(tag="loading_tag", show=False)
        
        dpg.add_spacer(height=20)
        dpg.add_separator()
        dpg.add_spacer(height=10)
        
        # Results section
        with dpg.group(horizontal=True):
            dpg.add_spacer(width=20)
            dpg.add_text("Analysis Results", color=(0, 0, 139))
        
        dpg.add_spacer(height=15)
        
        with dpg.table(header_row=False, borders_innerH=True, borders_outerH=True, 
                      borders_innerV=True, borders_outerV=True, row_background=True):
            dpg.add_table_column(width_fixed=True)
            dpg.add_table_column(width_stretch=True)
            
            with dpg.table_row():
                dpg.add_text("Tech Stack:", color=(0, 0, 139))
                dpg.add_text(tag="tech_stack", default_value="Waiting for analysis...")
            
            with dpg.table_row():
                dpg.add_text("Readability Score:", color=(0, 0, 139))
                dpg.add_text(tag="readability_score", default_value="N/A")
            
            with dpg.table_row():
                dpg.add_text("Project Complexity:", color=(0, 0, 139))
                dpg.add_text(tag="complexity_score", default_value="N/A")
            
            with dpg.table_row():
                dpg.add_text("Overall Rating:", color=(0, 0, 139))
                dpg.add_text(tag="rating_value", default_value="N/A")
        
        dpg.add_spacer(height=20)
        
        # README content section
        with dpg.group(horizontal=True):
            dpg.add_spacer(width=20)
            dpg.add_text("README Content Preview:", color=(0, 0, 139))
        
        dpg.add_spacer(height=10)
        
        with dpg.child_window(width=950, height=400, border=True):
            dpg.add_input_text(tag="output_text", multiline=True, width=930, height=380, 
                             readonly=True, default_value="Content will appear here...", tracked=True)
    
    # Apply themes to specific elements
    dpg.bind_item_theme("main_window", global_theme)
    dpg.bind_item_theme("fetch_btn", value_theme)
    
    # Set font
    with dpg.font_registry():
        default_font = dpg.add_font("C:\\Windows\\Fonts\\segoeui.ttf", 18)  # Adjust path as needed
    
    dpg.bind_font(default_font)
    
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("main_window", True)
    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == "__main__":
    create_gui()
