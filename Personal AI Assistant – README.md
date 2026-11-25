# 🤖 Joshwi – Your Personal AI Assistant

Meet **Joshwi**, a tool-enabled personal AI assistant built using **Python, LangChain, Ollama, and MySQL**.

Joshwi understands natural-language requests and uses specialized tools to perform calculations, manage daily tasks, retrieve date and time information, and open supported Windows applications and websites.

Instead of manually executing different operations, interact with Joshwi through a simple conversational interface in your terminal.

## ✨ Features

### 🧮 Smart Calculator
Perform mathematical operations using natural-language instructions.

- ➕ Addition
- ➖ Subtraction
- ✖️ Multiplication
- ➗ Division
- 🚫 Division-by-zero handling

### 📅 Date & Time Assistant

- 🕒 Get current date and time.
- 📆 Retrieve today's date.
- ⏰ Get current local time.
- 🗓️ Find the weekday for a given date.
- 🔢 Calculate the number of days between two dates.
- ➕ Add days to a specified date.

### 📝 Task Management System

Manage tasks using natural-language commands with MySQL as the database.

- ➕ Add new tasks.
- 📋 Retrieve all saved tasks.
- 🔄 Update task status.
- ⏳ Track pending tasks.
- ✅ Track completed tasks.

### 🖥️ Application Launcher

Open supported Windows desktop applications.

| Application | Supported command |
|---|---|
| Visual Studio Code | `vscode` |
| WhatsApp | `whatsapp` |
| Calculator | `calculator` |
| Notepad | `notepad` |
| File Explorer | `explorer` |
| Google Chrome | `chrome` |

### 🌐 Website Launcher

Open supported websites using natural-language instructions.

- 🔎 Google
- ▶️ YouTube
- 🐙 GitHub

### 🧠 AI-Powered Tool Calling

- Uses LangChain's agent framework.
- Uses Ollama with Llama 3.2 (3B).
- Selects relevant tools based on user intent.
- Uses tool descriptions to understand each tool's purpose.
- Maintains conversation history during the running session.
- Provides responses using actual tool execution results.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| LangChain | Agent orchestration |
| Ollama | Local LLM execution |
| Llama 3.2 (3B) | Natural-language understanding |
| LangChain Tools | Custom tool integration |
| MySQL | Task data storage |
| Python datetime | Date and time operations |
| subprocess | Launch desktop applications |
| Windows OS | Desktop application integration |

## 🏗️ Architecture

```text
                 👤 User
                    |
                    ▼
             💬 Natural Language
                    |
                    ▼
              🧠 Ollama LLM
              Llama 3.2 (3B)
                    |
                    ▼
             ⚙️ LangChain Agent
                    |
          Intent Understanding
                    |
        ┌───────────┼────────────┐
        |           |            |
        ▼           ▼            ▼
    🧮 Calculator 📅 Date/Time  📝 Task Manager
        |           |            |
        ▼           ▼            ▼
     Results     Results      🗄️ MySQL
        |           |            |
        └───────────┼────────────┘
                    |
                    ▼
             🖥️ App Launcher
                    |
                    ▼
              🌐 Websites
                    |
                    ▼
             🤖 Joshwi Response
                    |
                    ▼
                  👤 User
```

## 📂 Project Structure

```text
Joshwi/
│
├── main.py
├── database_connection.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

**Note:** `database_connection.py` should contain your MySQL connection implementation. The `.env` file is recommended for storing database configuration securely.

## ⚙️ Prerequisites

Before running Joshwi, install:

- Python 3.10 or later.
- Ollama.
- Llama 3.2 (3B) model.
- MySQL Server.
- MySQL database and task table.
- Visual Studio Code (optional).

## 🚀 Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Joshwi
```

### 2️⃣ Create a virtual environment

```bash
python -m venv venv
```

Activate on Windows:

```bash
venv\Scripts\activate
```

### 3️⃣ Install dependencies

```bash
pip install langchain langchain-ollama mysql-connector-python
```

