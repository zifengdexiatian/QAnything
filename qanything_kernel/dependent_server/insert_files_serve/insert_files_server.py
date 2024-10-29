import sys
import os

# 获取当前脚本的绝对路径
current_script_path = os.path.abspath(__file__)

# 将项目根目录添加到sys.path
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(current_script_path))))

sys.path.append(root_dir)
print(root_dir)

from sanic import Sanic, response
from qanything_kernel.utils.custom_log import insert_logger
from qanything_kernel.utils.general_utils import get_time_async
from qanything_kernel.core.retriever.general_document import LocalFileForInsert
from qanything_kernel.core.retriever.vectorstore import VectorStoreMilvusClient
from qanything_kernel.connector.database.mysql.mysql_client import KnowledgeBaseManager
from qanything_kernel.core.retriever.elasticsearchstore import StoreElasticSearchClient
from qanything_kernel.core.retriever.parent_retriever import ParentRetriever
from qanything_kernel.configs.model_config import MYSQL_HOST_LOCAL, MYSQL_PORT_LOCAL, \
    MYSQL_USER_LOCAL, MYSQL_PASSWORD_LOCAL, MYSQL_DATABASE_LOCAL, MAX_CHARS
from sanic.worker.manager import WorkerManager
import asyncio
import traceback
import time
import random
import aiomysql
import argparse
import json

WorkerManager.THRESHOLD = 6000

parser = argparse.ArgumentParser()
parser.add_argument('--port', type=int, default=8110, help='port')
parser.add_argument('--workers', type=int, default=4, help='workers')
# 检查是否是local或online，不是则报错
args = parser.parse_args()

INSERT_WORKERS = args.workers
insert_logger.info(f"INSERT_WORKERS: {INSERT_WORKERS}")

# 创建 Sanic 应用
app = Sanic("InsertFileService")

# 数据库配置
db_config = {
    'host': MYSQL_HOST_LOCAL,
    'port': MYSQL_PORT_LOCAL,
    'user': MYSQL_USER_LOCAL,
    'password': MYSQL_PASSWORD_LOCAL,
    'db': MYSQL_DATABASE_LOCAL,
}


@get_time_async
async def process_data(retriever, milvus_kb, mysql_client, file_info, time_record):
    parse_timeout_seconds = 300
    insert_timeout_seconds = 300
    content_length = -1
    status = 'green'
    process_start = time.perf_counter()
    insert_logger.info(f'Start insert file: {file_info}')
    _, file_id, user_id, file_name, kb_id, file_location, file_size, file_url, chunk_size = file_info
    # 获取格式为'2021-08-01 00:00:00'的时间戳
    insert_timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    mysql_client.update_knowlegde_base_latest_insert_time(kb_id, insert_timestamp)
    local_file = LocalFileForInsert(user_id, kb_id, file_id, file_location, file_name, file_url, chunk_size, mysql_client)
    msg = "success"
    chunks_number = 0
    mysql_client.update_file_msg(file_id, f'Processing:{random.randint(1, 5)}%')
    # 这里是把文件做向量化，然后写入Milvus的逻辑
    start = time.perf_counter()
    try:
        await asyncio.wait_for(
            asyncio.to_thread(local_file.split_file_to_docs),
            timeout=parse_timeout_seconds
        )
        content_length = sum([len(doc.page_content) for doc in local_file.docs])
        if content_length > MAX_CHARS:
            status = 'red'
            msg = f"{file_name} content_length too large, {content_length} >= MaxLength({MAX_CHARS})"
            return status, content_length, chunks_number, msg
        elif content_length == 0:
            status = 'red'
            msg = f"{file_name} content_length is 0, file content is empty or The URL exists anti-crawling or requires login."
            return status, content_length, chunks_number, msg
    except asyncio.TimeoutError:
        local_file.event.set()
        insert_logger.error(f'Timeout: split_file_to_docs took longer than {parse_timeout_seconds} seconds')
        status = 'red'
        msg = f"split_file_to_docs timeout: {parse_timeout_seconds}s"
        return status, content_length, chunks_number, msg
    except Exception as e:
        error_info = f'split_file_to_docs error: {traceback.format_exc()}'
        msg = error_info
        insert_logger.error(msg)
        status = 'red'
        msg = f"split_file_to_docs error"
        return status, content_length, chunks_number, msg
    end = time.perf_counter()
    time_record['parse_time'] = round(end - start, 2)
    insert_logger.info(f'parse time: {end - start} {len(local_file.docs)}')
    mysql_client.update_file_msg(file_id, f'Processing:{random.randint(5, 75)}%')

    try:
        start = time.perf_counter()
        chunks_number, insert_time_record = await asyncio.wait_for(
            retriever.insert_documents(local_file.docs, chunk_size),
            timeout=insert_timeout_seconds)
        insert_time = time.perf_counter()
        time_record.update(insert_time_record)
        insert_logger.info(f'insert time: {insert_time - start}')
    except asyncio.TimeoutError:
        insert_logger.error(f'Timeout: milvus insert took longer than {insert_timeout_seconds} seconds')
        expr = f'file_id == \"{local_file.file_id}\"'
        milvus_kb.delete_expr(expr)
        status = 'red'
        time_record['insert_timeout'] = True
        msg = f"milvus insert timeout: {insert_timeout_seconds}s"
        return status, content_length, chunks_number, msg
    except Exception as e:
        error_info = f'milvus insert error: {traceback.format_exc()}'
        insert_logger.error(error_info)
        status = 'red'
        time_record['insert_error'] = True
        msg = f"milvus insert error"
        return status, content_length, chunks_number, msg

    mysql_client.update_file_msg(file_id, f'Processing:{random.randint(75, 100)}%')
    time_record['upload_total_time'] = round(time.perf_counter() - process_start, 2)
    mysql_client.update_file_upload_infos(file_id, time_record)
    insert_logger.info(f'insert_files_to_milvus: {user_id}, {kb_id}, {file_id}, {file_name}, {status}')
    msg = json.dumps(time_record, ensure_ascii=False)
    return status, content_length, chunks_number, msg


