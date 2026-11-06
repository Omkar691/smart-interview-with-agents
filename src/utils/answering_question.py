from src.utils.states import InterviewState
from src.utils.nodes import generate_question, search_web, search_web2, generate_answer, save_interview, write_section
from src.utils.states import InterviewState
from src.utils.edges import  routes_messages
from langgraph.graph import StateGraph, START, END

# Add nodes and edges 
interview_builder = StateGraph(InterviewState)
interview_builder.add_node("ask_question", generate_question)
interview_builder.add_node("search_web", search_web)
interview_builder.add_node("search_web2", search_web2)
interview_builder.add_node("answer_question", generate_answer)
interview_builder.add_node("save_interview", save_interview)
interview_builder.add_node("write_section", write_section)

# Flow
interview_builder.add_edge(START, "ask_question")
interview_builder.add_edge("ask_question", "search_web")
interview_builder.add_edge("ask_question", "search_web2")
interview_builder.add_edge("search_web", "answer_question")
interview_builder.add_edge("search_web2", "answer_question")
interview_builder.add_conditional_edges("answer_question", routes_messages,['ask_question','save_interview'])
interview_builder.add_edge("save_interview", "write_section")
interview_builder.add_edge("write_section", END)

question_answer_graph = interview_builder.compile()


# from dotenv import load_dotenv
# from src.utils.states import GenerateAnalystState,InterviewState
# load_dotenv()
# from src.utils.models import llm
# from src.utils.objects import Analyst,Perspective,SeachQuery
# from src.utils.prompts import analyst_instructions
# from langchain.messages import SystemMessage,HumanMessage
# from langgraph.types import interrupt
# from src.utils.prompts import question_instructions,search_instructions,answer_instructions,section_writer_instructions
# import pydantic
# from langchain_tavily import TavilySearch
# from langchain_core.messages import get_buffer_string
# def create_analysts(state:GenerateAnalystState):
#     """create analysts"""
#     topic=state["topic"]
#     max_analysts=state["max_analyst"]
#     human_analyst_feedback=state.get("human_analyst_feedback","")

#     # Enforce structured output

#     structured_llm=llm.with_structured_output(Perspective)

#     # system message

#     system_message=analyst_instructions.format(topic=topic,
#                                                human_analyst_feedback=human_analyst_feedback,
#                                                max_analysts=max_analysts)

#     ## Generate questions 
#     analysts=structured_llm.invoke([SystemMessage(content=system_message)]+[HumanMessage(content="please generate the set of analysts")])


#     return {"analysts":analysts.analysts}


# def human_feedback(state: GenerateAnalystState):
#     """this is where human gives feedback about the analyst given"""
#     feedback= interrupt({
#         "questions": "Are these analyst okay for you",
#         "analysts":[
#             analyst.model_dump() if hasattr(analyst,"model_dump") else analyst
#             for analyst in state.get("analysts",[])
#            ],
#            "instructions":"Return feedback to regenerate analysts"
#            " or return empty/perfect/continue/okay to approve and continue the graph"
#     })

#     if feedback is None:
#         return {"human_analyst_feedback":None}
    
    
#     if isinstance(feedback,str):
#         feedback=feedback.strip()

#         if feedback=="":
#             return {"human_analyst_feedback":None}

#         if feedback.lower() in {"perfect","okay","continue","yes"}:
#             return {"human_analyst_feedback":None}

#         return {"human_analyst_feedback":feedback}

#     return {"human_analyst_feedback":None}


# def generate_question(state: InterviewState):
#     analyst = state["analyst"]
#     if isinstance(analyst, dict):
#         analyst = Analyst.model_validate(analyst)

#     system_message = question_instructions.format(goals=analyst.persona)   # lowercase, different name
#     question = llm.invoke([SystemMessage(content=system_message)] + state["messages"])
#     return {"messages": [question]}


# def search_web(state:InterviewState):
#     """Retrive docs from web"""
#     # seach query
#     structured_llm=llm.with_structured_output(SeachQuery)
#     # search instruction 

#     search_instruction_system_message=SystemMessage(content=search_instructions)
#     tavily_search=TavilySearch(max_results=3)
#     search_query= structured_llm.invoke([search_instruction_system_message]+state["messages"])
    
#     # seach 
#     data=tavily_search.invoke({"query":search_query.search_query})
#     search__docs=data.get("results",data)

#     #format

#     formatted_search_docs = "\n\n---\n\n".join(
#         [
#             f'<Document href="{doc["url"]}"/>\n{doc["content"]}\n</Document>'
#             for doc in search__docs
#         ]
#     )

#     return {"context": [formatted_search_docs]}


# def search_web2(state:InterviewState):
#     """Retrive docs from web"""
#     # seach query
#     structured_llm=llm.with_structured_output(SeachQuery)
#     # search instruction 

#     search_instruction_system_message=SystemMessage(content=search_instructions)
#     tavily_search=TavilySearch(max_results=3)
#     search_query= structured_llm.invoke([search_instruction_system_message]+state["messages"])
    
#     # seach 
#     data=tavily_search.invoke({"query":search_query.search_query})
#     search__docs=data.get("results",data)

#     #format

#     formatted_search_docs = "\n\n---\n\n".join(
#         [
#             f'<Document href="{doc["url"]}"/>\n{doc["content"]}\n</Document>'
#             for doc in search__docs
#         ]
#     )

#     return {"context": [formatted_search_docs]}

# def generate_answer(state: InterviewState):
#     """NOde to generate answere"""

#     analyst=state["analyst"]
#     message=state["messages"]
#     context=state["context"]

#     if isinstance(analyst,dict):
#         analyst=Analyst.model_validate(analyst)


#     # answere question
#     system_message=answer_instructions.format(goals=analyst.persona,context=context)
#     answer=llm.invoke([SystemMessage(content=system_message)]+message)

#     # name the message as coming from the expert

#     answer.name='expert'

#     # append to the state

#     return{"messages": [answer]}


# def save_interview(state: InterviewState):
#     "save interviews"

#     messages=state["messages"]

#     interview= get_buffer_string(messages)
#     return {"interview": interview}

# def write_section(state: InterviewState):
#     """Node to answere a question"""

#     inteeview=state["interview"]
#     context=state["context"]
#     analyst=state["analyst"]

#     if isinstance(analyst,dict):
#         analyst=Analyst.model_validate(analyst)

#     System_message=section_writer_instructions.format(focus=analyst.description)
#     section=llm.invoke([SystemMessage(content=System_message)]+
#                        [HumanMessage(content=f"Use this source to write your section : {context}")])

#     return {"section": [section.content]}

