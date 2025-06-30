# Week 11 Reflection

## Student Information
- **Name:** 
- **GitHub Username:** 
- **Preferred Feature Track:** Data / Visual / Interactive 
- **Team Interest:** Yes: Contributor

## Section 1: Week 11 Reflection
Answer each prompt with 3–5 bullet points:

### Key Takeaways
What did you learn about capstone goals and expectations?
- We kind of have weekly check points we work toward
- Groups will only be a small part of the project
- We have more freedom in this than originally thought
- 
- 

### Concept Connections
Which Week 1–10 skills feel strongest? Which need more practice?
- python
- tkinter
- sql
- pandas
- 

### Early Challenges
Any blockers (e.g., API keys, folder setup)?
- the api key originally, but we just had to wait on them to be active
- not having clear set up instructions on one of the projects, i dont remember which it was, but it took me 2 hours just to get started
- 
- 
- 

### Support Strategies
Which office hours or resources can help you move forward?
- Assigned capstone group
- my original small group 
- docs files and stack dump
- 
- 

## Section 2: Feature Selection Rationale
List three features + one enhancement you plan to build.

| # | Feature Name | Difficulty (1–3) | Why You Chose It / Learning Goal |
|---|--------------|------------------|----------------------------------|
| 1 |City Comparison |  1             |     I enjoy data visualzation                             |
| 2 |Theme Switcher|  2           | I like to use conditionals to make things happen, and this is a good way to do that|
| 3 |Tomorrow's Guess|3               |Push my limits, and tie my older skills in with the newer ones|
| Enhancement | let user choose color theme maybe  |                  | user personalization is good UX |

**Tip:** Pick at least one "level 3" feature to stretch your skills!

## Section 3: High-Level Architecture Sketch
Add a diagram or a brief outline that shows:
- Core modules and folders
- Feature modules
- Data flow between components

```

WEATHER-PROJECT/
├── data/                       
│   ├── data.py                 
│   ├── open_weather_*.txt      
│   └── weather_history.txt     
│
├── docs/                    
│   ├── LICENSE
│   └── Week11_Reflection.md
│
├── features/                
│   ├── __init__.py
│
├── gui/                      
│   ├── __init__.py
│   ├── gui_main.py             
│   └── gui_main2.py           
│
├── screenshots/                
│
├── tests/                   
│   ├── __init__.py
│   └── features_test.py       
│
├── .env                       
├── .gitignore
├── weather.csv              
├── config.py                 
├── main.py                    
├── README.md
└── requirements.txt            # dependencies

[Add your architecture diagram or outline here]
```

## Section 4: Data Model Plan
Fill in your planned data files or tables:

| File/Table Name | Format (txt, json, csv, other) | Example Row |
|-----------------|--------------------------------|-------------|
| `weather_history.txt` | txt | 2025-06-09,New Brunswick,78,Sunny |
|                 |                                |             |
|                 |           Im not sure yet                     |             |
|                 |                                |             |

## Section 5: Personal Project Timeline (Weeks 12–17)
Customize based on your availability:

| Week | Monday | Tuesday | Wednesday | Thursday | Key Milestone |
|------|--------|---------|-----------|----------|---------------|
| 12 | API setup | Error handling | Tkinter shell | Buffer day | Basic working app |
| 13 | Feature 1 | Integrate basics | test | fine tune | Feature 1 complete|
| 14 | Feature 2 start |  Integrate basics | test | fine tune |  Feature 2 complete |
| 15 | Feature 3 |  Integrate basics | test | fine tune |  All features complete |
| 16 | Enhancement | Docs | Tests | Packaging | Ready-to-ship app |
| 17 | Rehearse | Buffer | Showcase | | Demo Day |

## Section 6: Risk Assessment
Identify at least 3 potential risks and how you'll handle them.

| Risk | Likelihood (High/Med/Low) | Impact (High/Med/Low) | Mitigation Plan |
|------|---------------------------|----------------------|-----------------|
| API Rate Limit | Medium | Medium | Add delays or cache recent results |
|gettting stuck on the small things |   med   | low-high | focus mvp           |
| visualization / effects     |  med                         |         low             |       if it starts taking too long move on          |
| building the right sub query |   med                        |     med |take step by step, ask around           |

## Section 7: Support Requests
What specific help will you ask for in office hours or on Slack/Discord?

- I will probably watch some tutorials on different things on youtube before I even have any idea on specifics to ask. 
- I usually dont know what im going to ask until I get stuck for a long time on something
- 
- 

## Section 8: Before Monday (Start of Week 12)
Complete these setup steps before Monday:

- [ ] Push `main.py`, `config.py`, and a `/data/` folder to your repo
- [ ] Add OpenWeatherMap key to `.env` (⚠️ Do *not* commit the key)
- [ ] Copy chosen feature templates into `/features/`
- [ ] Commit and push a first-draft `README.md`
- [ ] Book office hours if you're still stuck on API setup

## Final Submission Checklist (Due Friday 23:59)
- [ ] `Week11_Reflection.md` completed
- [ ] File uploaded to GitHub repo `/docs/`
- [ ] Repo link submitted on Canvas