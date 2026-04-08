import os
import logging
import asyncio
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager

from nlp_engine import engine
from schemas import AnalysisRequest, AnalysisResponse, HealthStatus

# Configure structured JSON-compatible logging
logging.basicConfig(
    level=logging.INFO,
    format='{"timestamp": "%(asctime)s", "level": "%(levelname)s", "logger": "%(name)s", "message": "%(message)s"}'
)
logger = logging.getLogger("nlp-api")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles startup and shutdown logic.
    Pre-loads the default English model to avoid latency on first request.
    """
    logger.info("Starting up FastAPI application...")
    try:
        # Pre-load English model
        await asyncio.to_thread(engine.load_model, "en")
        logger.info("Default English model loaded successfully.")
    except Exception as e:
        logger.error(f"Failed to load default models: {str(e)}")
    
    yield
    
    logger.info("Shutting down application...")

app = FastAPI(
    title="Antigravity NLP Engine",
    description="Accelerated Named Entity Recognition and POS Tagging API.",
    version="2.0.0",
    lifespan=lifespan
)

# Mounting static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Hardened CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to specific domains
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.get("/", tags=["General"])
async def root(request: Request):
    """Serve the interactive web interface."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health", response_model=HealthStatus, tags=["Diagnostic"])
async def health_check():
    """Returns the service health and model status."""
    return HealthStatus(model_loaded=engine.is_model_loaded)

@app.post("/analyze", response_model=AnalysisResponse, tags=["NLP"])
async def analyze_text(request: AnalysisRequest):
    """
    Primary endpoint for high-performance NLP analysis.
    Offloads CPU-bound Spacy calls to secondary worker threads.
    """
    try:
        text = request.text
        
        # 1. Detect language (O(N))
        lang = request.language or await asyncio.to_thread(engine.detect_language, text)
        logger.info(f"Analyzing text of length {len(text)} with language {lang}")

        # 2. Extract features and entities asynchronously
        # Using asyncio.to_thread to avoid blocking the event loop on CPU-bound tasks
        tokens_task = asyncio.to_thread(engine.extract_nlp_features, text, lang)
        entities_task = asyncio.to_thread(engine.extract_entities, text, lang)
        
        # Parallel execution of extraction tasks
        tokens, entities = await asyncio.gather(tokens_task, entities_task)

        return AnalysisResponse(
            entities=entities,
            tokens=tokens,
            detected_language=lang,
            model_used="en_core_web_sm" # Fixed currently, can be dynamic
        )

    except Exception as e:
        logger.error(f"Internal processing error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="An error occurred during NLP analysis.")

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "status": "failed"}
    )

if __name__ == "__main__":
    import uvicorn
    # Changed default port from 8000 to 8001 to avoid conflicts
    port = int(os.environ.get("PORT", 8001))
    # Production-ready Uvicorn configuration
    uvicorn.run("main:app", host="0.0.0.0", port=port, log_level="info", workers=1)
