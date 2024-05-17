# PWP SPRING 2024
# FACIAL RECOGNITION FOR ACCESS CONTROL
# Group information
* Student 1. Tharindu Muthukuda Walawwe (tharindu.muthukudawalawwe@student.oulu.fi)
* Student 2. Shafin Salim (shafin.salim@student.oulu.fi)

## Overview
The Facial Recognition for Access Control API is a specialized component designed for identity verification and access management using facial recognition technology. This API is used as part of a larger security and access control ecosystem, integrating with physical access systems like electronic door locks and surveillance cameras.

The primary function of this API is to process and match facial images against a stored database to authenticate individuals for access control. It does not manage the entire access control system but focuses on the crucial aspect of identity verification through facial recognition. In a broader architecture, this API would interact with other systems that manage user permissions, access logs, and physical control of access points.

For example, in a smart building setup, this API could be integrated with an overarching building management system. It would provide the facial recognition capabilities required for access, while the building management system handles user permissions, access scheduling, and physical security protocols.

## Setup
This project has been set up using python 3.8.10. To start with the web application, run the following command
```
pip3 install -r requirements.txt
```

## Run on Local Server
To populate the DB and run the application server use the following command:
```
python3 app.py
```
The generated database file can be found inside ```instance``` folder as ```FacePass.db```

The server shall start on http://127.0.0.1:8080

## Client App
The client has been developed in VueJS which requires NodeJS. Run the following commands to setup client:
```
cd vue-app
npm install
npm run serve
```
The client will run on the next available port after 8080. Once it starts, you can access the client at http:127.0.0.1:8081 usually.

## Running Tests and Generating Coverage Report

This project uses `pytest` for testing and `pytest-cov` for generating coverage reports.

### Prerequisites

Make sure you have `pytest` and `pytest-cov` installed. You can install them using `pip`:

```sh
pip install pytest pytest-cov
```

### testing 

Navigate to the root directory of the project:

```sh
cd <project/directory>
```

Run the tests and generate a coverage report

```sh
pytest --cov=. --cov-report=html tests/
```

## Implementation Notes
The web application is currently under construction ⚒️


__Remember to include all required documentation and HOWTOs, including how to create and populate the database, how to run and test the API, the url to the entrypoint and instructions on how to setup and run the client__


