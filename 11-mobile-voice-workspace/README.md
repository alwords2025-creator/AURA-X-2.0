# AURA-X 2.0 Mobile Voice Workspace (UI starter)

Responsive HTML/CSS/JS interface for the first combined AURA-X 2.0 starter bundle. Features: multilingual browser speech-to-text (where supported), text-to-speech playback, chat/task UI, file selection/local download, camera preview/photo capture/video recording, experimental browser QR scanning, and a configurable backend API URL.

## Run
Open `index.html` in a modern browser for basic UI. Camera/microphone features generally require HTTPS or localhost. For mobile deployment, host this folder on HTTPS (for example, as a static site) and configure your backend API URL.

## Important limitations
- This is a front-end starter, not a complete production application.
- Chat works in demo mode until a compatible API endpoint is configured. The sample request sends `POST {"task":"..."}`; adapt the request/response shape to your deployed orchestrator. Browser CORS must allow the site origin.
- Selected files and camera captures stay in the browser and download locally; cloud upload/storage is not implemented.
- Messenger is a local UI placeholder; real multi-user live messaging needs authenticated WebSocket/backend infrastructure.
- Speech recognition and QR detection vary by browser/device. Full duplex voice conversation needs a speech/AI backend.
- Do not put API keys or secrets in this front-end.
