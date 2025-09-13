// Video Event Detection System JavaScript

class VideoEventDetector {
    constructor() {
        this.currentVideo = null;
        this.currentResults = [];
        this.supportedFormats = ['.mp4', '.webm', '.avi', '.mov', '.mkv'];
        this.maxFileSize = 500 * 1024 * 1024; // 500MB in bytes
        
        // Sample events data for mock detection
        this.sampleEvents = {
            "person walking": {
                timestamps: ["00:15", "01:23", "02:45"],
                confidence: [87, 92, 78]
            },
            "car driving": {
                timestamps: ["00:45", "02:10"],
                confidence: [95, 89]
            },
            "door opening": {
                timestamps: ["00:30", "01:50"],
                confidence: [84, 91]
            },
            "phone ringing": {
                timestamps: ["01:05"],
                confidence: [96]
            }
        };
        
        this.initializeElements();
        this.bindEvents();
        this.initializeFormState();
    }
    
    initializeElements() {
        // Upload elements
        this.uploadArea = document.getElementById('uploadArea');
        this.videoInput = document.getElementById('videoInput');
        this.uploadProgress = document.getElementById('uploadProgress');
        this.progressFill = document.getElementById('progressFill');
        this.progressText = document.getElementById('progressText');
        this.videoPreview = document.getElementById('videoPreview');
        this.previewThumbnail = document.getElementById('previewThumbnail');
        this.previewName = document.getElementById('previewName');
        this.previewSize = document.getElementById('previewSize');
        
        // Configuration elements
        this.configForm = document.getElementById('configForm');
        this.eventDescription = document.getElementById('eventDescription');
        this.sensitivity = document.getElementById('sensitivity');
        this.confidenceThreshold = document.getElementById('confidenceThreshold');
        this.confidenceValue = document.getElementById('confidenceValue');
        this.startDetection = document.getElementById('startDetection');
        this.clearForm = document.getElementById('clearForm');
        
        // Player elements
        this.playerSection = document.getElementById('playerSection');
        this.videoPlayer = document.getElementById('videoPlayer');
        this.eventMarkers = document.getElementById('eventMarkers');
        this.currentTime = document.getElementById('currentTime');
        this.duration = document.getElementById('duration');
        
        // Results elements
        this.resultsSection = document.getElementById('resultsSection');
        this.resultsList = document.getElementById('resultsList');
        this.exportResults = document.getElementById('exportResults');
        this.filterResults = document.getElementById('filterResults');
        this.resultsFilter = document.getElementById('resultsFilter');
        this.minConfidence = document.getElementById('minConfidence');
        this.minConfidenceValue = document.getElementById('minConfidenceValue');
        
        // Processing modal
        this.processingModal = document.getElementById('processingModal');
        this.processingProgress = document.getElementById('processingProgress');
        this.processingText = document.getElementById('processingText');
        
        // Toast container
        this.toastContainer = document.getElementById('toastContainer');
    }
    
    initializeFormState() {
        // Ensure Start Detection button is initially disabled
        this.startDetection.disabled = true;
        this.startDetection.classList.add('btn--disabled');
        
        // Initialize confidence threshold display
        this.confidenceValue.textContent = this.confidenceThreshold.value;
        this.minConfidenceValue.textContent = this.minConfidence.value;
    }
    
