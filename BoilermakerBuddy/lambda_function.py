# -*- coding: utf-8 -*-
import logging
import query_database
import entity_resolution
from pickle import TRUE
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import (
    Response, IntentRequest, DialogState, SlotConfirmationStatus, Slot)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Welcome to Boilermaker Buddy!"
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

#basic test case
class HelloWorldIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("HelloWorldIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Hello!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )

def getValueFromSlot(slotObj):
    n = slotObj.value
    return n

class AcademicCalendarIntentHandler(AbstractRequestHandler):
    #Handler for Academic Calendar Intent
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AcademicCalendarIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slotObj = handler_input.request_envelope.request.intent.slots["calevent"]
        acCalEventValue = getValueFromSlot(slotObj)
        acCalEvent = entity_resolution.resolveEvent(str(acCalEventValue)) # resolve to the "official" name for the event
        
        #get date from database, return date as speakable string
        dateString = query_database.queryDate(acCalEvent)
        if acCalEvent != None:
            speak_output = dateString + "."
            # speak_output = "You said " + acCalEvent
            return (
                handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
                )
        else:
            return (
                handler_input.response_builder
                .speak("event value is none").reponse
                )

class DiningMenuIntentHandler(AbstractRequestHandler):
    #Handler for Dining Menu Intent
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("DiningMenuIntent")(handler_input)
        
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # get slot values
        slotObj = handler_input.request_envelope.request.intent.slots["mealtime"]
        mealSlot = getValueFromSlot(slotObj)
        mealname = entity_resolution.resolveMealtime(mealSlot)

        slotObj = handler_input.request_envelope.request.intent.slots["diningCourts"]
        diningSlot = getValueFromSlot(slotObj)
        diningC = entity_resolution.resolveCourt(diningSlot)
        
        #return list of foods at mealtime at diningc
        foodList = query_database.queryMenu(diningC, mealname)
        if mealname != None and diningC != None:
            speak_output = "For " + str(mealname) + ", " + str(diningC) + " is serving " + foodList + "."
            return (
                handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
                )
        else:
            return (
                handler_input.response_builder
                .speak("Fail").reponse
                )

class BuildingIntentHandler(AbstractRequestHandler):
    #Handler for Dining Menu Intent
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("BuildingIntent")(handler_input)
        
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # get slot values
        slotObj = handler_input.request_envelope.request.intent.slots["buildingCodes"]
        building = getValueFromSlot(slotObj)
        
        #return list of foods at mealtime at diningc
        buildingCode = query_database.queryBuilding(building)
        if building == "BHEE":
            buildingCode = buildingCode + ", formerly known as Electrical Engineering"
        elif building == "PKRW":
            buildingCode = buildingCode + ", formerly known as Third Street Towers"
        elif building == "CREC":
            buildingCode = buildingCode + ", also known as the Co Rec"
        building = "BHEE"
        buildingDots = [char for char in building]
        buildingD = '.'.join(buildingDots)
        if building != None:
            speak_output = str(buildingD) + " is " + str(buildingCode) + "."
            return (
                handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
                )
        else:
            return (
                handler_input.response_builder
                .speak("Fail").reponse
                )

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = "Hmm, I'm not sure. You can say Hello or Help. What would you like to do?"
        reprompt = "I didn't catch that. What can I help you with?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "This is the catch all exception handler. There may have been a syntax or routing error."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelloWorldIntentHandler())
sb.add_request_handler(AcademicCalendarIntentHandler())
sb.add_request_handler(DiningMenuIntentHandler())
sb.add_request_handler(BuildingIntentHandler())
#sb.add_request_handler(TimeIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()