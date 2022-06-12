# from fastapi import FastAPI
# from typing import Optional
#
# app = FastAPI()
#
# @app.get("/")
# async def root():
#     return {"message": "Hello World"}
#
# @app.get("/hello")
# async def hello():
#     return 'hello'
#
# @app.get("/echo/{items_id}")
# async def echo(item_id: str, q: Optional[str] = None):
#     if q:
#         return {"item_id": item_id, "q": q}
#     return {"item_id": item_id}
def fib(n):
    fib_0, fib_1 = 0, 1
    for _ in range(n - 1):
        fib_0, fib_1 = fib_1, (fib_0 + fib_1) % 10
    return fib_1


def main():
    n = int(input())
    print(fib(n))


if __name__ == "__main__":
    main()