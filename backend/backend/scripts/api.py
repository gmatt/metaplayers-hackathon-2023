import uvicorn


def main():
    uvicorn.run("backend.api.api:app")


if __name__ == "__main__":
    main()
