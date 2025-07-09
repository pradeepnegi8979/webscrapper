 // Optional: change blob colors every few seconds
    const blobs = document.querySelectorAll('.blob');
    setInterval(() => {
      blobs.forEach(b => {
        b.style.background = `hsl(${Math.random()*360}, 70%, 60%)`;
      });
    }, 8000);


    
function copyToClipboard(text) {
  navigator.clipboard.writeText(text).then(() => {
    alert("Link copied to clipboard!");
  }).catch(err => {
    console.error('Could not copy text: ', err);
  });
}

