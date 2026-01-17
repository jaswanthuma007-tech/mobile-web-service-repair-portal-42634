from app import app

if __name__ == "__main__":
    # Default to the required port for this container.
    app.run(host="0.0.0.0", port=3001)
