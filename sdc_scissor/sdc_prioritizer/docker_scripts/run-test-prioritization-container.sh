# Stop and remove the previous docker container
CHECK_CONTAINERS=$(docker container ls | grep 'test-prioritization-container')
if [ -n "$CHECK_CONTAINERS" ]; then
  echo "Stopping and removing existing container..."
  docker stop test-prioritization-container > /dev/null
  docker rm test-prioritization-container > /dev/null
fi


# Run a new docker container.
docker run -dit --name test-prioritization-container \
--mount type=bind,source="$(pwd)/data",target=/home/user/experiment/data \
--mount type=bind,source="$(pwd)/testPrioritization",target=/home/user/experiment/testPrioritization \
test-prioritization-image



 docker exec -it test-prioritization-container bash -c "pip install --editable /home/user/experiment"