



# import requests
# import tkinter as tk
# from tkinter import messagebox, ttk
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# # Backend functions to fetch user data
# def fetch_codeforces_data(handle):
#     url = f"https://codeforces.com/api/user.info?handles={handle}"
#     contest_url = f"https://codeforces.com/api/user.rating?handle={handle}"
    
#     try:
#         # Get user info
#         response = requests.get(url)
#         response.raise_for_status()
#         data = response.json()
        
#         if data.get("status") != "OK":
#             return None
            
#         user = data["result"][0]
        
#         # Get contest participation
#         contests_response = requests.get(contest_url)
#         contests_response.raise_for_status()
#         contests_data = contests_response.json()
        
#         contest_count = 0
#         if contests_data.get("status") == "OK":
#             contest_count = len(contests_data.get("result", []))
            
#         return {
#             "Platform": "Codeforces",
#             "Handle": user["handle"],
#             "Rating": user.get("rating", 0),
#             "Max Rating": user.get("maxRating", 0),
#             "Rank": user.get("rank", "Unrated"),
#             "Max Rank": user.get("maxRank", "Unrated"),
#             "Contest Count": contest_count,
#             "Contribution": user.get("contribution", 0)
#         }
#     except requests.RequestException as e:
#         print("Error Fetching Codeforces Data:", e)
#         return None

# def fetch_codechef_data(handle):
#     url = f"https://codechef-api.vercel.app/handle/{handle}"
#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#         data = response.json()
        
#         # Extract necessary fields while handling null values
#         name = data.get("name", "N/A")
#         rating = data.get("currentRating") if data.get("currentRating") is not None else 0
#         stars = data.get("stars", "0")
#         global_rank = data.get("globalRank") if data.get("globalRank") is not None else 0
#         country_rank = data.get("countryRank") if data.get("countryRank") is not None else 0
#         contest_participated = len(data.get("contestParticipation", [])) if data.get("contestParticipation") else 0
        
#         return {
#             "Platform": "CodeChef",
#             "Handle": handle,
#             "Name": name,
#             "Rating": rating,
#             "Stars": stars,
#             "Global Rank": global_rank,
#             "Country Rank": country_rank,
#             "Contest Count": contest_participated
#         }
#     except requests.RequestException as e:
#         print("Error Fetching CodeChef Data:", e)
#         return None

# # Evaluation system
# def evaluate_candidate(cf_data, cc_data):
#     # Default weights (can be adjusted)
#     weights = {
#         "cf_rating": 0.25,
#         "cf_max_rating": 0.15,
#         "cf_contests": 0.10,
#         "cf_contribution": 0.05,
#         "cc_rating": 0.25,
#         "cc_stars": 0.10,
#         "cc_contests": 0.10
#     }
    
#     score = 0
#     score_breakdown = {}
#     max_possible_score = 100
    
#     # Evaluate Codeforces data
#     if cf_data:
#         # Rating normalization (assuming max possible is 3500)
#         cf_rating_score = min(cf_data.get("Rating", 0) / 3500 * 100, 100) * weights["cf_rating"]
#         cf_max_rating_score = min(cf_data.get("Max Rating", 0) / 3500 * 100, 100) * weights["cf_max_rating"]
        
#         # Contest participation (normalize to max of 100 contests)
#         cf_contests_score = min(cf_data.get("Contest Count", 0) / 100 * 100, 100) * weights["cf_contests"]
        
#         # Contribution score (normalize between -100 to 100+)
#         contribution = cf_data.get("Contribution", 0)
#         cf_contribution_score = (max(min(contribution, 100), -100) + 100) / 200 * 100 * weights["cf_contribution"]
        
#         score += cf_rating_score + cf_max_rating_score + cf_contests_score + cf_contribution_score
        
#         score_breakdown["Codeforces Rating"] = cf_rating_score
#         score_breakdown["Codeforces Max Rating"] = cf_max_rating_score
#         score_breakdown["Codeforces Contests"] = cf_contests_score
#         score_breakdown["Codeforces Contribution"] = cf_contribution_score
    
#     # Evaluate CodeChef data
#     if cc_data:
#         # Rating normalization (assuming max possible is 3000)
#         cc_rating_score = min(cc_data.get("Rating", 0) / 3000 * 100, 100) * weights["cc_rating"]
        