    bindEvents() {
        // Upload events
        this.uploadArea.addEventListener('click', () => this.videoInput.click());
        this.uploadArea.addEventListener('dragover', this.handleDragOver.bind(this));
        this.uploadArea.addEventListener('dragleave', this.handleDragLeave.bind(this));
        this.uploadArea.addEventListener('drop', this.handleDrop.bind(this));
        this.videoInput.addEventListener('change', this.handleFileSelect.bind(this));
        
        // Browse button
        const browseBtns = document.querySelectorAll('.upload-browse-btn');
        browseBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                this.videoInput.click();
            });
        });
        
        // Configuration events
        this.configForm.addEventListener('submit', this.handleStartDetection.bind(this));
        this.clearForm.addEventListener('click', this.handleClearForm.bind(this));
        
        // Enhanced confidence threshold slider event
        this.confidenceThreshold.addEventListener('input', (e) => {
            this.confidenceValue.textContent = e.target.value;
        });
        
        this.confidenceThreshold.addEventListener('change', (e) => {
            this.confidenceValue.textContent = e.target.value;
        });
        
        // Sensitivity dropdown change event
        this.sensitivity.addEventListener('change', (e) => {
            console.log('Sensitivity changed to:', e.target.value);
        });
        
        // Results events
        this.exportResults.addEventListener('click', this.handleExportResults.bind(this));
        this.filterResults.addEventListener('click', this.toggleResultsFilter.bind(this));
        this.minConfidence.addEventListener('input', (e) => {
            this.minConfidenceValue.textContent = e.target.value;
            this.filterResultsByConfidence(parseInt(e.target.value));
        });
        
        // Video player events
        this.videoPlayer.addEventListener('loadedmetadata', this.handleVideoLoaded.bind(this));
        this.videoPlayer.addEventListener('timeupdate', this.handleTimeUpdate.bind(this));
    }
    
    handleDragOver(e) {
        e.preventDefault();
        this.uploadArea.classList.add('drag-over');
    }
    
    handleDragLeave(e) {
        e.preventDefault();
        this.uploadArea.classList.remove('drag-over');
    }
    
    handleDrop(e) {
        e.preventDefault();
        this.uploadArea.classList.remove('drag-over');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            this.processFile(files[0]);
        }
    }
    
    handleFileSelect(e) {
        const file = e.target.files[0];
        if (file) {
            this.processFile(file);
        }
    }
    
    processFile(file) {
        // Validate file
        if (!this.validateFile(file)) {
            return;
        }
        
        this.currentVideo = file;
        this.showUploadProgress();
        
        // Simulate upload progress
        this.simulateUploadProgress(() => {
            this.generateVideoPreview(file);
            this.enableDetectionForm();
        });
    }
    
    validateFile(file) {
        // Check file type
        const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
        if (!this.supportedFormats.includes(fileExtension)) {
            this.showToast('Unsupported file format. Please use MP4, WebM, AVI, MOV, or MKV.', 'error');
            return false;
        }
        
        // Check file size
        if (file.size > this.maxFileSize) {
            this.showToast(`File too large. Maximum size is ${this.formatFileSize(this.maxFileSize)}.`, 'error');
            return false;
        }
        
        return true;
    }
    
    showUploadProgress() {
        this.uploadProgress.classList.remove('hidden');
        this.videoPreview.classList.add('hidden');
    }
    
    simulateUploadProgress(callback) {
        let progress = 0;
        const interval = setInterval(() => {
            progress += Math.random() * 20;
            if (progress >= 100) {
                progress = 100;
                clearInterval(interval);
                this.uploadProgress.classList.add('hidden');
                callback();
            }
            
            this.progressFill.style.width = `${progress}%`;
            this.progressText.textContent = `Uploading... ${Math.round(progress)}%`;
        }, 200);
    }
    
    generateVideoPreview(file) {
        const video = document.createElement('video');
        video.src = URL.createObjectURL(file);
        
        video.addEventListener('loadedmetadata', () => {
            // Create canvas to capture thumbnail
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            
            video.currentTime = 1; // Capture frame at 1 second
        });
        
        video.addEventListener('seeked', () => {
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            ctx.drawImage(video, 0, 0);
            
            this.previewThumbnail.src = canvas.toDataURL();
            this.previewName.textContent = file.name;
            this.previewSize.textContent = this.formatFileSize(file.size);
            
            this.videoPreview.classList.remove('hidden');
            URL.revokeObjectURL(video.src);
        });
        
        // Fallback for preview generation
        video.addEventListener('error', () => {
            // Use a default thumbnail
            this.previewThumbnail.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iODAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA4MCA2MCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHJlY3Qgd2lkdGg9IjgwIiBoZWlnaHQ9IjYwIiBmaWxsPSIjZjNmNGY2Ii8+CjxwYXRoIGQ9Ik0zMiAyMkw0OCAzMkwzMiA0MlYyMloiIGZpbGw9IiM5Y2EzYWYiLz4KPC9zdmc+';
            this.previewName.textContent = file.name;
            this.previewSize.textContent = this.formatFileSize(file.size);
            this.videoPreview.classList.remove('hidden');
            URL.revokeObjectURL(video.src);
        });
    }
    
    enableDetectionForm() {
        this.startDetection.disabled = false;
        this.startDetection.classList.remove('btn--disabled');
        this.showToast('Video uploaded successfully!', 'success');
    }
    
    handleStartDetection(e) {
        e.preventDefault();
        
        const eventDesc = this.eventDescription.value.trim();
        if (!eventDesc) {
            this.showToast('Please enter an event to detect.', 'error');
            return;
        }
        
        if (!this.currentVideo) {
            this.showToast('Please upload a video first.', 'error');
            return;
        }
        
        this.startDetectionProcess(eventDesc);
    }
    
    startDetectionProcess(eventDescription) {
        this.showProcessingModal();
        
        // Simulate AI processing
        this.simulateProcessing(() => {
            const results = this.generateMockResults(eventDescription);
            this.displayResults(results);
            this.setupVideoPlayer();
            this.hideProcessingModal();
        });
    }
    
    showProcessingModal() {
        this.processingModal.classList.remove('hidden');
    }
    
    hideProcessingModal() {
        this.processingModal.classList.add('hidden');
    }
    
    simulateProcessing(callback) {
        let progress = 0;
        const interval = setInterval(() => {
            progress += Math.random() * 15;
            if (progress >= 100) {
                progress = 100;
                clearInterval(interval);
                setTimeout(callback, 500);
            }
            
            this.processingProgress.style.width = `${progress}%`;
            this.processingText.textContent = `${Math.round(progress)}%`;
        }, 300);
    }
    
    generateMockResults(eventDescription) {
        const results = [];
        const lowerDesc = eventDescription.toLowerCase();
        
        // Check if event matches any sample events
        let matchedEvent = null;
        for (const [key, data] of Object.entries(this.sampleEvents)) {
            if (lowerDesc.includes(key) || key.includes(lowerDesc.split(' ')[0])) {
                matchedEvent = data;
                break;
            }
        }
        
        if (matchedEvent) {
            // Use predefined sample data
            matchedEvent.timestamps.forEach((timestamp, index) => {
                results.push({
                    event: eventDescription,
                    startTime: timestamp,
                    endTime: this.addSecondsToTimestamp(timestamp, Math.random() * 5 + 2),
                    confidence: matchedEvent.confidence[index],
                    thumbnail: this.previewThumbnail.src
                });
            });
        } else {
            // Generate random results
            const numResults = Math.floor(Math.random() * 4) + 2; // 2-5 results
            const videoDuration = 180; // Assume 3 minutes for demo
            
            for (let i = 0; i < numResults; i++) {
                const startSeconds = Math.floor(Math.random() * videoDuration);
                const startTime = this.secondsToTimestamp(startSeconds);
                const endTime = this.secondsToTimestamp(startSeconds + Math.random() * 5 + 2);
                
                results.push({
                    event: eventDescription,
                    startTime: startTime,
                    endTime: endTime,
                    confidence: Math.floor(Math.random() * 20) + 75, // 75-95%
                    thumbnail: this.previewThumbnail.src
                });
            }
        }
        
        this.currentResults = results;
        return results;
    }
    
    displayResults(results) {
        this.resultsList.innerHTML = '';
        
        results.forEach((result, index) => {
            const resultElement = this.createResultElement(result, index);
            this.resultsList.appendChild(resultElement);
        });
        
        this.resultsSection.classList.remove('hidden');
        this.showToast(`Found ${results.length} events!`, 'success');
    }
    
    createResultElement(result, index) {
        const div = document.createElement('div');
        div.className = 'result-item';
        div.dataset.index = index;
        
        const confidenceClass = result.confidence >= 90 ? 'high' : 
                               result.confidence >= 75 ? 'medium' : 'low';
        
        div.innerHTML = `
            <div class="result-header">
                <h4 class="result-title">${result.event}</h4>
                <span class="result-confidence ${confidenceClass}">${result.confidence}%</span>
            </div>
            <div class="result-timestamps">
                <div class="result-timestamp">
                    <span>Start: ${result.startTime}</span>
                </div>
                <div class="result-timestamp">
                    <span>End: ${result.endTime}</span>
                </div>
            </div>
        `;
        
        div.addEventListener('click', () => this.jumpToTimestamp(result.startTime, index));
        
        return div;
    }
    
    setupVideoPlayer() {
        if (this.currentVideo) {
            this.videoPlayer.src = URL.createObjectURL(this.currentVideo);
            this.playerSection.classList.remove('hidden');
        }
    }
    
    handleVideoLoaded() {
        this.updateDuration();
        this.createEventMarkers();
    }
    
    updateDuration() {
        const duration = this.videoPlayer.duration;
        this.duration.textContent = this.secondsToTimestamp(duration);
    }
    
    createEventMarkers() {
        this.eventMarkers.innerHTML = '';
        const videoDuration = this.videoPlayer.duration;
        
        this.currentResults.forEach((result, index) => {
            const startSeconds = this.timestampToSeconds(result.startTime);
            const position = (startSeconds / videoDuration) * 100;
            
            const marker = document.createElement('div');
            marker.className = 'event-marker';
            marker.style.left = `${position}%`;
            marker.title = `${result.event} at ${result.startTime}`;
            marker.addEventListener('click', () => this.jumpToTimestamp(result.startTime, index));
            
            this.eventMarkers.appendChild(marker);
        });
    }
    
    handleTimeUpdate() {
        const currentSeconds = this.videoPlayer.currentTime;
        this.currentTime.textContent = this.secondsToTimestamp(currentSeconds);
        
        // Highlight active result
        this.updateActiveResult(currentSeconds);
    }
    
    updateActiveResult(currentSeconds) {
        const resultItems = document.querySelectorAll('.result-item');
        
        resultItems.forEach((item, index) => {
            const result = this.currentResults[index];
            const startSeconds = this.timestampToSeconds(result.startTime);
            const endSeconds = this.timestampToSeconds(result.endTime);
            
            if (currentSeconds >= startSeconds && currentSeconds <= endSeconds) {
                item.classList.add('active');
            } else {
                item.classList.remove('active');
            }
        });
    }
    
    jumpToTimestamp(timestamp, resultIndex) {
        const seconds = this.timestampToSeconds(timestamp);
        this.videoPlayer.currentTime = seconds;
        
        // Highlight the clicked result
        const resultItems = document.querySelectorAll('.result-item');
        resultItems.forEach(item => item.classList.remove('active'));
        if (resultItems[resultIndex]) {
            resultItems[resultIndex].classList.add('active');
        }
    }
    
    handleClearForm() {
        this.configForm.reset();
        this.confidenceValue.textContent = '75';
        this.minConfidenceValue.textContent = '0';
        this.startDetection.disabled = true;
        this.startDetection.classList.add('btn--disabled');
        
        // Hide sections
        this.videoPreview.classList.add('hidden');
        this.playerSection.classList.add('hidden');
        this.resultsSection.classList.add('hidden');
        this.uploadProgress.classList.add('hidden');
        
        // Clear data
        this.currentVideo = null;
        this.currentResults = [];
        
        // Revoke object URLs
        if (this.videoPlayer.src) {
            URL.revokeObjectURL(this.videoPlayer.src);
            this.videoPlayer.src = '';
        }
        
        // Clear file input
        this.videoInput.value = '';
        
        this.showToast('Form cleared', 'info');
    }
    
    handleExportResults() {
        if (this.currentResults.length === 0) {
            this.showToast('No results to export', 'error');
            return;
        }
        
        const exportData = {
            video: this.currentVideo.name,
            detectionSettings: {
                event: this.eventDescription.value,
                sensitivity: this.sensitivity.value,
                confidenceThreshold: this.confidenceThreshold.value
            },
            results: this.currentResults
        };
        
        const blob = new Blob([JSON.stringify(exportData, null, 2)], {
            type: 'application/json'
        });
        
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `detection-results-${Date.now()}.json`;
        a.click();
        
        URL.revokeObjectURL(url);
        this.showToast('Results exported successfully!', 'success');
    }
    
    toggleResultsFilter() {
        this.resultsFilter.classList.toggle('hidden');
    }
    
    filterResultsByConfidence(minConfidence) {
        const resultItems = document.querySelectorAll('.result-item');
        
        resultItems.forEach((item, index) => {
            const result = this.currentResults[index];
            if (result.confidence >= minConfidence) {
                item.style.display = 'block';
            } else {
                item.style.display = 'none';
            }
        });
    }
    
    // Utility functions
    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
    
    secondsToTimestamp(seconds) {
        const mins = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }
    
    timestampToSeconds(timestamp) {
        const [mins, secs] = timestamp.split(':').map(Number);
        return mins * 60 + secs;
    }
    
    addSecondsToTimestamp(timestamp, seconds) {
        const totalSeconds = this.timestampToSeconds(timestamp) + Math.floor(seconds);
        return this.secondsToTimestamp(totalSeconds);
    }
    
    showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.innerHTML = `
            <span>${message}</span>
        `;
        
        this.toastContainer.appendChild(toast);
        
        // Auto remove after 4 seconds
        setTimeout(() => {
            if (toast.parentNode) {
                toast.remove();
            }
        }, 4000);
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new VideoEventDetector();
});