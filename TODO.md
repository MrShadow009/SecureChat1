# TODO: Fix Join Room Button Issue

## Steps to Complete
- [x] Add debugging logs to static/js/socket_main.js join button handler to confirm click and request payload.
- [x] Add logging to app.py join-room endpoint to log join attempts and passphrase verification.
- [x] Test the join flow by running the app and attempting to join a created room.
- [x] Identify and fix any issues found during testing (e.g., JS errors, backend errors, UI not updating).
- [x] Remove debugging logs after confirming the fix works.
- [x] Verify that users can successfully join rooms with correct room ID and passphrase.
- [x] Confirm UI updates correctly after join (modal closes, room title, leave button, messages start polling).
