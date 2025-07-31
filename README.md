# 🚀 RankForge – Precision Hiring Made Simple

**RankForge** is a precision hiring analytics platform that helps recruiters **evaluate and compare candidate profiles across GitHub, Codeforces, and CodeChef**. It aggregates coding and project data using public APIs, and applies intelligent scoring metrics to reduce hiring decision time. Designed for **scalable tech hiring**, RankForge transforms scattered developer profiles into a unified, sortable view.

🎥 **Demo Video**: [Watch Here](https://drive.google.com/file/d/1m3umuj3UcmEczY04kx3C3XLfps2BzS0f/view?usp=drive_link)

---

## 📌 Key Features

- 🔗 **Multi-Platform Aggregation**  
  Collects candidate data from GitHub, Codeforces, and CodeChef via APIs.

- 📊 **Custom Scoring Metrics**  
  Introduces three unique evaluation metrics:  
  - **ROC** (*Ratio of Code*) – evaluates consistency in coding practices.  
  - **GPR** (*GitHub Project Rating*) – scores GitHub repos based on project structure.  
  - **GDR** (*GitHub README Depth Rating*) – uses **NLP (NLTK)** to assess README quality.

- ⏱️ **Time-Saving Recruiter Dashboard**  
  Sort and shortlist candidates based on real-time scores and platform performance.

- 🧠 **Intelligent README Analysis**  
  Uses **Natural Language Toolkit (NLTK)** to compute depth ratings for over 100+ GitHub README files.

---

## 🛠 Tech Stack

- **Frontend**: React.js  
- **Backend**: Python Flask  
- **APIs**: GitHub API, Codeforces API, CodeChef scraping  
- **Data Processing**: Python, NLTK  
- **UI**: TailwindCSS (assumed)  
- **Version Control**: Git & GitHub

---

## 📦 How It Works

1. Candidate enters their GitHub, Codeforces, and CodeChef usernames.
2. RankForge fetches profile data from each platform.
3. GitHub repositories and READMEs are parsed and scored.
4. ROC, GPR, and GDR scores are calculated and visualized.
5. Recruiter dashboard allows sorting candidates based on custom metrics.

---

## 💼 Use Cases

- **Recruiters** can instantly evaluate developers’ real coding activity without manually visiting profiles.
- **Students/Developers** can audit their own performance across platforms and improve specific areas.
- **EdTech Platforms** can integrate RankForge into their evaluation tools for deeper analytics.

---

## 📽 Demo Preview

> 🎥 [Click to Watch the Video Demo](https://drive.google.com/file/d/1m3umuj3UcmEczY04kx3C3XLfps2BzS0f/view?usp=drive_link)  
> Showcasing profile fetching, metric computation, and dashboard UI in action.

---

## 🤝 Contributing

Have ideas to improve RankForge? PRs and feedback are always welcome!  
You can fork the repo and submit changes via pull requests.

---

## 📄 License

This project is under the **MIT License** — feel free to use, modify, and build on it!

---

## 🙌 Acknowledgements

- GitHub, Codeforces, and CodeChef for providing open access APIs
- NLTK community for open-source NLP tools
- [Harikrishna Gupta](https://github.com/GuptaHarry) — Creator & Maintainer

