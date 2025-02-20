import logging
import requests
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.dispatch_components import AbstractResponseInterceptor
from ask_sdk_core.dispatch_components import AbstractRequestInterceptor
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.response_helper import get_plain_text_response
import ask_sdk_core.utils as ask_utils
from controllers.device_controller import DeviceController

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        speak_output = "Welcome to Alexa Smart Home. You can ask me to play a song or to control your smart devices."
        reprompt_text = "You can ask me to play a song or to control your smart devices."
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt_text)
                .response
        )

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = "You can ask me to play a song or to control your smart devices."
        reprompt_text = "You can ask me to play a song or to control your smart devices."
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt_text)
                .response
        )

class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        speak_output = "Goodbye!"
        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Fallback Intent Handler."""
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("In FallbackIntentHandler")
        speech = "Hmm, I'm not sure. You can say Hello or Help. What would you like to do?"
        reprompt = "I didn't catch that. What can I help you with?"
        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        return handler_input.response_builder

class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch all exception handler."""
    def can_handle(self, handler_input, exception):
        return True

    def handle(self, handler_input, exception):
        logger.error(exception, exc_info=True)
        speech = "Sorry, there was some problem. Please try again!!"
        return handler_input.response_builder.speak(speech).ask(speech).response

class PlaySongIntentHandler(AbstractRequestHandler):
    """Handler for playing a song"""
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("PlaySongIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = "Playing a song on your smart speaker."
        return (
            handler_input.response_builder
                .speak(speak_output)
                .set_should_end_session(True)
                .response
        )

class ControlDeviceIntentHandler(AbstractRequestHandler):
    """Handler for controlling smart devices"""
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("ControlDeviceIntent")(handler_input)

    def handle(self, handler_input):
        device_controller = DeviceController()
        device_action = device_controller.control_device()  # Implement this method in device_controller.py
        speak_output = f"Controlling your smart devices: {device_action}."
        return (
            handler_input.response_builder
                .speak(speak_output)
                .set_should_end_session(True)
                .response
        )

sb = SkillBuilder()
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(PlaySongIntentHandler())
sb.add_request_handler(ControlDeviceIntentHandler())
sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
# End snippet
```
