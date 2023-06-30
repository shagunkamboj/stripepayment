import stripe
stripe.api_key = 'sk_test_51NKwuYSErS4Hkbpk3Nh4Lvv0nrkykCJOaWJy8qAXmdudVjDQIoKVQaq5KZAgfkzP55Vnou2ZWnEPkZSQAF7mHjcG00ZFF1tCov'


stripe.PaymentIntent.create(
  amount=2000,
  currency="usd",
  automatic_payment_methods={"enabled": True},
  confirm = True
)