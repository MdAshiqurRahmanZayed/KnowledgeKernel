import requests 
from django.conf import settings


def initiate_payment(amount, email, phone,course_id,user_id,current_site):
    url = "https://sandbox.sslcommerz.com/gwprocess/v4/api.php" # use the production URL for live payments
    payload = {
        'store_id': settings.STORE_ID,
        'store_passwd': settings.STORE_PASS,
        # 'course_id': course_id,
        'total_amount': amount,
        'currency': 'BDT',
        'tran_id': '1234dddsffsfdsfdssadf5',
        'success_url': f'http://{current_site}/{user_id}/{course_id}/payment/success/', # replace with your actual success URL
        'fail_url': f'http://{current_site}/{course_id}/payment/failure/', # replace with your actual failure URL
        'cancel_url': f'http://{current_site}/{course_id}/payment/cancel/', # replace with your actual cancel URL
        'cus_name': 'Customer Name',
        'cus_email': email,
        'cus_phone': phone,
        'cus_add1': 'Dhaka',
        'cus_city': 'Dhaka',
        'cus_country': 'Bangladesh',
        'shipping_method': 'NO',
        'product_name': 'Test Product',
        'product_category': 'Test Category',
        'product_profile': 'general',
        #
        'iframe_enabled': 'true',
    }

    response = requests.post(url, data=payload)
    # print(response)
    return response.json()
