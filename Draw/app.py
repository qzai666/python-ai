from flask import Flask,render_template
from random import randint


app = Flask(__name__)

hero_arr = ['盖伦', '提莫', '艾希', '安妮', '卡莎', '赵信', '布隆', '拉克丝']
hero_random = hero_arr[randint(0, len(hero_arr) - 1)]  # 随机选择一个英雄
@app.route('/hero')
def hero():
    return render_template('index.html', hero_arr=hero, hero_random=hero_random)

@app.route('/')
def index():
    return "Welcome to the Draw application!"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)  # 添加 host='0.0.0.0'