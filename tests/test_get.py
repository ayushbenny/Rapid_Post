from rapid_post_folder import RapidGet

payload = {
    "table_name": "test",
}
filter_data = {"title": "Sample Post", "amount": 1004.3}
instance = RapidGet(payload=payload, filters=True, filter_data=filter_data)
