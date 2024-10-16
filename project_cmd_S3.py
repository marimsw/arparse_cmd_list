#!/usr/bin/env python
# coding: utf-8

import os
import subprocess
import sys
import urllib3
from pathlib import Path

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Функция для проверки и установки необходимых библиотек
def check_and_install(package):
    try:
        __import__(package)
    except ImportError:
        print(f"Установка библиотеки {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])



# Проверка и установка необходимых библиотек
check_and_install('python-dotenv')
check_and_install('boto3')
check_and_install('pyzipper')
check_and_install('requests')

import argparse
import zipfile
import pyzipper
import getpass
import requests
import urllib.parse
import boto3
import tempfile
import shutil
from dotenv import load_dotenv
from botocore.exceptions import ClientError

# Проверка и установка необходимых библиотек
check_and_install('python-dotenv')
check_and_install('boto3')
check_and_install('pyzipper')
check_and_install('requests')


# Проверка и установка библиотеки pyzipper
# try:
#     import pyzipper
# except ImportError:
#     print("Установка библиотеки pyzipper...")
#     subprocess.check_call([sys.executable, "-m", "pip", "install", "pyzipper"])
#     import pyzipper  # Импортируем библиотеку после установки
#
#
# # Проверка и установка библиотеки requests
# try:
#     import requests
# except ImportError:
#     print("Установка библиотеки requests...")
#     subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
#     import requests  # Импортируем библиотеку после установки




load_dotenv()

class S3Handler:
    """Базовый методы для работы с S3:\n
    - скачивание файла из S3;\n
    - скачивание всех файлов из директрии S3;\n
    - загрузка в S3 файла;\n
    - загрузка в S3 всей директории."""
    def __init__(self, aws_access_key_id=None, aws_secret_access_key=None, endpoint_url=None, verify=False):
        """Инициализация соединения с S3 с возможностью передачи ключей через параметры."""
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id or os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=aws_secret_access_key or os.getenv('AWS_SECRET_ACCESS_KEY'),
            endpoint_url=endpoint_url or os.getenv('S3_ENDPOINT_URL'),
            verify=verify  # По умолчанию, верификация отключена
        )

    def download_file(self, bucket_name, s3_file_path, local_directory):
        """Скачивает файл из S3 в указанную локальную директорию, сохраняя его оригинальное имя."""
        try:
            # Получаем имя файла из полного пути на S3
            file_name = os.path.basename(s3_file_path)

            # Формируем полный путь для сохранения файла в локальной директории
            local_file_path = os.path.join(local_directory, file_name)

            if not os.path.exists(local_directory):
                os.makedirs(local_directory)

            # Скачиваем файл из S3
            self.s3.download_file(bucket_name, s3_file_path, local_file_path)
            print(f"Файл {s3_file_path} скачан успешно в {local_file_path} ")

        except ClientError as e:
            print(f"Error downloading {s3_file_path}: {e}")
        except OSError as e:
            print(f"OS error occurred: {e}")

    def download_directory(self, bucket_name, s3_directory_path, local_directory):
        """Скачивает все файлы из указанной директории в S3 в локальную директорию."""
        try:
            # Получаем список всех файлов в указанной директории
            files = self.list_files_in_directory(bucket_name, s3_directory_path)

            if not os.path.exists(local_directory):
                os.makedirs(local_directory)

            for file_key in files:
                # Проверяем, является ли file_key файлом или директорией
                if file_key.endswith('/'):
                    # Пропускаем директории
                    continue

                # Вычисляем локальный путь для сохранения файла с учетом вложенности
                local_file_path = os.path.join(local_directory, os.path.relpath(file_key, s3_directory_path))
                # Создаем директории для вложенных файлов, если их нет
                local_file_dir = os.path.dirname(local_file_path)

                if not os.path.exists(local_file_dir):
                    os.makedirs(local_file_dir)

                # Используем NamedTemporaryFile для предотвращения ошибок на Windows
                with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                    temp_file_path = tmp_file.name
                # Скачиваем файл во временное место
                self.s3.download_file(bucket_name, file_key, temp_file_path)
                # Копируем временный файл в нужное место
                shutil.copy(temp_file_path, local_file_path)
                # Удаляем временный файл
                os.remove(temp_file_path)
                print(f"Файл {file_key} скачан успешно в {local_file_path} !")
                
            #print(f"Директория {s3_directory_path} скачана успешно!")
            print(f"Директория {s3_directory_path} скачана успешно в {local_directory} !")
                
        except ClientError as e:
            print(f"Error downloading directory {s3_directory_path}: {e}")
        except OSError as e:
            print(f"OS error occurred: {e}")

    def upload_file(self, local_file_path, bucket_name, s3_directory):
        """Загружает файл в S3 в указанную директорию, сохраняя его оригинальное имя.\n
        s3_directory должна заканчиваться на '/'"""
        try:
            # Получаем имя файла из локального пути
            file_name = os.path.basename(local_file_path)

            # Формируем полный путь для сохранения файла в S3
            s3_file_path = os.path.join(s3_directory, file_name)
            print(f"Загрузка файла {local_file_path} в S3...")

            # Загружаем файл в S3
            self.s3.upload_file(local_file_path, bucket_name, s3_file_path)
            print(f"Файл {local_file_path} успешно загружен в S3!")

        except ClientError as e:
            print(f"Error uploading {local_file_path}: {e}")

    def upload_directory(self, local_directory_path, bucket_name, s3_directory_path):
        """Загружает все файлы из локальной директории в S3."""
        try:
            print(f"Загрузка директории {local_directory_path}...")
            for root, dirs, files in os.walk(local_directory_path):
                for file in files:
                    local_file_path = os.path.join(root, file)

                    # Получаем относительный путь относительно локальной директории
                    relative_path = os.path.relpath(local_file_path, local_directory_path)

                    # Формируем корректный путь на S3
                    s3_file_path = os.path.join(s3_directory_path, relative_path).replace("\\", "/")
                    
                    print(f"Загрузка файла {local_file_path}...")

                    # Загружаем файл с сохранением его оригинального пути
                    self.s3.upload_file(local_file_path, bucket_name, s3_file_path)
                    print(f"Файл {local_file_path} загружен успешно!")
                    
            print(f"Директория {local_directory_path} загружена успешно!")   
                
        except ClientError as e:
            print(f"Error uploading directory {local_directory_path}: {e}")

    def list_files_in_directory(self, bucket_name, s3_directory_path):
        """Возвращает список файлов в директории S3 (исключает префиксы/папки)."""
        try:
            paginator = self.s3.get_paginator('list_objects_v2')
            file_list = []
            print(f"Считывание файлов в директории {s3_directory_path}...")
            for result in paginator.paginate(Bucket=bucket_name, Prefix=s3_directory_path):
                if 'Contents' in result:
                    for obj in result['Contents']:
                        # print(obj['Key'])
                        if not obj['Key'].endswith('/'):
                            file_list.append(obj['Key'])
            #print(f"Файлы в директории {s3_directory_path} успешно прочитаны!")
            print("Список файлов в директории:")
            for file in file_list:
                print(file)
            print(f"Файлы в директории {s3_directory_path} успешно прочитаны!")
            return file_list

        except ClientError as e:
            print(f"Error listing files in directory {s3_directory_path}: {e}")
            return []

