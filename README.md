# Send emails from Yandex Cloud Postbox (postbox-sender.py). 
1. Use Yandex Cloud enviroment variables:
- **AWS_ACCESS_KEY_ID** - Yandex Cloud Service Account (SA) static access key
- **AWS_SECRET_ACCESS_KEY** - Yandex Cloud Service Account (SA) static access key secret
- **FROM** - your email address from Yandex Postbox verified domain
- **LIST_ID** - [RFC2919](https://datatracker.ietf.org/doc/html/rfc2919) comliant list id 
- **UNSUBSCRIBE_LINK** - Yandex Cloud Function link to unsubscribe
- **UNSUBSCRIBE_MAIL** - Yandex Cloud Email Trigger to unsubscribe
2. Attach Object Storage to Cloud Function with **bucket** mount point (or change file paths/names inside this code)
3. Use **bulkemail.xlsx** excel examble and **blacklist.xlsx** for restricted emails

# Unsubcribe Cloud Function (postbox-unsubscribe.py).
Append usubcribed emails to **blacklist.xlsx**. 
1. Attach Object Storage to Cloud Function with **bucket** mount point (or change file paths/names inside this code) and **disable read-only mode**.
2. Execute with URL params: _email_ (appended email) and _l_ (email list). I.e. https://functions.yandexcloud.net/d4sdxfer4243sdxfcvfr?email=a@example.com&l=demolist.example.com

[How to use video](https://yandex.cloud/ru/events/878)
