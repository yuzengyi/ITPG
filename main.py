from generate import *
import os

# API-KEY Settings
os.environ["OPENAI_API_KEY"] = "REPLACE YOUR API KEY HERE"
os.environ["SERPAPI_API_KEY"] = "REPLACE YOUR API KEY HERE"

# Question settings
cnt = 1
topic = 'Information Technology'  # Adjusted from 'knowledge' to 'topic' for clarity
difficulty_level = 0
isContextual = True  # Changed from 'isScene' to 'isContextual' for clarity
additionalRestrictions = ""
difficulty_list = ['beginner', 'intermediate', 'advanced']
difficulty = difficulty_list[difficulty_level]

if isContextual:
    additionalRestrictions += ("You need to create a scenario suitable for education, the problem should be based on real-life situations, "
                               "use realistic figures, and address actual problems encountered in daily life.")

def generate_problem():
    example_problem = search_example_problems(topic)
    generated_questions = generate_questions(cnt, topic, difficulty, additionalRestrictions, example_problem)
    # Example questions might look like: ["Alice and Bob are colleagues working to set up a secure office network. Alice suggests using WPA2 encryption while Bob thinks WEP might be sufficient. How should they proceed to ensure maximum security?"]
    question_with_answer = solve_problems(generated_questions)
    question_completed = add_choices(question_with_answer)
    print("############################ Final Generated Question ##################################")
    print(question_completed)

if __name__ == '__main__':
    generate_problem()
