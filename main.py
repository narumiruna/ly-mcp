import asyncio

from lymcp.api_client import make_api_request


async def main() -> None:
    resp = await make_api_request("/bills/203110077970000")

    print(resp)


if __name__ == "__main__":
    asyncio.run(main())
