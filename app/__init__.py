from flask import Flask

app = Flask(__name__)
app.config.from_object('config')
# 现在通过app.config["VAR_NAME"]，我们可以访问到对应的变量