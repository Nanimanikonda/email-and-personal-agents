from langchain_ollama import ChatOllama
from langchain.tools import tool
from langchain.agents import create_agent
from datetime import datetime,timedelta
from database_connection import Database
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage,AIMessage
import os,subprocess,shutil

llm=ChatOllama(model="llama3.2:3b", temperature=0.3)

class Calculator:
    @tool
    def add(numbers:list[float])->float:
        """use this method for addition operations"""
        return sum(numbers)
    @tool
    def subtraction(numbers:list[float])->float|str:
        """use this method for perfoming subractions"""
        if not numbers:
            return "Error: No numbers provided."
        ans=numbers[0]
        for i in range(1,len(numbers)):
            ans-=numbers[i]
        return ans
    @tool
    def multiplication(numbers:list[float])->float:
        """use this method for multiplications"""
        ans=1
        for i in numbers:
            ans*=i
        return ans
    @tool
    def division(a:float,b:float)->float|str:
        """use this method for dividing two numbers"""
        if b==0:
            return "Error: Cannot divide by zero."
        return a / b
calculator_tools=[Calculator.add,Calculator.subtraction,Calculator.multiplication,Calculator.division]
    
class DateTime:
    @tool
    def current_datetime():
        """Get the current local date and time."""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    @tool
    def current_date():
        """Get today's local date."""
        return datetime.now().strftime("%Y-%m-%d")
    @tool
    def current_time():
        """Get the current local time."""
        return datetime.now().strftime("%H:%M:%S")
    @tool
    def get_day(date: str):
        """Find the weekday for a given date in YYYY-MM-DD format."""
        try:
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            return date_obj.strftime("%A")
        except ValueError:
            return "Invalid date. Use YYYY-MM-DD format."
    @tool
    def days_between(date1: str, date2: str):
        """Calculate the number of days between two dates in YYYY-MM-DD format."""
        try:
            d1 = datetime.strptime(date1, "%Y-%m-%d")
            d2 = datetime.strptime(date2, "%Y-%m-%d")
            return abs((d2 - d1).days)
        except ValueError:
            return "Invalid date. Use YYYY-MM-DD format."
    @tool
    def add_days(date: str, days: int):
        """Add a specified number of days to a date in YYYY-MM-DD format."""
        try:
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            result = date_obj + timedelta(days=days)
            return result.strftime("%Y-%m-%d")
        except ValueError:
            return "Invalid date. Use YYYY-MM-DD format."
datetime_tools = [DateTime.current_datetime,DateTime.current_date,DateTime.current_time,DateTime.get_day,DateTime.days_between,DateTime.add_days]

class TaskManager:
    @tool
    def add_task(task: str) -> str:
        """Add a new task to the task database."""
        db = Database()
        connection = db.get_connection()
        cursor = connection.cursor()
        query = "INSERT INTO tasks (task, created_at) VALUES (%s, %s)"
        cursor.execute(query, (task, datetime.now()))
        connection.commit()
        cursor.close()
        connection.close()
        return "Task added successfully."
    @tool
    def get_tasks() -> list:
        """Retrieve all tasks from the task database."""
        db = Database()
        connection = db.get_connection()
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM tasks"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        return result
    @tool
    def update_task(task_id: int, status: str) -> str:
        """Update a task status. Status must be pending or completed."""
        if status not in ["pending", "completed"]:
            return "Invalid status. Use pending or completed."
        db = Database()
        connection = db.get_connection()
        cursor = connection.cursor()
        query = "UPDATE tasks SET status = %s WHERE id = %s"
        cursor.execute(query, (status, task_id))
        connection.commit()
        updated = cursor.rowcount
        cursor.close()
        connection.close()
        if updated == 0:
            return "Task not found or status was already unchanged."
        return "Task status updated successfully."
task_tools = [TaskManager.add_task,TaskManager.get_tasks,TaskManager.update_task]

