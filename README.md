# Boardroom — Free Chess Analyzer

A small, free-to-run chess analysis website built with Flask, python-chess, and Stockfish. Drag pieces to explore a position, then ask Stockfish for an evaluation and suggested move.

## Run locally

1. Install Python 3.10+ and [Stockfish](https://stockfishchess.org/download/). Stockfish must be installed separately from the Python packages.
2. Install the app dependencies:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
   pip install -r requirements.txt
   ```

3. If the `stockfish` executable is not on your PATH, set `STOCKFISH_PATH` to its location.
4. Start the website:

   ```bash
   python app.py
   ```

5. Open http://localhost:5000.

Set `ENGINE_DEPTH` to change search depth (default: 15), and `PORT` to change the web server port. The first analysis starts the Stockfish process. The web page uses CDN-hosted chessboard assets, so an internet connection is needed to load those assets.

## Note

This repository contains the website source, not a hosted website. To make it publicly accessible, deploy it on a Python host and install/provide a compatible Stockfish binary there. Do not expose Flask's development server as a production server.
