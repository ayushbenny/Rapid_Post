from rapid_post import RapidPost


url = "https://jsonplaceholder.typicode.com/posts"
payload = {
    "title": "Sample Post",
    "body": "This is a sample post using the JSONPlaceholder API.",
    "userId": 1,
    "amount": 22.04,
}
instance = RapidPost(url=url, payload=payload, request_type="POST", auto_rapid_db=True)
