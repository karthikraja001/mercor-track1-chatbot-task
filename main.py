from textbase import bot, Message
from textbase.models import OpenAI
from typing import List
import json
import prompts
import linkedin

OpenAI.api_key = "YOUR-OPENAI-KEY"

SYSTEM_PROMPT = """You are chatting with an Job Searching Bot. There are no specific prefixes for responses, so you can ask or talk about anything you like.
The AI will respond in a natural, conversational manner. Feel free to start the conversation with any question or topic, and let's have a
pleasant chat!
"""

SYSTEM_PROMPT_JOB = """You are an expert in knowing people's job requirements. Now you will get the user's input sentence
and find the keywords such as
{
    queryType: Job Search
    jobRole: <user's job role specified>
    jobLocation: <location specified>
    jobPositionType: <specified job's position type, should be in a list format. select only one of these (internship, entry level, associate, mid senior, director). If no keywords found, fill with default value internship, entry level>
}.
If the sentence is not based on job search query, check for if the sentence is about knowing about the company. So, if the sentence
is about getting to know about a company, extract the keywords such as
{
    queryType: Company Search
    company: <user's specified company name>
}.
I only want you to extract these data fields from the sentence. Do not ask any kind of questions and do not reply with other than
the json format. Very very important, do not change the key value of the json. It should be in the same format. Do not make them in
to lower case or upper case.
"""

@bot()
def on_message(message_history: List[Message], state: dict = None):
    print(message_history[-1])
    if message_history[-1]['content'][0]['value'] == "start":
        bot_response = OpenAI.generate(
            system_prompt=prompts.SYSTEM_PROMPT,
            message_history=message_history,
            model="gpt-3.5-turbo-16k",
        )
        reply = "Hello! I'm your Personal Job Finder 😎✨ AI. Let's find you the perfect jobs ! What role do you prefer? Eg.(Software Developer, Business Analyst, etc)"
    else:
        temp = []
        temp.append(message_history[1])
        for i in message_history:
            if i['role'] == 'user': temp.append(i)
        message_history 
        bot_response = OpenAI.generate(
            system_prompt=SYSTEM_PROMPT_JOB,
            message_history=temp,
            model="gpt-3.5-turbo-16k",
        )
        print("bot_response ", bot_response)
        try:
            resp = json.loads(bot_response)
            print(resp)
            if resp['queryType'] == 'Job Search':
                role = ""
                experience = []
                location = ""
                print(resp['jobRole'])
                print(resp['jobPositionType'])
                try: role = resp['jobRole']
                except: pass

                try: experience = resp['jobPositionType']
                except: pass

                try: location = resp['jobLocation']
                except: pass
                bot_response = linkedin.getJobs(experience=experience, location=location, role=role)
                print("LINKEDIN")
                reply = """"""    
                if bot_response["code"] != 200: 
                    reply = "Sorry. Some Internal error in the engine. Please try again."
                    print("Failed")
                else:
                    print(role)
                    print(location)
                    reply = "Your Job Recommendation for " + role
                    reply = (reply + " In " + location) if location != "" else reply
                    reply = (reply + " As " + ' ,'.join(experience)) if experience != [] else reply
                    for i in bot_response['message']:
                        print(i['Role'])
                        print(i['Company'])
                        print(i['location'])
                        print(i['url'])
                        temp = f'''
        Role:\t\t {i['Role']}
        Company:\t {i['Company']}
        Location:\t {i['location']}
        Apply:\t\t {i['url']}
                        
                        '''
                        print(temp)
                        reply += temp
            else:
                data = linkedin.getCompanyDetails(resp['company'])
                if data['code'] != 200: reply = "Internal Server Error. Please try again."
                else:
                    reply = f"""
    Name: {resp['company']}
    About: {data['description']}
    Works on: {data['worksOn']}
"""
                pass

        except:
            reply = bot_response
    response = {
        "data": {
            "messages": [
                {
                    "data_type": "STRING",
                    "value": reply
                }
            ],
            "state": state
        },
        "errors": [
            {
                "message": ""
            }
        ]
    }

    return {
        "status_code": 200,
        "response": response
    }