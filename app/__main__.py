from app import logger
from app.bq_stream_writer import run_bq_stream


def main() -> None:
    logger.info("running app...")
    run_bq_stream()
    logger.info("exiting app...")


if __name__ == "__main__":
    main()
