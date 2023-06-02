from typing import NamedTuple

from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import BaseOutputParser
import json
from .util import StreamingStdOutLimitedCallbackHandler


class JobDescription(NamedTuple):
    title: str
    about: str
    responsibilities: str
    requirements: str
    why: str
    text: str

    def save(self, filename):
        with open(filename, "w") as file:
            json.dump(self._asdict(), file, indent=2)


class JobDescriptionOutputParser(BaseOutputParser):
    def parse(self, text: str) -> JobDescription:
        title = text.split('Job Title:')[1].split('\n\n')[0].strip()
        about = text.split('About the Role:')[1].split('\n\n')[0].strip()
        responsibilities = text.split('Responsibilities:')[1].split('\n\n')[0].strip()
        requirements = text.split('Requirements:')[1].split('\n\n')[0].strip()
        why = text.split('Why Work at')[1].split(':\n')[1].split('\n\n')[0].strip()
        return JobDescription(
            title=title,
            about=about,
            responsibilities=responsibilities,
            requirements=requirements,
            why=why,
            text=text
        )


def create_job_description(
        company: str,
        job: str,
        years_of_experience: int,
        area: str,
        streaming: bool = False
) -> JobDescription:
    system_message_prompt = SystemMessagePromptTemplate.from_template(
        template="You are a helpful Human Resources assistant who creates "
                 "detailed job postings for {company} to attract talented "
                 "candidates."
    )

    human_message_prompt = HumanMessagePromptTemplate.from_template(
        template="Create a job posting for a {job} position at "
                 "{company}. The post must attract {job}s with at least "
                 "{years_of_experience} years of experience, with "
                 "relevant experience in {area}. The job posting must "
                 "contain 'Job Title', 'About the Role', 'Responsibilities', "
                 "'Requirements' and 'Why Work at {company}'."
    )

    chat_prompt = ChatPromptTemplate.from_messages([
        system_message_prompt,
        human_message_prompt
    ])

    if streaming:
        chain = LLMChain(
            llm=ChatOpenAI(
                temperature=0,
                streaming=True,
                callbacks=[StreamingStdOutLimitedCallbackHandler()]
            ), prompt=chat_prompt)
    else:
        chain = LLMChain(llm=ChatOpenAI(temperature=0), prompt=chat_prompt)

    output = chain.predict(
        company=company,
        job=job,
        years_of_experience=years_of_experience,
        area=area
    )
    return JobDescriptionOutputParser().parse(output)
