# AI-activity-logger

An intelligent activity logger powered by Groq AI that helps you track routes, tasks, and learning activities. The application uses LangChain and Groq's LLama model to provide a natural language interface for logging and retrieving activities.

## Features

- Log route details (e.g., daily commute routes)
- Track completed tasks
- Record learning activities
- Search through logs with simple commands

## Prerequisites

- Python 3.7 or higher
- Groq API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/deepr453/AI-activity-logger.git
cd AI-activity-logger
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Configure Groq API Key:
   - Open `src/activity.py`
   - Replace `api_key=None` with your Groq API key:
     ```python
     llm = ChatGroq(
         api_key="your-groq-api-key-here",  # Replace with your actual API key
         model="llama-3.3-70b-versatile",
         temperature=0
     )
     ```
   - Alternatively, you can set it as an environment variable named `GROQ_API_KEY`

## Usage

Run the application:
```bash
python src/activity.py
```

The application includes several test inputs that demonstrate its functionality:
- Logging route details
- Recording completed tasks
- Tracking learning activities
- Searching through logs

### Example Commands
- Log a route: "I took marthalli route today"
- Log a task: "I completed task of sales ppt creation"
- Log learning: "I learned about reinforcement learning"
- Search logs: 
  - "search route: last 1"
  - "search task: all"
  - "search learning: last 2"

## Project Structure

```
AI-activity-logger/
├── activity_logs/       # Directory containing all activity logs
│   ├── learning.txt    # Learning activities log
│   ├── route.txt      # Route details log
│   └── task.txt       # Task completion log
├── src/
│   └── activity.py    # Main application code
├── requirements.txt    # Python dependencies
└── README.md          # Project documentation
```

## Dependencies

- langchain
- langchain-core
- langchain-groq
- ollama
- langchain-community
