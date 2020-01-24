from base import Base
from globals import GlobalEvents, HouseModes
from typing import Tuple, Union

"""
A class that are the base class of all rooms and areas where devices are present.

- Define ambient_lights and they will turn_off/turn_on depending on house state.
- Define motion sensors and nightlights and it will turn on at night when motion
  and turn off after a time without motion. Event EV_MOTION_DETECTED/EV_MOTION_OFF 
  will be sent with room and entity
- In the morning (default after 5am) the morning lights will turn on if it is still
  night mode (ie the sun is still down) 

Inherit from this class and override default beahviour for specific needs in specific rooms

"""


class Area(Base):

    def initialize(self) -> None:
        super().initialize()
        self._ambient_lights = self.args.get('ambient_ligts', {})
        self._morning_lights = self.args.get('morning_ligts', {})
        self._morning_time = self.parse_time(
            self.args.get('morning_time', '05:00:00'))
        self._day_time = self.parse_time(
            self.args.get('morning_time', '10:00:00'))
        self._morning_ligths_on = False
        self._night_lights = self.args.get('night_lights', {})
        self._motion_sensors = self.args.get('motion_sensors', {})
        self._light_switches = self.args.get('light_switches', {})
        self._ambient_light_settings = self.args.get(
            'ambient_light_settings', {})

        self._min_time_motion = int(
            self.properties.get('min_time_motion', 0))          # No default delay when no motion set
        self._min_time_nightlights = int(
            self.properties.get('min_time_nightlights', 120))   # 2 minutes default time before turn off night ligths

        self._ambient_light_brightness = self._ambient_light_settings.get(
            "brightness_pct", "25")
        self._ambient_light_transition = self._ambient_light_settings.get(
            "transition", "25")

        self.register_constraint("constraint_housemode")

        self.listen_event(
            self.__on_house_home_changed,
            GlobalEvents.EV_HOUSE_MODE_CHANGED.value)

        self.listen_event(
            self.__on_cmd_ambient_lights_on,
            GlobalEvents.CMD_AMBIENT_LIGHTS_ON.value)

        self.listen_event(
            self.__on_cmd_ambient_lights_off,
            GlobalEvents.CMD_AMBIENT_LIGHTS_OFF.value)

        self._night_light_timer_handle = None

        self.__init_motion_sensors()
        self.__init_light_switches()

    # Common area constraints 
    def constraint_housemode(self, mode:str) -> bool:
        if str == 'morning' and self.house_status == HouseModes.morning:
            return True
        elif str == 'day' and self.house_status == HouseModes.day:
            return True
        elif str == 'evening' and self.house_status == HouseModes.evening:
            return True
        elif str == 'night' and self.house_status == HouseModes.night:
            return True
        elif str == 'cleaning' and self.house_status == HouseModes.cleaning:
            return True
        return False

    def __init_motion_sensors(self)->None:
        for motion_sensor in self._motion_sensors:
            # listen to motion
            self.listen_state(
                self.__on_motion,
                motion_sensor,
                new='on',
                old='off')

            # listen to motion
            self.listen_state(
                self.__off_motion,
                motion_sensor,
                new='off',
                old='on',
                duration=self._min_time_motion)

    def __init_light_switches(self)->None:
        for light_switch in self._light_switches:
            # listen to motion
            self.listen_state(
                self.__on_lightswich_state_changed,
                light_switch)

    def motion_on_detected(self, entity: str)->None:
        """called when motion detected in area"""
        if self._morning_ligths_on is True:
            return

        if self.house_status.is_night():
            if self._day_time > self.time() > self._morning_time:
                self.log_to_logbook('Lights', "Tänder morgonlampor")
                for morning_light in self._morning_lights:
                    self.turn_on_device(morning_light,
                        brightness_pct='35', 
                        transition='0') 
                self._morning_ligths_on = True
                return                     
            if self._night_light_timer_handle is None: # We have no running timeout
                self.log_to_logbook('Lights', "Tänder nattlampor")
                for night_light in self._night_lights:
                    self.turn_on_device(night_light,
                        brightness_pct='35', 
                        transition='0')            
                self._night_light_timer_handle = self.run_in(self.__on_night_light_timer, self._min_time_nightlights)
            else: #We are in a timer, lets 
                self.cancel_timer(self._night_light_timer_handle)
                self._night_light_timer_handle = self.run_in(self.__on_night_light_timer, self._min_time_nightlights)

    def __on_night_light_timer(self, kwargs: dict) -> None:
        for night_light in self._night_lights:
          self.turn_off_device(night_light)

        self._night_light_timer_handle = None

    def motion_off_detected(self, entity: str)->None:
        """called when motion off in area"""
        # No base functionality for this

    def on_housemode_day(self, old: HouseModes) -> None:
        self.turn_off_ambient()

    def on_housemode_morning(self, old: HouseModes) -> None:
        self.turn_off_ambient()

    def on_housemode_evening(self, old: HouseModes) -> None:
        self.turn_on_ambient()

    def on_housemode_night(self, old: HouseModes) -> None:
        self.turn_off_ambient()

    def on_housemode_cleaning(self, old: HouseModes) -> None:
        self.turn_on_ambient('100', '0')

    def on_lightswich_state_changed(self, entity: str, old: str, new: str)->None:
        return

    def turn_on_ambient(self, brigtness: str=None,
                        transition: str=None)->None:
        self.log_to_logbook('Lights', "Tänder allmänljuset för {}".format(self._ambient_lights))
        # if not brigtness:
        #     brigtness = self._ambient_light_brightness
        # if not transition:
        #     transition = self._ambient_light_transition

        # if not self._ambient_lights:
        #     return  # No ambient lights
        # for light in self._ambient_lights:
        #     self.turn_on_device(light,
        #                   brightness_pct=brigtness, 
        #                   transition=transition)
           
    def turn_off_ambient(self)->None:
        self.log_to_logbook('Lights', "Släcker allmänljuset för {}".format(self._ambient_lights))
        # self._morning_ligths_on = False 
        # if not self._ambient_lights:
        #     return  # No ambient lights
        # for light in self._ambient_lights:
        #     self.turn_off_device(light)'

    '''
    
    Callback functions from hass. 
    
    '''

    def __on_house_home_changed(
            self, event_name: str, data: dict, kwargs: dict) -> None:
        newMode = HouseModes(data['new'])
        oldMode = HouseModes(data['old'])

        if newMode == HouseModes.day:
            self.on_housemode_day(oldMode)
        elif newMode == HouseModes.evening:
            self.on_housemode_evening(oldMode)
        elif newMode == HouseModes.night:
            self.on_housemode_night(oldMode)
        elif newMode == HouseModes.morning:
            self.on_housemode_morning(oldMode)
        elif newMode == HouseModes.cleaning:
            self.on_housemode_cleaning(oldMode)

    def __on_cmd_ambient_lights_on(
            self, event_name: str, data: dict, kwargs: dict) -> None:
        """turn on ambient ligts if event is fired"""
        self.turn_on_ambient()

    def __on_cmd_ambient_lights_off(
            self, event_name: str, data: dict, kwargs: dict) -> None:
        """turn off ambient ligts if event is fired"""
        self.turn_off_ambient()

    def __on_motion(
            self, entity: Union[str, dict], attribute: str, old: dict,
            new: dict, kwargs: dict) -> None:
        """callback when motion detected in area"""
        self.fire_event(
            GlobalEvents.EV_MOTION_DETECTED.value,
            entity=entity,
            area=self.name)

        self.motion_on_detected(entity)

    def __off_motion(
            self, entity: Union[str, dict], attribute: str, old: dict,
            new: dict, kwargs: dict) -> None:
        """callback motion off in area"""
        self.fire_event(
            GlobalEvents.EV_MOTION_OFF.value,
            entity=entity,
            area=self.name)

        self.motion_off_detected(entity)

    def __on_lightswich_state_changed(
            self, entity: Union[str, dict], attribute: str, old: dict,
            new: dict, kwargs: dict) -> None:
        """callback motion off in area"""

        self.on_lightswich_state_changed(entity, old, new)

    def __nightlight_off(
            self, entity: Union[str, dict], attribute: str, old: dict,
            new: dict, kwargs: dict) -> None:
        """callback nightlight off in area"""

        self.nightlights_off_detected(entity)