#         # Stars evaluation (0-7 stars)
#         stars = 0
#         try:
#             stars = int(cc_data.get("Stars", "0").replace("★", ""))
#         except:
#             stars = len(cc_data.get("Stars", "").replace("★", ""))
        
#         cc_stars_score = min(stars / 7 * 100, 100) * weights["cc_stars"]
        
#         # Contest participation (normalize to max of 100 contests)
#         cc_contests_score = min(cc_data.get("Contest Count", 0) / 100 * 100, 100) * weights["cc_contests"]
        
#         score += cc_rating_score + cc_stars_score + cc_contests_score
        
#         score_breakdown["CodeChef Rating"] = cc_rating_score
#         score_breakdown["CodeChef Stars"] = cc_stars_score
#         score_breakdown["CodeChef Contests"] = cc_contests_score
    
#     # Get expertise level based on score
#     expertise_level = get_expertise_level(score)
    
#     return {
#         "Total Score": round(score, 2),
#         "Max Possible": max_possible_score,
#         "Expertise Level": expertise_level,
#         "Score Breakdown": score_breakdown
#     }



# def get_expertise_level(score):
#     if score >= 90:
#         return "Expert"
#     elif score >= 75:
#         return "Advanced"
#     elif score >= 60:
#         return "Intermediate"
#     elif score >= 40:
#         return "Regular"
#     elif score >= 20:
#         return "Beginner"
#     else:
#         return "Novice"

# # Function to fetch and display user data with evaluation
# def fetch_data():
#     cf_handle = cf_entry.get().strip()
#     cc_handle = cc_entry.get().strip()
   
#     if not cf_handle and not cc_handle:
#         messagebox.showerror("Input Error", "Please enter at least one handle.")
#         return
    
#     result_text.delete("1.0", tk.END)
    
#     cf_data = None
#     cc_data = None
   
#     if cf_handle:
#         cf_data = fetch_codeforces_data(cf_handle)
#         if cf_data:
#             result_text.insert(tk.END, f"Codeforces Profile:\nHandle: {cf_data['Handle']}\nRating: {cf_data['Rating']}\nMax Rating: {cf_data['Max Rating']}\nRank: {cf_data['Rank']}\nMax Rank: {cf_data['Max Rank']}\nContests: {cf_data['Contest Count']}\nContribution: {cf_data['Contribution']}\n\n")
#         else:
#             result_text.insert(tk.END, "Invalid Codeforces handle or data unavailable.\n\n")
    
#     if cc_handle:
#         cc_data = fetch_codechef_data(cc_handle)
#         if cc_data:
#             result_text.insert(tk.END, f"CodeChef Profile:\nHandle: {cc_data['Handle']}\nName: {cc_data['Name']}\nRating: {cc_data['Rating']}\nStars: {cc_data['Stars']}\nGlobal Rank: {cc_data['Global Rank']}\nContests: {cc_data['Contest Count']}\n\n")
#         else:
#             result_text.insert(tk.END, "Invalid CodeChef handle or data unavailable.\n\n")
    
#     # Evaluate candidate
#     if cf_data or cc_data:
#         evaluation = evaluate_candidate(cf_data, cc_data)
        
#         result_text.insert(tk.END, f"\n===== UNIFIED EVALUATION =====\n")
#         result_text.insert(tk.END, f"Total Score: {evaluation['Total Score']} / {evaluation['Max Possible']}\n")
#         result_text.insert(tk.END, f"Expertise Level: {evaluation['Expertise Level']}\n\n")
        
#         result_text.insert(tk.END, "Score Breakdown:\n")
#         for category, score in evaluation['Score Breakdown'].items():
#             result_text.insert(tk.END, f"- {category}: {round(score, 2)}\n")
        
#         # Update the progress bar
#         progress_value = evaluation['Total Score'] / evaluation['Max Possible'] * 100
#         progress_bar["value"] = progress_value
#         expertise_label.config(text=f"Expertise Level: {evaluation['Expertise Level']}")
        
#         # Update the chart
#         update_chart(evaluation['Score Breakdown'])

# # Function to update the visualization chart
# def update_chart(score_breakdown):
#     ax.clear()
    
