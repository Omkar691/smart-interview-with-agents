from pydantic import BaseModel, Field
from typing import List

# create our object Analyst
class Analyst(BaseModel):
    affiliation: str = Field(description="primary affiliation of the analyst")
    name: str = Field(description="Name of the analyst")
    role: str = Field(description="role of the analyst in the context of the topic")
    description: str = Field(description="description of the analyst,focus,concerns,and motives ")

    @property
    def persona(self) -> str:
        return f"Name:{self.name}\nRole:{self.role}\nAffiliation:{self.affiliation}\nDescription:{self.description}"

# Fix: Inherit from BaseModel instead of Analyst
class Perspective(BaseModel):
    analysts: List[Analyst] = Field(description="Comprehensive list of analysts with their roles and affiliations")



class SeachQuery(BaseModel):
    search_query: str = Field(description=" Search query for retrieval")
    max_results: int = Field(description="Maximum number of results to return")