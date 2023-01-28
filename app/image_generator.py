from config import config_init, Config
import os
import shutil
import requests
import openai
from tqdm import tqdm

class ImageGenerator:
    def __init__(self) -> None:
        config_init()
        openai.api_key = Config.API_KEY_OPEN_AI

        self.__image_prompt: str = ""
        self.__image_size: str = ""
        self.__image_request_response = None

    def start_message(self) -> None:
        [print("\n") for i in range(3)]
        print(".......... Welcome to [AI Image Generator] ..........")

    def get_image_prompt_from_user(self) -> None:
        while True:
            self.__image_prompt = input("\n> Enter prompt for image: ")

            try:
                self.__validate_image_prompt()
            except _InvalidImagePromptLength as error_prompt_length:
                print(error_prompt_length)
                continue

            break

    def __validate_image_prompt(self) -> None:
        if len(self.__image_prompt) < Config.IMAGE_PROMPT_MIN_CHARACTERS_NUMBER:
            raise _InvalidImagePromptLength()

    def get_image_size_from_user(self) -> None:
        while True:
            print("\n>>> Image size options:")

            for index, image_size in enumerate(Config.IMAGE_SIZES):
                print(f"{index + 1}. {image_size}")

            self.__image_size = input("> Enter image size: ")

            try:
                self.__validate_image_size()
            except _InvalidImageSize as error_image_size:
                print(error_image_size)
                continue

            self.__image_size = Config.IMAGE_SIZES[int(self.__image_size) - 1]
            break

    def __validate_image_size(self) -> None:
        if len(self.__image_size) != 1:
            raise _InvalidImageSize()
        
        if not self.__image_size.isdigit():
            raise _InvalidImageSize()
        
        temp_image_size: int = int(self.__image_size)
        
        if temp_image_size not in range(1, len(Config.IMAGE_SIZES) + 1):
            raise _InvalidImageSize()

    def image_send_generate_request(self) -> None:
        request_response = None

        print("\n..... Sending request for following data: ")
        print(f"> Prompt: {self.__image_prompt}")
        print(f"> Image size: {self.__image_size}")

        try:
            request_response = openai.Image.create(
                prompt=self.__image_prompt,
                n=1,
                size=self.__image_size,
                response_format="url",
            )
        except openai.InvalidRequestError as error_invalid_request:
            raise InvalidPromptRequest(error_invalid_request.__str__())
        except openai.APIError as error_api:
            raise APIError(error_api.__str__())
        except openai.OpenAIError as error_open_ai:
            raise OpenAIError(error_open_ai.__str__())
        
        self.__image_request_response = request_response

    def image_download(self) -> None:
        image_url: str = ""

        if isinstance(self.__image_request_response, dict):
            image_url = self.__image_request_response["data"][0]["url"]
        else:
            raise UnknowException()

        image_name: str = f"output_{Config.DIR_OUTPUT_FILES_COUNT + 1}.png"
        image_filepath: str = os.path.join(Config.DIR_OUTPUT, image_name)

        print("\n..... Requesting image download")

        try:
            with requests.get(image_url, stream=True) as request:
                total_length = int(request.headers.get("content-length", 0))
                
                print("..... Downloading image\n")

                with tqdm.wrapattr(request.raw, "read", total=total_length, desc="") as raw:
                    with open(image_filepath, 'wb') as image_file:
                        shutil.copyfileobj(raw, image_file)

                Config.DIR_OUTPUT_FILES_COUNT += 1
                print(f"\n[V] Image downloaded (file: {image_name}, dir: {image_filepath})")

        except requests.exceptions.Timeout as error_request_timeout:
            raise RequestTimeout(error_request_timeout.__str__())
        except requests.exceptions.TooManyRedirects as error_request_redirects:
            raise RequestRedirectsOverload(error_request_redirects.__str__())
        except requests.exceptions.RequestException as error_request:
            raise RequestsException(error_request.__str__())

class _ImageGeneratorException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def __str__(self) -> str:
        return "\nImageGeneratorException:"
    
class UnknowException(_ImageGeneratorException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def __str__(self) -> str:
        return f"{super().__str__()} Unknown error occured"
    
class _InvalidImagePromptLength(_ImageGeneratorException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def __str__(self) -> str:
        return f"{super().__str__()} InvalidImagePromptLength: Prompt has to be at least {Config.IMAGE_PROMPT_MIN_CHARACTERS_NUMBER} symbols."
    
class _InvalidImageSize(_ImageGeneratorException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def __str__(self) -> str:
        return f"{super().__str__()} InvalidImageSize: Image size is invalid or empty."
    
class _OpenAIException(_ImageGeneratorException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def __str__(self) -> str:
        return f"{super().__str__()} OpenAIException:"
    
class InvalidPromptRequest(_OpenAIException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.__args = args

    def __str__(self) -> str:
        return f"{super().__str__()} InvalidRequest: {self.__args[0]}"
    
class APIError(_OpenAIException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.__args = args

    def __str__(self) -> str:
        return f"{super().__str__()} APIError: {self.__args[0]}"
    
class OpenAIError(_OpenAIException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.__args = args

    def __str__(self) -> str:
        return f"{super().__str__()} OpenAIError: {self.__args[0]}"
    
class RequestsException(_ImageGeneratorException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def __str__(self) -> str:
        return f"{super().__str__()} RequestsException:"
    
class RequestTimeout(RequestsException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.__args = args

    def __str__(self) -> str:
        return f"{super().__str__()} RequestTimeout: {self.__args[0]}"
    
class RequestRedirectsOverload(RequestsException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.__args = args

    def __str__(self) -> str:
        return f"{super().__str__()} RequestRedirectsOverload: {self.__args[0]}"