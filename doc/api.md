# Potnanny Api

## Rooms
| URL           | Method    | Description  | Parameters | Data |
| ------------- | --------- | ------------ | ---------- | ---- |
| /rooms        | GET       | get list of rooms  | none  | none |
| /rooms        | POST      | create new room    | none  | name=STR(required) |
| /rooms/:id    | GET       | get room details   | id=INT(required) | none |
| /rooms/:id    | PUT       | edit room details  | id=INT(required) | name=STR(required)  |
| /rooms/:id    | DELETE    | delete room        | id=INT(required) | none |
| /rooms/:id/sensors | GET    |  get list of sensors assigned to room  | id=[integer](required) | none |
| /rooms/:id/overview | GET    |  get status/environment overview of room  | id=[integer](required) | none |


## Sensors
| URL           | Method    | Description  | Parameters | Data |
| ------------- | --------- | ------------ | ---------- | ---- |
| /sensors      | GET       | get list of sensors  | none  | none |
| /sensors      | POST      | create new sensor    | none  | name=STR(required), room_id=INT(optional) |
| /sensors/:id  | GET       | get sensor details   | id=INT(required) | none |
| /sensors/:id  | PUT       | edit sensor details  | id=INT(required) | name=STR(required), room_id=INT(optional) |
| /sensors/:id  | DELETE    | delete sensor       | id=INT(required) | none |
| /sensors/:id/measurements | GET | get sensor measurements | id=INT(required) | latest=BOOL, start=STR(start time), end=STR(end time) |


## Outlets
| URL           | Method    | Description  | Parameters | Data |
| ------------- | --------- | ------------ | ---------- | ---- |
| /outlets      | GET       | get list of outlets  | none  | none |
| /outlets      | POST      | create new outlet    | none  | name=STR(required), on_code=STR(required), off_code=STR(required), type=STR('wireless', required) |
| /outlets/:id  | GET       | get outlet details   | id=INT(required) | none |
| /outlets/:id  | PUT       | edit outlet details  | id=INT(required) | name=STR(required)  |
| /outlets/:id  | DELETE    | delete outlet        | id=INT(required) | none |
| /outlets/:id/switch  | POST    | switch outlet on or off        | id=INT(required) | state=INT(0|1 required) |


## RF Interface
| URL           | Method    | Description  | Parameters | Data |
| ------------- | --------- | ------------ | ---------- | ---- |
| /rfi/scan     | GET       | scan rf interface for transmit codes  | none  | none |