#     categories = list(score_breakdown.keys())
#     values = list(score_breakdown.values())
    
#     # Create color mapping
#     colors = []
#     for category in categories:
#         if "Codeforces" in category:
#             colors.append('#318CE7')  # Blue for Codeforces
#         else:
#             colors.append('#8A2BE2')  # Purple for CodeChef
    
#     ax.bar(categories, values, color=colors)
#     ax.set_ylabel('Score')
#     ax.set_title('Candidate Evaluation Breakdown')
    
#     # Rotate x-axis labels for better display
#     plt.xticks(rotation=45, ha='right')
    
#     # Adjust layout
#     fig.tight_layout()
    
#     # Update canvas
#     chart_canvas.draw()

# # UI setup using Tkinter
# root = tk.Tk()
# root.title("Coding Profile Evaluator")
# root.geometry("800x800")

# # Create notebook (tabs)
# notebook = ttk.Notebook(root)
# notebook.pack(fill='both', expand=True, padx=10, pady=10)

# # Create frames for tabs
# input_frame = ttk.Frame(notebook)
# viz_frame = ttk.Frame(notebook)

# notebook.add(input_frame, text="Input & Results")
# notebook.add(viz_frame, text="Visualization")


# # Input frame elements
# tk.Label(input_frame, text="Coding Profile Evaluator", font=("Arial", 16, "bold")).pack(pady=10)
# tk.Label(input_frame, text="Enter handles to evaluate candidate performance", font=("Arial", 12)).pack(pady=5)


# input_section = ttk.Frame(input_frame)
# input_section.pack(fill='x', pady=10)

# tk.Label(input_section, text="Codeforces Handle:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5, sticky='w')
# cf_entry = tk.Entry(input_section, width=30, font=("Arial", 12))
# cf_entry.grid(row=0, column=1, padx=5, pady=5)

# tk.Label(input_section, text="CodeChef Handle:", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5, sticky='w')
# cc_entry = tk.Entry(input_section, width=30, font=("Arial", 12))
# cc_entry.grid(row=1, column=1, padx=5, pady=5)

# # Fetch button
# fetch_button = tk.Button(input_frame, text="Evaluate Candidate", command=fetch_data, 
#                       font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", 
#                       padx=10, pady=5)
# fetch_button.pack(pady=10)


# # Progress section
# progress_frame = ttk.Frame(input_frame)
# progress_frame.pack(fill='x', pady=10)

# tk.Label(progress_frame, text="Overall Performance:", font=("Arial", 12, "bold")).pack(anchor='w')
# progress_bar = ttk.Progressbar(progress_frame, orient="horizontal", length=700, mode="determinate")
# progress_bar.pack(fill='x', padx=20, pady=5)
# expertise_label = tk.Label(progress_frame, text="Expertise Level: Not Evaluated", font=("Arial", 12))
# expertise_label.pack(anchor='w', padx=20)

# # Results section
# result_frame = ttk.Frame(input_frame)
# result_frame.pack(fill='both', expand=True, pady=10)

# tk.Label(result_frame, text="Evaluation Results:", font=("Arial", 12, "bold")).pack(anchor='w')
# result_text = tk.Text(result_frame, height=20, width=80, wrap="word", font=("Arial", 11))
# result_text.pack(fill='both', expand=True, padx=5)




# # Visualization frame
# # Create figure for matplotlib
# fig, ax = plt.subplots(figsize=(8, 6))
# chart_canvas = FigureCanvasTkAgg(fig, master=viz_frame)
# chart_canvas.get_tk_widget().pack(fill='both', expand=True)

# # Information section
# info_frame = ttk.Frame(viz_frame)
# info_frame.pack(fill='x', pady=10)


# info_text = """
# Evaluation Metrics:

# - Codeforces Rating (25%): Current rating normalized to a max of 3500
# - Codeforces Max Rating (15%): Highest achieved rating normalized to 3500
# - Codeforces Contests (10%): Number of contests participated (max score at 100 contests)
# - Codeforces Contribution (5%): Community contribution normalized between -100 and 100

# - CodeChef Rating (25%): Current rating normalized to a max of 3000
# - CodeChef Stars (10%): Star rating normalized to a 7-star scale
# - CodeChef Contests (10%): Number of contests participated (max score at 100 contests)

