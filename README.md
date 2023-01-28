# AI-Image-Generator

AI-Image-Generator is a Python script for generating AI-images (runs with OpenAI API).

## Usage

Copy ```.env.example``` into ```.env``` and fill in all required data. 

```python
API_KEY_OPEN_AI=YOUR_OPEN_AI_API_KEY
...
```

Poetry (https://python-poetry.org) is used for dependency management, Python 3.11 is required.

Dependencies installation and program run:
```shell
poetry install
cd ai_image_generator
poetry run python -m img_generator
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)