async def check_and_process(pool):
    process_type = 'MainProcess' if 'SANIC_WORKER_NAME' not in os.environ else os.environ['SANIC_WORKER_NAME']
    worker_id = int(process_type.split('-')[-2])
    insert_logger.info(f"{os.getpid()} worker_id is {worker_id}")
    mysql_client = KnowledgeBaseManager()
    milvus_kb = VectorStoreMilvusClient()
    es_client = StoreElasticSearchClient()
    retriever = ParentRetriever(milvus_kb, mysql_client, es_client)
    while True:
        sleep_time = 3
        # worker_id 根据时间变化，每x分钟变一次，获取当前时间的分钟数
        minutes = int(int(time.strftime("%M", time.localtime())) / INSERT_WORKERS)
        dynamic_worker_id = (worker_id + minutes) % INSERT_WORKERS
        id = None
        try:
            async with pool.acquire() as conn:  # 获取连接
                async with conn.cursor() as cur:  # 创建游标
                    query = f"""
                        SELECT id, timestamp, file_id, file_name FROM File
                        WHERE status = 'gray' AND MOD(id, %s) = %s AND deleted = 0
                        ORDER BY timestamp ASC LIMIT 1;
                    """

                    await cur.execute(query, (INSERT_WORKERS, dynamic_worker_id))

                    file_to_update = await cur.fetchone()

                    if file_to_update:
                        insert_logger.info(f"{worker_id}, file_to_update: {file_to_update}")
                        # 把files_to_update按照timestamp排序, 获取时间最早的那条记录的id
                        # file_to_update = sorted(files_to_update, key=lambda x: x[1])[0]

                        id, timestamp, file_id, file_name = file_to_update
                        # 更新这条记录的状态
                        await cur.execute("""
                            UPDATE File SET status='yellow'
                            WHERE id=%s;
                        """, (id,))
                        await conn.commit()
                        insert_logger.info(f"UPDATE FILE: {timestamp}, {file_id}, {file_name}, yellow")

                        await cur.execute(
                            "SELECT id, file_id, user_id, file_name, kb_id, file_location, file_size, file_url, "
                            "chunk_size FROM File WHERE id=%s", (id,))
                        file_info = await cur.fetchone()

                        time_record = {}
                        # 现在处理数据
                        status, content_length, chunks_number, msg = await process_data(retriever, milvus_kb,
                                                                                        mysql_client,
                                                                                        file_info, time_record)

                        insert_logger.info('time_record: ' + json.dumps(time_record, ensure_ascii=False))
                        # 更新文件处理后的状态和相关信息
                        await cur.execute(
                            "UPDATE File SET status=%s, content_length=%s, chunks_number=%s, msg=%s WHERE id=%s",
                            (status, content_length, chunks_number, msg, file_info[0]))
                        await conn.commit()
                        insert_logger.info(f"UPDATE FILE: {timestamp}, {file_id}, {file_name}, {status}")
                        sleep_time = 0.1
                    else:
                        await conn.commit()
        except Exception as e:
            insert_logger.error('MySQL或Milvus 连接异常：' + str(e))
            try:
                async with pool.acquire() as conn:
                    async with conn.cursor() as cur:
                        insert_logger.error(f"process_files Error {traceback.format_exc()}")
                        # 如果file的status是yellow，就改为red
                        if id is not None:
                            await cur.execute("UPDATE File SET status='red' WHERE id=%s AND status='yellow'", (id,))
                            await conn.commit()

                            await cur.execute(
                                "SELECT id, file_id, user_id, file_name, kb_id, file_location, file_size FROM File WHERE id=%s",
                                (id,))
                            file_info = await cur.fetchone()

                            insert_logger.info(f"UPDATE FILE: {timestamp}, {file_id}, {file_name}, yellow2red")
                            _, file_id, user_id, file_name, kb_id, file_location, file_size = file_info
                            # await post_data(user_id=user_id, charsize=-1, docid=file_id, status='red', msg="Milvus service exception")
            except Exception as e:
                insert_logger.error('MySQL 二次连接异常：' + str(e))
        finally:
            await asyncio.sleep(sleep_time)


@app.listener('after_server_stop')
async def close_db(app, loop):
    # 关闭数据库连接池
    app.ctx.pool.close()
    await app.ctx.pool.wait_closed()


@app.listener('before_server_start')
async def setup_workers(app, loop):
    # 创建数据库连接池
    app.ctx.pool = await aiomysql.create_pool(**db_config, minsize=1, maxsize=16, loop=loop, autocommit=False,
                                              init_command='SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED')  # 更改事务隔离级别
    app.add_task(check_and_process(app.ctx.pool))


# 启动服务
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=args.port, workers=INSERT_WORKERS, access_log=False)
