import json

from .candidate import Candidate
from .interview_simulator import InterviewSimulator
from .interviewer import Interviewer
from .job_description import create_job_description, JobDescription
from .util import BASE_DIR, print_limit


def main(company, job, area, years_of_experience_job, candidate_name,
         years_of_experience_candidate, work_experiences, data_dir,
         force_reload):

    # Create job description
    print('Creating job description...\n')

    job_description_file = data_dir/'job_description.json'

    if not job_description_file.exists() or force_reload:
        job_description = create_job_description(
            company=company,
            job=job,
            years_of_experience=years_of_experience_job,
            area=area
        )
        job_description.save(job_description_file)
    else:
        with job_description_file.open('r') as file:
            job_description = JobDescription(**json.load(file))

    print_limit(job_description.text)
    print('\n\n' + '*' * 80 + '\n')

    # Create candidate
    print('Creating the candidate...\n')

    filename = candidate_name.lower().replace(' ', '_')
    candidate_file = data_dir/f'{filename}.json'

    if not candidate_file.exists() or force_reload:
        candidate = Candidate(
            name=candidate_name,
            job=job,
            years_of_experience=years_of_experience_candidate,
            area=area,
            requirements=job_description.requirements,
            work_experiences=work_experiences,
            company=company
        )
        candidate.save(candidate_file)
    else:
        with candidate_file.open('r') as file:
            candidate = Candidate(**json.load(file))

    print_limit(candidate.resume)
    print('\n\n' + '*' * 80 + '\n')

    # Simulate the interview
    print('Simulating the interview...\n')

    full_transcript_file = data_dir/"full_transcript.txt"
    short_transcript_file = data_dir/"short_transcript.txt"

    if not short_transcript_file.exists() or force_reload:
        interviewer = Interviewer(
            candidate_name=candidate_name,
            job=job,
            area=area,
            company=company,
        )
        simulator = InterviewSimulator(
            interviewer=interviewer,
            candidate=candidate,
            job_description=job_description
        )
        simulator.start()

        with full_transcript_file.open('w') as file:
            file.write(simulator.full_transcript)
        with short_transcript_file.open('w') as file:
            file.write(simulator.short_transcript)
        full_transcript = simulator.full_transcript
        short_transcript = simulator.short_transcript
    else:
        with full_transcript_file.open('r') as file:
            full_transcript = file.read()
        with short_transcript_file.open('r') as file:
            short_transcript = file.read()
        print_limit(full_transcript)

    print('\n\n' + '*' * 80 + '\n')

    # Summarize the interview
    print('Summarizing the interview...\n')

    summary_file = data_dir/'summary.txt'

    if not summary_file.exists() or force_reload:
        interviewer = Interviewer(
            candidate_name=candidate_name,
            job=job,
            area=area,
            company=company,
        )
        summary = interviewer.summarize_interview(short_transcript)
        with summary_file.open('w') as file:
            file.write(summary)
    else:
        with summary_file.open('r') as file:
            summary = file.read()
        print_limit(summary)

    print('\n\n' + '*' * 80 + '\n')
