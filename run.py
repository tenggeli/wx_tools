from flask import Flask,redirect,url_for
app = Flask(__name__)

#from app import *

urls = (
    '/wx', 'Handle',
    '/t', 'test',  # 测试
    '/', 'home',
    '/reload','reload'#重启服务
)

@app.route('/')
def index():
    # login_url = url_for('login')
    # return redirect(login_url)
    return u'这是首页'


@app.route('/login/')
def login():
    return u'这是登陆页面'


@app.route('/question/<is_login>/')
def question(is_login):
    if is_login == '1':
        return u'这是发布问答的页面'
    else:
        return redirect(url_for('login'))

'''
@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id
'''

if __name__ == '__main__':
    app.run()
