# ✈️ SafarAI

 **AI-powered travel planner** that generates complete itineraries including flights, stays, and activities — in seconds.
 <p align="center" justify="center">
<img alt="image" height="500px" src="https://github.com/user-attachments/assets/2a7039e4-37af-439b-8a11-783056c10297" width="48%"/>
<img  alt="image" src="https://github.com/user-attachments/assets/976aee23-fbcd-4250-a34e-af3feb9ac2e5" width="48%"/>


</p>




## 🌍 Overview

**SafarAI** is an intelligent travel planning assistant that helps you:

* ✈️ Find flight options
* 🏨 Discover stays
* 🗺️ Plan activities
* 📄 Export a polished itinerary (PDF)

Built with a **multi-agent architecture**, SafarAI combines specialized services to create a seamless travel planning experience.



## 🚀 Features

* 🤖 AI-generated travel itineraries
* 🧠 Multi-agent backend (Flights, Stays, Activities)
* 📄 A2A used to enable seamless, secure communication and collaboration between AI agents




## 🛠️ Setup & Run

### Clone the repository

```bash
git clone <your-repo-url>
cd safarai
```

---

### Set environment variables

```bash
export GOOGLE_GENAI_USE_VERTEXAI=FALSE
export GOOGLE_API_KEY=<YOUR_API_KEY>
```

---

### Start backend agents

```bash
uvicorn agents.host_agent.__main__:app --port 8000 & \
uvicorn agents.flight_agent.__main__:app --port 8001 & \
uvicorn agents.stay_agent.__main__:app --port 8002 & \
uvicorn agents.activities_agent.__main__:app --port 8003
```

---

### Run the frontend

```bash
streamlit run travel_ui.py
```

---

