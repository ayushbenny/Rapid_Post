from rapid_post_folder import RapidUpdate


"""Need to provide all the columns and the values for PUT method annd in the \
PATCH method, just need to pass only the required field"""

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
