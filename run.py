from tigerevents import create_app
app = create_app()

if __name__ == "__main__":
    app.run(threaded=True, port=8000, debug=True)