from pyspark.sql import SparkSession
from hdfs import InsecureClient
import os

# Tạo SparkSession
spark = SparkSession.builder.appName("UploadImagesToHDFS").getOrCreate()

# Đường dẫn cục bộ đến thư mục chứa ảnh
local_dir = "/home/huuthocse/square_pick-2"
# Đường dẫn HDFS nơi bạn muốn lưu ảnh
hdfs_url = "http://namenode_host:50070"  # Địa chỉ WebHDFS
hdfs_dir = "/datasets/"

# Tạo client HDFS
client = InsecureClient(hdfs_url, user='your_username')

# Đọc toàn bộ file trong thư mục cục bộ
image_rdd = spark.sparkContext.binaryFiles(f"file://{local_dir}/*")

# Hàm để ghi file lên HDFS
def save_to_hdfs(file_data):
    file_path, file_content = file_data
    file_name = os.path.basename(file_path)  # Lấy tên file từ đường dẫn
    hdfs_file_path = os.path.join(hdfs_dir, file_name)  # Đường dẫn đầy đủ trên HDFS
    client.write(hdfs_file_path, file_content, overwrite=True)

# Ghi từng file lên HDFS
image_rdd.foreach(save_to_hdfs)

# Dừng SparkSession
spark.stop()