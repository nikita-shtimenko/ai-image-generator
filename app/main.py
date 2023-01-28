from app.image_generator import (
    ImageGenerator, 
    InvalidPromptRequest, 
    APIError, 
    OpenAIError,
    RequestTimeout, 
    RequestRedirectsOverload, 
    RequestsException,
    UnknowException
)

def main():
    img_generator: ImageGenerator = ImageGenerator()
    
    while True:
        img_generator.start_message()

        img_generator.get_image_prompt_from_user()
        img_generator.get_image_size_from_user()

        try:
            img_generator.image_send_generate_request()
        except InvalidPromptRequest as error_invalid_request:
            print(error_invalid_request)
            continue
        except APIError as error_api:
            print(error_api)
            continue
        except OpenAIError as error_open_ai:
            print(error_open_ai)
            continue

        try:
            img_generator.image_download()
        except RequestTimeout as error_request_timeout:
            print(error_request_timeout)
            continue
        except RequestRedirectsOverload as error_request_redirects:
            print(error_request_redirects)
            continue
        except RequestsException as error_request:
            print(error_request)
            continue
        except UnknowException as error_unknown:
            print(error_unknown)
            continue

if __name__ == "__main__":
    main()