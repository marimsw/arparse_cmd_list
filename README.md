Для работы с S3 хранилищем:

Использование переменных окружения: Вместо жесткого кодирования ключей доступа в коде, 
рассмотрите возможность использования переменных окружения:
(в терминале, в папке с кодом) 

export AWS_ACCESS_KEY_ID='ваш_ключ_доступа'
export AWS_SECRET_ACCESS_KEY='ваш_секретный_ключ'
export S3_ENDPOINT_URL='https://imb___.tech/'

Проверьте переменные окружения: Убедитесь, что переменные окружения AWS_ACCESS_KEY_ID и AWS_SECRET_ACCESS_KEY установлены правильно. Вы можете проверить это, выполнив следующую команду в терминале:

echo $AWS_ACCESS_KEY_ID
echo $AWS_SECRET_ACCESS_KEY
echo $S3_ENDPOINT_URL
===============================================================================================

Чтобы использовать скрипт в виде исполняемого файла, вы должны преобразовать его в формат py.
Вы можете сделать это, используя команду jupyter nbconvert в терминале:

jupyter nbconvert --to python msdis.ipynb

Замените msdis.ipynb на имя вашего файла Jupyter Notebook. Это создаст файл msdis.py


Команда sudo mv  kod.py /usr/local/bin/kod используется для перемещения файла kod.py в директорию /usr/local/bin и переименования его в kod
sudo mv kod.py /usr/local/bin/kod

==============================================================================================

Ошибка "Permission denied" означает, что у вас нет прав доступа к файлу или директории, которую вы пытаетесь использовать.

В данном случае, ошибка возникает, когда вы пытаетесь запустить файл msdis из директории /usr/local/bin.
Это может быть связано с тем, что права доступа к файлу msdis не установлены правильно.

Чтобы решить эту проблему, вы можете попробовать следующие шаги:

1. Проверьте права доступа к файлу kod:

ls -l /usr/local/bin/kod

Эта команда выведет информацию о правах доступа к файлу kod.

2. Измените права доступа к файлу kod:

sudo chmod 755 /usr/local/bin/kod

Эта команда установит права доступа к файлу kod так, чтобы он был доступен для чтения и запуска всем пользователям.

3. Проверьте, что файл kod является исполняемым:

file /usr/local/bin/kod

Эта команда выведет информацию о типе файла kod. 
Если файл не является исполняемым, вы можете сделать его исполняемым с помощью команды:

sudo chmod +x /usr/local/bin/kod

4. Попробуйте запустить файл msdis снова:

kod list /home/tbdbj/Marina/

=========================================================================================================================



Чтобы использовать скрипт в виде исполняемого файла, вы должны преобразовать его в формат py.
+ Вы можете сделать это, используя команду jupyter nbconvert в терминале:

+ jupyter nbconvert --to python arparse.ipynb

Замените argparse.ipynb на имя вашего файла Jupyter Notebook. Это создаст файл argparse.py

Чтобы запустить программу, вы можете использовать следующие команды в терминале:

+ Команда list пример : python script_name.py list /path/to/directory - список папок в директории

+ Команда clear пример : python script_name.py clear /path/to/file - удаление файла


+ Команда unzip пример : python script_name.py unzip /path/to/archive.zip /path/to/extract - Распаковка ZIP-архив

+ Команда download пример :python script_name.py download https://ссылка Название_архива.zip /path/to/save - скачивание ZIP-архива

Чтобы запустить программу, вы можете использовать следующие команды в терминале:

1. Список папок в директории
Чтобы получить список папок в указанной директории, используйте команду list:

Команда list пример : python script_name.py list /path/to/directory - список папок в директории


2. Удаление файла
Чтобы удалить файл, используйте команду clear и укажите путь к файлу:

Команда clear пример : python script_name.py clear /path/to/file - удаление файла

3. Распаковка ZIP-архива
Чтобы распаковать ZIP-архив, используйте команду unzip, указывая путь к ZIP-файлу и директорию для извлечения:

Команда unzip пример : python script_name.py unzip /path/to/archive.zip /path/to/extract - Распаковка ZIP-архив


4. Скачивание ZIP-архива по ссылке
Чтобы скачать ZIP-архив по URL, используйте команду download, указывая URL, имя файла для сохранения и путь для сохранения:

Команда download пример :python script_name.py download https://tinyurl.com/29lqesg2 Название_архива.zip /path/to/save - скачивание ZIP-архива

(Вписывать без ковычек, ковычки для примера)
5. Скачивание файла из S3
Чтобы скачать файл из S3, используйте команду s3_download, указывая имя бакета, путь к файлу в S3 и локальную директорию для сохранения:

python script_name.py s3_download "my-bucket" "path/to/file.txt" "C:\path\to\local\directory"


6. Скачивание директории из S3
Чтобы скачать все файлы из директории в S3, используйте команду s3_download_directory, указывая имя бакета, 
путь к директории в S3 и локальную директорию для сохранения:

python script_name.py s3_download_directory "my-bucket" "path/to/directory/" "C:\path\to\local\directory"

7. Загрузка файла в S3
Чтобы загрузить файл в S3, используйте команду s3_upload, указывая локальный путь к файлу, имя бакета и путь к директории в S3:

python script_name.py s3_upload "C:\path\to\local\file.txt" "my-bucket" "path/to/s3/directory/"

8. Загрузка директории в S3
Чтобы загрузить все файлы из локальной директории в S3, используйте команду s3_upload_directory, 
указывая локальный путь к директории, имя бакета и путь к директории в S3:

python script_name.py s3_upload_directory "C:\path\to\local\directory" "my-bucket" "path/to/s3/directory/"

9. Возвращает список файлов в директории S3 (исключает префиксы/папки) :

python script_name.py s3_list public moderate/files_to_script

10. Лучшие веса

python script_name.py best_weights /path/to/local/archive /path/to/weights/folder --delete_archives

script_name.py - это имя файла Python, в котором находится функция 
best_weights - это команда, которая вызывает функцию extract_best_weights.
/path/to/local/archive - это локальный путь к архиву, из которого будут извлечены лучшие веса.
/path/to/weights/folder - это папка, в которую будут сохранены лучшие веса.
--delete_archives - это опциональный аргумент, который указывает на то, что архивы должны быть удалены после извлечения лучших весов.

Если вы хотите сохранить архивы, вы можете вызвать функцию без аргумента --delete_archives

python script_name.py best_weights /path/to/local/archive /path/to/weights/folder



# arparse_cmd_list
