import os
from dotenv import load_dotenv

load_dotenv()


def fontawesome_token(request):
    FONTAWESOME_TOKEN = os.getenv('FONTAWESOME_TOKEN')
    return {'FONTAWESOME_TOKEN': FONTAWESOME_TOKEN}
