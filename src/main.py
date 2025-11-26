import uvicorn
from src.core.config import settings

if __name__ == "__main__":
    settings.validate_settings()
    uvicorn.run(
        "src.api.routes:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Disable in production
        workers=1
    )