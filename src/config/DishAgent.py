from core.llm_client import LLMClient
from langchain_core.prompts import ChatPromptTemplate
from model.Dish import Dishes, Dish
from typing import TypedDict, List, Annotated
import operator
from langgraph.types import Send

class State(TypedDict):
    meals: str  # The user's input listing the meals to prepare
    sections: List[Dish] # One section per meal/dish with ingredients
    completed_menu: Annotated[List[str], operator.add]  # Worker written dish guide chunks
    final_meal_guide: str  # Fully compiled, readable menu

class WorkerState(TypedDict):
    section: Dish
    completed_menu: Annotated[list, operator.add] # list with addition operators between elements    

class Node:
    def __init__(self):
        self.llm_client = LLMClient()
    def orchestrator(self, state: State):
        """Orchestrator that generates a structured dish list from the given meals."""
        # print(state, "orchestrator")
        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                "You are an assistant that generates a structured grocery list.\n\n"
                "The user wants to prepare the following meals: {meals}\n\n"
                "For each meal, return a section with:\n"
                "- the name of the dish\n"
                "- a comma-separated list of ingredients needed for that dish.\n"
                "- the cuisine or cultural origin of the food"
            ),
            ("human", "Generate a grocery list for these meals: {meals}")
        ])
        planner_pipe = prompt | self.llm_client.client.with_structured_output(Dishes)
        # use the planner_pipe LLM to break the user's meal list into structured dish sections
        dish_descriptions = planner_pipe.invoke({"meals": state["meals"]})

        # return the list of dish sections to be passed to worker nodes
        return {"sections": dish_descriptions.sections}
    def assign_workers(self, state: State):
        # print(state, "assign_workers")
        """Assign a worker to each section in the plan"""

            # Kick off section writing in parallel via Send() API
        return [Send("chef_worker", {"section": s}) for s in state["sections"]]    
    def chef_worker(self, state: WorkerState):
        chef_prompt =  ChatPromptTemplate.from_messages([
            (
                "system",
                "You are a world-class chef from {location}.\n\n"
                "Please introduce yourself briefly and present a detailed walkthrough for preparing the dish: {name}.\n"
                "Your response should include:\n"
                "- Start with hello with your  name and culinary background\n"
                "- A clear list of preparation steps\n"
                "- A full explanation of the cooking process\n\n"
                "Use the following ingredients: {ingredients}."
            ),
            ("human", "Please provide a cooking guide for {name} using {ingredients}.")
        ])
        # print(state, "chef_worker")
        chef_pipe = chef_prompt | self.llm_client.client
        """Worker node that generates the cooking instructions for one meal section."""

        # Use the language model to generate a meal preparation plan
        # The model receives the dish name, location, and ingredients from the current section
        meal_plan = chef_pipe.invoke({
            "name": state["section"].name,
            "location": state["section"].location,
            "ingredients": state["section"].ingredients
        })

        # Return the generated meal plan wrapped in a list under completed_sections
        # This will be merged into the main state using operator.add in LangGraph
        return {"completed_menu": [meal_plan.content]}
    def synthesizer(self, state: State):
        # print(state, "synthesizer")
        """Synthesize full report from sections"""

        # list of completed sections
        completed_sections = state["completed_menu"]

        # format completed section to str to use as context for final sections
        completed_menu = "\n\n---\n\n".join(completed_sections)

        return {"final_meal_guide": completed_menu}    


class DishAgent:
    def __init__(self):
        self.state : State = {
            "meals": "Spaghetti Bolognese and Chicken Stir Fry",
            "sections": [],
            "completed_menu": [],
            "final_meal_guide": ""
        }
        

class Workflow:
    
    def build_workflow(self):
        from langgraph.graph import StateGraph, START, END
        node = Node()
        orchestrator_worker_builder = StateGraph(State)

        # add the nodes
        orchestrator_worker_builder.add_node("orchestrator", node.orchestrator)
        orchestrator_worker_builder.add_node("chef_worker", node.chef_worker)
        orchestrator_worker_builder.add_node("synthesizer", node.synthesizer)


        orchestrator_worker_builder.add_conditional_edges(
            "orchestrator", node.assign_workers, ["chef_worker"] # source node, routing function, list of allowed targets
        )
        
        orchestrator_worker_builder.add_edge(START, "orchestrator")
        orchestrator_worker_builder.add_edge("chef_worker", "synthesizer")
        orchestrator_worker_builder.add_edge("synthesizer", END)


        return orchestrator_worker_builder.compile()
    
    def draw(self, workflow):
        """Draw the workflow graph using Mermaid (no pygraphviz needed)"""
        try:
            png_data = workflow.get_graph().draw_mermaid_png()
            
            with open("workflow_graph.png", "wb") as f:
                f.write(png_data)
            
            print("✅ Workflow graph saved to workflow_graph.png")
            
            try:
                from IPython.display import Image, display
                display(Image(png_data))
            except:
                pass
                
        except Exception as e:
            print("📊 Workflow Graph (Mermaid syntax):")
            print(workflow.get_graph().draw_mermaid())
            print("\nPaste the above into https://mermaid.live/ to visualize")

if __name__ == "__main__":
    workflow = Workflow()
    orchestrator_worker = workflow.build_workflow()
    # workflow.draw(orchestrator_worker)
    state = orchestrator_worker.invoke({"meals": "Spaghetti Bolognese, Chicken Curry"})
    # print(state["final_meal_guide"])
    # agent = DishAgent()
    # report_sections = agent.planner_pipe().invoke({"meals": agent.state['meals']})
    for i, section in enumerate(state.get("sections", [])):
        print(f"Dish {i+1}\n")
        # add each dish to our dummy state
        # self.state["sections"].append(section)
        print(f"Item Name: {section.name}")
        print(f"Location/Cuisine: {section.location}")
        print(f"Ingredients: {", ".join(section.ingredients)}.")
        print("\n")
        print(f"Completed Menu: {state.get('completed_menu', [])}")
    # # print(agent.planner_pipe().invoke({"meals": ["Spaghetti Bolognese, Chicken Curry"]}))       