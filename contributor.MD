First install the requirements by running the following commands:
  `python3 -m venv venv`
  `source venv/bin/active`
  `pip install -r requirements.txt`


To run using Dockerfile, execute the following commands:

- First build the image:
  `docker build -t cassandra-image`
- Run the container and expose the ports:
  `docker run -d -p 9042:9042 --name my-cassandra-container cassandra-image`

