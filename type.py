import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import subprocess
import threading
import re
import json
import logging
from pathlib import Path
from datetime import datetime
import queue
import time

# Internationalization support
LANGUAGES = {
    'en': {
        'title': 'Moaz Universal Video Downloader',
        'url_label': 'Video URL (YouTube, Facebook, Instagram, TikTok, etc.):',
        'batch_urls_label': 'Batch URLs (one per line):',
        'output_dir_label': 'Download Directory:',
        'browse': 'Browse',
        'download_options': 'Download Options',
        'video_quality': 'Video Quality:',
        'format': 'Format:',
        'audio_only': 'Audio only (MP3)',
        'playlist': 'Download entire playlist/channel',
        'cookie_file_label': 'Cookie File (Optional - for private content):',
        'custom_format_label': 'Custom Format (Advanced):',
        'download_video': 'Download Video',
        'batch_download': 'Batch Download',
        'cancel_download': 'Cancel Download',
        'status': 'Status:',
        'progress': 'Progress:',
        'download_log': 'Download Log:',
        'settings': 'Settings',
        'theme': 'Theme:',
        'language': 'Language:',
        'save_settings': 'Save Settings',
        'load_settings': 'Load Settings',
        'ready': 'Ready to download...',
        'downloading': 'Downloading...',
        'cancelled': 'Download cancelled',
        'completed': 'Download completed successfully!',
        'failed': 'Download failed!',
        'error': 'Error',
        'success': 'Success',
        'enter_url': 'Please enter a video URL',
        'invalid_url': 'Please enter a valid URL (must start with http:// or https://)',
        'dir_not_exist': "Download directory doesn't exist",
        'download_success': 'Video downloaded successfully!',
        'download_failed': 'Download failed. Check the log for details.',
        'batch_mode': 'Batch Mode',
        'single_mode': 'Single URL Mode',
        'light': 'Light',
        'dark': 'Dark'
    },
    'es': {
        'title': 'Descargador Universal de Videos Mejorado',
        'url_label': 'URL del video (YouTube, Facebook, Instagram, TikTok, etc.):',
        'batch_urls_label': 'URLs por lotes (una por línea):',
        'output_dir_label': 'Directorio de descarga:',
        'browse': 'Explorar',
        'download_options': 'Opciones de descarga',
        'video_quality': 'Calidad de video:',
        'format': 'Formato:',
        'audio_only': 'Solo audio (MP3)',
        'playlist': 'Descargar lista/canal completo',
        'cookie_file_label': 'Archivo de cookies (Opcional - para contenido privado):',
        'custom_format_label': 'Formato personalizado (Avanzado):',
        'download_video': 'Descargar Video',
        'batch_download': 'Descarga por lotes',
        'cancel_download': 'Cancelar descarga',
        'status': 'Estado:',
        'progress': 'Progreso:',
        'download_log': 'Registro de descarga:',
        'settings': 'Configuración',
        'theme': 'Tema:',
        'language': 'Idioma:',
        'save_settings': 'Guardar configuración',
        'load_settings': 'Cargar configuración',
        'ready': 'Listo para descargar...',
        'downloading': 'Descargando...',
        'cancelled': 'Descarga cancelada',
        'completed': '¡Descarga completada exitosamente!',
        'failed': '¡Descarga falló!',
        'error': 'Error',
        'success': 'Éxito',
        'enter_url': 'Por favor ingrese una URL de video',
        'invalid_url': 'Por favor ingrese una URL válida (debe comenzar con http:// o https://)',
        'dir_not_exist': 'El directorio de descarga no existe',
        'download_success': '¡Video descargado exitosamente!',
        'download_failed': 'Descarga falló. Revise el registro para detalles.',
        'batch_mode': 'Modo por lotes',
        'single_mode': 'Modo URL única',
        'light': 'Claro',
        'dark': 'Oscuro'
    },
    'fr': {
        'title': 'Téléchargeur Vidéo Universal Amélioré',
        'url_label': 'URL vidéo (YouTube, Facebook, Instagram, TikTok, etc.):',
        'batch_urls_label': 'URLs par lot (une par ligne):',
        'output_dir_label': 'Répertoire de téléchargement:',
        'browse': 'Parcourir',
        'download_options': 'Options de téléchargement',
        'video_quality': 'Qualité vidéo:',
        'format': 'Format:',
        'audio_only': 'Audio seulement (MP3)',
        'playlist': 'Télécharger toute la playlist/chaîne',
        'cookie_file_label': 'Fichier de cookies (Optionnel - pour contenu privé):',
        'custom_format_label': 'Format personnalisé (Avancé):',
        'download_video': 'Télécharger Vidéo',
        'batch_download': 'Téléchargement par lot',
        'cancel_download': 'Annuler téléchargement',
        'status': 'Statut:',
        'progress': 'Progrès:',
        'download_log': 'Journal de téléchargement:',
        'settings': 'Paramètres',
        'theme': 'Thème:',
        'language': 'Langue:',
        'save_settings': 'Sauvegarder paramètres',
        'load_settings': 'Charger paramètres',
        'ready': 'Prêt à télécharger...',
        'downloading': 'Téléchargement...',
        'cancelled': 'Téléchargement annulé',
        'completed': 'Téléchargement terminé avec succès!',
        'failed': 'Téléchargement échoué!',
        'error': 'Erreur',
        'success': 'Succès',
        'enter_url': 'Veuillez saisir une URL de vidéo',
        'invalid_url': 'Veuillez saisir une URL valide (doit commencer par http:// ou https://)',
        'dir_not_exist': "Le répertoire de téléchargement n'existe pas",
        'download_success': 'Vidéo téléchargée avec succès!',
        'download_failed': 'Téléchargement échoué. Vérifiez le journal pour les détails.',
        'batch_mode': 'Mode par lot',
        'single_mode': 'Mode URL unique',
        'light': 'Clair',
        'dark': 'Sombre'
    }
}

