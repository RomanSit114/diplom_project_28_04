import requests


class TelegramClient:
    TOKEN = '6380471666:AAFi2YUEeNo5AytrptRJ-eiPVI99n1AT4Jc'
    CHAT_ID = '1038982189'

    def send_message(self, message):
        url = f'https://api.telegram.org/bot{self.TOKEN}/sendMessage?chat_id={self.CHAT_ID}&text={message}'

        response = requests.get(url)

        if response.status_code == 200:
            return {
                'status': 'success'
            }
        
        return {
            'status': 'error'
        }
    
    def handle_feedback_form(self, user_name: str, user_mail: str, user_city: str, user_message: str):
        message = f'''
            Пользователь {user_name} оставил  заявку из города {user_city}:\n{user_message}\nПочта для связи:{user_mail}
        '''
        return self.send_message(message)
    