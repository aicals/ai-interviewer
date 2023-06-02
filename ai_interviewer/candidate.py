import json

from langchain import LLMChain, ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)


class Candidate:
    def __init__(
            self,
            name: str,
            job: str,
            years_of_experience: int,
            area: str,
            requirements: str,
            work_experiences: int,
            company: str,
            resume: str | None = None,
            verbose: bool = False
    ):
        """Initializes the agent"""
        self.name = name
        self.job = job
        self.years_of_experience = years_of_experience
        self.area = area
        self.work_experiences = work_experiences
        self.requirements = requirements
        self.company = company
        self.verbose = verbose
        if resume is None or resume == '':
            self.resume = self.create_resume()
        else:
            self.resume = resume
        self.conversation_chain = self.create_conversation_chain()

    def save(self, filename):
        """Saves the candidate's data"""
        data = {
            "name": self.name,
            "job": self.job,
            "years_of_experience": self.years_of_experience,
            "area": self.area,
            "requirements": self.requirements,
            "work_experiences": self.work_experiences,
            "company": self.company,
            "resume": self.resume
        }
        with open(filename, "w") as file:
            json.dump(data, file)

    def create_resume(self) -> str:
        """Creates the candidate's resume"""
        system_message_prompt = SystemMessagePromptTemplate.from_template(
            template="You are a creative assistant."
        )
        human_message_prompt = HumanMessagePromptTemplate.from_template(
            template="Create a resume for {name}, a talented {job} with "
                     "{years_of_experience} years of experience in {area}.\n"
                     "Be detailed in experiences and accomplishments.\n"
                     "The resume must be a good fit for the following job "
                     "requirements:\n{requirements}\n\nThe resume must show at "
                     "least {work_experiences} work experiences.\nUse names of "
                     "real companies in his work experiences.\nDo not use "
                     "{company}, {name} never worked there."
                     "The details of the work experiences must be different.\n"
                     "The work experiences must reflect seniority and career "
                     "progression. Older experiences must be compatible with "
                     "more junior roles, while recent experiences must be "
                     "compatible with more senior roles.\nThe details of each "
                     "work experience must be related to the company where {name} "
                     "worked at that time."
        )
        chat_prompt = ChatPromptTemplate.from_messages([
            system_message_prompt,
            human_message_prompt
        ])
        chain = LLMChain(llm=ChatOpenAI(temperature=0.5), prompt=chat_prompt)
        return chain.predict(
            name=self.name,
            job=self.job,
            years_of_experience=self.years_of_experience,
            area=self.area,
            requirements=self.requirements,
            work_experiences=self.work_experiences,
            company=self.company
        )

    def create_conversation_chain(self) -> ConversationChain:
        """Creates the conversation chain, needed for the agent to talk"""
        prompt = PromptTemplate(
            template="Your name is {name}. You are being interviewed for a "
                     "{job} position at {company} to work with {area}. "
                     "You are a talented {job} with {years_of_experience} years "
                     "of experience in {area}. You are talkative and provides "
                     "lots of specific details from yourself, your work "
                     "experience and your personality. If you do not know the "
                     "answer to a question, you create an answer to the question "
                     "based on your resume. Here's your resume:\n\n"
                     "{resume}\n\n\nCurrent conversation:\n{history}\n"
                     "Interviewer: {input}\n{name}: ",
            input_variables=["history", "input"],
            partial_variables={
                "name": self.name,
                "job": self.job,
                "years_of_experience": self.years_of_experience,
                "area": self.area,
                "company": self.company,
                "resume": self.resume
            }
        )

        conversation_chain = ConversationChain(
            llm=ChatOpenAI(temperature=0.5),
            verbose=self.verbose,
            memory=ConversationBufferWindowMemory(
                human_prefix='Interviewer',
                ai_prefix=self.name,
                k=4
            ),
            prompt=prompt
        )
        return conversation_chain

    def reply(self, message: str):
        """Bring the agent to life, enabling it to reply to messages"""
        return self.conversation_chain.predict(
            input=message,
            stop="Interviewer:"
        ).strip()

    @property
    def memory(self):
        return self.conversation_chain.memory
