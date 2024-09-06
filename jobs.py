import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


regions = {
    "львівська": {
        "url": "https://www.msp.gov.ua/children/search.php?form=%D0%9D%D0%B0%D1%86%D1%96%D0%BE%D0%BD%D0%B0%D0%BB%D1%8C%D0%BD%D0%B5+%D1%83%D1%81%D0%B8%D0%BD%D0%BE%D0%B2%D0%BB%D0%B5%D0%BD%D0%BD%D1%8F&male=*&age_from=0&age_to=10&region=%D1%8C%D0%B2%D1%96%D0%B2%D1%81%D1%8C%D0%BA%D0%B0&brothers=no&needs=no",
        "expected_count": 10
    },
    "івано-франківська": {
        "url": "https://www.msp.gov.ua/children/search.php?form=%D0%9D%D0%B0%D1%86%D1%96%D0%BE%D0%BD%D0%B0%D0%BB%D1%8C%D0%BD%D0%B5+%D1%83%D1%81%D0%B8%D0%BD%D0%BE%D0%B2%D0%BB%D0%B5%D0%BD%D0%BD%D1%8F&male=*&age_from=0&age_to=10&region=%D1%80%D0%B0%D0%BD%D0%BA%D1%96%D0%B2%D1%81%D1%8C%D0%BA%D0%B0&brothers=no&needs=no&number=",
        "expected_count": 4
    },
    "тернопільська": {
        "url": "https://www.msp.gov.ua/children/search.php?form=%D0%9D%D0%B0%D1%86%D1%96%D0%BE%D0%BD%D0%B0%D0%BB%D1%8C%D0%BD%D0%B5+%D1%83%D1%81%D0%B8%D0%BD%D0%BE%D0%B2%D0%BB%D0%B5%D0%BD%D0%BD%D1%8F&male=*&age_from=0&age_to=10&region=%D0%B5%D1%80%D0%BD%D0%BE%D0%BF%D1%96%D0%BB%D1%8C%D1%81%D1%8C%D0%BA%D0%B0&brothers=no&needs=no&number=",
        "expected_count": 4
    },
    "закарпатська": {
        "url": "https://www.msp.gov.ua/children/search.php?form=%D0%9D%D0%B0%D1%86%D1%96%D0%BE%D0%BD%D0%B0%D0%BB%D1%8C%D0%BD%D0%B5+%D1%83%D1%81%D0%B8%D0%BD%D0%BE%D0%B2%D0%BB%D0%B5%D0%BD%D0%BD%D1%8F&male=*&age_from=0&age_to=10&region=%D0%B0%D0%BA%D0%B0%D1%80%D0%BF%D0%B0%D1%82%D1%81%D1%8C%D0%BA%D0%B0&brothers=no&needs=no&number=",
        "expected_count": 5
    },
    "волинська": {
        "url": "https://www.msp.gov.ua/children/search.php?form=%D0%9D%D0%B0%D1%86%D1%96%D0%BE%D0%BD%D0%B0%D0%BB%D1%8C%D0%BD%D0%B5+%D1%83%D1%81%D0%B8%D0%BD%D0%BE%D0%B2%D0%BB%D0%B5%D0%BD%D0%BD%D1%8F&male=*&age_from=0&age_to=10&region=%D0%BE%D0%BB%D0%B8%D0%BD%D1%81%D1%8C%D0%BA%D0%B0&brothers=no&needs=no&number=",
        "expected_count": 4
    },
    "рівненська": {
        "url": "https://www.msp.gov.ua/children/search.php?form=%D0%9D%D0%B0%D1%86%D1%96%D0%BE%D0%BD%D0%B0%D0%BB%D1%8C%D0%BD%D0%B5+%D1%83%D1%81%D0%B8%D0%BD%D0%BE%D0%B2%D0%BB%D0%B5%D0%BD%D0%BD%D1%8F&male=*&age_from=0&age_to=10&region=%D1%96%D0%B2%D0%BD%D0%B5%D0%BD%D1%81%D1%8C%D0%BA%D0%B0&brothers=no&needs=no&number=",
        "expected_count": 9
    }
}


current_date = datetime.now()


email_subject = "Child check"
smtp_server = 'smtp.gmail.com'
smtp_port = 587

to_email = "smolynets@gmail.com"
# "oksana.mavdryk25@gmail.com>"
from_email = "smolynets2@gmail.com"
# email_app_password = os.getenv("EMAIL_APP_PASSWORD")
email_app_password = "ayfj apks ygvq uyue "

def send_html_email(email_subject, to_email, from_email, email_app_password, region_messages):
    email_html_body = f"""
    <html>
    <body>
    <h1>{current_date.strftime("%d %B")} - Child check</h1>
    <ul>
    """
    for region, message in region_messages.items():
        email_html_body += f"<li><strong>{region}: {message}</strong></li>\n"
        email_html_body += "<br>"
    email_html_body += """
        </ul>
        </body>
        </html>
    """

    to_emails = ["smolynets@gmail.com", "oksana.mavdryk25@gmail.com"]

    # Create the MIME message
    message = MIMEMultipart()
    message['From'] = from_email
    message['To'] = ", ".join(to_emails)
    message['Subject'] = email_subject

    # Attach the HTML body with UTF-8 encoding
    message.attach(MIMEText(email_html_body, 'html', 'utf-8'))

    # Send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # Start TLS Encryption
        server.login(from_email, email_app_password)
        server.send_message(message)

def main(regions):
    email_messages = {}

    for region, data in regions.items():
        response = requests.get(data["url"])
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        child_items = soup.find_all('div', class_='child__item')

        child_list = []

        for item in child_items:
            url = item.find('a')['href']
            parsed_url = urlparse(url)
            query_params = parse_qs(parsed_url.query)
            number = query_params.get('n', [None])[0]
            child_list.append(number)

        region_count = len(child_list)
        print(f"{region}: {region_count}")
        if region_count > data["expected_count"]:
            email_messages[region] = f"кількість збільшилася на {region_count - data["expected_count"]}"
        if region_count < data["expected_count"]:
            email_messages[region] = f"кількість зменшилася на {data["expected_count"] - region_count}"

    if email_messages:
        region_messages = email_messages
    else:
        region_messages = {"Всі області": "змін немає"}

    send_html_email(email_subject, to_email, from_email, email_app_password, region_messages)


if __name__ == '__main__':
    main(regions)
