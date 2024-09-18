from website import create_app

app = create_app()
#create app instance


if __name__ == '__main__':
    app.run(debug=True)
