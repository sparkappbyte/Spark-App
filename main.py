from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from flask import Flask, request, jsonify
import asyncio
import random

API_TOKEN = "8694731612:AAEAE9q6cg96CRS1kefQX_CUN_aJDfTB-Tc"
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

app = Flask(__name__)
users = {}  # хранение баланса
wheel_numbers = list(range(37))
red_numbers = [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]

# API для Mini App: делаем ставку
@app.route("/bet", methods=["POST"])
def bet():
    data = request.json
    user_id = data["user_id"]
    bet_type = data["bet_type"]
    amount = data["amount"]

    if user_id not in users:
        users[user_id] = {"balance": 1000, "daily_win": 0}

    if users[user_id]["balance"] < amount:
        return jsonify({"error": "Недостаточно баланса"})

    users[user_id]["balance"] -= amount
    result_number = random.choice(wheel_numbers)
    win = 0
    if bet_type == "red" and result_number in red_numbers:
        win = amount * 2
    # здесь можно добавлять остальные правила ставок

    users[user_id]["balance"] += win
    users[user_id]["daily_win"] += win

    return jsonify({
        "result_number": result_number,
        "win": win,
        "balance": users[user_id]["balance"]
    })

if __name__ == "__main__":
    # запуск Flask сервера + aiogram бота
    executor.start_polling(dp, skip_updates=True)
    app.run(host="0.0.0.0", port=8000)
