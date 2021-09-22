# Virtual Booking Assistant 

## Prequisites
- install packages in requirements.txt

## Coding:
- `records.py`: stores information during the conversation.  
- `context.py`: context for the conversation.
- `regex/`: predict intent with regex
- `template_action.json`: define text, text_tts, status
,properties, ... for the packet which pass to the master process
- `run_graph.sh`: show all the intents and actions in resource/graph.md

## Run server
- create "logs", "audio" and "audio_tts" folders in resource: ```$ cd resource && mkdir logs && mkdir audio && mkdir audio_tts```
- [Hospital API]: ```$ cd HospitalAPI && python3 main.py```
- [Main project]: ```$ python3 manage.py runserver```