# Лучшие веса
    def extract_best_weights(self, local_archive_path, weights_folder, delete_archives=False):
        """Разархивирует лучшие (best) веса."""
        os.makedirs(weights_folder, exist_ok=True)

        for archive in os.listdir(local_archive_path):
            archive_path = os.path.join(local_archive_path, archive)

            # Проверяем, является ли файл ZIP архивом
            if zipfile.is_zipfile(archive_path):
                with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                    for file in zip_ref.namelist():
                        if file.endswith('best.pt'):
                            output_path = os.path.join(weights_folder, f"{Path(archive_path).stem}.pt")
                            
                            if not os.path.exists(output_path):
                                zip_ref.extract(file, weights_folder)
                                os.rename(os.path.join(weights_folder, file), output_path)
                                print(f"Извлечен {file} в {output_path}")
                            else:
                                print(f"Файл веса уже существует: {output_path}")

                # Удаляем архив, если установлен флаг
                if delete_archives:
                    os.remove(archive_path)
                    print(f"Deleted archive: {archive}")



# Список папок в директории
def dataset_list(directory):
    try:
        folders = [folder for folder in os.listdir(directory) if os.path.isdir(os.path.join(directory, folder))]
        if folders:
            print(f"Folders in directory '{directory}':")
            for folder in folders:
                print(folder)
        else:
            print(f"No folders found in directory '{directory}'.")
    except FileNotFoundError:
        print(f"Directory '{directory}' not found.")
    except PermissionError:
        print(f"No access to directory '{directory}'.")


