from bs4 import BeautifulSoup
from requests import session
import datetime

BASE_URL = "https://profile.intra.42.fr"


class Slotter:
    def __init__(self, session_id):
        self.sess = session()
        self.session_id = session_id

    def login(self):
        self.sess.cookies.update(
            {"_intra_42_session_production": self.session_id})
        resp = self.sess.get(
            f"{BASE_URL}/", allow_redirects=False)
        if resp.is_redirect:
            return False
        soup = BeautifulSoup(resp.text, "html.parser")
        csrf_meta = soup.find("meta", attrs={"name": "csrf-token"})
        self.sess.headers['X-Csrf-Token'] = csrf_meta.get("content")
        return True

    def take_slots(self, duration=30):
        start = datetime.datetime.now() + datetime.timedelta(minutes=60)
        while True:
            data = {
                "slot[begin_at]": start.strftime("%Y-%m-%dT%H:%M:%S"),
                "slot[end_at]": (start + datetime.timedelta(minutes=duration)).strftime("%Y-%m-%dT%H:%M:%S"),
            }
            resp = self.sess.post(
                f"{BASE_URL}/slots.json", data=data)
            payload = resp.json()
            if payload['message'].startswith('Has') or payload['message'].startswith('No overlapping!'):
                start += datetime.timedelta(minutes=30)
                continue
            elif payload['message'].startswith('Ending') and payload['status'] != 200:
                break
            start = datetime.datetime.strptime(payload.get(
                'data')['end'][:-6], '%Y-%m-%dT%H:%M:%S.%f')
            start += datetime.timedelta(minutes=30)
            print("Taking slots...", end='\r')

    def delete_slots(self):
        start = datetime.datetime.now()
        end = start + datetime.timedelta(minutes=60 * 24 * 30)
        resp = self.sess.get(f'{BASE_URL}/slots.json', params={
            "start": start.strftime("%Y-%m-%d"),
            "end": end.strftime("%Y-%m-%d")})
        slots = resp.json()
        if not slots:
            print("There's no slots to delete!")
            return
        for slot in slots:
            resp = self.sess.post(f"{BASE_URL}/slots/{slot['id']}.json", data={
                "ids": slot['ids'],
                "_method": "delete",
                "confirm": False
            })
            print("Deleting Slots...", end="\r")
