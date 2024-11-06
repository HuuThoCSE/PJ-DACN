from pyspark.sql import SparkSession
from hdfs import InsecureClient
import os

# Tạo SparkSession
spark = SparkSession.builder.appName("UploadImagesToHDFS").getOrCreate()

# Đường dẫn cục bộ đến thư mục chứa ảnh
local_dir = "/home/huuthocse/square_pick-2"
# Đường dẫn HDFS nơi bạn muốn lưu ảnh
hdfs_url = "http://namenode_host:50070"  # Thay bằng địa chỉ WebHDFS
hdfs_dir = "/datasets/"

# Tạo client HDFS bên ngoài hàm
client = InsecureClient(hdfs_url, user='your_username')

# Đọc toàn bộ file trong thư mục cục bộ
image_rdd = spark.sparkContext.binaryFiles(f"file://{local_dir}/*")

# Hàm để ghi file lên HDFS
def save_to_hdfs(file_data, hdfs_dir):
    file_path, file_content = file_data
    file_name = os.path.basename(file_path)  # Lấy tên file từ đường dẫn
    hdfs_file_path = os.path.join(hdfs_dir, file_name)  # Đường dẫn đầy đủ trên HDFS
    
    # Ghi dữ liệu lên HDFS
    client.write(hdfs_file_path, file_content, overwrite=True)

# Sử dụng lambda để truyền đối số hdfs_dir cho mỗi phần tử RDD
image_rdd.foreach(lambda file_data: save_to_hdfs(file_data, hdfs_dir))

# Dừng SparkSession
spark.stop()
