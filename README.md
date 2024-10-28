# SSE Mentor Application

## Overview
The SSE Mentor Application is a desktop app, intended to run on the Mentor PC. This launches a google form and plays a sound to remind mentors when to fill out the form. This functionality is already present in the current system. The new features involve creating a test checkout system, to better track who has what test out, to help us log who has what test out in case of a lost test.

## Features

### Current Features
- Launches a google form at 30m and 55m of every hour
- Plays a sound at 30m and 55m of every hour to remind mentors to fill out the form

### New Features

#### Essential Features (MVP)
- When an ID is swiped, if the user is not registered in the system, the system will prompt the mentor to enter their name and email
- When an ID is swiped, if the user is registered in the system, the system will prompt the user to mentor the class they are checking out for
- The main screen will show the status current operations (e.g. "Waiting for ID", "Test Checked Out", "Test Checked In")
- For each test checked out, the system will log the student, mentor, and time checked out to a google sheet (for the department to access if needed)

#### Additional Features
- When an ID is swiped, if the student has a test already checked out, the system will prompt the mentor to check in the test
- In the absence of the student's ID, the system will allow the mentor to manually enter the student's name and email
- The mentoring head will be able to see what tests have not been checked in, and by whom (apart from the google sheet)

#### Future Features (After Initial Release)
- Tap Reader instead of Swipe Reader
- Some cool other stuff (submit a PR if you have an idea)

## Card Reader Data
RIT ID cards output the following format when swiped:
```plaintext
;111111111=0000?
```
Where `111111111` is the student's RIT UID (University ID Number), the rest of the data is not needed for this application.

Note: RIT UID's are considered Confidential Information and will not be stored in plain text. Instead, the UID will be hashed securely and stored locally on the Mentor PC.

## Google Sheets Data
The Google Sheet will have the following columns:
- Student Name
- Student Email
- Course
- Time Checked Out
- Time Checked In

A service account will be created to allow the application to write to the Google Sheet.

## Contributing
Please contact Ryan Yocum (rty4159@rit.edu) if you would like to contribute to this project.