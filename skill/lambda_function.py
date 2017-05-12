from mijnahlib import Server as AH
username = "yourAHusername"
password = "yourAHpassword"
ah = AH(username, password)

def lambda_handler(event, context):
    if (event["session"]["application"]["applicationId"] !=
            "amzn1.ask.skill.xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"):
        raise ValueError("Invalid Application ID")
    
    if event["session"]["new"]:
        on_session_started({"requestId": event["request"]["requestId"]}, event["session"])

    if event["request"]["type"] == "LaunchRequest":
        return on_launch(event["request"], event["session"])
    elif event["request"]["type"] == "IntentRequest":
        return on_intent(event["request"], event["session"])
    elif event["request"]["type"] == "SessionEndedRequest":
        return on_session_ended(event["request"], event["session"])

def on_session_started(session_started_request, session):
    print "Starting new session."

def on_launch(launch_request, session):
    return get_welcome_response()

def on_intent(intent_request, session):
    intent = intent_request["intent"]
    intent_name = intent_request["intent"]["name"]

    if intent_name == "GetList":
        return get_list()
    elif intent_name == "AddToList":
        return add_to_list(intent)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")

def on_session_ended(session_ended_request, session):
    print "Ending session."
    # Cleanup goes here...

def handle_session_end_request():
    card_title = "Appie - Thanks"
    speech_output = "Thank you for using the Appie skill.  See you next time!"
    should_end_session = True

    return build_response({}, build_speechlet_response(card_title, speech_output, None, should_end_session))

def get_welcome_response():
    session_attributes = {}
    card_title = "Appie by Albert Heijn"
    speech_output = "Welcome to the Alexa Appie skill. " \
                    "You can ask me to read your grocery list or add items to it"
    reprompt_text = "Please ask me to add an item to your grocery list, " \
                    "for example: Put milk on my list."
    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def add_to_list(intent):
    session_attributes = {}
    speech_output = "I was unable to understand what you would like me to add. Please try again."
    reprompt_text = "I was unable to understand what you would like me to add. Please try again."
    card_title = "Appie - Shopping list"
    should_end_session = True

    if "value" in intent["slots"]["grocery"]:
        item     = intent["slots"]["grocery"]["value"]
        product_id = get_product_id(item.lower())
    
        if product_id == item.lower():
            success = ah.shopping_cart.add_item_by_description(product_id, 1)
        else:
            success = ah.shopping_cart.add_item_by_id(product_id)

        if success == True:
            speech_output = product_id + " was added to your shopping list."
            reprompt_text = ""  

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_list():
    session_attributes = {}
    speech_output = "There was a problem getting your list."
    card_title = "Appie - Shopping list"
    should_end_session = False
    reprompt_text = ""

    s_list = ah.shopping_cart.contents

    n_items = len(s_list)
    n_count = 0
    
    if n_items > 0:
        speech_output = "I've found " + str(n_items) + " items on your shopping list: "

        for item in s_list:
            if item.quantity > 1:
                myitem = str(item.quantity) + " units of " + item.description
            else:
                myitem = item.description

            if item.has_discount:
                myitem += ". This item is in The Bonus!"

            speech_output += myitem

            if n_count == (n_items - 1):
                speech_output += ". Say: Add and then the name of a product, to add it to the list."
            elif n_count == (n_items - 2):
                speech_output += " and "
            else:
                speech_output += ", "

            n_count = n_count + 1
    else:
        speech_output = "You don't have any items on your list. Say: Add and then the name of a product, to add it to the list."

    print("Shopping list ready")

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_product_id(product_name):
    return {
        "milk": "wi200486",
        "dessert": "wi212524",
        }.get(product_name, product_name)

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        "outputSpeech": {
            "type": "PlainText",
            "text": output
        },
        "card": {
            "type": "Simple",
            "title": title,
            "content": output
        },
        "reprompt": {
            "outputSpeech": {
                "type": "PlainText",
                "text": reprompt_text
            }
        },
        "shouldEndSession": should_end_session
    }

def build_response(session_attributes, speechlet_response):
    return {
        "version": "1.0",
        "sessionAttributes": session_attributes,
        "response": speechlet_response
    }
