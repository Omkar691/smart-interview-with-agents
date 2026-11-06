from dotenv import load_dotenv
load_dotenv()
from typing_extensions import TypedDict,NotRequired,Annotated
from typing import Optional,List
from src.utils.objects import Analyst
from langgraph.graph import MessagesState
import operator
# State


class GenerateAnalystState(TypedDict):
    topic: str
    max_analysts: int  # Fixed: use plural
    human_analyst_feedback: NotRequired[Optional[str]]
    analysts: NotRequired[list[Analyst]]


class InterviewState(MessagesState):
    max_num_terms : int # number of terms of msgs
    context: Annotated [list,operator.add]
    analyst:Analyst # my analyst
    interview:str # interview talk
    section: list # final key we duplicated from other states for send() api
    
class ResearchGraphState(TypedDict):
    topic:str # Research topic
    max_analysts:int #number of analyst
    human_analyst_feedback:NotRequired[Optional[str]] # human feedback
    analysts:List[Analyst]# analyst asking questions
    sections:Annotated[List,operator.add]# send() api key
    introduction: str # intro of the final report
    content: str# content of the final report
    conclusion:str #conclusion of the final report
    final_report: str #final report 