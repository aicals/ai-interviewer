import argparse
from . import main
from .util import BASE_DIR


parser = argparse.ArgumentParser(description='AI Interviewer agent')
parser.add_argument(
    '--company',
    type=str,
    default='OpenAI',
    help='Company name')
parser.add_argument(
    '--job',
    type=str,
    default='software engineer',
    help='Job position')
parser.add_argument(
    '--area',
    type=str,
    default='Machine Learning and Artificial Intelligence',
    help='Area of expertise')
parser.add_argument(
    '--years_of_experience_job',
    type=int,
    default=5,
    help='Years of experience in the job')
parser.add_argument(
    '--candidate_name',
    type=str,
    default='Alan Bradley',
    help='Candidate name')
parser.add_argument(
    '--years_of_experience_candidate',
    type=int,
    default=7,
    help='Years of experience of the candidate')
parser.add_argument(
    '--work_experiences',
    type=int,
    default=3,
    help='Number of work experiences')
parser.add_argument(
    '--data_dir',
    type=str,
    default=BASE_DIR/'data',
    help='Data directory path')
parser.add_argument(
    '-f', '--force-reload',
    action='store_true',
    help='Force reload data')

args = parser.parse_args()
main(**vars(args))
