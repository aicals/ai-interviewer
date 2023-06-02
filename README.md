# How to make an AI assistant to automate job interviews
## Creating an AI agent to conduct structured behavioral interviews

Hiring is the single most important people activity in any organization. Any outstanding organization spends a great amount of energy in attracting, assessing and cultivating new hires. However, this process is painful and very time-consuming. **Can we use AI to help in this process?**

This tutorial aims to create an AI agent to conduct a structured behavioral interview.
Specifically, the agent will be able to:

- Ask general questions about a candidate's main experiences;
- Ask follow-up questions to gather detailed information about the candidate;
- Summarize the interview's findings.

We will follow the blueprint contained in the amazing [Work Rules](https://www.workrules.net/) from Laszlo Bock: the book reveals insightful lessons that Google learned through decades of experience in its quest to find & hire great talent.

To read the full tutorial, please go to [https://codebook.ai/articles/how-to-make-an-ai-assistant-to-automate-job-interviews](https://codebook.ai/articles/how-to-make-an-ai-assistant-to-automate-job-interviews).

To run it, just execute:
```bash
docker build -t ai_interviewer .
docker run --env-file=.env ai_interviewer
```

It's important to have an `.env` file with the following variables:
```bash
OPENAI_API_KEY=sk-your-openai-api-key
```
