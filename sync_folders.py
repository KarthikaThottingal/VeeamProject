import os
import shutil
import time
import argparse
from datetime import datetime

#git repository created

def sync_folders(source_folder, replica_folder, interval, log_file):
    print("Start --> In Synchroization Function")
    try:
        while True:
            # check if source folder is present
            if not os.path.exists(source_folder):
                print("Source Folder '{source_folder}' does not exist.")
                return

            # create replica folder if not present
            if not os.path.exists(replica_folder):
                os.makedirs(replica_folder)

            # read all source folder
            for root, dirs, files in os.walk(source_folder):
                for file in files:
                    source_file = os.path.join(root, file)
                    replica_file = os.path.join(replica_folder, os.path.relpath(source_file, source_folder))

                    # check if both files are same or not
                    if os.path.exists(replica_file) and os.path.getsize(replica_file) == os.path.getsize(source_file):
                        continue

                    # replicate the files
                    shutil.copy2(source_file, replica_file)
                    print(f"Copied: {source_file} -> {replica_file}")
                    log_operation(log_file, f"Copied: {source_file} -> {replica_file}")

            # To remove files from replicate folder
            for root, dirs, files in os.walk(replica_folder):
                for file in files:
                    replica_file = os.path.join(root, file)
                    source_file = os.path.join(source_folder, os.path.relpath(replica_file, replica_folder))

                    if not os.path.exists(source_file):
                        os.remove(replica_file)
                        print(f"Removed: {replica_file}")
                        log_operation(log_file, f"Removed: {replica_file}")

            time.sleep(interval)

    except KeyboardInterrupt:
        print("Synchronization stopped by user.")
    except Exception as e:
        print(f"Error: {str(e)}")

def log_operation(log_file, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a") as f:
        f.write(f"{timestamp} - {message}\n")

if __name__ == "__main__":

  parser = argparse.ArgumentParser(description="Folder Synchronization Program")
  parser.add_argument("source_folder", help="Path to the source folder")
  parser.add_argument("replica_folder", help="Path to the replica folder")
  parser.add_argument("interval", type=int, help="Synchronization interval in seconds")
  parser.add_argument("log_file", help="Path to the log file")

args = parser.parse_args()

sync_folders(args.source_folder, args.replica_folder, args.interval, args.log_file)


