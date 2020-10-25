### Instructions for creating the youtube API Key

- 1º: Create the project in the cosole of Google Developer Console 

Link: https://console.developers.google.com/

![01-CreateProject](https://user-images.githubusercontent.com/52248363/97109572-c29d2380-16b2-11eb-90e3-e2e750fe43a5.PNG)


- 2º: With the project open select the "YouTube API Data v3" API in the library

![02-Library](https://user-images.githubusercontent.com/52248363/97109598-e5c7d300-16b2-11eb-84b9-5c1b933ed1c3.PNG)


- 3º: With the API select you must enable the API in the project

![03-EnableAPI](https://user-images.githubusercontent.com/52248363/97109615-f710df80-16b2-11eb-8150-ad62b96431d0.PNG)


- 4º: You must create the credential

![04-CreateCredentials](https://user-images.githubusercontent.com/52248363/97109630-0ee86380-16b3-11eb-9d6c-08b6877c8d84.PNG)

- 5º: To create the credential, you must fill in the following fields

![05-AddCredentials](https://user-images.githubusercontent.com/52248363/97109649-23c4f700-16b3-11eb-9b6d-7adeb449433b.PNG)

- 6º: Your API key was generated

![06-APIKey](https://user-images.githubusercontent.com/52248363/97109654-32131300-16b3-11eb-94df-af0e5e5c64af.PNG)


**This KEY API has been stored in an environment variable to be used in the project.**

> **API Documentation:** https://developers.google.com/youtube/v3?hl=pt_BR

### Installation of google api client package for python

- In this project was used the google api client package for python (Documentation: https://github.com/googleapis/google-api-python-client)

Installation: `pip install google-api-python-client`

From this package was used the build function (http://googleapis.github.io/google-api-python-client/docs/epy/googleapiclient.discovery-module.html#build)
This function receives as parameters serviceName and version, which, can be checked in: https://github.com/googleapis/google-api-python-client/blob/master/docs/dyn/index.md, besides these parameters, it must also receive the KEY API, which, in turn, was previously created and is stored in an environment variable.

With this, you can consult the available YouTube API methods at: http://googleapis.github.io/google-api-python-client/docs/dyn/youtube_v3.html

Example of API request
```python
import os
from googleapiclient.discovery import build

api_key = os.environ.get('YT_API_KEY')

youtube = build('youtube','v3', developerKey=api_key)

request = youtube.channels().list(
			part='statistics',
			forUsername='PyDataTV'
	)

response = request.execute()
```
