# TimeTracker
TimeTracker is as name suggests tracks time in every window (currently client works only on windows)

Project is divided in all-in-one or server-client architecture (server isn't needed for client to gather data to .json files)

To run server use (being in server folder):
```
sudo ./install.sh
flask run
```
Optionally use for flask server to be visible in the local network
```
flask run --host=0.0.0.0
```

