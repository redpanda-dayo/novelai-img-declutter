import logging
logging.basicConfig(level=logging.INFO)

import asyncio
import sys
import os
import pathlib

from dotenv import load_dotenv
from pydantic import SecretStr

from novelai_python import APIError, LoginCredential, JwtCredential, ImageGenerateResp
from novelai_python import AugmentImageInfer
from novelai_python.sdk.ai.augment_image import ReqType, Moods


async def generate(
        image,
        request_type: ReqType = ReqType.SKETCH,
):
    jwt = os.getenv("NOVELAI_JWT", None)
    if jwt is None:
        raise ValueError("NOVELAI_JWT is not set in `.env` file, please create one and set it")
    credential = JwtCredential(jwt_token=SecretStr(jwt))
    """Or you can use the login credential to get the renewable jwt token"""
    # _login_credential = LoginCredential(
    #     username=os.getenv("NOVELAI_USER"),
    #     password=SecretStr(os.getenv("NOVELAI_PASS"))
    # )
    try:
        agent = AugmentImageInfer.build(
            req_type=request_type,
            image=image,
            # mood=Moods.Shy,
            prompt="",
            defry=0,
        )
        print(f"charge: {agent.calculate_cost(is_opus=True)} if you are vip3")
        # print(f"charge: {agent.calculate_cost(is_opus=False)} if you are not vip3")
        result = await agent.request(
            session=credential
        )
    except APIError as e:
        print(f"Error: {e.message}")
        return None
    else:
        print(f"Meta: {result.meta}")
    _res: ImageGenerateResp
    file = result.files[0]
    with open(f"{pathlib.Path(image).stem}_declutter.png", "wb") as f:
        f.write(file[1])

def main():
    if len(sys.argv) < 2:
        print("Please specify the file path as an argument.")
        return

    input_path = sys.argv[1]
    absolute_path = os.path.abspath(input_path)
    if not os.path.exists(absolute_path):
        print("The file does not exist.")
        return

    load_dotenv()
    loop = asyncio.new_event_loop()
    loop.run_until_complete(
        generate(
            # image=pathlib.Path(__file__).parent / "static_image.png",
            image=pathlib.Path(absolute_path),
            request_type=ReqType.DECLUTTER
        )
    )

if __name__ == "__main__":
    main()


# https://github.com/LlmKira/novelai-python/blob/main/src/novelai_python/sdk/ai/augment_image/_enum.py

# from enum import Enum


# class ReqType(Enum):
#     """
#     typing.Literal["bg-removal", "colorize", "lineart", "sketch", "emotion", "declutter"]
#     """
#     BG_REMOVAL = "bg-removal"
#     COLORIZE = "colorize"
#     LINEART = "lineart"
#     SKETCH = "sketch"
#     EMOTION = "emotion"
#     DECLUTTER = "declutter"


# class Moods(Enum):
#     """
#     The mood of the character in the image
#     """
#     Neutral = "neutral"
#     Happy = "happy"
#     Saf = "sad"
#     Angry = "angry"
#     Scared = "scared"
#     Surprised = "surprised"
#     Tired = "tired"
#     Excited = "excited"
#     Nervous = "nervous"
#     Thinking = "thinking"
#     Confused = "confused"
#     Shy = "shy"
#     Disgusted = "disgusted"
#     Smug = "smug"
#     Bored = "bored"
#     Laughing = "laughing"
#     Irritated = "irritated"
#     Aroused = "aroused"
#     Embarrassed = "embarrassed"
#     Worried = "worried"
#     Love = "love"
#     Determined = "determined"
#     Hurt = "hurt"
#     Playful = "playful"
