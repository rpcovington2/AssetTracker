import web
# from web import CreateApp  # LIVE
#from Dev import CreateApp   # Development

app = web.CreateApp()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9000)
