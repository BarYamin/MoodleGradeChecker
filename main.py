import moodle_api as m
import warnings
warnings.filterwarnings("ignore")

DEFAULT_URL = "moodle2.bgu.ac.il"

url = input(f"Enter your moodle's base url (default {DEFAULT_URL}):")
user = input("Enter username:")
password = input("Enter password:")

client = m.MoodleClient(url if url else DEFAULT_URL, user, password)

while True:
    class_id = int(input("Class ID:"))
    class_info = client.get_class_info(class_id)

    if len(class_info) > 0:
        print("==================================")
        print(f"[+] Info for Class ID {class_id}")
        for info in class_info:
            print(f"\t[-] Max Grade: {info['sumgrades']}")
            print(f"\t[-] Grade: {100*info['grade']/info['sumgrades']}")
            print("==================================")