# Expertise Levels:
# - Expert (90-100): Elite competitive programmer
# - Advanced (75-89): Highly skilled programmer
# - Intermediate (60-74): Competent competitive coder
# - Regular (40-59): Active participant with decent skills
# - Beginner (20-39): Starting to build competitive skills
# - Novice (0-19): New to competitive programming
# """

# info_label = tk.Label(info_frame, text=info_text, font=("Arial", 10), justify='left')
# info_label.pack(anchor='w', padx=20)

# root.mainloop()





































import requests
import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Backend functions to fetch user data
def fetch_codeforces_data(handle):
    url = f"https://codeforces.com/api/user.info?handles={handle}"
    contest_url = f"https://codeforces.com/api/user.rating?handle={handle}"
    
    try:
        # Get user info
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if data.get("status") != "OK":
            return None
            
        user = data["result"][0]
        
        # Get contest participation
        contests_response = requests.get(contest_url)
        contests_response.raise_for_status()
        contests_data = contests_response.json()
        
        contest_count = 0
        if contests_data.get("status") == "OK":
            contest_count = len(contests_data.get("result", []))
            
        return {
            "Platform": "Codeforces",
            "Handle": user["handle"],
            "Rating": user.get("rating", 0),
            "Max Rating": user.get("maxRating", 0),
            "Rank": user.get("rank", "Unrated"),
            "Max Rank": user.get("maxRank", "Unrated"),
            "Contest Count": contest_count,
            "Contribution": user.get("contribution", 0)
        }
    except requests.RequestException as e:
        print("Error Fetching Codeforces Data:", e)
        return None

def fetch_codechef_data(handle):
    url = f"https://codechef-api.vercel.app/handle/{handle}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # Extract necessary fields while handling null values
        name = data.get("name", "N/A")
        rating = data.get("currentRating") if data.get("currentRating") is not None else 0
        stars = data.get("stars", "0")
        global_rank = data.get("globalRank") if data.get("globalRank") is not None else 0
        country_rank = data.get("countryRank") if data.get("countryRank") is not None else 0
        contest_participated = len(data.get("contestParticipation", [])) if data.get("contestParticipation") else 0
        
        return {
            "Platform": "CodeChef",
            "Handle": handle,
            "Name": name,
            "Rating": rating,
            "Stars": stars,
            "Global Rank": global_rank,
            "Country Rank": country_rank,
            "Contest Count": contest_participated
        }
    except requests.RequestException as e:
        print("Error Fetching CodeChef Data:", e)
        return None


# Evaluation system
def evaluate_candidate(cf_data, cc_data):
    # Default weights (can be adjusted)
    weights = {
        "cf_rating": 0.25,
        "cf_max_rating": 0.15,
        "cf_contests": 0.10,
        "cf_contribution": 0.05,
        "cc_rating": 0.25,
        "cc_stars": 0.10,
        "cc_contests": 0.10
    }
    
    score = 0
    score_breakdown = {}
    max_possible_score = 100
    
    # Evaluate Codeforces data
    if cf_data:
        # Rating normalization (assuming max possible is 3500)
        cf_rating_score = min(cf_data.get("Rating", 0) / 3500 * 100, 100) * weights["cf_rating"]
        cf_max_rating_score = min(cf_data.get("Max Rating", 0) / 3500 * 100, 100) * weights["cf_max_rating"]
        
        # Contest participation (normalize to max of 100 contests)
        cf_contests_score = min(cf_data.get("Contest Count", 0) / 100 * 100, 100) * weights["cf_contests"]
        
        # Contribution score (normalize between -100 to 100+)
        contribution = cf_data.get("Contribution", 0)
        cf_contribution_score = (max(min(contribution, 100), -100) + 100) / 200 * 100 * weights["cf_contribution"]
        
        score += cf_rating_score + cf_max_rating_score + cf_contests_score + cf_contribution_score
        
        score_breakdown["Codeforces Rating"] = cf_rating_score
        score_breakdown["Codeforces Max Rating"] = cf_max_rating_score
        score_breakdown["Codeforces Contests"] = cf_contests_score
        score_breakdown["Codeforces Contribution"] = cf_contribution_score
    
    # Evaluate CodeChef data
    if cc_data:
        # Rating normalization (assuming max possible is 3000)
        cc_rating_score = min(cc_data.get("Rating", 0) / 3000 * 100, 100) * weights["cc_rating"]
        
        # Stars evaluation (0-7 stars)
        stars = 0
        try:
            stars = int(cc_data.get("Stars", "0").replace("★", ""))
        except:
            stars = len(cc_data.get("Stars", "").replace("★", ""))
        
        cc_stars_score = min(stars / 7 * 100, 100) * weights["cc_stars"]
        
        # Contest participation (normalize to max of 100 contests)
        cc_contests_score = min(cc_data.get("Contest Count", 0) / 100 * 100, 100) * weights["cc_contests"]
        
        score += cc_rating_score + cc_stars_score + cc_contests_score
        
        score_breakdown["CodeChef Rating"] = cc_rating_score
        score_breakdown["CodeChef Stars"] = cc_stars_score
        score_breakdown["CodeChef Contests"] = cc_contests_score
    
    # Get expertise level based on score
    expertise_level = get_expertise_level(score)
    
    return {
        "Total Score": round(score, 2),
        "Max Possible": max_possible_score,
        "Expertise Level": expertise_level,
        "Score Breakdown": score_breakdown
    }

