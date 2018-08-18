import time, datetime

from flask import Blueprint
from flashlearn.db import connect
from flask import render_template
from flask import request
from flask import jsonify


bp = Blueprint('learn', __name__)

engine = connect()


@bp.route('/learn/', methods=['GET'])
def learn():

    return render_template('learn.html')


@bp.route('/give_card/', methods=['POST'])
def give_card():
    '''
    Приоритет выдачи карт
    Выбрать все из выбранной колоды которые
        отвечал больше дня назад + начиная из самого низкого уровня
        выбираем все обновленные сегодня но больше часа назад + начиная из самого низкого уровня
        выбираем все обновленные меньше часа назад + начная из самого низкого уровня
        Когда карты закончились - выводим сообщение: Колода закончилась, с возможностью начать заново
    '''
    deck_id = request.form.get("deck_id")
    card_id = request.form.get("card_id")
    action = request.form.get('action')

    if action == 'give_first':
        # select card ids and insert them into temporary table in needed order
        card_ids_query = "SELECT id FROM `flashcard` WHERE deck_id=" + deck_id + " ORDER BY level ASC;"
        card_ids = engine.execute(card_ids_query)
        refresh_tmp_table(card_ids)

        # get first card
        first_card_id = engine.execute("SELECT card_id FROM `tmp_learning` WHERE id = 1").first()
        first_card_query = "SELECT * FROM `flashcard` WHERE id = " + str(first_card_id[0])
        card = engine.execute(first_card_query).first()

        return jsonify(card['id'], card['question'], card['answer'], card['level'])

    if action == 'give_next':
        next_card_query = "" \
                          "SELECT * FROM flashcard WHERE id = " \
                          "( SELECT card_id FROM `tmp_learning` WHERE id = " \
                          "(1 + ( SELECT id FROM `tmp_learning`WHERE card_id = " + card_id + " )) )"
        card = engine.execute(next_card_query).first()

        return jsonify(card['id'], card['question'], card['answer'], card['level'])

    if action == 'give_prev':
        prev_card_query = "" \
                          "SELECT * FROM flashcard WHERE id = " \
                          "( SELECT card_id FROM `tmp_learning` WHERE id = " \
                          "(( SELECT id FROM `tmp_learning`WHERE card_id = " + card_id + " )) - 1)"
        card = engine.execute(prev_card_query).first()

        return jsonify(card['id'], card['question'], card['answer'], card['level'])


def refresh_tmp_table(card_ids):

    # card_ids - iterable SQLAlchemy object
    engine.execute("TRUNCATE TABLE tmp_learning")
    card_ids_str = ','.join(map(lambda item: '(' + str(item[0]) + ')', card_ids))
    fill_table_query = 'INSERT INTO `tmp_learning` (card_id)  VALUES ' + card_ids_str
    engine.execute(fill_table_query)


@bp.route("/set_level", methods=["POST"])
def update_level():
    # TODO exception handling and sending operation status

    card_id = request.form.get('card_id')
    level = request.form.get('level')

    sql = 'UPDATE `flashcard` SET `level` = ' + str(level) + ' WHERE `flashcard`.`id` = ' + str(card_id)
    engine.execute(sql)
    return 'success'


