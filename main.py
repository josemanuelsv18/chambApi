from typing import Union
from fastapi import FastAPI

class Main:
    def __init__(self):
        self.app = FastAPI()

if __name__ == "__main__":
    app = Main()
    app.main()