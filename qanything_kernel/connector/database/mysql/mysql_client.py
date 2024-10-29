from qanything_kernel.configs.model_config import (MYSQL_HOST_LOCAL, MYSQL_PORT_LOCAL, MYSQL_USER_LOCAL,
                                                   MYSQL_PASSWORD_LOCAL,
                                                   MYSQL_DATABASE_LOCAL, KB_SUFFIX, MILVUS_HOST_LOCAL)
from qanything_kernel.utils.custom_log import debug_logger, insert_logger
import mysql.connector
from mysql.connector import pooling
import json
from typing import List, Optional, Dict
import uuid
from datetime import datetime, timedelta
from collections import defaultdict
from mysql.connector.errors import Error as MySQLError


class KnowledgeBaseManager:
    def __init__(self, pool_size=8):
        host = MYSQL_HOST_LOCAL
        port = MYSQL_PORT_LOCAL
        user = MYSQL_USER_LOCAL
        password = MYSQL_PASSWORD_LOCAL
        database = MYSQL_DATABASE_LOCAL

        self.check_database_(host, port, user, password, database)
        dbconfig = {
            "host": host,
            "user": user,
            "port": port,
            "password": password,
            "database": database,
        }
        self.cnxpool = pooling.MySQLConnectionPool(pool_size=pool_size, pool_reset_session=True, **dbconfig)
        self.free_cnx = pool_size
        self.used_cnx = 0
        self.create_tables_()
        debug_logger.info("[SUCCESS] 数据库{}连接成功".format(database))

    def check_database_(self, host, port, user, password, database_name):
        # 连接 MySQL 服务器
        cnx = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password
        )

        # 检查数据库是否存在
        cursor = cnx.cursor(buffered=True)
        cursor.execute('SHOW DATABASES')
        databases = [database[0] for database in cursor]

        if database_name not in databases:
            # 如果数据库不存在，则新建数据库
            cursor.execute('CREATE DATABASE IF NOT EXISTS {}'.format(database_name))
            debug_logger.info("数据库{}新建成功或已存在".format(database_name))
        debug_logger.info("[SUCCESS] 数据库{}检查通过".format(database_name))
        # 关闭游标
        cursor.close()
        # 连接到数据库
        cnx.database = database_name
        # 关闭数据库连接
        cnx.close()

    def execute_query_(self, query, params, commit=False, fetch=False, check=False, user_dict=False):
        try:
            conn = self.cnxpool.get_connection()
            self.used_cnx += 1
            self.free_cnx -= 1
            if self.free_cnx < 4:
                debug_logger.info("获取连接成功，当前连接池状态：空闲连接数 {}，已使用连接数 {}".format(
                    self.free_cnx, self.used_cnx))
        except MySQLError as err:
            debug_logger.error("从连接池获取连接失败：{}".format(err))
            return None

        result = None
        cursor = None
        try:
            if user_dict:
                cursor = conn.cursor(dictionary=True)
            else:
                cursor = conn.cursor(buffered=True)
            cursor.execute(query, params)

            if commit:
                conn.commit()

            if fetch:
                result = cursor.fetchall()
            elif check:
                result = cursor.rowcount
        except MySQLError as err:
            if err.errno == 1061:
                debug_logger.info(f"Index already exists (this is okay): {query}")
            else:
                debug_logger.error("执行数据库操作失败：{}，SQL：{}".format(err, query))
            if commit:
                conn.rollback()
        finally:
            if cursor is not None:
                cursor.close()
            conn.close()
            self.used_cnx -= 1
            self.free_cnx += 1
            if self.free_cnx <= 4:
                debug_logger.info("连接关闭，返回连接池。当前连接池状态：空闲连接数 {}，已使用连接数 {}".format(
                    self.free_cnx, self.used_cnx))

        return result

    def create_tables_(self):
        query = """
            CREATE TABLE IF NOT EXISTS User (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id VARCHAR(255) UNIQUE,
                user_name VARCHAR(255),
                creation_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """

        self.execute_query_(query, (), commit=True)
        query = """
            CREATE TABLE IF NOT EXISTS KnowledgeBase (
                id INT AUTO_INCREMENT PRIMARY KEY,
                kb_id VARCHAR(255) UNIQUE,
                user_id VARCHAR(255),
                kb_name VARCHAR(255),
                deleted BOOL DEFAULT 0,
                latest_qa_time TIMESTAMP,
                latest_insert_time TIMESTAMP
            );

        """
        self.execute_query_(query, (), commit=True)
        query = """
            CREATE TABLE IF NOT EXISTS File (
                id INT AUTO_INCREMENT PRIMARY KEY,
                file_id VARCHAR(255) UNIQUE,
                user_id VARCHAR(255) DEFAULT 'unknown',
                kb_id VARCHAR(255),
                file_name VARCHAR(255),
                status VARCHAR(255),
                msg VARCHAR(255) DEFAULT 'success',
                transfer_status VARCHAR(255),
                deleted BOOL DEFAULT 0,
                file_size INT DEFAULT -1,
                content_length INT DEFAULT -1,
                chunks_number INT DEFAULT -1,
                file_location VARCHAR(255) DEFAULT 'unknown',
                file_url VARCHAR(2048) DEFAULT '',
                upload_infos TEXT,
                chunk_size INT DEFAULT -1,
                timestamp VARCHAR(255) DEFAULT '197001010000'
            );

        """
        self.execute_query_(query, (), commit=True)

        # create_index_query = "CREATE INDEX IF NOT EXISTS index_kb_id_deleted ON File (kb_id, deleted);"
        # self.execute_query_(create_index_query, (), commit=True)
        # create_index_query = "CREATE INDEX idx_user_id_status ON File (user_id, status);"
        # self.execute_query_(create_index_query, (), commit=True)

        query = """
            CREATE TABLE IF NOT EXISTS Faqs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                faq_id  VARCHAR(255) UNIQUE,
                user_id VARCHAR(255) NOT NULL,
                kb_id VARCHAR(255) NOT NULL,
                question VARCHAR(512) NOT NULL,
                answer VARCHAR(2048) NOT NULL,
                nos_keys VARCHAR(768)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
        self.execute_query_(query, (), commit=True)

        query = """
            CREATE TABLE IF NOT EXISTS Documents (
                id INT AUTO_INCREMENT PRIMARY KEY,
                doc_id VARCHAR(255) UNIQUE,
                json_data LONGTEXT
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """

        self.execute_query_(query, (), commit=True)
        # 创建一个QaLogs表，用于记录用户的操作日志
        """
        chat_data = {'user_id': user_id, 'kb_ids': kb_ids, 'query': question, "model": model, "product_source": request_source,
                     'time_record': time_record, 'history': history,
                     'condense_question': resp['condense_question'],
                     'prompt': resp['prompt'], 'result': next_history[-1][1],
                     'retrieval_documents': retrieval_documents, 'source_documents': source_documents}
        """
        # 其中kb_ids是一个List[str], time_record是Dict，history是List[List[str]], retrieval_documents是List[Dict], source_documents是List[Dict]，其他项都是str
        query = """
            CREATE TABLE IF NOT EXISTS QaLogs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                qa_id VARCHAR(255) UNIQUE,
                user_id VARCHAR(255) NOT NULL,
                bot_id VARCHAR(255),
                kb_ids VARCHAR(2048) NOT NULL,
                query VARCHAR(512) NOT NULL,
                model VARCHAR(64) NOT NULL,
                product_source VARCHAR(64) NOT NULL,
                time_record VARCHAR(512) NOT NULL,
                history MEDIUMTEXT NOT NULL,
                condense_question VARCHAR(1024) NOT NULL,
                prompt MEDIUMTEXT NOT NULL,
                result TEXT NOT NULL,
                retrieval_documents MEDIUMTEXT NOT NULL,
                source_documents MEDIUMTEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
        self.execute_query_(query, (), commit=True)

        # create_index_query = "CREATE INDEX IF NOT EXISTS index_bot_id ON QaLogs (bot_id);"
        # self.execute_query_(create_index_query, (), commit=True)
        # create_index_query = "CREATE INDEX IF NOT EXISTS index_query ON QaLogs (query);"
        # self.execute_query_(create_index_query, (), commit=True)
        # create_index_query = "CREATE INDEX IF NOT EXISTS index_timestamp ON QaLogs (timestamp);"
        # self.execute_query_(create_index_query, (), commit=True)

        query = """
            CREATE TABLE IF NOT EXISTS FileImages (
                id INT AUTO_INCREMENT PRIMARY KEY,
                image_id VARCHAR(255) UNIQUE,
                file_id VARCHAR(255) NOT NULL,
                user_id VARCHAR(255) NOT NULL,
                kb_id VARCHAR(255) NOT NULL,
                nos_key VARCHAR(255) NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
        self.execute_query_(query, (), commit=True)

        query = """
            CREATE TABLE IF NOT EXISTS QanythingBot (
                id INT AUTO_INCREMENT PRIMARY KEY,
                bot_id          VARCHAR(64) UNIQUE,
                user_id         VARCHAR(255),
                bot_name        VARCHAR(512),
                description     VARCHAR(512),
                head_image      VARCHAR(512),
                prompt_setting  MEDIUMTEXT,
                welcome_message MEDIUMTEXT,
                kb_ids_str      VARCHAR(1024),
                deleted         INT DEFAULT 0,
                create_time     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                update_time     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                llm_setting     VARCHAR(512) DEFAULT '{}'
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
        self.execute_query_(query, (), commit=True)

        # 修改索引创建方式
        index_queries = [
            "CREATE INDEX index_kb_id_deleted ON File (kb_id, deleted)",
            "CREATE INDEX idx_user_id_status ON File (user_id, status)",
            "CREATE INDEX index_bot_id ON QaLogs (bot_id)",
            "CREATE INDEX index_query ON QaLogs (query)",
            "CREATE INDEX index_timestamp ON QaLogs (timestamp)",
            # 如果没有的话，给QanythingBot添加一列：llm_setting VARCHAR(512)
            "ALTER TABLE QanythingBot ADD COLUMN llm_setting VARCHAR(512) DEFAULT '{}'",
            "ALTER TABLE QanythingBot DROP COLUMN model",
        ]

        for query in index_queries:
            try:
                self.execute_query_(query, (), commit=True)
                debug_logger.info(f"Index created successfully: {query}")
            except mysql.connector.Error as err:
                if err.errno == 1061:  # 重复键错误
                    debug_logger.info(f"Index already exists (this is okay): {query}")
                elif err.errno == 1060:  # 已存在的列无需创建
                    debug_logger.info(f"Column already exists (this is okay): {query}")
                elif err.errno == 1091:  # 已经删除的列无需删除
                    debug_logger.info(f"Column already deleted (this is okay): {query}")
                else:
                    debug_logger.error(f"Error creating index: {err}")

        debug_logger.info("All tables and indexes checked/created successfully.")

    def update_file_msg(self, file_id, msg):
        query = "UPDATE File SET msg = %s WHERE file_id = %s"
        insert_logger.info(f"Update file msg: {file_id} {msg}")
        self.execute_query_(query, (msg, file_id), commit=True)

    def update_file_upload_infos(self, file_id, upload_infos):
        upload_infos = json.dumps(upload_infos, ensure_ascii=False)
        query = "UPDATE File SET upload_infos = %s WHERE file_id = %s"
        self.execute_query_(query, (upload_infos, file_id), commit=True)

    def add_file_images(self, image_id, file_id, user_id, kb_id, nos_key):
        nos_key = nos_key.split(' ')[0]
        query = "INSERT INTO FileImages (image_id, file_id, user_id, kb_id, nos_key) VALUES (%s, %s, %s, %s, %s)"
        self.execute_query_(query, (image_id, file_id, user_id, kb_id, nos_key), commit=True)
        insert_logger.info(f"Add file image: {image_id} {file_id} {user_id} {kb_id} {nos_key}")

    def get_image_id_by_nos_key(self, nos_key):
        query = "SELECT image_id FROM FileImages WHERE nos_key = %s"
        result = self.execute_query_(query, (nos_key,), fetch=True)
        return result[0][0] if result else None

    def get_nos_key_by_image_id(self, image_id):
        query = "SELECT nos_key FROM FileImages WHERE image_id = %s"
        result = self.execute_query_(query, (image_id,), fetch=True)
        return result[0][0] if result else None

    def check_user_exist_(self, user_id):
        query = "SELECT user_id FROM User WHERE user_id = %s"
        result = self.execute_query_(query, (user_id,), fetch=True)
        debug_logger.info("check_user_exist {}".format(result))
        return result is not None and len(result) > 0

    def check_kb_exist(self, user_id, kb_ids):
        if not kb_ids:
            return []
        kb_ids_str = ','.join("'{}'".format(str(x)) for x in kb_ids)
        query = "SELECT kb_id FROM KnowledgeBase WHERE kb_id IN ({}) AND deleted = 0 AND user_id = %s".format(
            kb_ids_str)
        result = self.execute_query_(query, (user_id,), fetch=True)
        debug_logger.info("check_kb_exist {}".format(result))
        valid_kb_ids = [kb_info[0] for kb_info in result]
        unvalid_kb_ids = list(set(kb_ids) - set(valid_kb_ids))
        return unvalid_kb_ids

    def get_file_by_status(self, kb_ids, status):
        kb_ids_str = ','.join("'{}'".format(str(x)) for x in kb_ids)
        query = "SELECT file_id, file_name FROM File WHERE kb_id IN ({}) AND deleted = 0 AND status = %s".format(
            kb_ids_str)
        result = self.execute_query_(query, (status,), fetch=True)
        return result

    def get_file_timestamp(self, file_id):
        query = "SELECT timestamp FROM File WHERE file_id = %s"
        result = self.execute_query_(query, (file_id,), fetch=True)
        return result[0][0] if result else None

    def check_file_exist(self, user_id, kb_id, file_ids):
        # 筛选出有效的文件
        if not file_ids:
            debug_logger.info("check_file_exist: file_ids is empty")
            return []

        file_ids_str = ','.join("'{}'".format(str(x)) for x in file_ids)
        query = """SELECT file_id, status FROM File
                 WHERE deleted = 0
                 AND file_id IN ({})
                 AND kb_id = %s
                 AND kb_id IN (SELECT kb_id FROM KnowledgeBase WHERE user_id = %s)""".format(file_ids_str)
        result = self.execute_query_(query, (kb_id, user_id), fetch=True)
        debug_logger.info("check_file_exist {}".format(result))
        return result

    def check_file_exist_by_name(self, user_id, kb_id, file_names):
        results = []
        batch_size = 100  # 根据实际情况调整批次大小

        # 分批处理file_names
        for i in range(0, len(file_names), batch_size):
            batch_file_names = file_names[i:i + batch_size]

            # 创建参数化的查询，用%s作为占位符
            placeholders = ','.join(['%s'] * len(batch_file_names))
            query = """
                SELECT file_id, file_name, file_size, status FROM File
                WHERE deleted = 0
                AND file_name IN ({})
                AND kb_id = %s
                AND kb_id IN (SELECT kb_id FROM KnowledgeBase WHERE user_id = %s)
            """.format(placeholders)

            # 使用参数化查询，将文件名作为参数传递
            query_params = batch_file_names + [kb_id, user_id]
            batch_result = self.execute_query_(query, query_params, fetch=True)
            debug_logger.info("check_file_exist_by_name batch {}: {}".format(i // batch_size, batch_result))
            results.extend(batch_result)

        return results

    # 对外接口不需要增加用户，新建知识库的时候增加用户就可以了
    def add_user_(self, user_id, user_name):
        query = "INSERT IGNORE INTO User (user_id, user_name) VALUES (%s, %s)"
        self.execute_query_(query, (user_id, user_name), commit=True)
        debug_logger.info(f"Add user: {user_id} {user_name}")

    def new_milvus_base(self, kb_id, user_id, kb_name, user_name=None):
        if not self.check_user_exist_(user_id):
            self.add_user_(user_id, user_name)
        query = "INSERT INTO KnowledgeBase (kb_id, user_id, kb_name) VALUES (%s, %s, %s)"
        self.execute_query_(query, (kb_id, user_id, kb_name), commit=True)
        return kb_id, "success"

    # [知识库] 获取指定用户的所有知识库
    def get_knowledge_bases(self, user_id):
        # 只获取后缀为KB_SUFFIX的知识库
        query = (f"SELECT kb_id, kb_name FROM KnowledgeBase WHERE user_id = %s AND deleted = 0 AND "
                 f"(kb_id LIKE '%{KB_SUFFIX}' OR kb_id LIKE '%{KB_SUFFIX}_FAQ')")
        # query = "SELECT kb_id, kb_name FROM KnowledgeBase WHERE user_id = %s AND deleted = 0"
        return self.execute_query_(query, (user_id,), fetch=True)

    def get_users(self):
        query = "SELECT user_id FROM User"
        return self.execute_query_(query, (), fetch=True)

    def get_user_by_kb_id(self, kb_id):
        query = "SELECT user_id FROM KnowledgeBase WHERE kb_id = %s"
        result = self.execute_query_(query, (kb_id,), fetch=True)
        if result:
            return result[0][0]
        else:
            return None

    # [知识库] 获取指定kb_ids的知识库
    def get_knowledge_base_name(self, kb_ids):
        kb_ids_str = ','.join("'{}'".format(str(x)) for x in kb_ids)
        query = "SELECT user_id, kb_id, kb_name FROM KnowledgeBase WHERE kb_id IN ({}) AND deleted = 0".format(
            kb_ids_str)
        return self.execute_query_(query, (), fetch=True)

    # [知识库] 删除指定知识库
    def delete_knowledge_base(self, user_id, kb_ids):
        # 删除知识库
        kb_ids_str = ','.join("'{}'".format(str(x)) for x in kb_ids)
        query = "UPDATE KnowledgeBase SET deleted = 1 WHERE user_id = %s AND kb_id IN ({})".format(kb_ids_str)
        self.execute_query_(query, (user_id,), commit=True)
        # 删除知识库下面的文件
        query = """UPDATE File SET deleted = 1 WHERE kb_id IN ({}) AND kb_id IN (SELECT kb_id FROM KnowledgeBase WHERE user_id = %s)""".format(
            kb_ids_str)
        self.execute_query_(query, (user_id,), commit=True)

    # [知识库] 重命名知识库
    def rename_knowledge_base(self, user_id, kb_id, kb_name):
        query = "UPDATE KnowledgeBase SET kb_name = %s WHERE kb_id = %s AND user_id = %s"
        self.execute_query_(query, (kb_name, kb_id, user_id), commit=True)

    def update_knowledge_base_latest_qa_time(self, kb_id, timestamp):
        # timestamp的格式为'2021-08-01 00:00:00'
        query = "UPDATE KnowledgeBase SET latest_qa_time = %s WHERE kb_id = %s"
        self.execute_query_(query, (timestamp, kb_id), commit=True)

    def update_knowlegde_base_latest_insert_time(self, kb_id, timestamp):
        query = "UPDATE KnowledgeBase SET latest_insert_time = %s WHERE kb_id = %s"
        self.execute_query_(query, (timestamp, kb_id), commit=True)

    # [文件] 向指定知识库下面增加文件
    def add_file(self, file_id, user_id, kb_id, file_name, file_size, file_location, chunk_size, timestamp, file_url='',
                 status="gray"):
        query = ("INSERT INTO File (file_id, user_id, kb_id, file_name, status, file_size, file_location, chunk_size, "
                 "timestamp, file_url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
        self.execute_query_(query,
                            (file_id, user_id, kb_id, file_name, status, file_size, file_location, chunk_size, timestamp, file_url),
                            commit=True)
        return "success"

    #  更新file中的content_length
    def update_content_length(self, file_id, content_length):
        query = "UPDATE File SET content_length = %s WHERE file_id = %s"
        self.execute_query_(query, (content_length, file_id), commit=True)

    #  更新file中的chunk_number
    def update_chunks_number(self, file_id, chunks_number):
        query = "UPDATE File SET chunks_number = %s WHERE file_id = %s"
        self.execute_query_(query, (chunks_number, file_id), commit=True)

    def update_file_status(self, file_id, status):
        query = "UPDATE File SET status = %s WHERE file_id = %s"
        self.execute_query_(query, (status, file_id), commit=True)

    def from_status_to_status(self, file_ids, from_status, to_status):
        file_ids_str = ','.join("'{}'".format(str(x)) for x in file_ids)
        query = "UPDATE File SET status = %s WHERE file_id IN ({}) AND status = %s".format(file_ids_str)
        self.execute_query_(query, (to_status, from_status), commit=True)

    def get_files(self, user_id, kb_id, file_id=None):
        limit = 100
        offset = 0
        all_files = []

        base_query = """
            SELECT file_id, file_name, status, file_size, content_length, timestamp,
                   file_location, file_url, chunk_size, msg
            FROM File
            WHERE kb_id = %s AND deleted = 0
        """

        params = [kb_id]

        if file_id is not None:
            base_query += " AND file_id = %s"
            params.append(file_id)
            # Since file_id is specified, we only need one query
            query = base_query
            current_params = params
            files = self.execute_query_(query, current_params, fetch=True)
            return files

        while True:
            query = base_query + " LIMIT %s OFFSET %s"
            current_params = params + [limit, offset]
            files = self.execute_query_(query, current_params, fetch=True)

            if not files:
                break

            all_files.extend(files)
            offset += limit

        return all_files

    def get_total_status_by_date(self, user_id):
        # 查询指定用户上传的文件数量，按日期和状态分组
        query = """
        SELECT
            LEFT(timestamp, 8) as date,  -- 提取前8个字符作为日期 (YYYYMMDD)
            status,
            COUNT(*) as number
        FROM File
        WHERE user_id = %s
        GROUP BY LEFT(timestamp, 8), status
        """
        result = self.execute_query_(query, (user_id,), fetch=True)

        files_by_date = defaultdict(lambda: defaultdict(int))

        for date, status, number in result:
            files_by_date[date][status] = number

        return {date: dict(status_dict) for date, status_dict in files_by_date.items()}

    def get_chunk_size(self, file_ids):
        limit = 100
        offset = 0
        all_chunk_sizes = []

        while True:
            file_ids_sublist = file_ids[offset:offset + limit]
            if not file_ids_sublist:
                break

            file_ids_str = ','.join("'{}'".format(str(x)) for x in file_ids_sublist)
            query = f"SELECT chunk_size FROM File WHERE file_id IN ({file_ids_str})"
            chunk_sizes = self.execute_query_(query, (), fetch=True)
            if not chunk_sizes:
                break
            all_chunk_sizes.extend(chunk_sizes)
            offset += limit

        file_chunks = [file_info[0] for file_info in all_chunk_sizes]
        return file_chunks

    def is_deleted_file(self, file_id):
        query = "SELECT deleted FROM File WHERE file_id = %s"
        result = self.execute_query_(query, (file_id,), fetch=True)
        if result:
            return result[0][0] == 1
        else:
            return False

    # [文件] 删除指定文件
    def delete_files(self, kb_id, file_ids):
        file_ids_str = ','.join("'{}'".format(str(x)) for x in file_ids)
        query = "UPDATE File SET deleted = 1 WHERE kb_id = %s AND file_id IN ({})".format(file_ids_str)
        debug_logger.info("delete_files: {}".format(file_ids))
        self.execute_query_(query, (kb_id,), commit=True)

    def add_document(self, doc_id, json_data):
        json_data = json.dumps(json_data, ensure_ascii=False)
        # insert_logger.info("add_document: {}".format(doc_id))
        query = "INSERT IGNORE INTO Documents (doc_id, json_data) VALUES (%s, %s)"
        self.execute_query_(query, (doc_id, json_data), commit=True, check=True)

    def update_document(self, doc_id, update_content):
        ori_doc_json = self.get_document_by_doc_id(doc_id)
        ori_doc_json['kwargs']['page_content'] = update_content
        new_doc_json = json.dumps(ori_doc_json, ensure_ascii=False)
        query = "UPDATE Documents SET json_data = %s WHERE doc_id = %s"
        self.execute_query_(query, (new_doc_json, doc_id), commit=True, check=True)

    def add_faq(self, faq_id, user_id, kb_id, question, answer, nos_keys):
        # insert_logger.info(f"add_faq: {faq_id}, {user_id}, {kb_id}, {question}, {nos_keys}")
        query = "INSERT INTO Faqs (faq_id, user_id, kb_id, question, answer, nos_keys) VALUES (%s, %s, %s, %s, %s, %s)"
        self.execute_query_(query, (faq_id, user_id, kb_id, question, answer, nos_keys), commit=True)

    def get_document_by_file_id(self, file_id, batch_size=100) -> Optional[List]:
        # 初始化结果列表
        all_json_datas = []

        # 搜索doc_id中包含file_id的所有Doc
        query = "SELECT doc_id, json_data FROM Documents WHERE doc_id LIKE %s"
        offset = 0

        while True:
            # 执行带有LIMIT和OFFSET的查询语句
            paginated_query = f"{query} LIMIT %s OFFSET %s"
            doc_all = self.execute_query_(paginated_query, (f"{file_id}_%", batch_size, offset), fetch=True)

            if not doc_all:
                break  # 如果没有更多数据，跳出循环

            doc_ids = [doc[0].split('_')[1] for doc in doc_all]
            json_datas = [json.loads(doc[1]) for doc in doc_all]
            for doc_id, json_data in zip(doc_ids, json_datas):
                json_data['kwargs']['chunk_id'] = file_id + '_' + str(doc_id)

            # 将doc_id和json_data打包并追加到结果列表
            all_json_datas.extend(zip(doc_ids, json_datas))

            offset += batch_size  # 更新offset

        debug_logger.info(f"get_document: file_id: {file_id}, mysql parent documents res: {len(all_json_datas)}")
        if all_json_datas:
            # 对所有数据进行排序
            all_json_datas.sort(key=lambda x: int(x[0]))
            # 解压排序后的结果
            sorted_json_datas = [json_data for _, json_data in all_json_datas]
            return sorted_json_datas
        return None

    def get_document_by_doc_id(self, doc_id) -> Optional[Dict]:
        query = "SELECT json_data FROM Documents WHERE doc_id = %s"
        doc_all = self.execute_query_(query, (doc_id,), fetch=True)
        if doc_all:
            doc = json.loads(doc_all[0][0])
            # debug_logger.info(f"get_document: doc_id: {doc_id}")
            return doc
        else:
            debug_logger.error(f"get_document: doc_id: {doc_id} not found")
            return None

    def get_faq(self, faq_id) -> tuple:
        query = "SELECT user_id, kb_id, question, answer, nos_keys FROM Faqs WHERE faq_id = %s"
        faq_all = self.execute_query_(query, (faq_id,), fetch=True)
        if faq_all:
            faq = faq_all[0]
            debug_logger.info(f"get_faq: faq_id: {faq_id}, mysql res: {faq}")
            return faq
        else:
            debug_logger.error(f"get_faq: faq_id: {faq_id} not found")
            return None

    def delete_documents(self, file_ids):
        #  获取所有形如"file_id_"开头的doc_id的documents，然后再删除
        total_deleted = 0
        for file_id in file_ids:
            query = f"SELECT doc_id FROM Documents WHERE doc_id LIKE \"{file_id}_%\""
            doc_ids = self.execute_query_(query, None, fetch=True)
            debug_logger.info(f"Found documents to delete: {doc_ids}, {file_id}")

            if doc_ids:
                doc_ids = [doc_id[0] for doc_id in doc_ids]
                batch_size = 100
                for i in range(0, len(doc_ids), batch_size):
                    batch_doc_ids = doc_ids[i:i + batch_size]
                    delete_query = "DELETE FROM Documents WHERE doc_id IN ({})".format(
                        ','.join(['%s'] * len(batch_doc_ids)))
                    res = self.execute_query_(delete_query, batch_doc_ids, commit=True, check=True)
                    total_deleted += res
        debug_logger.info(f"Deleted documents count: {total_deleted}")

    def delete_faqs(self, faq_ids):
        # 分批，因为多个faq_id的加一起可能会超过sql的最大长度
        batch_size = 100
        total_deleted = 0
        for i in range(0, len(faq_ids), batch_size):
            batch_faq_ids = faq_ids[i:i + batch_size]
            placeholders = ','.join(['%s'] * len(batch_faq_ids))
            query = "DELETE FROM Faqs WHERE faq_id IN ({})".format(placeholders)
            res = self.execute_query_(query, (batch_faq_ids), commit=True, check=True)
            total_deleted += res
        debug_logger.info(f"delete_faqs count: {total_deleted}")

    def add_qalog(self, user_id, bot_id, kb_ids, query, model, product_source, time_record, history, condense_question,
                  prompt, result, retrieval_documents, source_documents):
        debug_logger.info("add_qalog: {}".format(query))
        qa_id = uuid.uuid4().hex
        kb_ids = json.dumps(kb_ids, ensure_ascii=False)
        retrieval_documents = json.dumps(retrieval_documents, ensure_ascii=False)
        source_documents = json.dumps(source_documents, ensure_ascii=False)
        history = json.dumps(history, ensure_ascii=False)
        time_record = json.dumps(time_record, ensure_ascii=False)
        insert_query = (
            "INSERT INTO QaLogs (qa_id, user_id, bot_id, kb_ids, query, model, product_source, time_record, "
            "history, condense_question, prompt, result, retrieval_documents, source_documents) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
        self.execute_query_(insert_query, (qa_id, user_id, bot_id, kb_ids, query, model, product_source, time_record,
                                           history, condense_question, prompt, result, retrieval_documents,
                                           source_documents), commit=True)

    def get_qalog_by_filter(self, need_info, user_id=None, query=None, bot_id=None, time_range=None, any_kb_id=None, qa_ids=None):
        # 判断哪些条件不是None，构建搜索query
        need_info = ", ".join(need_info)
        if qa_ids is not None:
            mysql_query = f"SELECT {need_info} FROM QaLogs WHERE qa_id IN ({','.join(['%s'] * len(qa_ids))})"
            qa_infos = self.execute_query_(mysql_query, qa_ids, fetch=True)
        else:
            mysql_query = f"SELECT {need_info} FROM QaLogs WHERE timestamp BETWEEN %s AND %s"
            params = list(time_range)
            if user_id:
                mysql_query += " AND user_id = %s"
                params.append(user_id)
            if any_kb_id:
                mysql_query += " AND kb_ids LIKE %s"
                params.append(f'%{any_kb_id}%')
            if bot_id:
                mysql_query += " AND bot_id = %s"
                params.append(bot_id)
            if query:
                mysql_query += " AND query = %s"
                params.append(query)
            debug_logger.info("get_qalog_by_filter: {}".format(params))
            qa_infos = self.execute_query_(mysql_query, params, fetch=True)
        # 根据need_info构建一个dict
        qa_infos = [dict(zip(need_info.split(", "), qa_info)) for qa_info in qa_infos]
        for qa_info in qa_infos:
            if 'timestamp' in qa_info:
                qa_info['timestamp'] = qa_info['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
            if 'kb_ids' in qa_info:
                qa_info['kb_ids'] = json.loads(qa_info['kb_ids'])
            if 'time_record' in qa_info:
                qa_info['time_record'] = json.loads(qa_info['time_record'])
            if 'retrieval_documents' in qa_info:
                qa_info['retrieval_documents'] = json.loads(qa_info['retrieval_documents'])
            if 'source_documents' in qa_info:
                qa_info['source_documents'] = json.loads(qa_info['source_documents'])
            if 'history' in qa_info:
                qa_info['history'] = json.loads(qa_info['history'])
        if 'timestamp' in need_info:
            qa_infos = sorted(qa_infos, key=lambda x: x["timestamp"], reverse=True)
        return qa_infos

    def get_qalog_by_ids(self, ids, need_info):
        placeholders = ','.join(['%s'] * len(ids))
        need_info = ", ".join(need_info)
        query = "SELECT {} FROM QaLogs WHERE qa_id IN ({})".format(need_info, placeholders)
        return self.execute_query_(query, ids, fetch=True)

    def get_faq_by_question(self, question, kb_id):
        query = "SELECT faq_id FROM Faqs WHERE question = %s AND kb_id = %s"
        result = self.execute_query_(query, (question, kb_id), fetch=True)
        faq_id = result[0][0] if result else None
        if faq_id:
            query = "SELECT status FROM File WHERE file_id = %s"
            result = self.execute_query_(query, (faq_id,), fetch=True)
            if result and result[0][0] == 'green':
                return faq_id
        return None

    def get_statistic(self, time_range):
        query = """
            SELECT COUNT(DISTINCT user_id) AS total_users, COUNT(query) AS total_queries
            FROM QaLogs
            WHERE timestamp BETWEEN %s AND %s;
        """
        return self.execute_query_(query, time_range, fetch=True, user_dict=True)[0]

    def get_random_qa_infos(self, limit=10, time_range=None, need_info=None):
        if need_info is None:
            need_info = ["qa_id", "user_id", "kb_ids", "query", "result", "timestamp"]
        if "qa_id" not in need_info:
            need_info.append("qa_id")
        if "user_id" not in need_info:
            need_info.append("user_id")
        if "timestamp" not in need_info:
            need_info.append("timestamp")
        need_info = ", ".join(need_info)
        query = f"SELECT {need_info} FROM QaLogs WHERE timestamp BETWEEN %s AND %s ORDER BY RAND() LIMIT %s"
        qa_infos = self.execute_query_(query, (time_range[0], time_range[1], limit), fetch=True, user_dict=True)
        for qa_info in qa_infos:
            qa_info['timestamp'] = qa_info['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
        return qa_infos

    def get_related_qa_infos(self, qa_id, need_info=None, need_more=False):
        if need_info is None:
            need_info = ["user_id", "kb_ids", "query", "condense_question", "result", "timestamp", "product_source"]
        if "user_id" not in need_info:
            need_info.append("user_id")
        if "kb_ids" not in need_info:
            need_info.append("kb_ids")
        need_info = ", ".join(need_info)
        query = f"SELECT {need_info} FROM QaLogs WHERE qa_id = %s"
        qa_log = self.execute_query_(query, (qa_id,), fetch=True, user_dict=True)[0]
        qa_log['timestamp'] = qa_log['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
        user_id = qa_log['user_id']
        # 获取当前时间和7天前的时间
        current_time = datetime.utcnow()
        seven_days_ago = current_time - timedelta(days=7)
        if not need_more:
            return qa_log, [], []

        # 查询7天以内的日志
        recent_logs = []
        offset = 0
        limit = 50
        while True:
            query_recent_logs = f"""
                SELECT {need_info}
                FROM QaLogs
                WHERE user_id = %s AND timestamp >= %s
                ORDER BY timestamp
                LIMIT %s OFFSET %s
            """
            logs = self.execute_query_(query_recent_logs, (user_id, seven_days_ago, limit, offset), fetch=True,
                                       user_dict=True)
            if not logs:
                break
            for log in logs:
                log['timestamp'] = log['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
            recent_logs.extend(logs)
            offset += limit
            # TODO 最多返回50条，后续可以有翻页逻辑
            break

        # 查询7天之前的日志
        older_logs = []
        offset = 0
        while True:
            query_older_logs = f"""
                SELECT {need_info}
                FROM QaLogs
                WHERE user_id = %s AND timestamp < %s
                ORDER BY timestamp
                LIMIT %s OFFSET %s
            """
            logs = self.execute_query_(query_older_logs, (user_id, seven_days_ago, limit, offset), fetch=True,
                                       user_dict=True)
            if not logs:
                break
            for log in logs:
                log['timestamp'] = log['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
            older_logs.extend(logs)
            offset += limit
            # TODO 最多返回50条，后续可以有翻页逻辑
            break
        return qa_log, recent_logs, older_logs

    def check_bot_is_exist(self, bot_id):
        # 使用参数化查询
        query = "SELECT bot_id FROM QanythingBot WHERE bot_id = %s AND deleted = 0"
        result = self.execute_query_(query, (bot_id,), fetch=True)
        debug_logger.info("check_bot_exist {}".format(result))
        return result is not None and len(result) > 0

    def new_qanything_bot(self, bot_id, user_id, bot_name, description, head_image, prompt_setting, welcome_message,
                          kb_ids_str):
        query = "INSERT INTO QanythingBot (bot_id, user_id, bot_name, description, head_image, prompt_setting, welcome_message, kb_ids_str) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        self.execute_query_(query, (
        bot_id, user_id, bot_name, description, head_image, prompt_setting, welcome_message, kb_ids_str),
                            commit=True)
        return bot_id, "success"

    def delete_bot(self, user_id, bot_id):
        # 使用参数化查询
        query = "UPDATE QanythingBot SET deleted = 1 WHERE user_id = %s AND bot_id = %s"
        self.execute_query_(query, (user_id, bot_id), commit=True)

    def get_bot(self, user_id, bot_id):
        if not bot_id:
            query = "SELECT bot_id, bot_name, description, head_image, prompt_setting, welcome_message, kb_ids_str, update_time, user_id, llm_setting FROM QanythingBot WHERE user_id = %s AND deleted = 0"
            return self.execute_query_(query, (user_id,), fetch=True)
        elif not user_id:
            query = "SELECT bot_id, bot_name, description, head_image, prompt_setting, welcome_message, kb_ids_str, update_time, user_id, llm_setting FROM QanythingBot WHERE bot_id = %s AND deleted = 0"
            return self.execute_query_(query, (bot_id,), fetch=True)
        else:
            query = "SELECT bot_id, bot_name, description, head_image, prompt_setting, welcome_message, kb_ids_str, update_time, user_id, llm_setting FROM QanythingBot WHERE user_id = %s AND bot_id = %s AND deleted = 0"
            return self.execute_query_(query, (user_id, bot_id), fetch=True)

    def update_bot(self, user_id, bot_id, bot_name, description, head_image, prompt_setting, welcome_message,
                   kb_ids_str, update_time, llm_setting):
        llm_setting = json.dumps(llm_setting, ensure_ascii=False)
        query = "UPDATE QanythingBot SET bot_name = %s, description = %s, head_image = %s, prompt_setting = %s, welcome_message = %s, kb_ids_str = %s, update_time = %s, llm_setting = %s WHERE user_id = %s AND bot_id = %s AND deleted = 0"
        self.execute_query_(query, (
        bot_name, description, head_image, prompt_setting, welcome_message, kb_ids_str, update_time, llm_setting, user_id,
        bot_id), commit=True)

    def get_files_by_status(self, status):
        query = "SELECT file_id, file_name FROM File WHERE status = %s AND deleted = 0"
        return self.execute_query_(query, (status,), fetch=True)

    def get_file_location(self, file_id):
        query = "SELECT file_location FROM File WHERE file_id = %s"
        result = self.execute_query_(query, (file_id,), fetch=True)
        file_location = result[0][0] if result else None
        return file_location
