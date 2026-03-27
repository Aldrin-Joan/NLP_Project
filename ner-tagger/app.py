import os
import logging
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from ner_engine import extract_nlp_features, extract_entities

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__, 
            static_folder="static", 
            template_folder="templates")
CORS(app) # Enable CORS for local development flexibility

# Safety constraint: limit input text length
MAX_TEXT_LENGTH = 10000

@app.route("/")
def index():
    """Serves the main UI page."""
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    """
    Primary endpoint for NLP analysis.
    Expects JSON: { "text": "..." }
    """
    try:
        data = request.get_json()
        if not data or "text" not in data:
            return jsonify({"error": "Missing 'text' field in request body"}), 400
        
        text = data["text"]
        
        if not isinstance(text, str):
            return jsonify({"error": "Input 'text' must be a string"}), 400
            
        if len(text) > MAX_TEXT_LENGTH:
            return jsonify({
                "error": f"Input text exceeds maximum length of {MAX_TEXT_LENGTH} characters"
            }), 413

        logger.info(f"Analyzing text of length: {len(text)}")
        
        entities = extract_entities(text)
        tokens = extract_nlp_features(text)
        
        return jsonify({
            "entities": entities,
            "tokens": tokens,
            "status": "success"
        })

    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    # Use Waitress for a more production-ready local server
    # Fallback to Flask dev server if waitress is not available
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "True").lower() == "true"
    
    logger.info(f"Starting NER Tagger server on port {port} (debug={debug})")
    
    try:
        from waitress import serve
        serve(app, host="127.0.0.1", port=port)
    except ImportError:
        logger.warning("Waitress not found. Falling back to Flask development server.")
        app.run(host="127.0.0.1", port=port, debug=debug)
