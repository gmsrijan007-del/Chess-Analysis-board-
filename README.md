# Chess

A minimal chessboard website with position analysis from Stockfish. Drag pieces to make moves and press **Analyze position** to see the engine's suggested move and evaluation.

## Run locally

1. Install Python 3.10+ and install **Stockfish 19** for your operating system.
2. Install the Python packages:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
   pip install -r requirements.txt
   ```

3. Start the app:

   ```bash
   python app.py
   ```

4. Open http://localhost:5000.

The server looks for an executable named `stockfish` on `PATH`. If your Stockfish 19 binary is elsewhere, set `STOCKFISH_PATH` to its full path before starting the app. The engine is run on the server; it is not bundled in this repository. The web page loads board assets from CDNs, so an internet connection is needed.

For deployment, use a Python host that allows a Stockfish 19 executable and run Flask behind a production WSGI server.
