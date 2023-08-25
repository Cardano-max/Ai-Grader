import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def parse_checks_list(my_list):
  final = ""
  if len(my_list) == 1:
    final = my_list[0].title()
  elif len(my_list) == 2:
    final = f'{my_list[0].title()} and {my_list[1].title()}'
  elif len(my_list) == 3:
    final = f'{my_list[0].title()}, {my_list[1].title()} and {my_list[0].title()}'
  return final


def get_assessment(feedback, context_country, context_year_level, context_subject,
                context_curriculum, criteria, checks, work_sample, model, temperature, 
                max_tokens, frequency_penalty, top_p
                   ):
    
    feedback_length = '''It should start with one - two sentences on what was done well. 
            It should then include one sentence on a suggested improvement.'''
    if feedback=="detailed":
        feedback_length = '''It should start with three to four sentences on what was done well. 
            It should then include three difference suggested improvements.'''


    gpt_prompt = '''You are an expert teacher in {context_country} of grade {context_year_level} and 
            subject {context_subject} under the {context_curriculum}. 
            Assesses students for the following criteria, identified within the triple hyphen — {criteria} —
            Provide some feedback that should match the following layout. 
            The response should be conversational in nature. 
            {feedback_length} 
            Include a comment on {checks}

            The student work is below, the start and end is identified by triple backdash ```  {work_sample} ```
        '''.format(
            context_country=context_country,
            context_year_level=context_year_level,
            context_subject=context_subject,
            context_curriculum=context_curriculum,
            criteria=criteria,
            checks=parse_checks_list(checks),
            feedback_length=feedback_length,
            work_sample=work_sample
        )


    # Use the openai `Completion` class to generate text using the GPT-3 model
    if model in ['gpt-4', 'gpt-4-32k']:
        message=[{"role": "user", "content": gpt_prompt}]
        completion = openai.ChatCompletion.create(
            model=model,
            messages = message,
            temperature=temperature,
            max_tokens=max_tokens,
            frequency_penalty=frequency_penalty
        )
        response = completion.choices[0].message.content
    else:
        completion = openai.Completion.create(
            engine="text-davinci-002" if model=='gpt-3' else "text-davinci-003",
            prompt=gpt_prompt,
            max_tokens=max_tokens,
            n=1,
            temperature=temperature,
            top_p=top_p
        )
        # Return the generated text as a response to the request
        response = completion.choices[0].text
            
    return completion, response

