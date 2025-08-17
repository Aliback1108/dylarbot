import os
from dotenv import load_dotenv
from app import create_app

# Charge .env (FOOTBALL_DATA_TOKEN, PORT, etc.)
load_dotenv()

app = create_app()

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "5000"))
    debug = os.getenv("FLASK_DEBUG", "1") == "1"
    app.run(host=host, port=port, debug=debug)
