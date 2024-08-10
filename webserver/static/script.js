document.getElementById('fetchButton').addEventListener('click', async () => {
    const username = document.getElementById('usernameInput').value;
    if (!username) {
        alert('Please enter a username.');
        return;
    }

    const resultLabel = document.getElementById('resultLabel');
    const imagePopup = document.getElementById('imagePopup');
    const profileImage = document.getElementById('profileImage');
    const downloadButton = document.getElementById('downloadButton');

    try {
        // Show loading indicator (if implemented)
        resultLabel.textContent = 'Fetching profile picture...';

        // Fetch the profile picture URL from the Flask API
        const response = await fetch(`/api/getProfilePicture?username=${encodeURIComponent(username)}`);
        const data = await response.json();

        if (data && data.imageUrl) {
            profileImage.src = data.imageUrl;
            imagePopup.style.display = 'flex';
            downloadButton.disabled = false;
            resultLabel.textContent = '';

            // Remove existing click listener to avoid multiple attachments
            downloadButton.removeEventListener('click', handleDownload);
            downloadButton.addEventListener('click', handleDownload);
        } else {
            resultLabel.textContent = data.message || 'Profile picture not found or user is private.';
        }
    } catch (error) {
        resultLabel.textContent = `Error: ${error.message}`;
    }
});

async function handleDownload() {
    const imageUrl = document.getElementById('profileImage').src;

    try {
        // Fetch the image as a Blob
        const response = await fetch(imageUrl);
        const blob = await response.blob();

        // Create a temporary link element
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = 'profile_image.jpg';

        // Append to the document to trigger the download
        document.body.appendChild(link);
        link.click();

        // Clean up and remove the link
        document.body.removeChild(link);
    } catch (error) {
        console.error('Error downloading the image:', error);
    }
}

document.getElementById('closePopup').addEventListener('click', () => {
    document.getElementById('imagePopup').style.display = 'none';
});