def get_expertise_level(score):
    if score >= 90:
        return "Expert"
    elif score >= 75:
        return "Advanced"
    elif score >= 60:
        return "Intermediate"
    elif score >= 40:
        return "Regular"
    elif score >= 20:
        return "Beginner"
    else:
        return "Novice"

# Function to fetch and display user data with evaluation
def fetch_data():
    cf_handle = cf_entry.get().strip()
    cc_handle = cc_entry.get().strip()
   
    if not cf_handle and not cc_handle:
        messagebox.showerror("Input Error", "Please enter at least one handle.")
        return
    
    result_text.delete("1.0", tk.END)
    
    cf_data = None
    cc_data = None
   
    if cf_handle:
        cf_data = fetch_codeforces_data(cf_handle)
        if cf_data:
            result_text.insert(tk.END, f"Codeforces Profile:\nHandle: {cf_data['Handle']}\nRating: {cf_data['Rating']}\nMax Rating: {cf_data['Max Rating']}\nRank: {cf_data['Rank']}\nMax Rank: {cf_data['Max Rank']}\nContests: {cf_data['Contest Count']}\nContribution: {cf_data['Contribution']}\n\n")
        else:
            result_text.insert(tk.END, "Invalid Codeforces handle or data unavailable.\n\n")
    
    if cc_handle:
        cc_data = fetch_codechef_data(cc_handle)
        if cc_data:
            result_text.insert(tk.END, f"CodeChef Profile:\nHandle: {cc_data['Handle']}\nName: {cc_data['Name']}\nRating: {cc_data['Rating']}\nStars: {cc_data['Stars']}\nGlobal Rank: {cc_data['Global Rank']}\nContests: {cc_data['Contest Count']}\n\n")
        else:
            result_text.insert(tk.END, "Invalid CodeChef handle or data unavailable.\n\n")
    
    # Evaluate candidate
    if cf_data or cc_data:
        evaluation = evaluate_candidate(cf_data, cc_data)
        
        result_text.insert(tk.END, f"\n===== UNIFIED EVALUATION =====\n")
        result_text.insert(tk.END, f"Total Score: {evaluation['Total Score']} / {evaluation['Max Possible']}\n")
        result_text.insert(tk.END, f"Expertise Level: {evaluation['Expertise Level']}\n\n")
        
        result_text.insert(tk.END, "Score Breakdown:\n")
        for category, score in evaluation['Score Breakdown'].items():
            result_text.insert(tk.END, f"- {category}: {round(score, 2)}\n")
        
        # Update the progress bar
        progress_value = evaluation['Total Score'] / evaluation['Max Possible'] * 100
        progress_bar["value"] = progress_value
        expertise_label.config(text=f"Expertise Level: {evaluation['Expertise Level']}")
        
        # Update the chart
        update_chart(evaluation['Score Breakdown'])