@tool
def open_application(app: str) -> str:
    """Open installed Windows desktop applications or supported websites by name."""
    apps = {
        "vscode": "code",
        "vs code": "code",
        "whatsapp": "whatsapp:",
        "calculator": "calc.exe",
        "notepad": "notepad.exe",
        "explorer": "explorer.exe",
        "file explorer": "explorer.exe",
        "chrome": "chrome",
        "youtube": "https://www.youtube.com",
        "google": "https://www.google.com",
        "github": "https://github.com"
    }
    app = app.lower().strip()
    if app not in apps:
        return f"{app} is not supported."
    target = apps[app]
    try:
        if target.startswith("https://"):
            os.startfile(target)
        elif target.endswith(":"):
            os.startfile(target)
        elif os.path.isabs(target) and os.path.exists(target):
            subprocess.Popen([target])
        elif shutil.which(target):
            subprocess.Popen([target])
        else:
            return f"Could not find {app}. Check whether it is installed."
        return f"Successfully requested opening {app}."
    except Exception as e:
        return f"Unable to open {app}: {str(e)}"

agent=create_agent(model=llm,
                   tools=calculator_tools+datetime_tools+task_tools+[open_application],
                   system_prompt = """
You are Joshwi, a professional personal AI assistant.
Your purpose is to help users through natural conversation,
task management, calculations, date/time operations and
supported website interactions.
IDENTITY AND CONVERSATION:
1. Your name is Joshwi.
2. Respond naturally and professionally.
3. Remember names and details provided in the current
   conversation.
4. Never call tools for greetings, introductions or
   ordinary conversations.
5. Never generate tasks unless explicitly requested.
TOOL USAGE:
1. Use tools only when the user's request requires them.
2. Never expose tool calls, JSON arguments, function names
   or internal execution details.
3. Never generate example tool calls unless explicitly
   requested by the user.
4. Execute only the tools relevant to the request.
5. Use actual tool results. Never fabricate results.
6. If a tool fails, communicate the failure clearly.
TASK MANAGEMENT:
1. Use add_task only when the user explicitly asks
   to create or save a task.
2. Use get_tasks when the user asks to view, list,
   check or organize tasks.
3. Use update_task only when the user requests a change
   to an existing task.
4. Never assume a task is completed.
5. Distinguish pending and completed tasks accurately.
6. Use task IDs when updating tasks.
TASK RESPONSE FORMATTING:
When users request all tasks, organize them into two
separate sections.
PENDING TASKS:
Present pending tasks in a Markdown table with:
- Task ID
- Task Description
- Status
COMPLETED TASKS:
Present completed tasks in a Markdown table with:
- Task ID
- Task Description
- Status
If either category has no tasks, explicitly mention:
"No pending tasks found."
or
"No completed tasks found."
If there are no tasks at all, clearly communicate that.
CALCULATOR:
1. Use calculator tools for arithmetic.
2. Never invent calculation results.
3. Return results clearly with appropriate units.
DATE AND TIME:
1. Use datetime tools for current date/time and
   date-related calculations.
2. Never guess current date or time.
WEBSITE INTERACTION:
1. Open websites only when explicitly requested.
2. Use only supported websites.
3. Never open websites during normal conversation.
RESPONSE STYLE:
1. Be concise, professional and conversational.
2. Understand the user's actual intention.
3. Answer directly.
4. Use Markdown formatting when appropriate.
5. Use tables for structured information when requested.
6. Avoid unnecessary explanations.
7. Never display raw JSON or internal tool information.
8. Never claim an operation succeeded without confirmation.
Your priority is to provide accurate, useful and
natural responses while using tools intelligently.
"""
)
history=[]
while True:
    query=input("👱 : ")
    if query.upper()=="EXIT":
        break
    history.append(HumanMessage(content=query))
    response = agent.invoke({
        "messages": history
    })
    ai_response=response["messages"][-1].content
    print("🤖 :", ai_response)
    history.append(AIMessage(content=ai_response))