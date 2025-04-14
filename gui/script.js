// Video paths
const videoPaths = [
    "vids/23712-337108764_medium.mp4",
    "vids/cars.mp4",
    "vids/23712-337108764_medium.mp4",
    "vids/cars.mp4"
];

// Mask paths
const maskPaths = [
    "masks/vid1.png",
    "masks/vid2.png",
    "masks/vid1.png",
    "masks/vid2.png"
];

let currentVideoIndex = 0;
let yoloExecuted = false;
const videoElement = document.getElementById('video-display');
const trafficLights = document.querySelectorAll('.traffic-light');

// Function to update traffic lights
function updateTrafficLights(activeIndex) {
    console.log(`Updating traffic lights. Active index: ${activeIndex}`);
    trafficLights.forEach((light, index) => {
        const redLight = light.querySelector('.red');
        const yellowLight = light.querySelector('.yellow');
        const greenLight = light.querySelector('.green');

        // Reset all lights
        redLight.classList.remove('active');
        yellowLight.classList.remove('active');
        greenLight.classList.remove('active');

        // Set active light
        if (index === activeIndex) {
            greenLight.classList.add('active');
            console.log(`Setting green light for index ${index}`);
        } else {
            redLight.classList.add('active');
            console.log(`Setting red light for index ${index}`);
        }
    });
}

// Function to handle video end
function handleVideoEnd() {
    console.log('Video ended');
    // Reset YOLO execution flag
    yoloExecuted = false;
    
    // Update traffic lights - turn current light to red
    updateTrafficLights(currentVideoIndex);
    
    // Switch to next video
    currentVideoIndex = (currentVideoIndex + 1) % videoPaths.length;
    console.log(`Switching to video ${currentVideoIndex}: ${videoPaths[currentVideoIndex]}`);
    
    // Set up the next video
    videoElement.src = videoPaths[currentVideoIndex];
    videoElement.load(); // Ensure the video is loaded
    videoElement.play().catch(error => {
        console.error('Error playing video:', error);
    });
    
    // Update traffic lights for new video
    updateTrafficLights(currentVideoIndex);
}

// Function to run YOLO (placeholder for actual implementation)
async function runYOLO() {
    if (!yoloExecuted) {
        try {
            console.log(`Running YOLO on next video: ${videoPaths[(currentVideoIndex + 1) % videoPaths.length]}`);
            yoloExecuted = true;
        } catch (error) {
            console.error('YOLO execution error:', error);
        }
    }
}

// Initialize the application
function init() {
    console.log('Initializing application');
    
    // Set up video element
    videoElement.src = videoPaths[0];
    videoElement.addEventListener('ended', handleVideoEnd);
    videoElement.addEventListener('error', (e) => {
        console.error('Video error:', e);
    });
    
    // Set up YOLO execution timer
    videoElement.addEventListener('timeupdate', () => {
        const duration = videoElement.duration;
        const currentTime = videoElement.currentTime;
        
        if (duration && currentTime) {
            // Run YOLO 3 seconds before the video ends
            if (duration - currentTime <= 3 && !yoloExecuted) {
                runYOLO();
            }
        }
    });
    
    // Start with first video
    videoElement.play().then(() => {
        console.log('First video started playing');
        updateTrafficLights(0);
    }).catch(error => {
        console.error('Error playing first video:', error);
    });
}

// Start the application
init(); 