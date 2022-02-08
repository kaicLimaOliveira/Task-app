from flask import Flask, Blueprint
from routers import userRoutes
from routers import pagesRoutes

app = Flask(__name__)
app.register_blueprint(pagesRoutes.pages)
app.register_blueprint(userRoutes.user)

@app.template_filter()
def pretty_date(dttm):
    return dttm.strftime("%m/%d/%Y")

@app.template_filter()
def length(l):
    return len(l)

if __name__ == '__main__':
    app.run(host='localhost', port=4000, debug=True)
