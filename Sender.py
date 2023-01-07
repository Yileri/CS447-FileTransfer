"""
Client that sends the file (uploads)
"""
import socket
import tqdm 
import os
import boto3
import argparse

ec2 = boto3.client("ec2", "us-east-1", aws_access_key_id="AKIATWW5D5EFTRY6JQE6",
                   aws_secret_access_key="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")

SEPARATOR = "<SEPARATOR>"

BUFFER_SIZE = 1024 * 4


def send_file(filename, host, port):
    # get the file size
    filesize = os.path.getsize(filename)
    # create the client socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"[+] Connecting to {host}:{port}")
    s.connect((host, port))
    print("[+] Connected.")

    # send the filename and filesize
    s.send(f"{filename}{SEPARATOR}{filesize}".encode())

    # start sending the file
    progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "rb") as f:
        while True:
            # read the bytes from the file
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                # file transmitting is done
                break
            # we use sendall to assure transimission in
            # busy networks
            s.sendall(bytes_read)
            # update the progress bar
            progress.update(len(bytes_read))

    # close the socket
    s.close()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Simple File Sender")
    parser.add_argument("file", help="File name to send")
    parser.add_argument("host", help="The host/IP address of the receiver")
    parser.add_argument("-p", "--port", help="Port to use, default is 5001", type=int, default=5001)
    args = parser.parse_args()
    filename = args.file
    host = args.host  #3.87.215.252 süperi
    port = args.port
    send_file(filename, host, port)
