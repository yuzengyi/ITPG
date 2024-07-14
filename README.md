# ITPG: Designing Multiple Agents in Human-AI Collaborative Information Technology Problem Generation Dataset
> Leveraging LLMs to automatically generate multiple-choice questions for information technology topics using langchain tools, integrated with Google search and PoT assistance

## How to run
### 1. Environment Requirements

python version == 3.11.1

pip version == 24.0


### 2. Create Conda Virtual Environment

Run the command in root folder:

```bash
conda create -n ITQG
conda activate ITQG
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Replace Your Keys
Open main.py and edit lines 4 & 5
```python
# API-KEY Settings
os.environ["OPENAI_API_KEY"] = "your openai key"
os.environ["SERPAPI_API_KEY"] = "your serpapi key"
```
### 5. Modify Question Settings
Open main.py and edit lines 7-11
```python
# Question settings
cnt = 1 # number of questions
topic = 'Networking Basics' # focus topic
difficulty_level = 0 # difficulty level: 0 easy, 1 medium, 2 hard
isContextual = True # Whether to set a scenario context
additionalConstraints = ""
```
### 6. Run
Execute the command in the root folder:
```python
python main.py
```
