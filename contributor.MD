To run using Dockerfile, execute the following commands:

- First build the image:
  `docker build -t cassandra-image`
- Run the container and expose the ports:
  `docker run -d -p 9042:9042 --name my-cassandra-container cassandra-image`
