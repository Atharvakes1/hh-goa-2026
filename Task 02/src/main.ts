// Grab the elements from our HTML
const uploadInput = document.getElementById('upload') as HTMLInputElement;
const canvas = document.getElementById('canvas') as HTMLCanvasElement;
const ctx = canvas.getContext('2d');
const downloadBtn = document.getElementById('downloadBtn') as HTMLButtonElement;
const shareBtn = document.getElementById('shareBtn') as HTMLButtonElement;

// UI Elements for Format B
const radioA = document.getElementById('radioA') as HTMLInputElement;
const radioB = document.getElementById('radioB') as HTMLInputElement;
const textInputs = document.getElementById('textInputs') as HTMLDivElement;
const nameInput = document.getElementById('nameInput') as HTMLInputElement;
const roleInput = document.getElementById('roleInput') as HTMLInputElement;

let currentImg: HTMLImageElement | null = null;

// --- EVENT LISTENERS ---
function handleFormatChange() {
  if (radioB.checked) {
    textInputs.style.display = 'flex';
  } else {
    textInputs.style.display = 'none';
  }
  renderCanvas();
}

radioA.addEventListener('change', handleFormatChange);
radioB.addEventListener('change', handleFormatChange);
nameInput.addEventListener('input', renderCanvas);
roleInput.addEventListener('input', renderCanvas);

// Handle file upload and force unlock buttons
uploadInput?.addEventListener('change', (event) => {
  const target = event.target as HTMLInputElement;
  const file = target.files?.[0];
  if (!file || !ctx) return;

  const reader = new FileReader();
  reader.onload = (e) => {
    const img = new Image();
    img.onload = () => {
      currentImg = img;
      renderCanvas(); 
      
      // Force enable both buttons
      downloadBtn.disabled = false;
      shareBtn.disabled = false;
      downloadBtn.removeAttribute('disabled');
      shareBtn.removeAttribute('disabled');
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
    // FORMAT A: PFP FRAME
    // ------------------------------------
    canvas.width = 400;
    canvas.height = 400;

    const size = Math.min(currentImg.width, currentImg.height);
    const startX = (currentImg.width - size) / 2;
    const startY = (currentImg.height - size) / 2;
    ctx.drawImage(currentImg, startX, startY, size, size, 0, 0, canvas.width, canvas.height);

    ctx.lineWidth = 40;
    ctx.strokeStyle = '#FF5722'; 
    ctx.strokeRect(0, 0, canvas.width, canvas.height);
    
    ctx.fillStyle = 'white';
    ctx.font = 'bold 28px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('HH GOA 2026', canvas.width / 2, canvas.height - 10);

  } else {
    // ------------------------------------
    // FORMAT B: BUILDER ID CARD
    // ------------------------------------
    canvas.width = 400;
    canvas.height = 600;

    // Background
    ctx.fillStyle = '#111111';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Top Banner
    ctx.fillStyle = '#FF5722';
    ctx.fillRect(0, 0, canvas.width, 60);
    ctx.fillStyle = 'white';
    ctx.font = 'bold 22px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('HACKER HOUSE GOA 2026', canvas.width / 2, 38);

    // Photo
    const size = Math.min(currentImg.width, currentImg.height);
    const startX = (currentImg.width - size) / 2;
    const startY = (currentImg.height - size) / 2;
    const imgSize = 200; 
    ctx.drawImage(currentImg, startX, startY, size, size, 100, 100, imgSize, imgSize);

    // Photo Border
    ctx.lineWidth = 4;
    ctx.strokeStyle = '#FF5722';
    ctx.strokeRect(100, 100, imgSize, imgSize);

    // Text Fields
    const nameText = nameInput.value || 'Your Name';
    ctx.fillStyle = 'white';
    ctx.font = 'bold 32px sans-serif';
    ctx.fillText(nameText, canvas.width / 2, 360);

    const roleText = roleInput.value || 'Builder'; 
    ctx.fillStyle = '#aaaaaa';
    ctx.font = '22px sans-serif';
    ctx.fillText(roleText, canvas.width / 2, 400);

    // Bottom ID
    ctx.fillStyle = '#222222';
    ctx.fillRect(0, 500, canvas.width, 100);
    ctx.fillStyle = 'white';
    ctx.font = 'bold 20px monospace';
    ctx.fillText('BUILDER_ID_2026', canvas.width / 2, 555);
  }
}

// --- EXPORT & SHARE LOGIC ---
downloadBtn.addEventListener('click', () => {
  if (!currentImg) return;
  const dataUrl = canvas.toDataURL('image/png');
  const link = document.createElement('a');
  link.download = radioA.checked ? 'HH-Goa-PFP.png' : 'HH-Goa-Badge.png';
  link.href = dataUrl;
  document.body.appendChild(link); // Required for Safari/Firefox support
  link.click();
  document.body.removeChild(link);
});

shareBtn.addEventListener('click', () => {
  if (!currentImg) return;
  const text = encodeURIComponent("Ready to build at Hacker House Goa 2026! 🌴💻 #FrameInGoa");
  const twitterUrl = `https://twitter.com/intent/tweet?text=${text}`;
  window.open(twitterUrl, '_blank');
  alert("Awesome! Just make sure to attach the graphic you downloaded to your tweet.");
});