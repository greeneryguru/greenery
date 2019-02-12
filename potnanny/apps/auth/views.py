import json
from flask import (Blueprint, render_template, redirect, request,
    url_for, current_app, jsonify)
from .forms import LoginForm

bp = Blueprint('login', __name__, template_folder='templates' )

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():

        print("REQUEST")
        print(request)
        print(request.__dict__)

        username = form.username.data
        password = form.password.data
        next_page = "/"
        client = current_app.test_client()
        response = client.post(url_for('auth_api.login'),
                                headers=list(request.headers),
                                content_type='application/json',
                                data=json.dumps(dict(
                                                username=username,
                                                password=password,
                                                next=next_page )))

        if response.status_code in [200, 302, 303, 307]:
            return response
        else:
            print("BAD RESPONSE")
            print(response)
            print(response.__dict__)
            print(response.response.__dict__)
            form.username.errors = ['login error']

    return render_template('auth/login.html', form=form)


def logout():
    pass
