# Define variables
$networkName = "stalkme-network"
$webappImage = "saurabhlatambale/stalkme:latest"
$tunnelImage = "saurabhlatambale/stalkme-packetriot-image:latest"
$webappContainer = "stalkme-webapp"
$tunnelContainer = "stalkme-tunnel"
$url = "https://stalkme.fun"
$waitTime = 10
$maxAttempts = 5

# Function to check if a Docker network exists
function Test-DockerNetworkExists {
    param([string]$networkName)
    $networks = docker network ls --format "{{.Name}}"
    return $networks -contains $networkName
}
Write-Output "Starting Deployment..."
Write-Output "********************************************************"
# Create Docker network if it doesn't exist
Write-Output "Creating Docker network '$networkName' if not already exists..."
if (-not (Test-DockerNetworkExists -networkName $networkName)) {
    docker network create $networkName
    if ($LASTEXITCODE -ne 0) {
        Write-Output "Failed to create Docker network. It might already exist."
    } else {
        Write-Output "Docker network '$networkName' created successfully."
    }
} else {
    Write-Output "Docker network '$networkName' already exists."
}
Write-Output "********************************************************"
Write-Output "Deleting Docker container '$webappContainer' for refreshing deployment..."
docker stop $webappContainer
docker rm $webappContainer
Write-Output "Docker container '$webappContainer' has been deleted successfully..."
Write-Output "********************************************************"
Write-Output "Deleting local copy of Docker container Image'$tunnelContainer' for refreshing deployment..."
docker rmi $webappImage
Write-Output "Local copy of Docker container Image'$tunnelContainer' has been deleted successfully..."
Write-Output "********************************************************"
# Run Docker containers
Write-Output "Running Docker container '$webappContainer'..."
docker run -p 80:80 -d --name $webappContainer --restart=always $webappImage
if ($LASTEXITCODE -ne 0) {
    Write-Output "Failed to start Docker container '$webappContainer'."
}
Write-Output "********************************************************"
Write-Output "Deleting Docker container '$tunnelContainer' for refreshing deployment..."
docker stop $tunnelContainer
docker rm $tunnelContainer
Write-Output "Docker container '$tunnelContainer' has been deleted successfully..."
Write-Output "********************************************************"
Write-Output "Deleting local copy of Docker container Image'$tunnelContainer' for refreshing deployment..."
docker rmi $tunnelImage
Write-Output "Local copy of Docker container Image '$tunnelContainer' has been deleted successfully..."
Write-Output "********************************************************"
Write-Output "Running Docker container '$tunnelContainer'..."
docker run -d --name $tunnelContainer --restart=always $tunnelImage
if ($LASTEXITCODE -ne 0) {
    Write-Output "Failed to start Docker container '$tunnelContainer'."
}
Write-Output "********************************************************"
# Connect containers to Docker network
Write-Output "Connecting Docker containers to network '$networkName'..."
docker network connect $networkName $webappContainer
docker network connect $networkName $tunnelContainer
if ($LASTEXITCODE -ne 0) {
    Write-Output "Failed to connect Docker containers to network."
}
Write-Output "********************************************************"
# Wait for 10 seconds
Write-Output "Waiting for $waitTime seconds before checking the URL..."
Start-Sleep -Seconds $waitTime
Write-Output "********************************************************"
# Check if the URL is up, with retries
for ($attempt = 1; $attempt -le $maxAttempts; $attempt++) {
    Write-Output "Attempt $attempt to check if URL '$url' is up..."
    try {
        $response = Invoke-WebRequest -Uri $url -Method Head -UseBasicP
        if ($response.StatusCode -eq 200) {
            Write-Output "URL '$url' is up."
            Write-Output "********************************************************"
            break
        } else {
            Write-Output "URL '$url' returned status code $($response.StatusCode)."
            Write-Output "********************************************************"
        }
    } catch {
        Write-Output "Failed to access URL '$url'. Error: $_"
        Write-Output "********************************************************"
    }

    if ($attempt -lt $maxAttempts) {
        Write-Output "Waiting for $waitTime seconds before next attempt..."
        Write-Output "********************************************************"
        Start-Sleep -Seconds $waitTime
    } else {
        Write-Output "All attempts to check the URL have failed."
        Write-Output "********************************************************"
    }
}
