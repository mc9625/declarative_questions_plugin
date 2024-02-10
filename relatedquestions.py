from cat.mad_hatter.decorators import tool, hook, plugin
from pydantic import BaseModel
from datetime import datetime, date

class MySettings(BaseModel):
    threshold_declarative_memories: float = 0.82
    quick_no_reply_string : str = "Non parlo di questi argomenti."
    number_of_related_questions: int = 4
    


@plugin
def settings_schema():
    return MySettings.schema()

is_a_question = False
declarative_memories_str = ""
message = ""

@hook
def before_cat_sends_message(final_output, cat):
    global related_questions
    setting = cat.mad_hatter.plugins["declarative_questions_plugin"].load_settings()
    if is_a_question and len(declarative_memories_str) > 0:
            related_questions = str(cat.llm("starting from the message " + message + " write 4 related questions considering this context: " + declarative_memories_str + " Return the questions always in Italian and in a json format {\"questions\":[]}."))
            final_output["relatedquestions"] = related_questions
            
    # Return the modified final output
    return final_output
     
@hook
def after_cat_recalls_memories(cat):
    global declarative_memories_str
    declarative_memories_str = ""
    memories = cat.working_memory["declarative_memories"]
    for item in memories:
        if len(item) > 0:
            memory = item[0]
            score = item[1]
            print(f"Memoria: {memory.page_content}")
            print(f"Score: {score}")
            #add each item to the string
            if score > 0.82:
                declarative_memories_str += memory.page_content + " "

@hook
def agent_fast_reply(fast_reply, cat):
    setting = cat.mad_hatter.plugins["declarative_questions_plugin"].load_settings()
    n_declarative_mempries = len(cat.working_memory["declarative_memories"])
    
    if n_declarative_mempries == 0:
        fast_reply["output"]= setting["quick_no_reply_string"]
        return fast_reply
    
    return fast_reply

@hook
def before_cat_recalls_declarative_memories(config,cat):
    setting = cat.mad_hatter.plugins["declarative_questions_plugin"].load_settings()
    config["threshold"] = setting["threshold_declarative_memories"]
    return config

@hook
def before_cat_reads_message(user_message_json: dict, cat):
    global is_a_question
    global message
    message = user_message_json["text"]

    if message.endswith("?"):
        is_a_question = True
        print("The message is a question")
    else:
        is_a_question = False
        print("The message is not a question")