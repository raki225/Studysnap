📚 StudySnap AI

> Your personal AI-powered study assistant for understanding, learning, and revising study materials.

## ✨ About the Project

**StudySnap AI** is an AI-powered study assistant that helps students understand study materials in a simple and interactive way.

Users can upload questions, textbook pages, handwritten notes, diagrams, equations, assignments, or code. StudySnap AI analyzes the uploaded material using **Google Gemini** and provides beginner-friendly explanations.

Users can also ask follow-up questions and generate a personalized study summary that can be sent to WhatsApp through **Twilio**.

---

## 🎯 Problem It Solves

Students often find it difficult to understand complex questions, textbook content, handwritten notes, diagrams, and technical concepts.

StudySnap AI provides a simple AI-powered learning experience where students can:

- 📸 Upload study material
- 🤖 Get AI-powered explanations
- 💬 Ask follow-up questions
- 🧠 Understand how and why something works
- 📝 Generate study summaries
- 📲 Send study summaries to WhatsApp

---

## 🚀 Features

### 📸 AI Image Analysis

Upload different types of study material:

- Questions
- Textbook pages
- Handwritten notes
- Diagrams
- Equations
- Assignments
- Programming code

The AI analyzes the uploaded material and explains it in an easy-to-understand way.

### 💬 Follow-Up Questions

After uploading study material, users can continue the conversation with questions such as:

- Explain this in simple English
- Why did you use this formula?
- Show me the steps
- Give me an easy example
- Explain it like a beginner
- Give me quick revision notes

### 🤖 Gemini AI

StudySnap AI uses Google's Gemini AI to analyze study materials and generate explanations.

### 📝 Study Summary

Users can generate a personalized study summary from their learning conversation for quick revision.

### 📲 WhatsApp Integration

StudySnap AI integrates with Twilio to send study summaries to WhatsApp.

> WhatsApp messaging availability depends on the Twilio account configuration and messaging restrictions.

### 🎨 Premium AI Interface

The application includes a modern AI-focused interface with:

- Glassmorphism
- Animated AI elements
- Premium cards
- Responsive layout
- Dark cinematic design
- Interactive study experience

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application development |
| Streamlit | Web application framework |
| Google Gemini | AI analysis and explanations |
| Twilio | WhatsApp integration |
| HTML | Custom UI components |
| CSS | Styling and animations |
| Git | Version control |
| GitHub | Source code hosting |

---

## 🏗️ How It Works

```text
                ┌──────────────────────┐
                │        Student       │
                │ Uploads Study Image  │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │     StudySnap AI     │
                │    Streamlit App     │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │     Google Gemini    │
                │    AI Processing     │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ Explanation + Chat   │
                │ + Follow-up Questions│
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │   Study Summary      │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │   Twilio WhatsApp    │
                └──────────────────────┘
```

---

## 📂 Project Structure

```text
Studysnap/
│
├── app.py
├── prompts.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── .streamlit/
    └── secrets.toml
```

---

## 🔐 Configuration

StudySnap AI uses API credentials for external services.

Create a local Streamlit secrets file:

```text
.streamlit/secrets.toml
```

Example:

```toml
GEMINI_API_KEY = "your_gemini_api_key"

TWILIO_ACCOUNT_SID = "your_twilio_account_sid"
TWILIO_AUTH_TOKEN = "your_twilio_auth_token"
TWILIO_WHATSAPP_FROM = "your_twilio_whatsapp_number"
TWILIO_CONTENT_SID = "your_twilio_content_sid"
```

### ⚠️ Security

**Never commit your real API keys or authentication tokens to GitHub.**

Your `.gitignore` should include:

```gitignore
.streamlit/secrets.toml
.env
.env.*
__pycache__/
*.py[cod]
.venv/
venv/
env/
.vscode/
.idea/
```

---

## ▶️ Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/raki225/Studysnap.git
```

### 2. Open the project

```bash
cd Studysnap
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the environment

#### Windows

```bash
venv\Scripts\activate
```

#### macOS / Linux

```bash
source venv/bin/activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure secrets

Create:

```text
.streamlit/secrets.toml
```

and add your Gemini and Twilio credentials.

### 7. Start the application

```bash
streamlit run app.py
```

The application will normally open at:

```text
http://localhost:8501
```

---

## 🧪 Example Usage

1. Open StudySnap AI.
2. Upload a study-related image.
3. Let Gemini analyze the material.
4. Read the AI-generated explanation.
5. Ask follow-up questions.
6. Generate a study summary.
7. Send the summary to WhatsApp when the Twilio configuration supports it.

---

## 🤖 AI-Assisted Development

This project was developed with the assistance of AI tools during the development process.

AI assistance was used for:

- Code development
- Debugging
- UI refinement
- Prompt improvement
- Error analysis
- Feature implementation
- Documentation

The project idea, requirements, development direction, feature decisions, testing, integration, and final implementation were reviewed and developed as part of the project-building process.

---

## 🔮 Future Improvements

Planned or possible future improvements include:

- 📚 PDF study material support
- 🎤 Voice-based questions
- 🔊 AI-generated audio explanations
- 🌐 Multi-language explanations
- 📊 Personal learning analytics
- 📝 Automatic quiz generation
- 🎯 Personalized study plans
- 📱 Mobile application
- 💾 Saved study history
- 🔐 User authentication
- 📈 Learning progress dashboard

---

## 👨‍💻 Developer

### Rakesh Sivala

Computer Science Engineering

Interested in:

- Artificial Intelligence
- Generative AI
- Full-Stack Development
- Data Analytics
- AI-powered applications

---

## 📄 License

This project is currently intended for educational and demonstration purposes.

---

## 🙏 Acknowledgements

- Google Gemini for AI capabilities
- Streamlit for the application framework
- Twilio for WhatsApp integration
- GitHub for version control and project hosting
- AI tools used during development

---

## ⭐ StudySnap AI

**Learn. Understand. Remember.**

> Not just answers — understand how and why.
