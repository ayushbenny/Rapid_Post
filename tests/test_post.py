from rapid_post_folder import RapidPost


url = "https://jsonplaceholder.typicode.com/posts"
payload = {
    "title": "Rapid Post",
    "body": "Hello API, how are you.",
    "userId": 2,
    "amount": 12.04,
}
instance = RapidPost(url=url, payload=payload, request_type="POST", auto_rapid_db=True)
