# appdaemon-dahua2mqtt
A port of existing dahua2mqtt, but using Requests instead of pycurl, as pycurl causes constant issues with alpine packages

Dahua IP Camera events to MQTT app. Implemented from: https://github.com/johnnyletrois/dahua-watch

Example configuration:
```
DahuaMQTT:
  class: DahuaMQTT
  module: dahua_mqtt
  cameras:
    - host: 192.168.0.1
      port: 80
      user: user
      pass: pass
      topic: cameras/1
      events: VideoMotion,VideoBlind,VideoLoss,AlarmLocal,....
    - host: 192.168.0.2
      port: 80
      user: user
      pass: pass
      topic: cameras/2
      events: VideoMotion,VideoBlind,VideoLoss,AlarmLocal,....
```
Note: If you are using an NVR rather than individual cameras, you can configure a single entry, along with a single MQTT topic, and the camera index number will be appended.

NVR Example Configuration:
```
DahuaMQTT:
  class: DahuaMQTT
  module: dahua_mqtt
  cameras:
    - host: 192.168.0.1
      port: 80
      user: user
      pass: pass
      topic: cameras/
      events: VideoMotion,VideoBlind,VideoLoss,AlarmLocal,....
```
In this case, you will get messages published to cameras/1, cameras/2 etc

App sends to the configured MQTT topic:

eg: cameras/1/<event>, ex: cameras/1/VideoMotion and payload will be action: Start or Stop<br/>

According to the API docs, these events are available: (availability depends on your device and firmware)
  
        VideoMotion: motion detection event<br/>
        VideoLoss: video loss detection event<br/>
        VideoBlind: video blind detection event<br/>
        AlarmLocal: alarm detection event<br/>
        CrossLineDetection: tripwire event<br/>
        CrossRegionDetection: intrusion event<br/>
        LeftDetection: abandoned object detection<br/>
        TakenAwayDetection: missing object detection<br/>
        VideoAbnormalDetection: scene change event<br/>
        FaceDetection: face detect event<br/>
        AudioMutation: intensity change<br/>
        AudioAnomaly: input abnormal<br/>
        VideoUnFocus: defocus detect event<br/>
        WanderDetection: loitering detection event<br/>
        RioterDetection: People Gathering event<br/>
        ParkingDetection: parking detection event<br/>
        MoveDetection: fast moving event<br/>
        MDResult: motion detection data reporting event. The motion detect window contains 18 rows and 22 columns. The event info contains motion detect data with mask of every row.<br/>
        HeatImagingTemper: temperature alarm event<br/>


  Example Home Assistant Configuration:
  ```
  mqtt:
    binary_sensor:
      - name: Motion Front Yard
      state_topic: cameras/2/VideoMotion
      payload_on: Start
      payload_off: Stop
      device_class: motion
  ```
  
  
  
