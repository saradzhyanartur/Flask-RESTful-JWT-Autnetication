# FlaskUserBaseAPI
Flask RESTful API with JWT Authentication and Redis store

## Description
This project is meant to serve as a foundation for future projects that intend to use JSON Web Tokens as means of authenticating users. The API is stateless and utilizes Redis to black list tokens.

## Implementation
The API was tested with
```
implementation = CPython
version_info = 3.7.6.final.0
```
To install the requirements please enter a virtual environment and run
```
pip install -r requirements.txt
```
The Project comes with a Postman file that is set up to interact with the API. 

**PLEASE REMEMBER TO RESET THE SECRET KEYS IN THE CONFIG.PY FILE**