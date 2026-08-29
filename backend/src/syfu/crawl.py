from searxng_wrapper import SearxngWrapper

if __name__ == "__main__":
    client = SearxngWrapper(
            base_url="",
    )

    result = client.search(
    )

    print(result)
