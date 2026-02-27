// Main entry point for the application
import './styles/main.css';
import { invoke } from '@tauri-apps/api/core';

// Types
interface Wallpaper {
  id: string;
  title: string;
  preview: string;
  wp_type: string;
  size: number;
}

// State
let wallpapers: Wallpaper[] = [];
let selectedWallpaper: Wallpaper | null = null;
let currentPage = 'wallpapers';

// Initialize the application
document.addEventListener('DOMContentLoaded', async () => {
  console.log('Initializing Linux Wallpaper Engine GUI...');
  
  // Setup navigation
  setupNavigation();
  
  // Load wallpapers
  await loadWallpapers();
  
  // Start performance monitoring
  startPerformanceMonitoring();
});

// Navigation
function setupNavigation() {
  const navBtns = document.querySelectorAll('.nav-btn');
  
  navBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const page = btn.getAttribute('data-page');
      if (page) {
        switchPage(page);
      }
    });
  });
}

function switchPage(page: string) {
  currentPage = page;
  
  // Update nav buttons
  document.querySelectorAll('.nav-btn').forEach(btn => {
    btn.classList.toggle('active', btn.getAttribute('data-page') === page);
  });
  
  // Update pages
  document.querySelectorAll('.page').forEach(p => {
    p.classList.remove('active');
  });
  
  const pageEl = document.getElementById(`${page}-page`);
  if (pageEl) {
    pageEl.classList.add('active');
  }
}

// Wallpaper loading
async function loadWallpapers() {
  try {
    const result = await invoke<Wallpaper[]>('scan_wallpapers');
    wallpapers = result;
    renderWallpapers();
  } catch (error) {
    console.error('Failed to load wallpapers:', error);
    const grid = document.getElementById('wallpaper-grid');
    if (grid) {
      grid.innerHTML = `<div class="error">加载壁纸失败: ${error}</div>`;
    }
  }
}

function renderWallpapers() {
  const grid = document.getElementById('wallpaper-grid');
  if (!grid) return;
  
  if (wallpapers.length === 0) {
    grid.innerHTML = '<div class="empty">没有找到壁纸</div>';
    return;
  }
  
  grid.innerHTML = wallpapers.map(wp => `
    <div class="wallpaper-card" data-id="${wp.id}">
      <div class="wallpaper-thumbnail">
        <img src="${wp.preview}" alt="${wp.title}" loading="lazy">
      </div>
      <div class="wallpaper-info">
        <div class="wallpaper-title">${wp.title}</div>
        <div class="wallpaper-type">${wp.wp_type}</div>
      </div>
    </div>
  `).join('');
  
  // Add click handlers
  grid.querySelectorAll('.wallpaper-card').forEach(card => {
    card.addEventListener('click', () => {
      const id = card.getAttribute('data-id');
      if (id) {
        selectWallpaper(id);
      }
    });
    
    card.addEventListener('dblclick', () => {
      const id = card.getAttribute('data-id');
      if (id) {
        applyWallpaper(id);
      }
    });
  });
}

async function selectWallpaper(id: string) {
  const wp = wallpapers.find(w => w.id === id);
  if (!wp) return;
  
  selectedWallpaper = wp;
  
  // Update selection UI
  document.querySelectorAll('.wallpaper-card').forEach(card => {
    card.classList.toggle('selected', card.getAttribute('data-id') === id);
  });
  
  // Update sidebar
  updateSidebar(wp);
}

function updateSidebar(wp: Wallpaper) {
  const sidebar = document.querySelector('.sidebar-content');
  if (!sidebar) return;
  
  sidebar.innerHTML = `
    <div class="wallpaper-details">
      <h3>${wp.title}</h3>
      <div class="detail-row">
        <span class="label">类型:</span>
        <span class="value">${wp.wp_type}</span>
      </div>
      <div class="detail-row">
        <span class="label">大小:</span>
        <span class="value">${(wp.size / 1024 / 1024).toFixed(1)} MB</span>
      </div>
      <div class="sidebar-actions">
        <button class="btn-primary" id="apply-btn">应用壁纸</button>
        <button class="btn-secondary" id="open-folder-btn">打开文件夹</button>
        <button class="btn-danger" id="delete-btn">删除</button>
      </div>
    </div>
  `;
  
  // Add button handlers
  document.getElementById('apply-btn')?.addEventListener('click', () => applyWallpaper(wp.id));
  document.getElementById('open-folder-btn')?.addEventListener('click', () => openFolder(wp.id));
  document.getElementById('delete-btn')?.addEventListener('click', () => deleteWallpaper(wp.id));
}

async function applyWallpaper(id: string) {
  try {
    await invoke('apply_wallpaper', { id });
    console.log('Wallpaper applied:', id);
  } catch (error) {
    console.error('Failed to apply wallpaper:', error);
    alert(`应用壁纸失败: ${error}`);
  }
}

async function openFolder(id: string) {
  try {
    await invoke('open_wallpaper_folder', { id });
  } catch (error) {
    console.error('Failed to open folder:', error);
  }
}

async function deleteWallpaper(id: string) {
  if (!confirm('确定要删除这个壁纸吗？')) return;
  
  try {
    await invoke('delete_wallpaper', { id });
    await loadWallpapers();
  } catch (error) {
    console.error('Failed to delete wallpaper:', error);
    alert(`删除失败: ${error}`);
  }
}

// Performance monitoring
function startPerformanceMonitoring() {
  setInterval(async () => {
    if (currentPage !== 'performance') return;
    
    try {
      const stats = await invoke<{ cpu: number; memory: number }>('get_performance_stats');
      
      const cpuEl = document.getElementById('cpu-usage');
      const memEl = document.getElementById('memory-usage');
      
      if (cpuEl) cpuEl.textContent = `${stats.cpu.toFixed(1)}%`;
      if (memEl) memEl.textContent = `${stats.memory.toFixed(0)} MB`;
    } catch (error) {
      console.error('Failed to get performance stats:', error);
    }
  }, 1000);
}