from rapid_post_folder import RapidGet

payload = {
    "table_name": "test",
}
filter_data = {"filter": "userId=2 AND id=4"}
instance = RapidGet(
    payload=payload,
    filters=True,
    filter_data_payload=filter_data,
)
