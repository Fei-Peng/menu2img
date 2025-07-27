const { contextBridge, ipcRenderer } = require('electron');

// Expose protected methods that allow the renderer process to use
// the ipcRenderer without exposing the entire object
contextBridge.exposeInMainWorld('electronAPI', {
  selectFile: () => ipcRenderer.invoke('select-file'),
  showError: (title, message) => ipcRenderer.invoke('show-error', title, message),
  showInfo: (title, message) => ipcRenderer.invoke('show-info', title, message),
  
  // App info
  getAppVersion: () => process.versions.electron,
  getPlatform: () => process.platform,
  
  // Window controls
  minimize: () => ipcRenderer.send('minimize-window'),
  maximize: () => ipcRenderer.send('maximize-window'),
  close: () => ipcRenderer.send('close-window')
}); 