# Function to update the visualization chart
def update_chart(score_breakdown):
    ax.clear()
    
    categories = list(score_breakdown.keys())
    values = list(score_breakdown.values())
    
    # Create color mapping
    colors = []
    for category in categories:
        if "Codeforces" in category:
            colors.append('#318CE7')  # Blue for Codeforces
        else:
            colors.append('#8A2BE2')  # Purple for CodeChef
    
    ax.bar(categories, values, color=colors)
    ax.set_ylabel('Score')
    ax.set_title('Candidate Evaluation Breakdown')
    
    # Rotate x-axis labels for better display
    plt.xticks(rotation=45, ha='right')
    
    # Adjust layout
    fig.tight_layout()
    
    # Update canvas
    chart_canvas.draw()

# UI setup using Tkinter
root = tk.Tk()
root.title("RankForge: ROC Rating Calculator")
root.geometry("900x800")
root.configure(bg='#f0f2f5')

# Set theme colors
PRIMARY_COLOR = '#2c3e50'
SECONDARY_COLOR = '#3498db'
ACCENT_COLOR = '#e74c3c'
LIGHT_BG = '#ecf0f1'
DARK_TEXT = '#2c3e50'

# Style configuration
style = ttk.Style()
style.theme_use('clam')

# Configure styles
style.configure('TFrame', background=LIGHT_BG)
style.configure('TLabel', background=LIGHT_BG, foreground=DARK_TEXT, font=('Arial', 10))
style.configure('TNotebook', background=LIGHT_BG)
style.configure('TNotebook.Tab', background=PRIMARY_COLOR, foreground='white', padding=[10, 5], font=('Arial', 10, 'bold'))
style.map('TNotebook.Tab', background=[('selected', SECONDARY_COLOR)], foreground=[('selected', 'white')])
style.configure('TButton', font=('Arial', 10, 'bold'), padding=6, background=SECONDARY_COLOR, foreground='white')
style.map('TButton', background=[('active', '#2980b9')])
style.configure('TEntry', font=('Arial', 11), padding=5)
style.configure('Horizontal.TProgressbar', troughcolor=LIGHT_BG, background=SECONDARY_COLOR, thickness=20)

# Header frame
header_frame = ttk.Frame(root, style='TFrame')
header_frame.pack(fill='x', padx=10, pady=10)

# App title with logo
logo_label = tk.Label(header_frame, text="⚔️", font=('Arial', 24), bg=LIGHT_BG)
logo_label.pack(side='left', padx=5)
title_label = tk.Label(header_frame, text="RankForge: ROC Rating Calculator", font=('Arial', 20, 'bold'), 
                      bg=LIGHT_BG, fg=PRIMARY_COLOR)
title_label.pack(side='left', pady=10)

# Create notebook (tabs)
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True, padx=10, pady=(0, 10))

# Create frames for tabs
input_frame = ttk.Frame(notebook, style='TFrame')
viz_frame = ttk.Frame(notebook, style='TFrame')

notebook.add(input_frame, text="Input & Results")
notebook.add(viz_frame, text="Visualization")

# Input frame elements
input_container = ttk.Frame(input_frame, style='TFrame')
input_container.pack(fill='both', expand=True, padx=15, pady=15)

# Input section
input_section = ttk.LabelFrame(input_container, text="Enter Profile Handles", style='TFrame')
input_section.pack(fill='x', pady=(0, 15))

# Codeforces input
cf_frame = ttk.Frame(input_section, style='TFrame')
cf_frame.pack(fill='x', pady=5)
tk.Label(cf_frame, text="Codeforces Handle:", font=("Arial", 11, 'bold')).pack(side='left', padx=5)
cf_entry = ttk.Entry(cf_frame, width=30, font=("Arial", 11))
cf_entry.pack(side='left', fill='x', expand=True, padx=5)

# CodeChef input
cc_frame = ttk.Frame(input_section, style='TFrame')
cc_frame.pack(fill='x', pady=5)
tk.Label(cc_frame, text="CodeChef Handle:", font=("Arial", 11, 'bold')).pack(side='left', padx=5)
cc_entry = ttk.Entry(cc_frame, width=30, font=("Arial", 11))
cc_entry.pack(side='left', fill='x', expand=True, padx=5)

