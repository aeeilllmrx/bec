import anthropic
import base64
import json
import os

from dotenv import load_dotenv

load_dotenv()


def get_item_and_price(name):
    image_path = f"menus/{name}_menu.png"
    api_key = os.environ["CLAUDE_API_KEY"]
    client = anthropic.Anthropic(api_key=api_key)

    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

    system_content = (
        "You must respond in valid JSON format with keys 'item' and 'price'."
    )
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": encoded_image,
                    },
                },
                {
                    "type": "text",
                    "text": """
                        Please look at this photo of a menu and answer the following questions:
                        1. Is there a egg and cheese sandwich on the menu?
                        2. If yes, how much does it cost?
                        Return your answer in JSON format with keys 'item' and 'price'. 
                        If there is no egg and cheese sandwich on the menu, return None as the value for both fields.
                    """,
                },
            ],
        },
    ]

    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1000,
        messages=messages,
        system=system_content,
    )
    try:
        result = json.loads(response.content[0].text)
        return result["item"], result["price"]
    except:
        return None, None
