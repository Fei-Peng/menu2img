// Desktop app enhancements
document.addEventListener('DOMContentLoaded', () => {
  // Add desktop app title bar
  addTitleBar();
  
  // Enhance file selection with native dialog
  enhanceFileSelection();
  
  // Add app menu
  addAppMenu();
  
  // Add keyboard shortcuts
  addKeyboardShortcuts();
});

function addTitleBar() {
  if (window.electronAPI) {
    const titleBar = document.createElement('div');
    titleBar.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      height: 30px;
      background: linear-gradient(135deg, #667eea, #764ba2);
      -webkit-app-region: drag;
      z-index: 1000;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 10px;
      color: white;
      font-size: 12px;
    `;
    
    titleBar.innerHTML = `
      <div style="display: flex; align-items: center;">
        <span style="margin-right: 10px;">🍽️ Menu2Img</span>
        <span style="opacity: 0.8;">Desktop App</span>
      </div>
      <div style="-webkit-app-region: no-drag;">
        <button onclick="window.electronAPI.minimize()" style="background: none; border: none; color: white; padding: 5px; cursor: pointer;">─</button>
        <button onclick="window.electronAPI.maximize()" style="background: none; border: none; color: white; padding: 5px; cursor: pointer;">□</button>
        <button onclick="window.electronAPI.close()" style="background: none; border: none; color: white; padding: 5px; cursor: pointer;">×</button>
      </div>
    `;
    
    document.body.insertBefore(titleBar, document.body.firstChild);
    
    // Adjust main container to account for title bar
    const container = document.querySelector('.container');
    if (container) {
      container.style.marginTop = '30px';
    }
  }
}

function enhanceFileSelection() {
  if (window.electronAPI) {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');
    
    // Add native file dialog button
    const nativeButton = document.createElement('button');
    nativeButton.textContent = '📁 Choose File (Native)';
    nativeButton.style.cssText = `
      background: linear-gradient(135deg, #667eea, #764ba2);
      color: white;
      border: none;
      padding: 10px 20px;
      border-radius: 8px;
      cursor: pointer;
      margin-top: 10px;
      font-size: 14px;
      transition: all 0.3s ease;
    `;
    
    nativeButton.addEventListener('click', async () => {
      try {
        const filePath = await window.electronAPI.selectFile();
        if (filePath) {
          // Create a File object from the selected path
          const response = await fetch(`file://${filePath}`);
          const blob = await response.blob();
          const file = new File([blob], filePath.split('/').pop(), { type: blob.type });
          
          // Trigger file processing
          handleFile(file);
        }
      } catch (error) {
        console.error('Error selecting file:', error);
        if (window.electronAPI.showError) {
          window.electronAPI.showError('File Selection Error', 'Failed to select file: ' + error.message);
        }
      }
    });
    
    uploadArea.appendChild(nativeButton);
  }
}

function addAppMenu() {
  if (window.electronAPI) {
    const menuBar = document.createElement('div');
    menuBar.style.cssText = `
      position: fixed;
      top: 30px;
      left: 0;
      right: 0;
      height: 40px;
      background: #f8f9fa;
      border-bottom: 1px solid #dee2e6;
      z-index: 999;
      display: flex;
      align-items: center;
      padding: 0 20px;
      font-size: 14px;
    `;
    
    menuBar.innerHTML = `
      <div style="display: flex; gap: 20px;">
        <span style="cursor: pointer; padding: 5px 10px; border-radius: 4px;" onmouseover="this.style.background='#e9ecef'" onmouseout="this.style.background='transparent'" onclick="showAbout()">About</span>
        <span style="cursor: pointer; padding: 5px 10px; border-radius: 4px;" onmouseover="this.style.background='#e9ecef'" onmouseout="this.style.background='transparent'" onclick="showHelp()">Help</span>
        <span style="cursor: pointer; padding: 5px 10px; border-radius: 4px;" onmouseover="this.style.background='#e9ecef'" onmouseout="this.style.background='transparent'" onclick="openOutputFolder()">Open Output Folder</span>
      </div>
    `;
    
    document.body.insertBefore(menuBar, document.body.children[1]);
    
    // Adjust main container further
    const container = document.querySelector('.container');
    if (container) {
      container.style.marginTop = '70px';
    }
  }
}

function addKeyboardShortcuts() {
  document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + O to open file
    if ((e.ctrlKey || e.metaKey) && e.key === 'o') {
      e.preventDefault();
      document.getElementById('fileInput').click();
    }
    
    // Ctrl/Cmd + Q to quit (handled by Electron)
    if ((e.ctrlKey || e.metaKey) && e.key === 'q') {
      e.preventDefault();
      if (window.electronAPI && window.electronAPI.close) {
        window.electronAPI.close();
      }
    }
  });
}

// Menu functions
function showAbout() {
  if (window.electronAPI && window.electronAPI.showInfo) {
    window.electronAPI.showInfo('About Menu2Img', 
      'Menu2Img Desktop App v1.0.0\n\n' +
      'Generate beautiful food images from menu photos using AI.\n\n' +
      'Features:\n' +
      '• Upload menu images\n' +
      '• Extract dish names with AI\n' +
      '• Generate food photos with DALL-E 3\n' +
      '• Smart caching and file tracking\n\n' +
      'Built with Electron, Flask, and OpenAI APIs.'
    );
  }
}

function showHelp() {
  if (window.electronAPI && window.electronAPI.showInfo) {
    window.electronAPI.showInfo('Help', 
      'How to use Menu2Img:\n\n' +
      '1. Upload a menu image by dragging and dropping or clicking to browse\n' +
      '2. The AI will extract dish names from the menu\n' +
      '3. Beautiful food images will be generated for each dish\n' +
      '4. Results are cached for future uploads\n\n' +
      'Keyboard Shortcuts:\n' +
      '• Ctrl/Cmd + O: Open file dialog\n' +
      '• Ctrl/Cmd + Q: Quit application\n\n' +
      'Make sure to set your OPENAI_API_KEY environment variable!'
    );
  }
}

function openOutputFolder() {
  // This would need to be implemented in the main process
  console.log('Opening output folder...');
} 