# Fetch button with icon
fetch_button = ttk.Button(input_section, text="Evaluate Candidate", command=fetch_data, 
                        style='TButton')
fetch_button.pack(pady=10, ipadx=10, ipady=5)

# Progress section
progress_section = ttk.LabelFrame(input_container, text="Performance Evaluation", style='TFrame')
progress_section.pack(fill='x', pady=(10, 15))

progress_bar = ttk.Progressbar(progress_section, orient="horizontal", length=700, mode="determinate", 
                             style='Horizontal.TProgressbar')
progress_bar.pack(fill='x', padx=10, pady=5)

expertise_label = tk.Label(progress_section, text="Expertise Level: Not Evaluated", 
                          font=("Arial", 12, 'bold'), bg=LIGHT_BG, fg=PRIMARY_COLOR)
expertise_label.pack(pady=5)

# Results section
results_section = ttk.LabelFrame(input_container, text="Evaluation Results", style='TFrame')
results_section.pack(fill='both', expand=True)

# Scrollable text area
text_scroll = ttk.Scrollbar(results_section)
text_scroll.pack(side='right', fill='y')

result_text = tk.Text(results_section, height=15, wrap="word", font=("Arial", 11), 
                     yscrollcommand=text_scroll.set, padx=10, pady=10,
                     bg='white', fg=DARK_TEXT, selectbackground=SECONDARY_COLOR)
result_text.pack(fill='both', expand=True)

text_scroll.config(command=result_text.yview)

# Visualization frame
viz_container = ttk.Frame(viz_frame, style='TFrame')
viz_container.pack(fill='both', expand=True, padx=15, pady=15)

# Create figure for matplotlib with custom style
plt.style.use('ggplot')  # Using ggplot style instead of seaborn
fig, ax = plt.subplots(figsize=(8, 5), facecolor=LIGHT_BG)
fig.patch.set_facecolor(LIGHT_BG)
ax.set_facecolor(LIGHT_BG)

# Customize plot colors
ax.spines['bottom'].set_color(PRIMARY_COLOR)
ax.spines['top'].set_color(PRIMARY_COLOR) 
ax.spines['right'].set_color(PRIMARY_COLOR)
ax.spines['left'].set_color(PRIMARY_COLOR)
ax.tick_params(axis='x', colors=PRIMARY_COLOR)
ax.tick_params(axis='y', colors=PRIMARY_COLOR)
ax.yaxis.label.set_color(PRIMARY_COLOR)
ax.xaxis.label.set_color(PRIMARY_COLOR)
ax.title.set_color(PRIMARY_COLOR)

chart_canvas = FigureCanvasTkAgg(fig, master=viz_container)
chart_canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)

# Information section
info_frame = ttk.LabelFrame(viz_container, text="Evaluation Metrics", style='TFrame')
info_frame.pack(fill='x', pady=(10, 0))

info_text = """Evaluation Metrics:
- Codeforces Rating (25%): Current rating normalized to max of 3500
- Codeforces Max Rating (15%): Highest achieved rating
- Codeforces Contests (10%): Number of contests participated
- Codeforces Contribution (5%): Community contribution score

- CodeChef Rating (25%): Current rating normalized to max of 3000
- CodeChef Stars (10%): Star rating (0-7 scale)
- CodeChef Contests (10%): Number of contests participated

Expertise Levels:
- Expert (90-100): Elite competitive programmer
- Advanced (75-89): Highly skilled programmer
- Intermediate (60-74): Competent coder
- Regular (40-59): Active participant
- Beginner (20-39): Building skills
- Novice (0-19): New to competitive programming
"""



info_label = tk.Label(info_frame, text=info_text, font=("Consolas", 10), 
                     justify='left', bg=LIGHT_BG, fg=DARK_TEXT)
info_label.pack(anchor='w', padx=10, pady=10)




# Footer
footer_frame = ttk.Frame(root, style='TFrame')
footer_frame.pack(fill='x', pady=(0, 10))
tk.Label(footer_frame, text="RankForge v1.0 · Competitive Programming Profile Evaluator", 
        font=("Arial", 9), bg=LIGHT_BG, fg=PRIMARY_COLOR).pack()

root.mainloop()








