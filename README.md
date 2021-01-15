# TimeTracker
TimeTracker is as name suggests tracks time in every window (currently client works only on windows)

# About
Project is divided in all-in-one or server-client architecture (server isn't needed for client to gather data to .json files)

# Client
To run client use (being in client folder):
```
py main.py
```
It will save data of all window names and how long it was active. 
After breaking terminal (ctrl+c) script will save data to ./client/data/TimeTrackerData and try to send it to local server (it will communicate if it was succesfull or not).
If you want to setup server on specific IP address you can change (line 7 in main.py):
```python
SERVER_IP = "your IP address"
```

# Server
To run server use (being in server folder):
```
sudo ./install.sh
flask run
```
Optionally use
```
flask run --host=0.0.0.0
```
for flask server to be visible in the local network

Server allows to create new categories and adding keywords for them to automatically add window names to them.
 
# Attribution
* icon - Stopwatch by Dmitry Mirolyubov from the Noun Project

# WORK IN PROGRESS
* Site to add keywords from activities saved. Some apps/sites have very good window naming policies, but not all of them. For example YouTube will always have YouTube in their window name so you need "YouTube" as the keyword and TimeTracker will always detect it, but for example Metro Exodus sometimes have "4A Engine" as window name (which is checked by TimeTracker) and keyword "Metro Exodus" will not work. 

