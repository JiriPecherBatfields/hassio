using System;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;
using JoySoftware.HomeAssistant.NetDaemon.Common;

/// <summary>
///     Application manage the carheater. Implements following use-cases:
///         - Automatically turns off carheater if on for 3 hours as protection for the car
///         - Reads departure time and turn on heater a specific time
///           before depending on temperature
///         - Can be turned on/off depending if it is a weekday or weekend
/// </summary>
/// <remarks>
///     The application is running every minute and decides if the heater is
///     going to be on or off. This logic will work also after restart.
/// </remarks>
public class CarHeaterManager : NetDaemonApp
{
    // The entities used in the automation
    private readonly string _tempSensor = "sensor.ute_temp";
    private readonly string _departureTime = "sensor.car_departure_time";
    private readonly string _scheduleOnWeekend = "input_boolean.schedule_on_weekends";
    private readonly string _heaterSwitch = "switch.motorvarmare";

    // True if the heater is started outside this script
    private bool _manuallyStarted = false;
    // True if the script just turn on the heater,
    // used to prohibit logic being run on state change
    private bool _justTurnedOn = false;
    // Used for logging at startup and no more
    private bool _appJustStarted = true;

    /// <summary>
    ///     Initialize the automations
    /// </summary>
    /// <remarks>
    ///     - Schedules check every minute if heater should be on or off depending on temperature
    ///     - Set the manually started flag if heater is turn on and not turned on by this script
    /// </remarks>
    public override Task InitializeAsync()
    {
        Scheduler.RunEvery(TimeSpan.FromMinutes(1), () => HandleCarHeater());

        Entity(_heaterSwitch).WhenStateChange(to: "on").Call(async (e, to, from) =>
        {
            if (_justTurnedOn == false)
            {
                // It is manually turned on
                _manuallyStarted = true;
            }
            _justTurnedOn = false;
        }).Execute();
        // No async so return completed task
        return Task.CompletedTask;
    }

    /// <summary>
    ///     Handle the logic run every minute if heater
    ///     should be on or off
    /// </summary>
    private async Task HandleCarHeater()
    {
        try
        {
            // First do the failsave logic, no heater should run for more than 3 hours
            await TurnOffHeaterIfOnMoreThanThreeHours();

            // Get relevant states
            var currentOutsideTemp = (double?)GetState(_tempSensor).State;
            var configuredDepartureTime = GetState(_departureTime).State;
            var scheduleOnWeekend = GetState(_scheduleOnWeekend).State == "on" ? true : false;

            // Calculate correct set departure time
            var now = DateTime.Now;
            var hours = int.Parse(configuredDepartureTime.Split(':')[0]);       // configured departure is in format hh:mm
            var minutes = int.Parse(configuredDepartureTime.Split(':')[1]);
            var nextDeparture = new DateTime(now.Year, now.Month, now.Day, hours, minutes, 0);

            // Add the next day if we passed todays time
            if (nextDeparture < now)
                nextDeparture = nextDeparture.AddDays(1);

            if (_appJustStarted)
            {
                // Just log some useful information if we at startup
                Log($"The time is {DateTime.Now}, if the time does not match local time, see time zone settings");
                Log($"Next departure is {nextDeparture}");
                _appJustStarted = false;
            }


            // If weekend and not set to schedule on weekends then just return
            if ((nextDeparture.DayOfWeek == DayOfWeek.Saturday || nextDeparture.DayOfWeek == DayOfWeek.Sunday) && !scheduleOnWeekend)
            {
                return;
            }

            // Calculate total minutes to departure
            var totalMinutesUntilDeparture = nextDeparture.Subtract(now).TotalMinutes;

            if (currentOutsideTemp >= -1.0 && currentOutsideTemp <= 5.0)
            {
                // Within 30 minutes
                if (totalMinutesUntilDeparture <= 30)
                {
                    await TurnOnHeater();
                    return;
                }

            }
            else if (currentOutsideTemp >= -5.0 && currentOutsideTemp < -1.0)
            {
                // Within one hour
                if (totalMinutesUntilDeparture <= 60)
                {
                    await TurnOnHeater();
                    return;
                }
            }
            else if (currentOutsideTemp >= -10.0 && currentOutsideTemp < -5.0)
            {
                // Within 1.5 hour
                if (totalMinutesUntilDeparture <= 90)
                {
                    await TurnOnHeater();
                    return;
                }
            }
            else if (currentOutsideTemp >= -20.0 && currentOutsideTemp < -10.0)
            {
                // Within two hours
                if (totalMinutesUntilDeparture <= 120)
                {
                    await TurnOnHeater();
                    return;
                }
            }
            else if (currentOutsideTemp < -20.0)
            {
                // Within three hours
                if (totalMinutesUntilDeparture <= 180)
                {
                    await TurnOnHeater();
                    return;
                }
            }

            // If not manually started and heater is on, turn heater off
            if (GetState(_heaterSwitch).State == "on" && !_manuallyStarted)
            {
                Log("Turning off heater");
                await Entity(_heaterSwitch).TurnOff().ExecuteAsync();
                Log($"Next departure is {nextDeparture}");
            }

        }
        catch (System.Exception e)
        {
            // Log all errors!
            Log("Error in car heater app", e, LogLevel.Error);
        }

    }

    /// <summary>
    ///     Turn the heater on if it is not already on
    /// </summary>
    private async Task TurnOnHeater()
    {
        try
        {
            // Temp is debuginformation to make sure the logic works, will be removed
            var currentOutsideTemp = (double?)GetState(_tempSensor).State;

            if (GetState(_heaterSwitch).State != "on")
            {
                // Flag that this script actually turn the heater on and non manually
                _manuallyStarted = false;
                _justTurnedOn = true;

                Log($"{DateTime.Now} : Turn on heater temp ({currentOutsideTemp})");
                await Entity(_heaterSwitch)
                    .TurnOn()
                        .ExecuteAsync();
            }
        }
        catch (System.Exception e)
        {
            Log("Error turn on heater", e, LogLevel.Error);
        }
    }

    /// <summary>
    ///     Turns the heater off if it has been on for more than three hours
    /// </summary>
    /// <remarks>
    ///     For any reason the switch has been on for more than three hours
    ///     the heater will be turned off. This will save energy and prohibit
    ///     the heater being on accidentally
    /// </remarks>
    /// <returns></returns>
    private async Task TurnOffHeaterIfOnMoreThanThreeHours()
    {
        try
        {
            // Turn off heater if it has been on for more than 3 hours
            await Entities(n =>
                n.EntityId == _heaterSwitch
                && n.State == "on"
                && DateTime.Now.Subtract(n.LastChanged) > TimeSpan.FromHours(3))
                .TurnOff().ExecuteAsync();
        }
        catch (System.Exception e)
        {
            Log("Error doing failsafe", e, LogLevel.Error);
        }

    }
}