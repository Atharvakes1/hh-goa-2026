// Grab the elements from our HTML
// Grab the elements from our HTML
const uploadInput = document.getElementById('upload') as HTMLInputElement;
const canvas = document.getElementById('canvas') as HTMLCanvasElement;
const ctx = canvas.getContext('2d');
const downloadBtn = document.getElementById('downloadBtn') as HTMLButtonElement;
const shareBtn = document.getElementById('shareBtn') as HTMLButtonElement;

// New UI Elements for Format B
const radioA = document.getElementById('radioA') as HTMLInputElement;
const radioB = document.getElementById('radioB') as HTMLInputElement;
const textInputs = document.getElementById('textInputs') as HTMLDivElement;
const nameInput = document.getElementById('nameInput') as HTMLInputElement;
const roleInput = document.getElementById('roleInput') as HTMLInputElement;

// We store the uploaded image so we can redraw it instantly without re-uploading
let currentImg: HTMLImageElement | null = null;
// Preload the official branding assets from the public folder
const frameImg = new Image();
frameImg.src = '/frame.png'; 

const badgeImg = new Image();
badgeImg.src = '/badge.png';

// --- EVENT LISTENERS ---

// Toggle visibility of text boxes based on radio selection
function handleFormatChange() {
  if (radioB.checked) {
    textInputs.style.display = 'flex';
  } else {
    textInputs.style.display = 'none';
  }
  renderCanvas(); // Redraw immediately when format changes
}

radioA.addEventListener('change', handleFormatChange);
radioB.addEventListener('change', handleFormatChange);

// Re-render the canvas in real-time as the user types
nameInput.addEventListener('input', renderCanvas);
roleInput.addEventListener('input', renderCanvas);

// Handle file upload
uploadInput?.addEventListener('change', (event) => {
  const target = event.target as HTMLInputElement;
  const file = target.files?.[0];
  if (!file || !ctx) return;

  const reader = new FileReader();
  reader.onload = (e) => {
    const img = new Image();
    img.onload = () => {
      currentImg = img;
      renderCanvas(); // Draw for the first time
      
      // Enable buttons
      downloadBtn.disabled = false;
      shareBtn.disabled = false;
    };
    img.src = e.target?.result as string;
  };
  reader.readAsDataURL(file);
});


// --- THE MASTER DRAWING FUNCTION ---
function renderCanvas() {
  if (!ctx || !currentImg) return;

  if (radioA.checked) {
    // ------------------------------------
    // FORMAT A: PFP FRAME (400x400 Square)
    // ------------------------------------
    canvas.width = 400;
    canvas.height = 400;

    // 1. Smart Crop
    const size = Math.min(currentImg.width, currentImg.height);
    const startX = (currentImg.width - size) / 2;
    const startY = (currentImg.height - size) / 2;
    ctx.drawImage(currentImg, startX, startY, size, size, 0, 0, canvas.width, canvas.height);

    // 2. Temporary Fake Frame
    // 2. Draw the Official Format A Frame
    ctx.drawImage(frameImg, 0, 0, canvas.width, canvas.height);
    
    ctx.fillStyle = 'white';
    ctx.font = 'bold 28px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('HH GOA 2026', canvas.width / 2, canvas.height - 10);

  } else {
    // ------------------------------------
    // FORMAT B: BUILDER ID CARD (400x600 Vertical Badge)
    // ------------------------------------
    canvas.width = 400;
    canvas.height = 600;

    // 1. Dark Background
    // 1. Draw the Official Format B Background
// 1. Draw the Official Format B Background
    ctx.drawImage(badgeImg, 0, 0, canvas.width, canvas.height);

    // 3. User Photo (Cropped and centered)
    const size = Math.min(currentImg.width, currentImg.height);
    const startX = (currentImg.width - size) / 2;
    const startY = (currentImg.height - size) / 2;
    const imgSize = 200; // Smaller photo for the badge
    ctx.drawImage(currentImg, startX, startY, size, size, 100, 100, imgSize, imgSize);

    // 4. Photo Border
    ctx.lineWidth = 4;
    ctx.strokeStyle = '#FF5722';
    ctx.strokeRect(100, 100, imgSize, imgSize);

    // 5. Dynamic Text Rendering
    const nameText = nameInput.value || 'Your Name'; // Fallback if empty
    ctx.fillStyle = 'white';
    ctx.font = 'bold 32px sans-serif';
    ctx.fillText(nameText, canvas.width / 2, 360);

    const roleText = roleInput.value || 'Builder'; // Fallback if empty
    ctx.fillStyle = '#aaaaaa';
    ctx.font = '22px sans-serif';
    ctx.fillText(roleText, canvas.width / 2, 400);

    // 6. Bottom Badge ID
     
  }
}

// --- EXPORT & SHARE LOGIC ---
downloadBtn.addEventListener('click', () => {
  const dataUrl = canvas.toDataURL('image/png');
  const link = document.createElement('a');
  link.download = radioA.checked ? 'HH-Goa-PFP.png' : 'HH-Goa-Badge.png';
  link.href = dataUrl;
  link.click();
});

shareBtn.addEventListener('click', () => {
  const text = encodeURIComponent("Ready to build at Hacker House Goa 2026! 🌴💻 #FrameInGoa");
  const twitterUrl = `https://twitter.com/intent/tweet?text=${text}`;
  window.open(twitterUrl, '_blank');
  alert("Awesome! Just make sure to attach the graphic you downloaded to your tweet.");
});