### 4️⃣ Configure Ollama

Download Ollama:

https://ollama.com/download

Pull the required model:

```bash
ollama pull llama3.2:3b
```

Ensure Ollama is running before starting Joshwi.

### 5️⃣ Configure MySQL

Create the database:

```sql
CREATE DATABASE joshwi;
```

Select the database:

```sql
USE joshwi;
```

Create the tasks table:

```sql
CREATE TABLE tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    task VARCHAR(500) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    created_at DATETIME
);
```

The application expects the following task fields:

| Column | Description |
|---|---|
| id | Unique task identifier |
| task | Task description |
| status | pending or completed |
| created_at | Task creation date and time |

### 6️⃣ Configure database connection

Update your `database_connection.py` to connect to your MySQL database.

Your `Database` class should provide a `get_connection()` method that returns a valid MySQL connection.

Example configuration values:

```text
DB_HOST=localhost
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=joshwi
```

Keep database credentials private. Do not upload real credentials to GitHub.

### 7️⃣ Run Joshwi

```bash
python main.py
```

Joshwi starts in the terminal and waits for your instructions.

To stop the application:

```text
EXIT
```

## 💡 Example Interactions

### 🧮 Calculator

**You:**

```text
Add 250, 350 and 400.
```

**Joshwi:**

```text
The result is 1000.
```

### 📅 Date & Time

**You:**

```text
What is today's date?
```

**Joshwi:**

```text
Today's date is YYYY-MM-DD.
```

*The actual date is obtained dynamically from your computer.*

### 📝 Task Management

**You:**

```text
Add a task to complete my Python project.
```

**Joshwi:**

```text
Task added successfully.
```

**You:**

```text
Show all my tasks.
```

**Joshwi:**

```text
PENDING TASKS

| Task ID | Task Description | Status |
|---------|------------------|--------|
| 1       | Complete Python project | pending |
```

**You:**

```text
Mark task 1 as completed.
```

**Joshwi:**

```text
Task status updated successfully.
```

### 🖥️ Application Launcher

**You:**

```text
Open Visual Studio Code.
```

**Joshwi:**

```text
Successfully requested opening vscode.
```

### 🌐 Website Launcher

**You:**

```text
Open GitHub.
```

**Joshwi:**

```text
Successfully requested opening github.
```

## 🔐 Security & Privacy

- 🔒 Keep MySQL credentials outside your source code.
- 🚫 Never commit `.env` files containing real credentials.
- 🛡️ Validate inputs before executing database operations.
- 🔐 Restrict database permissions to the operations required by the application.
- ⚠️ Only allow trusted users to execute desktop application tools.
- 🧹 Always close database connections after operations.

Recommended `.gitignore`:

```gitignore
.env
venv/
__pycache__/
*.pyc
*.log
```

## ⚠️ Limitations

- Joshwi currently supports only the applications and websites defined in its application mapping.
- Desktop application launching is designed for Windows.
- Task information is stored in MySQL and is available across application sessions.
- Conversation history is maintained in memory only while the application is running.
- The assistant depends on Ollama being available locally.
- Date and time operations use the computer's local clock.
- The assistant's ability to select tools depends on the LLM's tool-calling capabilities.

## 🔮 Future Enhancements

- 🎙️ Voice-based interaction.
- 🌍 Multilingual communication.
- 📧 Gmail integration.
- 📆 Google Calendar integration.
- ⏰ Task reminders and notifications.
- 📊 Task analytics and productivity reports.
- 🧠 Long-term conversational memory.
- 🌐 Browser automation.
- 🖥️ Interactive graphical user interface.
- 🔐 User authentication and role-based access.

## 👨‍💻 Author

Developed using Python, LangChain, Ollama, and MySQL.

⭐ If you find Joshwi useful, consider giving this project a star on GitHub!

---

**Disclaimer:** Joshwi uses an AI agent to select and execute tools. Always validate important operations and restrict access to tools that can affect your computer or database.