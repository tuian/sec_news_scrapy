import pymysql
import re


def dbHandle():
    conn = pymysql.connect(
        host="localhost",
        user="root",
        passwd="1234",
        charset="utf8",
        db='secnews',
        port=3306)
    return conn


def get_key_word_from_db():
    words = {}
    conn = dbHandle()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "select `key`, sum(val) as s from t_security_news_words group by `key` order by s desc limit 300")
            for res in cursor.fetchall():
                words[res[0]] = int(res[1])
        return words
    except BaseException as e:
        print("存储错误", e, "<<<<<<原因在这里")
        conn.rollback()
        return {}
    finally:
        conn.close()


def opt_file(new_str, f_path):
    try:
        with open(f_path, 'r', encoding='utf-8') as f:
            content = f.read()
            new_content = re.sub(r'keywords\s=\s(?s)(.*?})', 'keywords=' + new_str, content)

        with open(f_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
    except Exception as e:
        print(e)
    finally:
        f.close()


file_path = '..\echart\optionKeywords.html'

print('Getting words from database.')
words_dict = get_key_word_from_db()

print('Format words and writing into D3 file.')
opt_file(str(words_dict), file_path)
