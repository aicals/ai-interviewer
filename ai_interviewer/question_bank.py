from dataclasses import dataclass, field
from enum import Enum

import pandas as pd

from .util import BASE_DIR, split_punctuation

questions = pd.read_csv(
    BASE_DIR /'ai_interviewer'/'pbi_sample_questions.csv'
).fillna('')


class QuestionType(str, Enum):
    CREATIVE_THINKING = 'Creative Thinking'
    CUSTOMER_SERVICE = 'Customer Service'
    FLEXIBILITY_ADAPTABILITY = 'Flexibility/Adaptability'
    INTERPERSONAL_EFFECTIVENESS = 'Interpersonal Effectiveness'
    ORGANIZATIONAL_STEWARDSHIP = 'Organizational Stewardship'
    PERSONAL_MASTERY = 'Personal Mastery'
    SYSTEMS_THINKING = 'Systems Thinking'
    TECHNICAL_SKILLS = 'Technical Skills'

    ICE_BREAKERS = 'Ice breakers'
    WRAP_UP = 'Wrap up'


@dataclass
class Question:
    level: str = ''
    question_type: str = ''
    text: str = ''
    follow_ups: list = field(default_factory=lambda: [])
    is_streamed: bool = False


def sample_questions(
        question_type: QuestionType,
        num_questions: int = 1
) -> list[Question]:
    rows = questions[questions['Type'] == question_type].sample(num_questions)
    qs = []
    for index, row in rows.iterrows():
        qs.append(Question(
            level=row['Level'].strip(),
            question_type=row['Type'].strip(),
            text=row['Question'].strip(),
            follow_ups=split_punctuation(row['Follow-ups'])
        ))
    return qs
