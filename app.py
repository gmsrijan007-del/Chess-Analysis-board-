import atexit
import os
import threading

import chess
import chess.engine
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# Set STOCKFISH_PATH if Stockfish is not available on PATH.
ENGINE_PATH = os.environ.get("STOCKFISH_PATH", "stockfish")
ENGINE_DEPTH = int(os.environ.get("ENGINE_DEPTH", "15"))

_engine = None
_engine_lock = threading.Lock()


def get_engine():
    """Start Stockfish only when the first analysis is requested."""
    global _engine
    if _engine is None:
        _engine = chess.engine.SimpleEngine.popen_uci(ENGINE_PATH)
    return _engine


def close_engine():
    if _engine is not None:
        _engine.quit()


atexit.register(close_engine)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json(silent=True) or {}
    fen = data.get("fen")
    if not isinstance(fen, str):
        return jsonify(error="Send a chess position as a FEN string."), 400

    try:
        board = chess.Board(fen)
    except ValueError:
        return jsonify(error="That FEN position is not valid."), 400

    if not board.is_valid():
        return jsonify(error="That chess position is not valid."), 400

    if board.is_game_over():
        return jsonify(error="This game is over; there is no best move to analyze."), 400

    try:
        # A single UCI engine process handles one request at a time.
        with _engine_lock:
            result = get_engine().analyse(
                board,
                chess.engine.Limit(depth=ENGINE_DEPTH),
            )
        best_move = result["pv"][0]
        score = result["score"].relative
        return jsonify(
            evaluation=str(score),
            best_move=board.san(best_move),
            best_move_uci=best_move.uci(),
        )
    except (FileNotFoundError, chess.engine.EngineError, OSError) as exc:
        app.logger.exception("Could not run Stockfish")
        return jsonify(
            error="Stockfish could not be started. Install Stockfish and make sure it is on PATH, or set STOCKFISH_PATH."
        ), 503


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")), debug=False)
