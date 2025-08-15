import requests
import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from datetime import datetime

# PredictHQ API
API_KEY = "TU_WKLEJ_SWÓJ_PREDICTHQ_API_TOKEN"
API_URL = "https://api.predicthq.com/v1/events/?category=expos"

# Email setup
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_FROM = "twoj_mail@gmail.com"
EMAIL_TO = "potega.adam@gmail.com"
EMAIL_PASSWORD = "twoje_hasło_do_aplikacji"  # Użyj "App Password" z Gmail

# Pobierz dane z API
response = requests.get(API_URL, headers={"Authorization": f"Bearer {API_KEY}"})
print("Status Code:", response.status_code)
print("API Response:", response.text)
events = response.json()

# Filtrowanie eventów z Europy
countries_of_interest = {"DE", "BE", "NL", "IT", "FR", "GB", "PL", "SE", "ES", "RU"}
filtered_events = [event for event in events["results"] if event["country"] in countries_of_interest]

# Zapis do CSV
csv_file = "european_events.csv"
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=["title", "country", "start", "end", "phq_attendance", "location"])
    writer.writeheader()
    for event in filtered_events:
        writer.writerow({
            "title": event["title"],
            "country": event["country"],
            "start": event["start"],
            "end": event["end"],
            "phq_attendance": event["phq_attendance"],
            "location": event["geo"]["address"]["formatted_address"]
        })

# Wysyłka maila
msg = MIMEMultipart()
msg['From'] = EMAIL_FROM
msg['To'] = EMAIL_TO
msg['Subject'] = f"Daily European Events Report - {datetime.now().strftime('%Y-%m-%d')}"

body = "Hi Adam,\n\nAttached is your daily report of European events.\n\nBest regards,\nYour PredictHQ Bot"
msg.attach(MIMEText(body, 'plain'))

with open(csv_file, "rb") as attachment:
    part = MIMEApplication(attachment.read(), Name=csv_file)
    part['Content-Disposition'] = f'attachment; filename="{csv_file}"'
    msg.attach(part)

with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
    server.starttls()
    server.login(EMAIL_FROM, EMAIL_PASSWORD)
    server.send_message(msg)
