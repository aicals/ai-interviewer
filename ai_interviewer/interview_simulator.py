from .candidate import Candidate
from .interviewer import Interviewer
from .job_description import JobDescription
from .question_bank import QuestionType
from .util import print_limit


class InterviewSimulator:
    def __init__(
            self,
            interviewer: Interviewer,
            candidate: Candidate,
            job_description: JobDescription,
            min_follow_ups: int = 1
    ):
        self.interviewer = interviewer
        self.candidate = candidate
        self.job_description = job_description
        self.questions_with_follow_up = [
            QuestionType.CREATIVE_THINKING,
            QuestionType.CUSTOMER_SERVICE,
            QuestionType.FLEXIBILITY_ADAPTABILITY,
            QuestionType.INTERPERSONAL_EFFECTIVENESS,
            QuestionType.ORGANIZATIONAL_STEWARDSHIP,
            QuestionType.PERSONAL_MASTERY,
            QuestionType.SYSTEMS_THINKING,
            QuestionType.TECHNICAL_SKILLS,
        ]
        self.min_follow_ups = min_follow_ups
        self.full_transcript = ''
        self.short_transcript = ''

    @property
    def is_interview_over(self):
        return len(self.interviewer.interview_plan) == 0

    def start(self):
        # Keep asking questions until the interview is over
        while not self.is_interview_over:
            interviewer_message = self.interviewer.ask()

            # Before asking, we personalize behavioral questions
            if interviewer_message.question_type in self.questions_with_follow_up:
                interviewer_message.text = self.interviewer.personalize_the_question(
                    interviewer_message.text
                )

            # This means that the previous candidate reply contain a question
            # from the candidate. Reply it before finishing the interview
            if self.is_interview_over:
                answer = self.interviewer.answer_candidate(candidate_reply)
                interviewer_message.text = f'{answer}\n\n{interviewer_message.text}'

            self.log(
                f'Interviewer:\n{interviewer_message.text}\n\n',
                interviewer_message.question_type
            )

            # Make the candidate reply to the personalized question
            candidate_reply = self.candidate.reply(interviewer_message.text)
            self.log(
                f'{self.candidate.name}:\n{candidate_reply}\n\n',
                interviewer_message.question_type
            )

            # For the behavioral questions, let's ask follow-up questions
            if interviewer_message.question_type in self.questions_with_follow_up:
                # Let's define the number of follow-up questions to ask
                num_follow_ups = max(
                    self.min_follow_ups,
                    len(interviewer_message.follow_ups)
                )
                for i in range(num_follow_ups):
                    # If there are no follow-up questions in the bank, we
                    # generate them; otherwise, we customize them
                    if len(interviewer_message.follow_ups) == 0:
                        follow_up = self.interviewer.generate_followup_question(
                            raw_follow_up=None,
                            memory=self.candidate.memory
                        )
                    else:
                        follow_up = self.interviewer.generate_followup_question(
                            raw_follow_up=interviewer_message.follow_ups[i],
                            memory=self.candidate.memory
                        )

                    self.log(
                        f'Interviewer follow-up:\n{follow_up}\n\n',
                        interviewer_message.question_type
                    )

                    # Make the candidate reply to the personalized follow-up
                    candidate_reply = self.candidate.reply(follow_up)
                    self.log(
                        f'{self.candidate.name}:\n{candidate_reply}\n\n',
                        interviewer_message.question_type
                    )

    def log(
            self,
            message: str,
            question_type: QuestionType,
            verbose: bool = False
    ):
        self.full_transcript = f'{self.full_transcript}{message}'

        if question_type in self.questions_with_follow_up:
            self.short_transcript = f'{self.short_transcript}{message}'

        if verbose:
            print_limit(message)