class EnhancedVideoDownloader:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Enhanced Universal Video Downloader")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Initialize settings
        self.settings_file = Path.home() / ".video_downloader_settings.json"
        self.log_file = Path.home() / "video_downloader.log"
        
        # Setup logging FIRST
        self.setup_logging()
        
        # Then load settings
        self.current_language = 'en'
        self.current_theme = 'light'
        self.load_settings()
        
        # Variables
        self.url_var = tk.StringVar()
        self.batch_urls_var = tk.StringVar()
        self.output_dir_var = tk.StringVar(value=str(Path.home() / "Downloads"))
        self.quality_var = tk.StringVar(value="best")
        self.format_var = tk.StringVar(value="mp4")
        self.custom_format_var = tk.StringVar()
        self.progress_var = tk.StringVar(value=self.t('ready'))
        self.cookie_file_var = tk.StringVar()
        self.audio_only_var = tk.BooleanVar()
        self.playlist_var = tk.BooleanVar()
        self.batch_mode_var = tk.BooleanVar()
        self.language_var = tk.StringVar(value=self.current_language)
        self.theme_var = tk.StringVar(value=self.current_theme)
        
        # Progress tracking
        self.progress_queue = queue.Queue()
        self.download_process = None
        self.is_downloading = False
        
        # Available formats (will be populated by format detection)
        self.available_formats = []
        
        self.ytdlp_command = None
        self.ffmpeg_available = False
        
        # Add CREATE_NO_WINDOW constant for Windows
        self.CREATE_NO_WINDOW = subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
        
        self.setup_ui()
        self.apply_theme()
        self.check_dependencies()
        self.start_progress_monitor()
    
    def t(self, key):
        """Translate text based on current language"""
        return LANGUAGES.get(self.current_language, LANGUAGES['en']).get(key, key)
    
    def setup_logging(self):
        """Setup logging to file"""
        try:
            # Ensure the log file directory is writable
            log_dir = self.log_file.parent
            if not log_dir.exists():
                log_dir.mkdir(parents=True, exist_ok=True)
            
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s',
                handlers=[
                    logging.FileHandler(self.log_file),
                    logging.StreamHandler()
                ]
            )
            self.logger = logging.getLogger(__name__)
            self.logger.info("Logging initialized successfully")
        except Exception as e:
            # Fallback to console-only logging if file handler fails
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s',
                handlers=[logging.StreamHandler()]
            )
            self.logger = logging.getLogger(__name__)
            self.logger.error(f"Failed to initialize file logging at {self.log_file}: {e}. Using console logging only.")
    
    def load_settings(self):
        """Load settings from file"""
        try:
            if self.settings_file.exists():
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                    self.current_language = settings.get('language', 'en')
                    self.current_theme = settings.get('theme', 'light')
                    if hasattr(self, 'output_dir_var'):
                        self.output_dir_var.set(settings.get('output_dir', str(Path.home() / "Downloads")))
                self.logger.info("Settings loaded successfully")
        except Exception as e:
            self.logger.error(f"Failed to load settings: {e}")
    
    def save_settings(self):
        """Save current settings to file"""
        try:
            settings = {
                'language': self.current_language,
                'theme': self.current_theme,
                'output_dir': self.output_dir_var.get(),
                'quality': self.quality_var.get(),
                'format': self.format_var.get(),
                'audio_only': self.audio_only_var.get(),
                'playlist': self.playlist_var.get()
            }
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f, indent=2)
            self.log_message("✓ Settings saved successfully")
            self.logger.info("Settings saved successfully")
        except Exception as e:
            self.log_message(f"✗ Failed to save settings: {e}")
            self.logger.error(f"Failed to save settings: {e}")
    
    def setup_ui(self):
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Main download tab
        self.main_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.main_frame, text="Download")
        
        # Settings tab
        self.settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_frame, text=self.t('settings'))
        
        self.setup_main_tab()
        self.setup_settings_tab()
    
    def setup_main_tab(self):
        main_frame = self.main_frame
        main_frame.columnconfigure(1, weight=1)
        
        row = 0
        
        # Mode selection
        mode_frame = ttk.LabelFrame(main_frame, text="Mode", padding="5")
        mode_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Radiobutton(mode_frame, text=self.t('single_mode'), 
                       variable=self.batch_mode_var, value=False,
                       command=self.toggle_mode).grid(row=0, column=0, sticky=tk.W, padx=(0, 20))
        ttk.Radiobutton(mode_frame, text=self.t('batch_mode'), 
                       variable=self.batch_mode_var, value=True,
                       command=self.toggle_mode).grid(row=0, column=1, sticky=tk.W)
        
        row += 1
        
        # Single URL input
        self.single_url_frame = ttk.Frame(main_frame)
        self.single_url_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        self.single_url_frame.columnconfigure(0, weight=1)
        
        ttk.Label(self.single_url_frame, text=self.t('url_label')).grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.url_entry = ttk.Entry(self.single_url_frame, textvariable=self.url_var)
        self.url_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Format detection button
        ttk.Button(self.single_url_frame, text="Detect Formats", 
                  command=self.detect_formats).grid(row=1, column=1, padx=(5, 0))
        
        row += 1
        
        # Batch URLs input
        self.batch_url_frame = ttk.Frame(main_frame)
        self.batch_url_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        self.batch_url_frame.columnconfigure(0, weight=1)
        self.batch_url_frame.rowconfigure(1, weight=1)
        
        ttk.Label(self.batch_url_frame, text=self.t('batch_urls_label')).grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.batch_text = scrolledtext.ScrolledText(self.batch_url_frame, height=6, wrap=tk.WORD)
        self.batch_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        row += 1
        
        # Output directory
        ttk.Label(main_frame, text=self.t('output_dir_label')).grid(row=row, column=0, sticky=tk.W, pady=(0, 5))
        row += 1
        
        dir_frame = ttk.Frame(main_frame)
        dir_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        dir_frame.columnconfigure(0, weight=1)
        
        ttk.Entry(dir_frame, textvariable=self.output_dir_var).grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        ttk.Button(dir_frame, text=self.t('browse'), command=self.browse_directory).grid(row=0, column=1)
        
        row += 1
        
        # Options frame
        options_frame = ttk.LabelFrame(main_frame, text=self.t('download_options'), padding="5")
        options_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        options_frame.columnconfigure(1, weight=1)
        
        # Quality selection
        ttk.Label(options_frame, text=self.t('video_quality')).grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.quality_combo = ttk.Combobox(options_frame, textvariable=self.quality_var, 
                                         values=["best", "worst", "1080p", "720p", "480p", "360p", "240p"], 
                                         state="readonly", width=15)
        self.quality_combo.grid(row=0, column=1, sticky=tk.W, padx=(0, 20))
        
        # Format selection
        ttk.Label(options_frame, text=self.t('format')).grid(row=0, column=2, sticky=tk.W, padx=(0, 10))
        self.format_combo = ttk.Combobox(options_frame, textvariable=self.format_var,
                                        values=["mp4", "webm", "mkv", "avi", "mov", "flv"],
                                        state="readonly", width=10)
        self.format_combo.grid(row=0, column=3, sticky=tk.W)
        
        # Custom format
        ttk.Label(options_frame, text=self.t('custom_format_label')).grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(5, 0))
        self.custom_format_entry = ttk.Entry(options_frame, textvariable=self.custom_format_var, width=30)
        self.custom_format_entry.grid(row=1, column=1, columnspan=3, sticky=tk.W, pady=(5, 0))
        
        # Checkboxes
        ttk.Checkbutton(options_frame, text=self.t('audio_only'), 
                       variable=self.audio_only_var).grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=(5, 0))
        
        ttk.Checkbutton(options_frame, text=self.t('playlist'), 
                       variable=self.playlist_var).grid(row=2, column=2, columnspan=2, sticky=tk.W, pady=(5, 0))
        
        row += 1
        
        # Cookie file option
        ttk.Label(main_frame, text=self.t('cookie_file_label')).grid(row=row, column=0, sticky=tk.W, pady=(0, 5))
        row += 1
        
        cookie_frame = ttk.Frame(main_frame)
        cookie_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        cookie_frame.columnconfigure(0, weight=1)
        
        self.cookie_entry = ttk.Entry(cookie_frame, textvariable=self.cookie_file_var)
        self.cookie_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        ttk.Button(cookie_frame, text=self.t('browse'), command=self.browse_cookie_file).grid(row=0, column=1)
        ttk.Button(cookie_frame, text="Validate", command=self.validate_cookie_file).grid(row=0, column=2, padx=(5, 0))
        
        row += 1
        
        # Download buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=row, column=0, columnspan=2, pady=10)
        
        self.download_btn = ttk.Button(button_frame, text=self.t('download_video'), 
                                     command=self.start_download)
        self.download_btn.grid(row=0, column=0, padx=(0, 10))
        
        self.batch_download_btn = ttk.Button(button_frame, text=self.t('batch_download'), 
                                           command=self.start_batch_download)
        self.batch_download_btn.grid(row=0, column=1, padx=(0, 10))
        
        self.cancel_btn = ttk.Button(button_frame, text=self.t('cancel_download'), 
                                   command=self.cancel_download, state="disabled")
        self.cancel_btn.grid(row=0, column=2)
        
        row += 1
        
        # Status and Progress
        ttk.Label(main_frame, text=self.t('status')).grid(row=row, column=0, sticky=tk.W, pady=(10, 5))
        row += 1
        
        self.progress_label = ttk.Label(main_frame, textvariable=self.progress_var, foreground="blue")
        self.progress_label.grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))
        
        row += 1
        
        ttk.Label(main_frame, text=self.t('progress')).grid(row=row, column=0, sticky=tk.W, pady=(5, 5))
        row += 1
        
        self.progress_bar = ttk.Progressbar(main_frame, mode='determinate')
        self.progress_bar.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        row += 1
        
        # Output text area
        ttk.Label(main_frame, text=self.t('download_log')).grid(row=row, column=0, sticky=tk.W, pady=(10, 5))
        row += 1
        
        text_frame = ttk.Frame(main_frame)
        text_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(row, weight=1)
        
        self.output_text = tk.Text(text_frame, height=8, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.output_text.yview)
        self.output_text.configure(yscrollcommand=scrollbar.set)
        
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Initially hide batch mode
        self.toggle_mode()
    
    def setup_settings_tab(self):
        settings_frame = self.settings_frame
        settings_frame.columnconfigure(1, weight=1)
        
        row = 0
        
        # Theme selection
        ttk.Label(settings_frame, text=self.t('theme')).grid(row=row, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 5))
        theme_combo = ttk.Combobox(settings_frame, textvariable=self.theme_var,
                                  values=[self.t('light'), self.t('dark')], state="readonly")
        theme_combo.grid(row=row, column=1, sticky=tk.W, pady=(10, 5))
        theme_combo.bind('<<ComboboxSelected>>', self.change_theme)
        
        row += 1
        
        # Language selection
        ttk.Label(settings_frame, text=self.t('language')).grid(row=row, column=0, sticky=tk.W, padx=(0, 10), pady=5)
        lang_combo = ttk.Combobox(settings_frame, textvariable=self.language_var,
                                 values=['English', 'Español', 'Français'], state="readonly")
        lang_combo.grid(row=row, column=1, sticky=tk.W, pady=5)
        lang_combo.bind('<<ComboboxSelected>>', self.change_language)
        
        row += 1
        
        # Settings buttons
        settings_btn_frame = ttk.Frame(settings_frame)
        settings_btn_frame.grid(row=row, column=0, columnspan=2, pady=20)
        
        ttk.Button(settings_btn_frame, text=self.t('save_settings'), 
                  command=self.save_settings).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(settings_btn_frame, text=self.t('load_settings'), 
                  command=self.load_settings).grid(row=0, column=1)
        
        row += 1
        
        # Dependencies status
        deps_frame = ttk.LabelFrame(settings_frame, text="Dependencies Status", padding="10")
        deps_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        self.ytdlp_status = ttk.Label(deps_frame, text="yt-dlp: Checking...")
        self.ytdlp_status.grid(row=0, column=0, sticky=tk.W, pady=2)
        
        self.ffmpeg_status = ttk.Label(deps_frame, text="ffmpeg: Checking...")
        self.ffmpeg_status.grid(row=1, column=0, sticky=tk.W, pady=2)
    
    def toggle_mode(self):
        """Toggle between single and batch mode"""
        if self.batch_mode_var.get():
            self.single_url_frame.grid_remove()
            self.batch_url_frame.grid()
            self.download_btn.config(state="disabled")
            self.batch_download_btn.config(state="normal")
        else:
            self.batch_url_frame.grid_remove()
            self.single_url_frame.grid()
            self.download_btn.config(state="normal")
            self.batch_download_btn.config(state="disabled")
    
    def change_theme(self, event=None):
        """Change application theme"""
        selected = self.theme_var.get()
        if selected == self.t('light'):
            self.current_theme = 'light'
        elif selected == self.t('dark'):
            self.current_theme = 'dark'
        self.apply_theme()
    
    def change_language(self, event=None):
        """Change application language"""
        selected = self.language_var.get()
        lang_map = {'English': 'en', 'Español': 'es', 'Français': 'fr'}
        if selected in lang_map:
            self.current_language = lang_map[selected]
            self.refresh_ui_text()
    
    def apply_theme(self):
        """Apply the selected theme"""
        if self.current_theme == 'dark':
            self.root.configure(bg='#2b2b2b')
            style = ttk.Style()
            style.theme_use('clam')
            
            # Configure dark theme colors
            style.configure('TFrame', background='#2b2b2b')
            style.configure('TLabel', background='#2b2b2b', foreground='white')
            style.configure('TButton', background='#404040', foreground='white')
            style.configure('TEntry', background='#404040', foreground='white')
            style.configure('TCombobox', background='#404040', foreground='white')
            style.configure('TCheckbutton', background='#2b2b2b', foreground='white')
            style.configure('TRadiobutton', background='#2b2b2b', foreground='white')
            style.configure('TLabelFrame', background='#2b2b2b', foreground='white')
            style.configure('TNotebook', background='#2b2b2b')
            style.configure('TNotebook.Tab', background='#404040', foreground='white')
            
            self.output_text.configure(bg='#404040', fg='white', insertbackground='white')
            self.batch_text.configure(bg='#404040', fg='white', insertbackground='white')
        else:
            self.root.configure(bg='SystemButtonFace')
            style = ttk.Style()
            style.theme_use('default')
            self.output_text.configure(bg='white', fg='black', insertbackground='black')
            self.batch_text.configure(bg='white', fg='black', insertbackground='black')
    
    def refresh_ui_text(self):
        """Refresh all UI text with current language"""
        self.root.title(self.t('title'))
        # Note: In a full implementation, you'd update all text elements
        # This is simplified for brevity
    
    def start_progress_monitor(self):
        """Start monitoring progress updates"""
        def monitor():
            self.logger.info("Progress monitor started")
            while True:
                try:
                    progress = self.progress_queue.get(timeout=0.1)
                    if progress is None:
                        self.logger.info("Progress monitor stopping")
                        break
                    
                    if isinstance(progress, dict):
                        if 'percentage' in progress:
                            self.progress_bar['value'] = progress['percentage']
                        if 'status' in progress:
                            self.progress_var.set(progress['status'])
                        if 'log' in progress:
                            self.log_message(progress['log'])
                    
                    self.root.update_idletasks()
                except queue.Empty:
                    continue
                except Exception as e:
                    self.logger.error(f"Progress monitor error: {e}")
                    break
        
        thread = threading.Thread(target=monitor, daemon=True)
        thread.start()
        self.logger.info("Progress monitor thread launched")
    
    def check_dependencies(self):
        """Check if yt-dlp and ffmpeg are installed"""
        commands_to_try = [
            ["yt-dlp", "--version"],
            [sys.executable, "-m", "yt_dlp", "--version"],
            ["python", "-m", "yt_dlp", "--version"],
            ["py", "-m", "yt_dlp", "--version"]
        ]
        
        ytdlp_found = False
        for cmd in commands_to_try:
            try:
                result = subprocess.run(cmd, capture_output=True, check=True, text=True, creationflags=self.CREATE_NO_WINDOW)
                self.log_message(f"✓ yt-dlp is installed and ready (Command: {' '.join(cmd)})")
                self.log_message(f"Version: {result.stdout.strip()}")
                self.ytdlp_command = cmd[:-1]  # Remove --version
                self.ytdlp_status.config(text="yt-dlp: ✓ Installed", foreground="green")
                ytdlp_found = True
                break
            except (subprocess.CalledProcessError, FileNotFoundError) as e:
                self.log_message(f"⚠ Failed to run {' '.join(cmd)}: {e}")
                continue
        
        if not ytdlp_found:
            self.ytdlp_status.config(text="yt-dlp: ✗ Not found", foreground="red")
            self.log_message("⚠ yt-dlp not found. Installing...")
            self.install_ytdlp()
        
        # Check ffmpeg
        try:
            result = subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True, text=True, creationflags=self.CREATE_NO_WINDOW)
            self.ffmpeg_available = True
            self.ffmpeg_status.config(text="ffmpeg: ✓ Installed", foreground="green")
            self.log_message("✓ ffmpeg is available")
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.ffmpeg_available = False
            self.ffmpeg_status.config(text="ffmpeg: ✗ Not found", foreground="red")
            self.log_message("⚠ ffmpeg not found. Some features may be limited.")
    
    def install_ytdlp(self):
        """Install yt-dlp using pip"""
        try:
            result = subprocess.run([sys.executable, "-m", "pip", "install", "yt-dlp"], 
                                  capture_output=True, text=True, creationflags=self.CREATE_NO_WINDOW)
            if result.returncode == 0:
                self.log_message("✓ yt-dlp installed successfully")
                self.ytdlp_command = [sys.executable, "-m", "yt_dlp"]
                self.ytdlp_status.config(text="yt-dlp: ✓ Installed", foreground="green")
                try:
                    subprocess.run(self.ytdlp_command + ["--version"], 
                                 capture_output=True, check=True, creationflags=self.CREATE_NO_WINDOW)
                    self.log_message("✓ yt-dlp verified and ready to use")
                except:
                    self.log_message("⚠ yt-dlp installed but verification failed")
            else:
                raise subprocess.CalledProcessError(result.returncode, "pip install")
        except Exception as e:
            error_msg = "Failed to install yt-dlp. Please install it manually using:\npython -m pip install yt-dlp"
            self.log_message(f"✗ {error_msg}")
            messagebox.showerror("Dependency Error", error_msg)
    
    def browse_directory(self):
        """Open directory browser"""
        directory = filedialog.askdirectory(initialdir=self.output_dir_var.get())
        if directory:
            self.output_dir_var.set(directory)

    def browse_cookie_file(self):
        """Open file browser for cookie file"""
        file_path = filedialog.askopenfilename(
            title="Select Cookie File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialdir=self.output_dir_var.get()
        )
        if file_path:
            self.cookie_file_var.set(file_path)
    
    def validate_cookie_file(self):
        """Validate the selected cookie file"""
        cookie_file = self.cookie_file_var.get().strip()
        if not cookie_file:
            messagebox.showwarning("Warning", "No cookie file selected")
            return
        
        if not os.path.exists(cookie_file):
            messagebox.showerror("Error", "Cookie file does not exist")
            return
        
        try:
            with open(cookie_file, 'r') as f:
                content = f.read().strip()
                if not content:
                    messagebox.showerror("Error", "Cookie file is empty")
                    return
                
                # Basic validation - check if it looks like a cookie file
                lines = content.split('\n')
                valid_lines = 0
                for line in lines:
                    if line.strip() and not line.startswith('#'):
                        parts = line.split('\t')
                        if len(parts) >= 6:  # Basic cookie format check
                            valid_lines += 1
                
                if valid_lines > 0:
                    messagebox.showinfo("Success", f"Cookie file validated successfully!\nFound {valid_lines} cookie entries.")
                    self.log_message(f"✓ Cookie file validated: {valid_lines} entries found")
                else:
                    messagebox.showwarning("Warning", "Cookie file format may not be correct")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to validate cookie file: {e}")
    
    def detect_formats(self):
        """Detect available formats for the given URL"""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a URL first")
            return
        
        if not self.validate_url(url):
            messagebox.showerror("Error", "Please enter a valid URL")
            return
        
        def detect():
            try:
                if not self.ytdlp_command:
                    raise Exception("yt-dlp is not properly installed")
                
                cmd = self.ytdlp_command + [url, "--list-formats", "--no-download"]
                
                process = subprocess.run(cmd, capture_output=True, text=True, timeout=30, creationflags=self.CREATE_NO_WINDOW)
                
                if process.returncode == 0:
                    formats = []
                    lines = process.stdout.split('\n')
                    for line in lines:
                        if line.strip() and not line.startswith('[') and '|' in line:
                            parts = line.split()
                            if len(parts) > 0 and parts[0] not in ['format', 'code']:
                                format_id = parts[0]
                                if format_id.isdigit() or '+' in format_id:
                                    formats.append(format_id)
                    
                    self.available_formats = formats[:20]  # Limit to first 20 formats
                    
                    # Update custom format combobox
                    if hasattr(self, 'custom_format_entry'):
                        self.custom_format_entry.config(values=self.available_formats)
                    
                    self.root.after(0, lambda: messagebox.showinfo("Success", 
                        f"Detected {len(self.available_formats)} available formats!\nCheck the custom format field."))
                    self.root.after(0, self.log_message, f"✓ Detected {len(self.available_formats)} formats for URL")
                else:
                    self.root.after(0, lambda: messagebox.showerror("Error", 
                        "Failed to detect formats. Check if the URL is valid."))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Format detection failed: {e}"))
        
        thread = threading.Thread(target=detect, daemon=True)
        thread.start()
        self.log_message("🔍 Detecting available formats...")
    
    def detect_platform(self, url):
        """Detect video platform from URL"""
        url_lower = url.lower()
        
        platforms = {
            'youtube.com': 'YouTube', 'youtu.be': 'YouTube',
            'facebook.com': 'Facebook', 'fb.watch': 'Facebook',
            'instagram.com': 'Instagram', 'tiktok.com': 'TikTok',
            'twitter.com': 'Twitter', 'x.com': 'Twitter/X',
            'vimeo.com': 'Vimeo', 'dailymotion.com': 'Dailymotion',
            'reddit.com': 'Reddit', 'twitch.tv': 'Twitch',
            'bilibili.com': 'Bilibili', 'streamable.com': 'Streamable'
        }
        
        for domain, platform in platforms.items():
            if domain in url_lower:
                return platform
        return "Unknown Platform"
    
    def validate_url(self, url):
        """Basic URL validation"""
        url_pattern = re.compile(
            r'^https?://'
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
            r'localhost|'
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
            r'(?::\d+)?'
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return url_pattern.match(url) is not None
    
    def log_message(self, message):
        """Add message to output text area and log file"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}"
        
        self.output_text.insert(tk.END, f"{formatted_message}\n")
        self.output_text.see(tk.END)
        self.root.update_idletasks()
        
        # Log to file
        self.logger.info(message)
    
    def parse_progress(self, line):
        """Parse progress information from yt-dlp output"""
        try:
            # Look for download progress pattern
            if '%' in line and 'ETA' in line:
                # Extract percentage
                percent_match = re.search(r'(\d+\.?\d*)%', line)
                if percent_match:
                    percentage = float(percent_match.group(1))
                    self.progress_queue.put({
                        'percentage': percentage,
                        'status': f"Downloading... {percentage:.1f}%",
                        'log': line
                    })
                    return
            
            # Look for other status indicators
            if any(keyword in line.lower() for keyword in ['downloading', 'extracting', 'merging']):
                self.progress_queue.put({
                    'status': line.split(']')[-1].strip() if ']' in line else line,
                    'log': line
                })
        except Exception as e:
            self.logger.error(f"Progress parsing error: {e}")
    
    def start_download(self):
        """Start single URL download"""
        url = self.url_var.get().strip()
        
        if not url:
            messagebox.showerror(self.t('error'), self.t('enter_url'))
            return
        
        if not self.validate_url(url):
            messagebox.showerror(self.t('error'), self.t('invalid_url'))
            return
        
        output_dir = self.output_dir_var.get().strip()
        if not output_dir or not os.path.exists(output_dir) or not os.access(output_dir, os.W_OK):
            messagebox.showerror(self.t('error'), "Invalid or inaccessible download directory")
            return
        
        self.start_download_process([url])
    
    def start_batch_download(self):
        """Start batch download from text area"""
        batch_text = self.batch_text.get(1.0, tk.END).strip()
        if not batch_text:
            messagebox.showerror(self.t('error'), "Please enter URLs for batch download")
            return
        
        urls = []
        for line in batch_text.split('\n'):
            url = line.strip()
            if url and self.validate_url(url):
                urls.append(url)
        
        if not urls:
            messagebox.showerror(self.t('error'), "No valid URLs found")
            return
        
        output_dir = self.output_dir_var.get().strip()
        if not output_dir or not os.path.exists(output_dir) or not os.access(output_dir, os.W_OK):
            messagebox.showerror(self.t('error'), "Invalid or inaccessible download directory")
            return
        
        self.log_message(f"📋 Starting batch download of {len(urls)} URLs")
        self.start_download_process(urls)
    
    def start_download_process(self, urls):
        """Start the download process for given URLs"""
        if self.is_downloading:
            messagebox.showwarning("Warning", "Download already in progress")
            return
        
        # Update UI state
        self.download_btn.config(state="disabled")
        self.batch_download_btn.config(state="disabled")
        self.cancel_btn.config(state="normal")
        self.progress_bar['value'] = 0
        self.progress_var.set(self.t('downloading'))
        self.is_downloading = True
        
        # Start download in separate thread
        thread = threading.Thread(target=self.download_videos, args=(urls,))
        thread.daemon = True
        thread.start()
    
    def download_videos(self, urls):
        """Download videos using yt-dlp"""
        try:
            if not self.ytdlp_command:
                raise Exception("yt-dlp is not properly installed or configured")
            
            total_urls = len(urls)
            
            for i, url in enumerate(urls):
                if not self.is_downloading:  # Check for cancellation
                    break
                
                # Update progress for multiple URLs
                if total_urls > 1:
                    overall_progress = (i / total_urls) * 100
                    self.progress_queue.put({
                        'percentage': overall_progress,
                        'status': f"Processing URL {i+1}/{total_urls}",
                        'log': f"🔗 [{i+1}/{total_urls}] Starting: {url}"
                    })
                
                platform = self.detect_platform(url)
                self.progress_queue.put({'log': f"🎯 Detected platform: {platform}"})
                
                # Build output template
                if self.audio_only_var.get():
                    output_template = "%(uploader)s - %(id)s.%(ext)s"
                else:
                    output_template = "%(uploader)s - %(id)s.%(ext)s"
                
                output_path = os.path.join(self.output_dir_var.get(), output_template)
                
                # Build command
                cmd = self.ytdlp_command + [
                    url,
                    "-o", output_path,
                    "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "--ignore-errors",
                    "--no-abort-on-error",
                    "--skip-unavailable-fragments",
                    "--fragment-retries", "3",
                    "--retries", "3",
                    "--newline"
                ]
                
                # Playlist handling
                if not self.playlist_var.get():
                    cmd.append("--no-playlist")
                
                # Audio only option
                if self.audio_only_var.get():
                    cmd.extend([
                        "--extract-audio",
                        "--audio-format", "mp3",
                        "--audio-quality", "192K"
                    ])
                else:
                    # Video format selection
                    custom_format = self.custom_format_var.get().strip()
                    if custom_format:
                        cmd.extend(["-f", custom_format])
                    else:
                        quality = self.quality_var.get()
                        video_format = self.format_var.get()
                        
                        if quality == "best":
                            format_selector = f"best[ext={video_format}]/best"
                        elif quality == "worst":
                            format_selector = f"worst[ext={video_format}]/worst"
                        else:
                            height = quality.replace('p', '')
                            format_selector = f"best[height<={height}][ext={video_format}]/best[height<={height}]"
                        
                        cmd.extend(["-f", format_selector])
                
                # Cookie file
                cookie_file = self.cookie_file_var.get().strip()
                if cookie_file and os.path.exists(cookie_file):
                    cmd.extend(["--cookies", cookie_file])
                    self.progress_queue.put({'log': f"🍪 Using cookie file: {os.path.basename(cookie_file)}"})
                
                # Log download info
                quality_info = "Audio only (MP3)" if self.audio_only_var.get() else f"{self.quality_var.get()} ({self.format_var.get()})"
                if custom_format:
                    quality_info += f" (Custom: {custom_format})"
                
                self.progress_queue.put({'log': f"📽️ Quality: {quality_info}"})
                self.progress_queue.put({'log': f"📁 Output: {self.output_dir_var.get()}"})
                self.progress_queue.put({'log': f"🚀 Executing command: {' '.join(cmd)}"})
                self.progress_queue.put({'log': "-" * 60})
                
                # Execute command
                try:
                    self.download_process = subprocess.Popen(
                        cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        universal_newlines=True,
                        bufsize=1,
                        creationflags=self.CREATE_NO_WINDOW
                    )
                    
                    # Read output in real-time
                    while self.download_process.poll() is None and self.is_downloading:
                        line = self.download_process.stdout.readline()
                        if line:
                            line = line.strip()
                            self.parse_progress(line)
                        else:
                            time.sleep(0.1)  # Prevent tight loop
                    
                    if not self.is_downloading:  # Download was cancelled
                        if self.download_process and self.download_process.poll() is None:
                            self.download_process.terminate()
                        break
                    
                    if self.download_process.returncode != 0:
                        error_output = self.download_process.stdout.read() or "No error output"
                        self.progress_queue.put({'log': f"❌ Failed to download: {url}. Error: {error_output}"})
                    else:
                        self.progress_queue.put({'log': f"✅ Successfully downloaded: {url}"})
                except Exception as e:
                    self.progress_queue.put({'log': f"❌ Error executing download for {url}: {e}"})
            
            # Final status
            if self.is_downloading:
                self.root.after(0, self.download_complete, True)
            else:
                self.root.after(0, self.download_complete, False, "cancelled")
                
        except Exception as e:
            self.root.after(0, self.download_error, str(e))
    
    def cancel_download(self):
        """Cancel the current download"""
        if self.is_downloading:
            self.is_downloading = False
            if self.download_process and self.download_process.poll() is None:
                try:
                    self.download_process.terminate()
                    self.download_process.wait(timeout=5)
                except:
                    try:
                        self.download_process.kill()
                    except:
                        pass
            
            self.progress_var.set(self.t('cancelled'))
            self.log_message("🛑 Download cancelled by user")
            self.reset_ui_state()
    
    def download_complete(self, success, reason=None):
        """Handle download completion"""
        self.is_downloading = False
        self.reset_ui_state()
        
        if success:
            self.progress_var.set(self.t('completed'))
            self.progress_bar['value'] = 100
            self.log_message("=" * 60)
            self.log_message("✅ Download completed successfully!")
            messagebox.showinfo(self.t('success'), self.t('download_success'))
        elif reason == "cancelled":
            self.progress_var.set(self.t('cancelled'))
            self.log_message("=" * 60)
            self.log_message("🛑 Download was cancelled")
        else:
            self.progress_var.set(self.t('failed'))
            self.log_message("=" * 60)
            self.log_message("❌ Download failed!")
            messagebox.showerror(self.t('error'), self.t('download_failed'))
    
    def download_error(self, error_msg):
        """Handle download error"""
        self.is_downloading = False
        self.reset_ui_state()
        self.progress_var.set(self.t('failed'))
        self.log_message(f"❌ Error: {error_msg}")
        messagebox.showerror(self.t('error'), f"Download error: {error_msg}")
    
    def reset_ui_state(self):
        """Reset UI to initial state"""
        self.download_btn.config(state="normal")
        self.batch_download_btn.config(state="normal")
        self.cancel_btn.config(state="disabled")
    
    def run(self):
        """Start the GUI application"""
        try:
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            self.root.mainloop()
        except KeyboardInterrupt:
            self.logger.info("Application interrupted by user")
        except Exception as e:
            self.logger.error(f"Application error: {e}")
    
    def on_closing(self):
        """Handle application closing"""
        if self.is_downloading:
            if messagebox.askokcancel("Quit", "Download in progress. Do you want to quit?"):
                self.cancel_download()
                self.save_settings()
                self.progress_queue.put(None)  # Stop progress monitor
                self.root.destroy()
        else:
            self.save_settings()
            self.progress_queue.put(None)  # Stop progress monitor
            self.root.destroy()

def download_video_cli(url, output_dir=".", quality="best", audio_only=False, playlist=False, cookie_file=None):
    """Enhanced command-line interface for downloading videos"""
    try:
        output_path = os.path.join(output_dir, "%(uploader)s - %(id)s.%(ext)s")
        
        cmd = [
            "yt-dlp",
            url,
            "-o", output_path,
            "--ignore-errors",
            "--retries", "3",
            "--newline"
        ]
        
        if not playlist:
            cmd.append("--no-playlist")
        
        if audio_only:
            cmd.extend([
                "--extract-audio",
                "--audio-format", "mp3",
                "--audio-quality", "192K"
            ])
        else:
            if quality == "worst":
                cmd.extend(["-f", "worst"])
            elif quality != "best":
                height = quality.replace('p', '')
                cmd.extend(["-f", f"best[height<={height}]"])
        
        if cookie_file and os.path.exists(cookie_file):
            cmd.extend(["--cookies", cookie_file])
        
        print(f"🔗 Downloading from: {url}")
        print(f"📁 Output directory: {output_dir}")
        print(f"📽️ Quality: {'Audio only (MP3)' if audio_only else quality}")
        print(f"📋 Playlist: {'Yes' if playlist else 'No'}")
        if cookie_file:
            print(f"🍪 Cookie file: {cookie_file}")
        print("-" * 50)
        
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                                 universal_newlines=True, bufsize=1)
        
        for line in process.stdout:
            print(line.strip())
        
        process.wait()
        
        if process.returncode == 0:
            print("✅ Download completed successfully!")
            return True
        else:
            print("❌ Download failed!")
            return False
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Download failed: {e}")
        return False
    except FileNotFoundError:
        print("❌ yt-dlp not found. Please install it: pip install yt-dlp")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def main():
    """Main function with enhanced CLI support"""
    if len(sys.argv) > 1:
        # Command-line mode with argument parsing
        import argparse
        
        parser = argparse.ArgumentParser(description="Enhanced Universal Video Downloader")
        parser.add_argument("url", help="Video URL to download")
        parser.add_argument("-o", "--output", default=".", help="Output directory")
        parser.add_argument("-q", "--quality", default="best", 
                          choices=["best", "worst", "1080p", "720p", "480p", "360p", "240p"],
                          help="Video quality")
        parser.add_argument("--audio", action="store_true", help="Download audio only (MP3)")
        parser.add_argument("--playlist", action="store_true", help="Download entire playlist")
        parser.add_argument("--cookies", help="Path to cookie file")
        parser.add_argument("--batch", help="File containing URLs (one per line)")
        
        args = parser.parse_args()
        
        if args.batch:
            # Batch download from file
            try:
                with open(args.batch, 'r') as f:
                    urls = [line.strip() for line in f if line.strip()]
                
                success_count = 0
                for i, url in enumerate(urls, 1):
                    print(f"\n{'='*60}")
                    print(f"Processing URL {i}/{len(urls)}: {url}")
                    print('='*60)
                    
                    if download_video_cli(url, args.output, args.quality, 
                                        args.audio, args.playlist, args.cookies):
                        success_count += 1
                
                print(f"\n🎉 Batch download completed: {success_count}/{len(urls)} successful")
            except Exception as e:
                print(f"❌ Batch download error: {e}")
        else:
            # Single URL download
            download_video_cli(args.url, args.output, args.quality, 
                             args.audio, args.playlist, args.cookies)
    else:
        # GUI mode
        try:
            app = EnhancedVideoDownloader()
            app.run()
        except KeyboardInterrupt:
            print("\nApplication interrupted by user")
        except Exception as e:
            print(f"Application error: {e}")

if __name__ == "__main__":
    main()