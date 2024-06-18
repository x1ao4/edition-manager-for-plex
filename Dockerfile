# 使用 Alpine Linux 作为基础镜像
FROM python:3.8-alpine

# 将工作目录设置为 /app
WORKDIR /app

# 将当前目录的内容复制到容器的 /app 目录中
COPY . /app

# 安装需要的 Python 库
RUN pip install --no-cache-dir -r requirements.txt

# 将启动脚本添加到镜像中
COPY start.sh /start.sh
RUN chmod +x /start.sh

# 设置容器的启动命令
ENTRYPOINT ["/start.sh"]
CMD ["python", "edition-manager-for-plex.py"]
