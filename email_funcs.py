def generate_email_body(news_stories):
    if not news_stories:
        return "No results found."

    body = "Here are today's top news stories:\n\n"
    for story in news_stories:
        body += f"- {story['title']} ({story['source']})\n  {story['url']}\n\n"
    return body