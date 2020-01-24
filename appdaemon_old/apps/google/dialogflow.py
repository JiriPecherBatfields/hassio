"""App for google flow.

This application supports the google flow with the following use-cases:
- Reads relevat temperatures in house
- car heater
  - Sets time
  - Turn on/off

"""
from enum import Enum
from typing import Tuple
import re

from globals import HouseModes
import appdaemon.plugins.hass.hassapi as hass

class Intent(Enum):
    """Provide enum for supported intents."""
    TEMPERATURE = 'temperature'
    CAR_HEATER_TIME = 'car_heater_time'
    HOUSE_STATUS = 'house_status'
    TURN_ON = 'turn_on'
    TURN_OFF = 'turn_off'

class DialogFlow(hass.Hass):
    """Proved dialog flow use-cases."""
    def initialize(self) -> None:
        self._temperatur_sensorer = self.args.get('temperatur', {})
        self._heater_switch = self.args.get('heater_switch', {})
        self._rooms = self.args.get('rooms', {})
        self._tv = self.args.get('tv', {})
 
        self.register_endpoint(self.__api_call, 'dialogflow')

    def __api_call(self, data: dict) -> Tuple[dict, int]:
        """Define endpoint for google dialog flow api to call"""
        intent = dlgflow_get_intent(data)
        self.log("INTENT : {}".format(intent))
     
        if intent is None:
            self.log("DialogFlow error encountered: Result is empty")
            return "", 201
        
        response = dlgflow_response(self.__respond_intent(intent, data))
        return response, 200

    def __respond_intent(self, intent: str, data: dict) -> str:
        """Choose the correct action depedning on intent type."""
        if intent == Intent.TEMPERATURE.value:
            return self.__respond_temperature(data)
        elif  intent == Intent.CAR_HEATER_TIME.value:
            return self.__respond_car_heater_set_time(data)
        elif  intent == Intent.HOUSE_STATUS.value:
            return self.__respond_house_status(data)
        elif  intent == Intent.TURN_ON.value:
            return self.__respond_turn_on(data)
        elif  intent == Intent.TURN_OFF.value:
            return self.__respond_turn_off(data)
        else:
            return "<p><s>Känner inte igen kommandot.</s><s>Snälla försök igen.</s></p>"

    def __respond_turn_on(self, data: dict) -> str:
        """Turn on device."""
        device = dlgflow_get_parameter(data, 'devices')
        if not device:
            return "Vad vill du slå på?"
        device = device.replace(" ", "-")
        self.log("Turn on device {}".format(device))
        
        if device == "Tv":
            self.log_to_logbook('DialogFlow', "Slår på TV {}".format(self.friendly_name(self._tv)))
            self.turn_on(entity_id=self._tv)
        elif device == "motorvärmare":
            self.log_to_logbook('DialogFlow', "Slår på motorvärmaren {}".format(self.friendly_name(self._heater_switch)))
            self.turn_on(entity_id=self._heater_switch)
        elif device in self._rooms:
            self.log_to_logbook('DialogFlow', "Slår på {}".format(self.friendly_name(self._rooms[device])))
            self.turn_on(entity_id=self._rooms[device])
        else:
            return "Vet inte hur jag slår på {}".format(device)
        
        return "Slår på {}".format(device)

    def __respond_turn_off(self, data: dict) -> str:
        """Turn off device."""
        device = dlgflow_get_parameter(data, 'devices')
        if not device:
            return "Vad vill du stänga av?"
        device = device.replace(" ", "-")
        self.log("Turn off device {}".format(device))
        
        if device == "Tv":
            self.log_to_logbook('DialogFlow', "Slår av TV {}".format(self.friendly_name(self._tv)))
            self.turn_off(entity_id=self._tv)
        elif device == "motorvärmare":
            self.log_to_logbook('DialogFlow', "Slår av motorvärmaren {}".format(self.friendly_name(self._heater_switch)))
            self.turn_off(entity_id=self._heater_switch)
        elif device in self._rooms:
            self.log_to_logbook('DialogFlow', "Slår av {}".format(self.friendly_name(self._rooms[device])))
            self.turn_off(entity_id=self._rooms[device])
        else:
            return "Vet inte hur jag stänger av {}".format(device)
        
        return "Stänger av {}".format(device)

    def __respond_temperature(self, data: dict) -> str:
        """Respond with temperatures around the house."""
        temp_outside = round(float(self.get_state(self._temperatur_sensorer['ute'])))
        temp_inside = round(float(self.get_state(self._temperatur_sensorer['inne'])))
        return "<p><s>Temperaturen ute är {} grader.</s><s>Innetemperaturen är {} grader.</s></p>".format(temp_outside, temp_inside)

    def __respond_car_heater_set_time(self, data: dict) -> str:
        """Sets time for car heater depending on parameter."""
        date_time_parameter = dlgflow_get_parameter(data, 'date-time')
        if date_time_parameter:
            self.log("TIME: {}".format(date_time_parameter['date_time']))
            time = self.convert_utc(date_time_parameter['date_time'])
            self.set_state(entity_id='input_number.car_heater_dep_time_hour', state=time.hour)
            self.set_state(entity_id='input_number.car_heater_dep_time_minutes', state=time.minute)
            return "Sätter motorvärmare till tiden <say-as interpret-as=\"time\" format=\"hms24\">{}:{}</say-as>".format(time.hour, time.minute)
        else:
            return "<p><s>Förstår inte tiden.</s><s>Försök igen. </s></p>"

    def __respond_car_heater_status(self, data: dict) -> str:
        """Turn on/off heater."""
        command = dlgflow_get_parameter(data, 'command')
        if command:
            if command == 'Stäng av':
                self.turn_off(entity_id=self._heater_switch)
                return "Stänger av motorvärmaren."
            elif command == 'Sätt på':
                self.turn_on(entity_id=self._heater_switch)
                return "Sätter på motorvärmaren i tre timmar."
        else:
            return "<p><s>Förstår inte kommandot.</s><s>Försök igen. </s></p>"

    def __respond_house_status(self, data: dict) -> str:
        command = dlgflow_get_parameter(data, 'house_status')
        if command:
            if command == 'god natt':
                self.set_state(entity_id='input_select.house_mode_select', state=HouseModes.night.value)
                return "Sov gott"
            elif command == 'god morgon':
                self.set_state(entity_id='input_select.house_mode_select', state=HouseModes.morning.value)
                return "God morgon."
            elif command == 'god kväll':
                self.set_state(entity_id='input_select.house_mode_select', state=HouseModes.evening.value)
                return "God kväll."
            elif command == 'god dag':
                self.set_state(entity_id='input_select.house_mode_select', state=HouseModes.day.value)
                return "Goddag, ha det bra."
            else:
                return "<p><s>Förstår inte kommandot {} för husstatus.</s><s>Försök igen. </s></p>".format(command)
        else:
            return "<p><s>Förstår inte kommandot för husstatus.</s><s>Försök igen. </s></p>"

        

def clean_tags(text_with_tags):
    """Clean all tags from the ssml."""
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', text_with_tags)
    return cleantext

def dlgflow_get_parameter(data, parameter: str):
    """Return parameter from webhook api v2.0"""
    return data['queryResult']['parameters'].get(parameter, None)

def dlgflow_get_intent(data) -> str:
    """Return the intent from webhook api v2.0"""
    return data['queryResult']['action']

def dlgflow_response(message):
    """Return dialogflow fullfilment response v2.0 API using ssml.
    
    ssml is a way to get more natural sounding voice. See
    https://developers.google.com/actions/reference/ssml
    to view what it can do in detail.
    """
    return \
    {
        'fulfillmentText': clean_tags(message),
        'fulfillmentMessages': [
        {
            'platform': "ACTIONS_ON_GOOGLE",
            'simpleResponses': {
                'simpleResponses': [
                    {   
                        'ssml': "<speak>{}</speak>".format(message)
                    }
                ]     
            }   
            
        
        }
        ],
        "source": "appdaemon"
    }