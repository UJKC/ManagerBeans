FROM ubuntu:latest

# Command to create the files inside the volume at runtime
CMD ["sh", "-c", "mkdir -p /dummy_volume && touch /dummy_volume/dummy_file.txt && echo 'Dummy file created.' > /dummy_volume/creation_message.txt && sleep infinity"]
