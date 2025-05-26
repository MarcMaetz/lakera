# Procedure

I used Cursor for developing this MVP, so everything was built AI-assisted. 

There was first a very simple MVP that was not properly split. I split it into the files for a reosonable separation of concerns to be extensible but without overdoing it too much. I prompted it to make the routers like I wanted, the validation and also the tests.

# Comments

For tracking the RPS, I chose a separate logger with a configurable window of 60 seconds. It is using log rotation and we could add easily an alert if the RPS is getting too high.

I tried to use libraries e.g. for validation as much as possible to develop more efficiently and have a good and clean MVP quickly set up.