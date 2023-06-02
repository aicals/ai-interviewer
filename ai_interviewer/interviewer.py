from types import MappingProxyType

from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import BaseMemory

from .question_bank import sample_questions, QuestionType, Question
from .util import print_limit


class Interviewer:
    def __init__(
            self,
            candidate_name: str,
            job: str,
            area: str,
            company: str,
            questions_to_ask: dict = MappingProxyType({
                QuestionType.CREATIVE_THINKING: 1,
                QuestionType.CUSTOMER_SERVICE: 0,
                QuestionType.FLEXIBILITY_ADAPTABILITY: 1,
                QuestionType.INTERPERSONAL_EFFECTIVENESS: 1,
                QuestionType.ORGANIZATIONAL_STEWARDSHIP: 1,
                QuestionType.PERSONAL_MASTERY: 1,
                QuestionType.SYSTEMS_THINKING: 1,
                QuestionType.TECHNICAL_SKILLS: 1
            }),
    ):
        self.candidate_name = candidate_name
        self.first_name = candidate_name.split(' ')[0]
        self.job = job,
        self.area = area
        self.company = company

        ice_breakers = [
            f"Hi! Welcome, {self.first_name}!",
            "Tell me a little bit about yourself."
        ]
        ice_breakers = [Question(text=text, question_type=QuestionType.ICE_BREAKERS)
                        for text in ice_breakers]

        wrap_up = [
            "Do you have any questions for me regarding our company or the "
            "position?",
            f"All right! {self.first_name}, thank you so much for your time! "
            "Our team will be in touch with a decision and next steps over the "
            "upcoming days. If you have any questions, please do not hesitate "
            "in reaching out over my email. Thank you, and have a great day!"
        ]
        wrap_up = [Question(text=text, question_type=QuestionType.WRAP_UP)
                   for text in wrap_up]

        self.interview_plan = ice_breakers
        for question_type, num_questions in questions_to_ask.items():
            self.interview_plan += sample_questions(question_type, num_questions)

        self.interview_plan += wrap_up

    def ask(self):
        if len(self.interview_plan) > 0:
            return self.interview_plan.pop(0)
        else:
            return None

    def personalize_the_question(self, question: str) -> str:
        system_message_prompt = SystemMessagePromptTemplate.from_template(
            template="You are an interviewer working at {company}. You are "
                     "interviewing {name} for a {job} position. This is "
                     "an ongoing interview. You are in the middle of it.\n"
                     "Rewrite the question below, considering this. Do not "
                     "change the meaning of the question. You may or may not "
                     "mention the candidate's name. Make it friendly.\n\n"
        )
        human_message_prompt = HumanMessagePromptTemplate.from_template(
            template="Question: {question}"
        )
        chat_prompt = ChatPromptTemplate.from_messages([
            system_message_prompt,
            human_message_prompt
        ])

        chain = LLMChain(llm=ChatOpenAI(temperature=0.5), prompt=chat_prompt)
        output = chain.predict(
            company=self.company,
            job=self.job,
            name=self.candidate_name,
            question=question
        )
        return output

    def generate_followup_question(
            self,
            raw_follow_up: str | None,
            memory: BaseMemory | str,
    ) -> str:
        if isinstance(memory, BaseMemory):
            history = memory.buffer
        elif isinstance(memory, str):
            history = memory

        if raw_follow_up == '' or raw_follow_up is None:
            system_message_prompt = SystemMessagePromptTemplate.from_template(
                template="You are an interviewer working at {company}. You are "
                         "interviewing {name} for a {job} position.\n"
                         "You must ask a follow-up question related to the "
                         "conversation so far. The follow-up question must be "
                         "related to {name}'s last answer.\n"
            )
        else:
            system_message_prompt = SystemMessagePromptTemplate.from_template(
                template="You are an interviewer working at {company}. You are "
                         "interviewing {name} for a {job} position.\n"
                         "You must ask a follow-up question related to the "
                         "conversation so far. The follow-up question must be "
                         "related to {name}'s last answer.\n"
                         "Use this follow-up question idea, and adapt it to "
                         "the context of the current interview.\n\n"
                         "Follow-up question idea:\n{raw_follow_up}\n"
            )

        human_message_prompt = HumanMessagePromptTemplate.from_template(
            template="Conversation so far:\n{history}"
        )
        chat_prompt = ChatPromptTemplate.from_messages([
            system_message_prompt,
            human_message_prompt
        ])

        chain = LLMChain(llm=ChatOpenAI(temperature=0.5), prompt=chat_prompt)
        output = chain.predict(
            company=self.company,
            job=self.job,
            name=self.candidate_name,
            history=history,
            raw_follow_up=raw_follow_up
        )
        return output

    def answer_candidate(self, question: str) -> str:
        system_message_prompt = SystemMessagePromptTemplate.from_template(
            template="You are an interviewer working at {company}. You are "
                     "interviewing {name} for a {job} position.\n"
                     "Answer the questions that the candidate is asking."
                     "Be creative. Give a detailed answer.\n\n"
        )
        human_message_prompt = HumanMessagePromptTemplate.from_template(
            template="{name}: {question}\nInterviewer:"
        )
        chat_prompt = ChatPromptTemplate.from_messages([
            system_message_prompt,
            human_message_prompt
        ])

        chain = LLMChain(llm=ChatOpenAI(temperature=0.5), prompt=chat_prompt)
        output = chain.predict(
            company=self.company,
            job=self.job,
            name=self.candidate_name,
            question=question
        )
        return output

    def summarize_interview(
            self,
            transcript: str,
            num_words: int = 200,
            verbose: bool = True
    ) -> str:
        summary = ''

        system_message_prompt = SystemMessagePromptTemplate.from_template(
            template="You are an interviewer working at {company}. You just "
                     "interviewed {name} for a {job} position.\n"
                     "You have the interview transcript.\n"
                     "Your objective is to summarize the interview, "
                     "answering questions about it.\n"
                     "Your answers must only be based on the interview "
                     "transcript. If you cannot answer the questions, "
                     "just say that there is not enough evidence in the "
                     "interview to assertively answer the questions.\n"
                     "Your answer must be no longer than 1 paragraph.\n\n"
        )
        human_message_prompt = HumanMessagePromptTemplate.from_template(
            template="Interview transcript:\n\n{transcript}\n\n\n"
                     "Based on the interview transcript, answer the following "
                     "question:\n{question}\n{final_instruction}"
        )
        chat_prompt = ChatPromptTemplate.from_messages([
            system_message_prompt,
            human_message_prompt
        ])

        chain = LLMChain(llm=ChatOpenAI(temperature=0.5), prompt=chat_prompt)

        final_instruction = (
            'Please support your answers with specific examples provided by '
            'the candidate in the interview transcript. To support your '
            'answers with specific examples, mention the companies and the '
            'projects that he/she worked on and all details. Be critical.\n'
            'Your answer must be no longer than 1 paragraph.'
        )

        criteria_and_questions = {
            'General cognitive ability': [
                'Please describe how well or not the candidate '
                'demonstrated general cognitive ability. ',
                'Describe how well or not the candidate is a good problem '
                'solver.',
                'Describe how well the candidate can learn and adapt to '
                'situations. '
            ],
            'Leadership': [
                'Please describe how well or not the candidate demonstrated '
                'leadership. ',
                'Describe how well or not the candidate demonstrated the '
                'ability to set a vision, energize the team to accomplish '
                'that vision, and enable the team by removing obstacles.',
                'Describe how well or not the candidate collaborates well in '
                'a team. '
            ],
            'Cultural fit': [
                'Please describe how well or not the candidate demonstrated '
                'intellectual humility. ',
                'Describe how well or not the candidate demonstrated '
                'conscientiousness and acted as an owner. ',
                'Describe how well or not the candidate demonstrated comfort '
                'with ambiguity. '
            ],
            'Role related knowledge': [
                'Please describe how well or not the candidate demonstrated '
                '{job} skills, specifically in the area of {area}. '
            ]
        }

        for criteria, questions in criteria_and_questions.items():
            summary = f'{summary}{criteria}:\n\n'
            if verbose:
                print_limit(f'{criteria}:\n\n')

            for question in questions:
                output = chain.predict(
                    company=self.company,
                    job=self.job,
                    area=self.area,
                    name=self.candidate_name,
                    transcript=transcript,
                    question=question,
                    num_words=num_words,
                    final_instruction=final_instruction
                ).strip()
                summary = f'{summary}{output}\n\n'
                if verbose:
                    print_limit(f'{output}\n\n')

            summary = f'{summary}\n'
            if verbose:
                print(' ')

        overall = self.overall_recommendation(summary)
        summary = f'Recommendation:\n\n{overall}\n\n\n{summary}'
        return summary

    def overall_recommendation(self, summary):
        system_message_prompt = SystemMessagePromptTemplate.from_template(
            template="You are an interviewer working at {company}. You just "
                     "interviewed {name} for a {job} position, to work with "
                     "{area}.\nYou have the interview summary.\n"
                     "Your objective is to generate 1 paragraph with an "
                     "overall recommendation of whether or not the candidate "
                     "should be hired. Your answer must be no longer than 1 "
                     "paragraph.\n\n"
        )
        human_message_prompt = HumanMessagePromptTemplate.from_template(
            template="Interview summary:\n\n{summary}\n\n\n"
                     "Based on the interview summary, please provide an "
                     "overall recommendation of whether or not the candidate "
                     "should be hired. Provide strengths and weaknesses in "
                     "your assessment. Be critical. Your answer must be no "
                     "longer than 1 paragraph."
        )
        chat_prompt = ChatPromptTemplate.from_messages([
            system_message_prompt,
            human_message_prompt
        ])

        chain = LLMChain(llm=ChatOpenAI(temperature=0.5), prompt=chat_prompt)
        output = chain.predict(
            company=self.company,
            job=self.job,
            area=self.area,
            name=self.candidate_name,
            summary=summary
        ).strip()
        return output
