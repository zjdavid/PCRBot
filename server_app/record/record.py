from quart import Blueprint, request, jsonify, g
import datetime
from ..auth_tools import login_required
from data.model import *
from ..group_tools import get_group_of_user
from .record_tools import damage_to_score, subtract_damage_from_group

record_blueprint = Blueprint(
    "record_v1",
    __name__,
    url_prefix='/v1/record'
)


@record_blueprint.route('/add_record', methods=['POST'])
@login_required
def add_record():
    """
    @api {post} /v1/record/add_record 出刀
    @apiVersion 1.0.0
    @apiName add_record
    @apiGroup Records
    @apiParam {String}  damage       (必须)    伤害
    @apiParam {String}  boss_gen     (可选)    boss周目（如果没有则为当前boss）
    @apiParam {String}  boss_order   (可选)    第几个boss（如果没有则为当前boss）

    @apiSuccess (回参) {String}     msg   为"Successful!"
    @apiSuccess (回参) {Dictionary} record  添加的Record，具体内容参照Records表
    @apiSuccess (回参) {Dictionary} group   更新后的当前公会信息，具体内容参照Groups表

    @apiErrorExample {json} 参数不存在
        HTTP/1.1 400 Bad Request
        {"msg": "Parameter is missing", "code": 401}

    @apiErrorExample {json} 用户没有加入公会
        HTTP/1.1 403 Forbidden
        {"msg": "User is not in any group.", "code": 402}

    @apiErrorExample {json} 用户的公会不存在
        HTTP/1.1 403 Forbidden
        {"msg": "User's group not found.", "code": 403}

    """
    user: Users = g.user
    damage = request.args.get('damage', None)
    boss_gen = request.form.get('boss_gen', None)
    boss_order = request.form.get('boss_order', None)

    if not damage:
        return jsonify({"msg": "Parameter is missing", "code": 401}), 400
    if user.group_id == -1:
        return jsonify({"msg": "User is not in any group.", "code": 402}), 403

    group: Groups = get_group_of_user()
    if not group:
        return jsonify({"msg": "User's group not found.", "code": 403}), 403
    if not boss_gen:
        boss_gen = group.current_boss_gen
    if not boss_order:
        boss_order = group.current_boss_order

    added_record: Records = Records(group_id=user.group_id,
                                    boss_gen=boss_gen,
                                    boss_order=boss_order,
                                    damage=damage,
                                    user_id=user.id,
                                    nickname=user.nickname,
                                    date=datetime.datetime.now())
    added_record.score = damage_to_score(record=added_record)
    subtract_damage_from_group(record=added_record, group=group)
    db.session.add(added_record)

    db.session.commit()
    return jsonify({
        "msg": "Successful!",
        "record": added_record.__dict__,
        "group": group.__dict__
    }), 200
