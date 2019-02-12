# POTNANNY
_"Plant care when you're not there"_

Potnanny turns a Raspberry Pi into a powerful greenhouse monitor/controller. Keep all of your potted plants healthy and happy.

## CONFIGURATION
### Rooms
Potnanny requires that you have at least one room defined. A Room keeps related
things grouped together, such as Bluetooth Sensors, Grow Cycles, and Actions.

 1. From the main dashboard page, click on the plus-symbol icon to add a new Room.
 2. Name the room.
 3. Click "Save"

### Sensors
The following Bluetooth LE devices are currently supported.
 - [Xiaomi Mi Flora soil sensors](https://miot-global.com/sockets-and-sensors/xiaomi-huahuacaocao-flower-care-smart-monitor/) (senses temperature, soil-moisture, ambient-light, soil-conductivity(EC))
 - [Xiaomi Mi BT Thermometer](https://www.xiaomistore.pk/mi-bluetooth-temperature-humidity-monitor.html) (senses temperature, humidity)

 _Support for more devices is in progress_

Newly discovered Sensors must be assigned to a Room before they can be used to trigger Actions.

 1. From the main dashboard page, click on a room.
 2. Click on the "sensors" button.
 3. Look through the list of sensors, and click on one that says "unassigned".
 4. Select the Room you want to assign it to.
 5. Click "save"
 
### Actions
Actions are applied to a Room.
Action Plugins each have slightly different options, so be sure to check the documentation
for each plugin. But, in general, all Actions share these basic attributes.

 - **measurement_type**: Defines what type of measurement will activate the Action. Some options are,
   * temperature
   * humidity
   * soil moisture

 - **sensor**: Declare if the Action will activate based on measurements from only one particular sensor, or any sensor in the room.

 - **trigger thresholds**: These define when an Action will trigger (activate or deactivate), based on measurements received from sensors. For instance, if you wanted to keep the room humidity between 50-55%, a Triggered-On/Off Action would be defined with the following trigger thresholds:
   * "If value lt (less than) 51, turn outlet called 'humidifier' ON"
   * "If value gt (greater than) 54, turn outlet called 'humidifier' OFF"

 - **sleep timer**: This setting forces an Action to go to sleep for a certain amount of time (in minutes), after it has been activated. During this sleep period the Action cannot activate again, even if measurements are received that would normally cause the Action to activate. This can help minimize outlets turning on/off too frequently, or notifications being sent too often.

### Outlets
#### Wifi
Potnanny currently supports the Etekcity Vesync wifi power outlets. We like these because they are simple, reliable, and they provide power usage readings, which many other inexpensive wifi outlets do not.
Before integrating your Vesync outlets into Potnanny, you should first sign up for an account with Vesync. Then discover and configure the devices using the native VesyncOutlet mobile app.


Potnanny also supports control of RF Wireless outlets. These can provide more reliable control over outlets if you have weak or intermittent wifi support and However, this requires technical expertise with soldering and electronics, as you will need to connect 433Mhz transmit and receive modules to your raspberry pi.
