FROM cassandra:latest
EXPOSE 9042
CMD ["cassandra" "-f"]
