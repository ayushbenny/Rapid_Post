from rapid_post_folder import RapidUpdate


data_id = {"id": 4}
table_name = {"table_name": "test"}
payload = {
    "amount": 12345,
}
instance = RapidUpdate(
    id=data_id,
    table_name=table_name,
    payload=payload,
    method="PATCH",
)
