# Stop and remove the previous docker container
CHECK_CONTAINERS=$(docker container ls | grep 'test-prioritization-container')
if [ -n "$CHECK_CONTAINERS" ]; then
  echo "Stopping and removing existing container..."
  docker stop test-prioritization-container > /dev/null
  docker rm test-prioritization-container > /dev/null
fi

# Remove previous docker image
CHECK_IMAGES=$(docker images | grep 'test-prioritization-image')
if [ -n "$CHECK_IMAGES" ]; then
  docker rmi 'test-prioritization-image'
fi

# Build the new image from Dockerfile.testPrioritization
docker image build -t test-prioritization-image \
$(pwd) -f Dockerfile.testPrioritization
