from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import os
from langchain.agents import AgentExecutor, create_openai_tools_agent, load_tools, initialize_agent, AgentType
from typing import List, Dict
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.prompts import MessagesPlaceholder

def search_example_problems(topic):
    llm = ChatOpenAI(temperature=0, model_name="gpt-4-turbo-preview", max_tokens=500)
    serpapi_api_key = os.environ["SERPAPI_API_KEY"]
    tools = load_tools(["serpapi"], llm=llm, serpapi_api_key=serpapi_api_key)
    questions = f"Please help me find some typical application questions in IT and summarize common question types."
    template = ChatPromptTemplate.from_messages([
        ("system", "You are an IT research expert, please answer the following questions in English"),
        ("human", "{user_input}"),
        MessagesPlaceholder("agent_scratchpad")
    ])
    agent = create_openai_tools_agent(llm, tools, template)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
    example_problem = agent_executor.invoke({"user_input": questions})
    print("Example problem search results: \n")
    print(example_problem)

    return example_problem["output"]

def generate_questions(cnt, topic, difficulty, additionalRestrictions, example_problem):
    question_list = []
    for i in range(cnt):
        llm = ChatOpenAI(temperature=0.5, model_name="gpt-4-turbo-preview")
        serpapi_api_key = os.environ["SERPAPI_API_KEY"]
        tools = load_tools(["serpapi"], llm=llm, serpapi_api_key=serpapi_api_key)
        questions = f"""I need you to write one question about {topic}, 
                        based on the example {example_problem}, check with search engines to ensure it matches real-life applicability
                        with difficulty {difficulty}, {additionalRestrictions}, just provide the question, ending with a question mark."""
        template = ChatPromptTemplate.from_messages([
            ("system", "You are an IT research expert, please answer the following questions in English"),
            ("human", "{user_input}"),
            MessagesPlaceholder("agent_scratchpad")
        ])
        agent = create_openai_tools_agent(llm, tools, template)
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
        generated_problem = agent_executor.invoke({"user_input": questions})
        print("Generated question: \n", generated_problem)
        question_list.append(generated_problem["output"])

    return question_list

def solve_problems(generated_questions):
    llm = ChatOpenAI(temperature=0, model_name="gpt-4-turbo-preview")
    tools = load_tools(["llm-math"], llm=llm)
    template = ChatPromptTemplate.from_messages([
        ("system", "You are an IT expert, please answer the following questions in English"),
        ("human", "{user_input}"),
        MessagesPlaceholder("agent_scratchpad")
    ])
    agent = create_openai_tools_agent(llm, tools, template)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
    
    question_with_answer = []
    for question in generated_questions:
        solution = agent_executor.invoke({"user_input": question + " Return the problem-solving process and answer, only single-line Python expressions can be used for calculations, such as '470 // 60, 470 % 60', if there are multiple expressions, they must be calculated step-by-step, undefined variables are not allowed"})
        question_with_answer.append({"content": question, "description": solution})
    print(question_with_answer)
    return question_with_answer

class QuestionFormat(BaseModel):
    content: str = Field(description="Question content")
    options: Dict[str, str] = Field(description="Options for the question, keys are A, B, C, D, values are option content")
    description: str = Field(description="Explanation of the question")
    correct_answer: str = Field(description="Correct answer option")

def add_choices(question_with_answer):
    llm = ChatOpenAI(temperature=0, model_name="gpt-4-turbo-preview")
    parser = JsonOutputParser(pydantic_object=QuestionFormat)

    template = """Now, I will provide you with a problem and answer suitable for elementary students, please convert it into a multiple-choice question. Make the options distracting, such as having similar numerical values or proportional relationships. Question: {question}, Answer: {answer},
                {format_instructions}
                """
    prompt = ChatPromptTemplate(
        template=template,
        input_variables=["question", "answer"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    chain = prompt | llm | parser
    question_completed = []
    for item in question_with_answer:
        ans = chain.invoke({"question": item["content"], "answer": item["description"]})
        question_completed.append(ans)

    return question_completed
