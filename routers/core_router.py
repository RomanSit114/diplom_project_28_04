from fastapi import APIRouter
from fastapi.responses import FileResponse
from utils.telegram_client import TelegramClient
from utils.calculator import Calculator
import json


core_routes = APIRouter()


@core_routes.get("/")
def main():
    return FileResponse("public/index.html")


@core_routes.get("/calculator")
def calculator():
    return FileResponse("public/calculator.html")


@core_routes.post("/send_message_to_telegram")
def send_mssage_to_tg(user_name: str, user_mail: str, user_city: str, user_message: str):
    client = TelegramClient()
    return client.handle_feedback_form(user_name, user_mail, user_city, user_message)


@core_routes.post("/send_calculation_info")
def send_calculation_info(rooms: str):
    calculator = Calculator()
    result = calculator.handle_calculation_form(json.loads(rooms))
    return result
