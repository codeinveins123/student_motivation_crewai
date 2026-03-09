from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class Iws2():
    """Iws2 crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['analyst'], # type: ignore[index]
            verbose=True,
        )

    @agent
    def advisor(self) -> Agent:
        return Agent(
            config=self.agents_config['advisor'], # type: ignore[index]
            verbose=True,
            temperature = 0.8,
        )

    @task
    def analyz_history_task(self) -> Task:
        return Task(
            config=self.tasks_config['analyz_history_task'], # type: ignore[index]
        )

    @task
    def create_plan_task(self) -> Task:
        return Task(
            config=self.tasks_config['create_plan_task'], # type: ignore[index]
            output_file='plan.txt',
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Iws2Crew crew"""

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
