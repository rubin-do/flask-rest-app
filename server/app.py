from flask import Flask, abort, request, jsonify
from flask import make_response, render_template, send_from_directory

import helper
import os

import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='rabbitmq', heartbeat=0))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)


app = Flask(__name__, template_folder='./src', static_folder='./static')

@app.route("/register", methods=["POST"])
def register_user():
    
    if not request.json or not 'username' in request.json:
        abort(400)
    
    r = request.get_json()
    
    username = r['username']
    avatar = r['avatar'] if 'avatar' in r.keys() else '-'
    sex = r['sex'] if 'sex' in r.keys() else '-'
    email = r['email'] if 'email' in r.keys() else '-'

    response = helper.add_user(username, avatar, sex, email)
    
    if not response:
        abort(404)
    
    return response

@app.route("/users/all", methods=["GET"])
def get_all():
    template_user_profile = '''
                                    <div class="container mt-5">
    <div class="row d-flex justify-content-center">
        <div class="col-md-7">
            <div class="card p-3 py-4">
                <div class="text-center"> <img src="{}" width="100" class="rounded-circle"> </div>
                <div class="text-center mt-3"> <span class="bg-secondary p-1 px-4 rounded text-white">{}</span>
                    <h5 class="mt-2 mb-0">{}</h5> 
                    <h5 class="mt-2 mb-0">{}</h5> 
                </div>
            </div>
        </div>
    </div>
</div>
    '''

    content = ''
    for user in helper.get_all():
        avatar_url = user['avatar'] if user['avatar'] != '-' else "/static/ico.jpg"
        content += template_user_profile.format(avatar_url, user['username'], user['email'], user['sex'])

    return render_template('users.html', content=content)


@app.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    
    response = helper.get_user(id)
    stats = helper.get_user_stats(id)

    if not response:
        abort(404)
    
    response = response.get_json()

    avatar_url = response['avatar'] if response['avatar'] != '-' else "/static/ico.jpg"

    return render_template('./user.html', 
        avatar=f'"{avatar_url}"', 
        username=response['username'], 
        sex=response['sex'], 
        email=response['email'],
        total_games = stats['total_games'],
        wins = stats['wins'],
        losses = stats['losses'],
        time_spent = stats['time_spent']
    )

@app.route("/users/<int:id>/getstats", methods=["GET"])
def get_stats(id):
    #os.system(f"touch /user/src/app/pdfs/{id}-stats.pdf")

    message = str(id)
    channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body=message,
    )

    return jsonify({
        "url": f"http://localhost:5000/pdf/{id}"
    })

@app.route("/pdf/<int:id>", methods=["GET"])
def get_pdf(id):
    return send_from_directory('/user/src/app/pdfs', f'{id}-stats.pdf')


@app.route("/users/<int:id>", methods=["POST"])
def update_user(id):

    if not request.json:
        abort(400)
    
    r = request.get_json()

    username = r['username'] if 'username' in r.keys() else '-'
    avatar = r['avatar'] if 'avatar' in r.keys() else '-'
    sex = r['sex'] if 'sex' in r.keys() else '-'
    email = r['email'] if 'email' in r.keys() else '-'
    
    if username == '-' and sex == '-' and email == '-' and avatar == '-':
        abort(400)
    
    resp = helper.get_user(id)

    if not resp:
        abort(404)
    
    resp = resp.get_json()
    
    if username == '-':
        username = resp['username']
    
    if avatar == '-':
        avatar = resp['avatar']

    if sex == '-':
        sex = resp['sex']
    
    if email == '-':
        email = resp['email']

    helper.update_user(id, username, avatar, sex, email)

    return make_response("OK\n", 200)


@app.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    
    helper.remove_user(id)

    return make_response("DELETED\n", 200)


@app.route("/add_game", methods=["POST"])
def add_game():
    if not request.json or not "losers" in request.json \
        or not "winners" in request.json or not "duration" in request.json:
        abort(400)
    
    req = request.get_json()

    for uid in req["winners"]:
        uid_stats = helper.get_user_stats(uid)
        helper.update_user_stats(
            uid,
            total_games=uid_stats['total_games']+1,
            wins=uid_stats['wins']+1,
            losses=uid_stats['losses'],
            time_spent=uid_stats['time_spent']+req['duration']
        )

    for uid in req["losers"]:
        uid_stats = helper.get_user_stats(uid)
        helper.update_user_stats(
            uid,
            total_games=uid_stats['total_games']+1,
            wins=uid_stats['wins'],
            losses=uid_stats['losses']+1,
            time_spent=uid_stats['time_spent']+req['duration']
        )
    
    return make_response("OK", 200)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)