# Удаление файла
def dataset_clear(file_path):
    try:
        # Проверяем, является ли путь файлом
        if os.path.isfile(file_path):
            os.remove(file_path)  # Удаляем файл
            print(f"Файл '{file_path}' успешно удален.")
        else:
            print(f"'{file_path}' не является файлом или не существует.")
    except FileNotFoundError:
        print(f"Ошибка: Файл '{file_path}' не найден.")
    except PermissionError:
        print(f"Ошибка: У вас нет прав для удаления файла '{file_path}'.")
    except Exception as e:
        print(f"Произошла ошибка при удалении файла '{file_path}': {e}")


# Распаковка ZIP-архива
def unzip_file(zip_file_path, extract_to):
    try:
        # Проверяем, существует ли ZIP-файл
        if not os.path.exists(zip_file_path):
            raise FileNotFoundError(f"Файл {zip_file_path} не найден.")

        # Проверяем, является ли файл ZIP-архивом
        if not zipfile.is_zipfile(zip_file_path):
            raise zipfile.BadZipFile(f"Файл {zip_file_path} не является ZIP-архивом.")

        # Запрашиваем пароль у пользователя
        password = getpass.getpass("Введите пароль для ZIP-архива(если есть): ")

        # Открываем ZIP-архив
        with pyzipper.AESZipFile(zip_file_path, 'r') as zip_ref:
            # Устанавливаем пароль
            zip_ref.pwd = password.encode('utf-8')

            # Извлекаем все содержимое
            zip_ref.extractall(extract_to)
            print(f"Файлы успешно извлечены в {extract_to}")

    except FileNotFoundError as e:
        print(f"Ошибка: {e}")
    except zipfile.BadZipFile as e:
        print(f"Ошибка: {e}")
    except RuntimeError as e:
        if 'Bad password' in str(e):
            print("Ошибка: Неверный пароль для ZIP-архива.")
        else:
            print(f"Ошибка: {e}")
    except PermissionError:
        print("Ошибка: У вас нет разрешения на запись в указанную директорию.")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")


