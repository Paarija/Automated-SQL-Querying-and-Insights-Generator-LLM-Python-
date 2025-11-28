# Automated-SQL-Querying-and-Insights-Generator-LLM-Python-
## Natural Language → SQL → Insights

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![LLM](https://img.shields.io/badge/AI-Gemini%202.5-green)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey)
![Streamlit](https://img.shields.io/badge/Deployment-Streamlit-red)

## Project Overview

This project is an **AI-driven Business Intelligence tool** that converts **plain English questions into SQL queries**, runs them on a structured wholesale database, and returns **instant analytical insights with auto-generated visualizations**.

The system acts like a **virtual Data Analyst**, capable of:
- Understanding natural language queries  
- Generating valid SQL using an LLM (Gemini 2.5)  
- Executing queries on `clients`, `catalog`, and `invoices` tables  
- Computing metrics like **Revenue**, **Profit**, and **Margin**  
- Producing interactive charts automatically  

This is a compact but powerful end-to-end project demonstrating **LLM integration, data engineering, SQL logic, and dashboard development** 

---

## App Demo
<img width="1348" height="626" alt="1" src="https://github.com/user-attachments/assets/3f86fedb-0e8e-4da1-bd41-3945bd9f6a4a" />


<img width="1365" height="620" alt="2" src="https://github.com/user-attachments/assets/fbbfc3c4-ac19-4395-8307-b034dfca5c27" />



> The interactive UI allows users to ask business questions, view generated SQL, analyze the output table, and explore auto-generated charts 

---

## Tech Stack

* **Language:** Python 3.x  
* **Frontend / UI:** Streamlit  
* **AI Engine:** Google Gemini 2.5 Flash (Text-to-SQL)  
* **Database:** SQLite  
* **Data Analysis:** Pandas  
* **Visualization:** Altair  

---

## Core Features

### 1. Natural Language → SQL Generation  
Automatically converts English questions into executable SQL using a structured prompt and schema awareness.

### 2. Automated Visualizations  
Creates bar charts or pie charts depending on the result type, with no manual configuration needed.

### 3. Built-In Business Metrics  
Revenue, Profit, and Margin logic embedded directly into the system prompt.

### 4. Interactive Dashboard  
Preview SQL, view tables, switch between predefined business queries, and explore insights instantly.

---

## Installation & Usage

### Prerequisites
* Python 3.8+
* A valid Gemini API key

### Setup
1. Clone the repository:
 ```bash
git clone <Automated-SQL-Querying-and-Insights-Generator-LLM-Python->
cd Automated-SQL-Querying-and-Insights-Generator-LLM-Python
 ```

2. Install dependencies:
 ```bash
pip install -r requirements.txt
 ```

3. Add your Gemini API key inside `text2sql.py`.

4. Run the application:
 ``` bash
streamlit run text2sql.py
 ```



---




