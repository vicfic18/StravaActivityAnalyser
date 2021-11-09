# Strava Activity Analyser

This is just a guide on what I did to get 100+ people's strava activity for a club challenge. My only target was to get all of these people's activities in a spreadsheet, so if you want to use it, you need need make some tweaks to get it working.
**I also recommend reading [this guide](https://medium.com/swlh/using-python-to-connect-to-stravas-api-and-analyse-your-activities-dummies-guide-5f49727aac86\), since I mostly followed what it says.**

### FYI

- First, you need register your app in your strava profile (https://www.strava.com/settings/api).

- The server outputs profile json responses to a google sheet, so

- You should setup a google api service account and put the credentials(`creds.json`) in the same folder as `app.py`

- `profiles.csv` should be a copy of your google sheet

- `activity_ouput.csv` is the output of `fetch.py`
