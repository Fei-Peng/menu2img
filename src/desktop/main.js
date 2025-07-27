const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const isDev = require('electron-is-dev');

let mainWindow;
let pythonProcess;

function createWindow() {
  // Create the browser window
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    minWidth: 1000,
    minHeight: 700,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    },
    icon: path.join(__dirname, '../assets/icons/icon.png'),
    titleBarStyle: 'default',
    show: false
  });

  // Load the app
  const startUrl = isDev ? 'http://localhost:5051' : 'http://localhost:5051';
  mainWindow.loadURL(startUrl);

  // Show window when ready
  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
  });

  // Handle window closed
  mainWindow.on('closed', () => {
    mainWindow = null;
  });

  // Open DevTools in development
  if (isDev) {
    mainWindow.webContents.openDevTools();
  }
}

function startPythonBackend() {
  return new Promise((resolve, reject) => {
    const pythonPath = 'python3';
    const scriptPath = path.join(__dirname, '../web/app.py');
    
    pythonProcess = spawn(pythonPath, [scriptPath], {
      stdio: ['pipe', 'pipe', 'pipe']
    });

    pythonProcess.stdout.on('data', (data) => {
      console.log('Python stdout:', data.toString());
      if (data.toString().includes('Running on http://0.0.0.0:5051')) {
        resolve();
      }
    });

    pythonProcess.stderr.on('data', (data) => {
      console.error('Python stderr:', data.toString());
    });

    pythonProcess.on('error', (error) => {
      console.error('Failed to start Python process:', error);
      reject(error);
    });

    pythonProcess.on('close', (code) => {
      console.log('Python process exited with code:', code);
    });

    // Timeout after 10 seconds
    setTimeout(() => {
      reject(new Error('Python backend startup timeout'));
    }, 10000);
  });
}

// App event handlers
app.whenReady().then(async () => {
  try {
    await startPythonBackend();
    createWindow();
  } catch (error) {
    console.error('Failed to start backend:', error);
    dialog.showErrorBox('Startup Error', 'Failed to start the Python backend. Please make sure Python and the required packages are installed.');
    app.quit();
  }
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

app.on('before-quit', () => {
  if (pythonProcess) {
    pythonProcess.kill();
  }
});

// IPC handlers
ipcMain.handle('select-file', async () => {
  const result = await dialog.showOpenDialog(mainWindow, {
    properties: ['openFile'],
    filters: [
      { name: 'Images', extensions: ['jpg', 'jpeg', 'png', 'gif', 'bmp'] }
    ]
  });
  
  if (!result.canceled && result.filePaths.length > 0) {
    return result.filePaths[0];
  }
  return null;
});

ipcMain.handle('show-error', async (event, title, message) => {
  await dialog.showErrorBox(title, message);
});

ipcMain.handle('show-info', async (event, title, message) => {
  await dialog.showMessageBox(mainWindow, {
    type: 'info',
    title: title,
    message: message
  });
}); 