# Скачивание ZIP-архива по ссылке с S3
def download_archive(url, file_name, save_path):
    try:
        # Кодирование ссылки для правильной обработки символов и русских букв
        encoded_url = urllib.parse.quote(url, safe=':/?=&%')
        response = requests.get(encoded_url, stream=True)
        response.raise_for_status()  # Проверяем, что запрос был успешным
        full_path = os.path.join(save_path, file_name)
        if os.path.exists(full_path):
            print("Файл с таким именем уже существует. Хотите перезаписать его? (y/n)")
            answer = input().lower()
            if answer != 'y':
                print("Скачивание отменено.")
                return
        with open(full_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        print(f"Архив скачан успешно: {full_path}")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса: {e}")

def main():
    parser = argparse.ArgumentParser(description='Утилита для работы с файлами и папками')
    subparsers = parser.add_subparsers(dest='command')

    list_parser = subparsers.add_parser('list', help='Список папок в директории')
    list_parser.add_argument('directory', help='Путь к директории')

    clear_parser = subparsers.add_parser('clear', help='Удаление файла')
    clear_parser.add_argument('file_path', help='Путь к файлу')

    unzip_parser = subparsers.add_parser('unzip', help='Распаковка ZIP-архива')
    unzip_parser.add_argument('zip_file_path', help='Путь к ZIP-файлу')
    unzip_parser.add_argument('extract_to', help='Директория для извлечения')

    download_parser = subparsers.add_parser('download', help='Скачивание ZIP-архива')
    download_parser.add_argument('url', help='Ссылка на ZIP-архив')
    download_parser.add_argument('file_name', help='Имя файла для сохранения архива')
    download_parser.add_argument('save_path', help='Путь для сохранения архива')

    s3_download_parser = subparsers.add_parser('s3_download', help='Скачивание файла из S3')
    s3_download_parser.add_argument('bucket_name', help='Имя бакета S3')
    s3_download_parser.add_argument('s3_file_path', help='Путь к файлу в S3')
    s3_download_parser.add_argument('local_directory', help='Локальная директория для скачивания файла')

    s3_download_directory_parser = subparsers.add_parser('s3_download_directory', help='Скачивание директории из S3')
    s3_download_directory_parser.add_argument('bucket_name', help='Имя бакета S3')
    s3_download_directory_parser.add_argument('s3_directory_path', help='Путь к директории в S3')
    s3_download_directory_parser.add_argument('local_directory', help='Локальная директория для скачивания директории')

    s3_upload_parser = subparsers.add_parser('s3_upload', help='Загрузка файла в S3')
    s3_upload_parser.add_argument('local_file_path', help='Локальный путь к файлу')
    s3_upload_parser.add_argument('bucket_name', help='Имя бакета S3')
    s3_upload_parser.add_argument('s3_directory', help='Путь к директории в S3')

    s3_upload_directory_parser = subparsers.add_parser('s3_upload_directory', help='Загрузка директории в S3')
    s3_upload_directory_parser.add_argument('local_directory_path', help='Локальный путь к директории')
    s3_upload_directory_parser.add_argument('bucket_name', help='Имя бакета S3')
    s3_upload_directory_parser.add_argument('s3_directory_path', help='Путь к директории в S3')

    s3_list_parser = subparsers.add_parser('s3_list', help='Список файлов в директории S3')
    s3_list_parser.add_argument('bucket_name', help='Имя бакета S3')
    s3_list_parser.add_argument('s3_directory_path', help='Путь к директории в S3')


    best_weights_parser = subparsers.add_parser('best_weights', help='Извлечение лучших весов')
    best_weights_parser.add_argument('local_archive_path', help='Локальный путь к архиву')
    best_weights_parser.add_argument('weights_folder', help='Папка для сохранения весов')
    best_weights_parser.add_argument('--delete_archives', action='store_true', help='Удалить архивы после извлечения')

    args = parser.parse_args()
    s3_handler = S3Handler()
    if args.command == 'list':
        dataset_list(args.directory)
    elif args.command == 'clear':
        dataset_clear(args.file_path)
    elif args.command == 'unzip':
         unzip_file(args.zip_file_path, args.extract_to)
    elif args.command == 'download':
        download_archive(args.url, args.file_name, args.save_path)
    elif args.command == 's3_download':
        s3_handler.download_file(args.bucket_name, args.s3_file_path, args.local_directory)
    elif args.command == 's3_download_directory':
        s3_handler.download_directory(args.bucket_name, args.s3_directory_path, args.local_directory)
    elif args.command == 's3_upload':
        s3_handler.upload_file(args.local_file_path, args.bucket_name, args.s3_directory)
    elif args.command == 's3_upload_directory':
        s3_handler.upload_directory(args.local_directory_path, args.bucket_name, args.s3_directory_path)

    elif args.command == 's3_list':
        s3_handler.list_files_in_directory(args.bucket_name, args.s3_directory_path)

    elif args.command == 'best_weights':
        s3_handler.extract_best_weights(args.local_archive_path, args.weights_folder, args.delete_archives)

if __name__ == '__main__':
    main()
