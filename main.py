import asyncio
import shutil
from pathlib import Path
import logging
from argparse import ArgumentParser

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="logger.log",
    filemode="w",
    encoding="utf-8",
)
logger = logging.getLogger()

# Обробка аргументів командного рядка
parser = ArgumentParser(description="Асинхронний сортувальник файлів за розширенням")
parser.add_argument("source", type=str, help="Шлях до вихідної папки")
parser.add_argument("output", type=str, help="Шлях до цільової папки")
args = parser.parse_args()

source_folder = Path(args.source).resolve()
output_folder = Path(args.output).resolve()

if not source_folder.exists() or not source_folder.is_dir():
    logger.error("Вихідна папка не існує або це не директорія.")
    raise FileNotFoundError("Вихідна папка не існує або це не директорія.")

output_folder.mkdir(parents=True, exist_ok=True)


async def read_folder(source: Path):
    tasks = []
    for item in source.iterdir():
        if item.is_dir():
            tasks.append(read_folder(item))
        elif item.is_file():
            tasks.append(copy_file(item))
        else:
            logger.warning(f"Пропущено: {item}")
    await asyncio.gather(*tasks)


async def copy_file(file: Path):
    try:
        ext = file.suffix.lower()
        if not ext:
            ext = "unknown"

        target_folder = output_folder / ext.strip(".")
        target_folder.mkdir(parents=True, exist_ok=True)

        target_file = target_folder / file.name
        shutil.copy2(file, target_file)
        logger.info(f"Скопійовано: {file} -> {target_file}")
    except Exception as e:
        logger.error(f"Помилка копіювання {file}: {e}")


async def main():
    await read_folder(source_folder)


if __name__ == "__main__":
    asyncio.run(main())
