from flask import Blueprint, request, jsonify, make_response, redirect
from flask_jwt_extended import (
    jwt_required, create_access_token, jwt_refresh_token_required,
    create_refresh_token, get_jwt_identity )
from potnanny_core.models import User


bp = Blueprint('auth_api', __name__, url_prefix='/token')


@bp.route('/auth', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    next_page = request.json.get('next', None)

    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    obj = User.query.filter_by(username=username).first()
    if not obj or not obj.check_password(password):
        return jsonify({"msg": "invalid credentials"}), 401

    access_token = create_access_token(identity=username)
    refresh_token = create_refresh_token(identity=username)

    if next_page:
        resp = make_response(redirect(next_page))
        set_access_cookies(resp, access_token)
        set_refresh_cookies(resp, refresh_token)
        return resp, 302
    else:
        resp = jsonify({
            'login': True,
            'access_token': access_token,
            'refresh_token': refresh_token,
        })
        # set_access_cookies(resp, access_token)
        # set_refresh_cookies(resp, refresh_token)
        return resp, 200


@bp.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    # Create the new access token
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)

    resp = jsonify({'refresh': True})
    set_access_cookies(resp, access_token)
    return resp, 200


@bp.route('/remove', methods=['POST'])
@jwt_required
def logout():
    resp = jsonify({'logout': True})
    unset_jwt_cookies(resp)
    return resp, 200
