# AI Resume Builder

An intelligent AI-powered Resume Builder that enables users to create professional, ATS-friendly resumes effortlessly. The application leverages Large Language Models (LLMs) to generate optimized resume content based on user input while providing an intuitive web interface built with Django.

---

## Features

- 🤖 AI-powered resume content generation
- 📄 ATS-friendly resume creation
- ✍️ Professional summary generation
- 💼 Work experience suggestions
- 🎓 Education and skills management
- 📥 Download generated resumes
- 🌐 User-friendly web interface
- 🔒 Secure Django backend

---

## Tech Stack

| Category | Technologies |
|----------|--------------|
| Frontend | HTML, CSS, JavaScript, Bootstrap |
| Backend | Django |
| Database | SQLite3 |
| AI | Groq API / LLaMA Model *(or your configured LLM)* |
| Language | Python |

---

## Project Structure

```
AI-Resume-Builder/
│
├── resumeAI/              # Django Project Configuration
├── resumes/               # Resume Application
├── manage.py              # Django Management Script
├── db.sqlite3             # SQLite Database
├── .gitignore
└── README.md
```

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/your-username/AI-Resume-Builder.git

cd AI-Resume-Builder
```

---

### Create Virtual Environment

Windows

```bash
python -m venv venv

venv\Scripts\activate
```

Linux/macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is not available, generate it using:

```bash
pip freeze > requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root.

```env
GROQ_API_KEY=your_groq_api_key
SECRET_KEY=your_django_secret_key
DEBUG=True
```

---

## Database Migration

```bash
python manage.py makemigrations

python manage.py migrate
```

---

## Run the Development Server

```bash
python manage.py runserver
```

Open your browser:

```
http://127.0.0.1:8000/
```

---

## How It Works

1. User enters personal and professional information.
2. The application sends prompts to the AI model.
3. AI generates optimized resume content.
4. Django processes and formats the response.
5. Users can preview and download their resume.

---

## AI Capabilities

- Professional Summary Generation
- Skills Enhancement
- Resume Bullet Point Optimization
- ATS Keyword Optimization
- Grammar Improvement
- Resume Formatting Suggestions

---

## Future Enhancements

- PDF Export
- Multiple Resume Templates
- Cover Letter Generator
- LinkedIn Profile Import
- Resume Score Analysis
- Interview Question Generator
- Multi-language Resume Support
- User Authentication & Dashboard
- Cloud Deployment

---

## Screenshots

You can include screenshots of:

- Home Page
- Resume Form
- AI Generated Resume
- Resume Preview
- Download Feature

---

## Author

**Santheesh P M**

- GitHub: https://github.com/SantheeshCS

---

## Acknowledgements

- Django
- Groq API
- LLaMA Models
- Bootstrap
- Python Community
