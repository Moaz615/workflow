import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import threading
import subprocess
import logging
from typing import Optional, List, Callable, Any, Dict, Tuple
from pathlib import Path
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
import yt_dlp
import webbrowser
import datetime
import shutil
import glob
import time
try:
    from ttkthemes import ThemedTk
    HAS_THEMES = True
except ImportError:
    HAS_THEMES = False

APP_NAME = "Moaz Video Downloader"
APP_VERSION = "1.0"
APP_AUTHOR = "Moaz"

# Optional: Desktop notifications
try:
    from plyer import notification
    HAS_NOTIFICATIONS = True
except ImportError:
    HAS_NOTIFICATIONS = False
    
# --- i18n ---
LANGUAGES = {
    'en': {
        'title': 'Moaz Video Downloader',
        'url_label': 'Video URL:',
        'output_dir_label': 'Download Directory:',
        'browse': 'Browse',
        'download': 'Download',
        'batch_download': 'Batch Download',
        'quality': 'Quality:',
        'format': 'Format:',
        'custom_format': 'Custom Format:',
        'audio_only': 'Audio Only (MP3)',
        'playlist': 'Download Playlist',
        'settings': 'Settings',
        'help': 'Help',
        'about': 'About',
        'save': 'Save',
        'cancel': 'Cancel',
        'language': 'Language:',
        'theme': 'Theme:',
        'light': 'Light',
        'dark': 'Dark',
        'cookie_file': 'Cookie File:',
        'validate': 'Validate',
        'cookie_valid': 'Cookie file validated successfully!',
        'cookie_invalid': 'Cookie file is invalid or empty.',
        'drag_drop': 'Drag & drop URLs here',
        'notification_success': 'Download completed!',
        'notification_fail': 'Download failed!',
        'invalid_url': 'Invalid URL',
        'output_dir_missing': 'Output directory does not exist',
        'downloading': 'Downloading...',
        'done': 'Done!',
        'failed': 'Failed.',
        'batch_urls': 'Batch URLs (one per line):',
        'add_urls': 'Add URLs',
        'parallel_downloads': 'Parallel Downloads:',
        'about_text': 'Universal Video Downloader\nBuilt with Python & yt-dlp\nAuthor: Your Name',
        'help_text': 'Paste or drag URLs. Configure options. Click Download. For batch, enter one URL per line.',
        'detect_formats': 'Detect Formats',
        'log': 'Log:',
        'progress': 'Progress:',
        'status': 'Status:',
        'download_cancelled': 'Download cancelled.',
        'download_completed': 'Download completed successfully!',
        'download_failed': 'Download failed. Check the log for details.',
        'no_valid_urls': 'No valid URLs found.',
        'batch_completed': 'Batch download completed.',
        'batch_failed': 'Batch download failed.',
        'recent_batch': 'Recent Batch Files:',
        'select_batch': 'Select Batch File',
        'error': 'Error',
        'warning': 'Warning',
        'success': 'Success',
        'info': 'Info',
        'cancel_download': 'Cancel Download',
        'proxy': 'Proxy:',
        'schedule': 'Schedule Download',
        'schedule_time': 'Schedule Time (HH:MM):',
        'enable_notifications': 'Enable Notifications',
        'check_updates': 'Check for yt-dlp Updates',
        'update_available': 'yt-dlp update available!',
        'up_to_date': 'yt-dlp is up to date.',
        'export_settings': 'Export Settings',
        'import_settings': 'Import Settings',
        'log_level': 'Log Level:',
        'clear_log': 'Clear Log',
        'file_template': 'File Naming Template:',
        'pause': 'Pause',
        'resume': 'Resume',
        'scheduled_for': 'Scheduled for',
        'now': 'Now',
        'user_agent': 'User-Agent:',
        'bandwidth': 'Bandwidth Limit (K/s):',
        'plugin_dir': 'Plugin Directory:',
        'history': 'History',
        'recent_downloads': 'Recent Downloads',
        'clear_history': 'Clear History',
        'remove_recent_downloads': 'Remove Recent Downloads',
        'skip_downloaded': 'Skip already downloaded videos',
        'install_ytdlp': 'Install yt-dlp',
        'not_found': 'Not found',
        'auto_detect_qualities_formats': 'Auto-Detect Qualities & Formats',
        'copy_log': 'Copy Log',
        'export_log': 'Export Log',
        'open_log_file': 'Open Log File',
        'ready': 'Ready.',
        'detected_formats': 'Detected formats:',
        'no_formats_detected': 'No formats detected.',
        'best': 'Best',
        'worst': 'Worst',
        'tooltip_quality': "Select the desired video quality for your download. 'Best' will download the highest available quality.",
        'tooltip_format': "Select the desired file format for your download. 'mp4' is recommended for most users.",
        'tooltip_download': "Start downloading the video from the URL above.",
        'tooltip_cancel': "Cancel the current download.",
        'tooltip_log': "This area shows logs and download progress.",
        'tooltip_progress': "Shows download progress.",
        'tooltip_recent': "Select a recently used URL.",
        'dir_not_writable': 'Download directory is not writable.',
        'about_message': "I'm Moaz (pronounced Mu'adh), or Abulbara', a G12 student at STEM October. I'm into tech, problem-solving, and I enjoy building projects that make a real difference.",
        'ytdlp_installed': 'yt-dlp installed successfully!',
        'ytdlp_install_failed': 'Failed to install yt-dlp.',
        'ffmpeg_missing': 'ffmpeg is missing! Audio downloads will not work. Please place ffmpeg.exe in the app folder or install ffmpeg and add it to your PATH.',
        'merge_failed': 'Merging failed! The video could not be downloaded or merged. Please ensure ffmpeg is available.',
        'reset': 'Reset',
        'reset_settings': 'Reset Settings',
        'reset_confirm_title': 'Confirm Reset',
        'reset_confirm_message': 'Are you sure you want to reset all settings to their defaults? This cannot be undone.',
        'settings_reset_message': 'Settings have been reset to their default values.',
    },
    'es': {
        'title': 'Moaz Descargador de Videos',
        'url_label': 'URL del video:',
        'output_dir_label': 'Directorio de descarga:',
        'browse': 'Explorar',
        'download': 'Descargar',
        'batch_download': 'Descarga por lotes',
        'quality': 'Calidad:',
        'format': 'Formato:',
        'custom_format': 'Formato personalizado:',
        'audio_only': 'Solo audio (MP3)',
        'playlist': 'Descargar lista',
        'settings': 'Configuración',
        'help': 'Ayuda',
        'about': 'Acerca de',
        'save': 'Guardar',
        'cancel': 'Cancelar',
        'language': 'Idioma:',
        'theme': 'Tema:',
        'light': 'Claro',
        'dark': 'Oscuro',
        'cookie_file': 'Archivo de cookie:',
        'validate': 'Validar',
        'cookie_valid': 'Archivo de cookie validado correctamente!',
        'cookie_invalid': 'El archivo de cookie es inválido o vacío.',
        'drag_drop': 'Arrastra y suelta URLs aquí',
        'notification_success': '¡Descarga completada!',
        'notification_fail': '¡Descarga fallida!',
        'invalid_url': 'URL inválida',
        'output_dir_missing': 'El directorio no existe',
        'downloading': 'Descargando...',
        'done': '¡Hecho!',
        'failed': 'Falló.',
        'batch_urls': 'URLs por lotes (una por línea):',
        'add_urls': 'Agregar URLs',
        'parallel_downloads': 'Descargas paralelas:',
        'about_text': 'Descargador Universal de Videos\nHecho con Python & yt-dlp\nAutor: Tu Nombre',
        'help_text': 'Pega o arrastra URLs. Configura opciones. Haz clic en Descargar. Para lotes, una URL por línea.',
        'detect_formats': 'Detectar formatos',
        'log': 'Registro:',
        'progress': 'Progreso:',
        'status': 'Estado:',
        'download_cancelled': 'Descarga cancelada.',
        'download_completed': '¡Descarga completada exitosamente!',
        'download_failed': 'Descarga falló. Revise el registro para detalles.',
        'no_valid_urls': 'No se encontraron URLs válidas.',
        'batch_completed': 'Descarga por lotes completada.',
        'batch_failed': 'Descarga por lotes falló.',
        'recent_batch': 'Archivos de lote recientes:',
        'select_batch': 'Seleccionar archivo de lote',
        'error': 'Error',
        'warning': 'Advertencia',
        'success': 'Éxito',
        'info': 'Info',
        'cancel_download': 'Cancelar descarga',
        'proxy': 'Proxy:',
        'schedule': 'Programar descarga',
        'schedule_time': 'Hora programada (HH:MM):',
        'enable_notifications': 'Habilitar notificaciones',
        'check_updates': 'Buscar actualizaciones de yt-dlp',
        'update_available': '¡Actualización de yt-dlp disponible!',
        'up_to_date': 'yt-dlp está actualizado.',
        'export_settings': 'Exportar configuración',
        'import_settings': 'Importar configuración',
        'log_level': 'Nivel de registro:',
        'clear_log': 'Limpiar registro',
        'file_template': 'Plantilla de nombre de archivo:',
        'pause': 'Pausar',
        'resume': 'Reanudar',
        'scheduled_for': 'Programado para',
        'now': 'Ahora',
        'user_agent': 'Agente de Usuario:',
        'bandwidth': 'Límite de ancho de banda (K/s):',
        'plugin_dir': 'Directorio de plugins:',
        'history': 'Historial',
        'recent_downloads': 'Descargas recientes',
        'clear_history': 'Borrar historial',
        'remove_recent_downloads': 'Eliminar descargas recientes',
        'skip_downloaded': 'Omitir videos ya descargados',
        'install_ytdlp': 'Instalar yt-dlp',
        'not_found': 'No encontrado',
        'auto_detect_qualities_formats': 'Detectar automáticamente calidades y formatos',
        'copy_log': 'Copiar registro',
        'export_log': 'Exportar registro',
        'open_log_file': 'Abrir archivo de registro',
        'ready': 'Listo.',
        'detected_formats': 'Formatos detectados:',
        'no_formats_detected': 'No se detectaron formatos.',
        'best': 'Mejor',
        'worst': 'Peor',
        'tooltip_quality': "Selecciona la calidad de video deseada para tu descarga. 'Mejor' descargará la mayor calidad disponible.",
        'tooltip_format': "Selecciona el formato de archivo deseado para tu descarga. 'mp4' es recomendado para la mayoría de los usuarios.",
        'tooltip_download': "Comienza a descargar el video de la URL de arriba.",
        'tooltip_cancel': "Cancela la descarga actual.",
        'tooltip_log': "Esta área muestra los registros y el progreso de la descarga.",
        'tooltip_progress': "Muestra el progreso de la descarga.",
        'tooltip_recent': "Selecciona una URL usada recientemente.",
        'dir_not_writable': 'Directorio de descarga no es writable.',
        'about_message': "I'm Moaz (pronounced Mu'adh), or Abulbara', a G12 student at STEM October. I'm into tech, problem-solving, and I enjoy building projects that make a real difference.",
        'ytdlp_installed': 'yt-dlp instalado correctamente!',
        'ytdlp_install_failed': 'Error al instalar yt-dlp.',
        'ffmpeg_missing': '¡Falta ffmpeg! Las descargas de audio no funcionarán. Por favor, coloque ffmpeg.exe en la carpeta de la aplicación o instale ffmpeg y agréguelo a su PATH.',
        'merge_failed': '¡Error al fusionar! El video no se pudo descargar o fusionar. Por favor, asegúrese de que ffmpeg esté disponible.',
        'reset': 'Reset',
        'reset_settings': 'Restablecer Ajustes',
        'reset_confirm_title': 'Confirmar Restablecimiento',
        'reset_confirm_message': '¿Estás seguro de que quieres restablecer todos los ajustes a sus valores predeterminados? Esto no se puede deshacer.',
        'settings_reset_message': 'Los ajustes se han restablecido a sus valores predeterminados.',
    },
    'fr': {
        'title': 'Moaz Téléchargeur de Vidéos',
        'url_label': 'URL de la vidéo :',
        'output_dir_label': 'Dossier de téléchargement :',
        'browse': 'Parcourir',
        'download': 'Télécharger',
        'batch_download': 'Téléchargement par lot',
        'quality': 'Qualité :',
        'format': 'Format :',
        'custom_format': 'Format personnalisé :',
        'audio_only': 'Audio seulement (MP3)',
        'playlist': 'Télécharger la playlist',
        'settings': 'Paramètres',
        'help': 'Aide',
        'about': 'À propos',
        'save': 'Enregistrer',
        'cancel': 'Annuler',
        'language': 'Langue :',
        'theme': 'Thème :',
        'light': 'Clair',
        'dark': 'Sombre',
        'cookie_file': 'Fichier de cookie :',
        'validate': 'Valider',
        'cookie_valid': 'Fichier de cookie validé avec succès !',
        'cookie_invalid': 'Fichier de cookie invalide ou vide.',
        'drag_drop': 'Glisser-déposer les URLs ici',
        'notification_success': 'Téléchargement terminé !',
        'notification_fail': 'Échec du téléchargement !',
        'invalid_url': 'URL invalide',
        'output_dir_missing': "Le dossier de téléchargement n'existe pas",
        'downloading': 'Téléchargement...',
        'done': 'Terminé !',
        'failed': 'Échec.',
        'batch_urls': 'URLs par lot (une par ligne) :',
        'add_urls': 'Ajouter des URLs',
        'parallel_downloads': 'Téléchargements parallèles :',
        'about_text': 'Téléchargeur Universel de Vidéos\nConstruit avec Python & yt-dlp\nAuteur : Votre Nom',
        'help_text': 'Collez ou glissez les URLs. Configurez les options. Cliquez sur Télécharger. Pour les lots, une URL par ligne.',
        'detect_formats': 'Détecter les formats',
        'log': 'Journal :',
        'progress': 'Progression :',
        'status': 'Statut :',
        'proxy': 'Proxy :',
        'schedule': 'Planifier le téléchargement',
        'schedule_time': 'Heure planifiée (HH:MM) :',
        'enable_notifications': 'Activer les notifications',
        'check_updates': 'Vérifier les mises à jour de yt-dlp',
        'update_available': 'Mise à jour yt-dlp disponible !',
        'up_to_date': 'yt-dlp est à jour.',
        'export_settings': 'Exporter les paramètres',
        'import_settings': 'Importer les paramètres',
        'log_level': 'Niveau de journalisation :',
        'clear_log': 'Effacer le journal',
        'file_template': 'Modèle de nom de fichier :',
        'pause': 'Pause',
        'resume': 'Reprendre',
        'scheduled_for': 'Planifié pour',
        'now': 'Maintenant',
        'user_agent': 'User-Agent :',
        'bandwidth': 'Limite de bande passante (K/s) :',
        'plugin_dir': 'Dossier de plugins :',
        'history': 'Historique',
        'download_cancelled': 'Téléchargement annulé.',
        'download_completed': 'Téléchargement terminé avec succès !',
        'download_failed': 'Échec du téléchargement. Consultez le journal pour plus de détails.',
        'no_valid_urls': 'Aucune URL valide trouvée.',
        'batch_completed': 'Téléchargement par lot terminé.',
        'batch_failed': 'Échec du téléchargement par lot.',
        'recent_batch': 'Fichiers de lot récents :',
        'select_batch': 'Sélectionner un fichier de lot',
        'error': 'Erreur',
        'warning': 'Avertissement',
        'success': 'Succès',
        'info': 'Info',
        'cancel_download': 'Annuler le téléchargement',
        'url_required': 'Veuillez entrer une URL',
        'cancelling': 'Annulation en cours...',
        'cancelled': 'Annulé',
        'ready': 'Prêt',
        'user_agent': 'Agent utilisateur :',
        'bandwidth': 'Limite de bande passante (K/s) :',
        'plugin_dir': 'Dossier des plugins :',
        'history': 'Historique',
        'recent_downloads': 'Téléchargements récents',
        'clear_history': "Effacer l'historique",
        'remove_recent_downloads': 'Supprimer les téléchargements récents',
        'skip_downloaded': 'Ignorer les vidéos déjà téléchargées',
        'install_ytdlp': 'Installer yt-dlp',
        'not_found': 'Non trouvé',
        'auto_detect_qualities_formats': 'Détecter automatiquement les qualités et formats',
        'copy_log': 'Copier Log',
        'export_log': 'Exporter Log',
        'open_log_file': 'Ouvrir le fichier de log',
        'ready': 'Prêt.',
        'detected_formats': 'Formats détectés :',
        'no_formats_detected': 'Aucun format détecté.',
        'best': 'Meilleur',
        'worst': 'Pire',
        'tooltip_quality': "Sélectionnez la qualité vidéo souhaitée pour votre téléchargement. 'Meilleur' téléchargera la meilleure qualité disponible.",
        'tooltip_format': "Sélectionnez le format de fichier souhaité pour votre téléchargement. 'mp4' est recommandé pour la plupart des utilisateurs.",
        'tooltip_download': "Commencez à télécharger la vidéo à partir de l'URL ci-dessus.",
        'tooltip_cancel': "Annulez le téléchargement en cours.",
        'tooltip_log': "Cette zone affiche les journaux et la progression du téléchargement.",
        'tooltip_progress': "Affiche la progression du téléchargement.",
        'tooltip_recent': "Sélectionnez une URL récemment utilisée.",
        'dir_not_writable': 'Dossier de téléchargement non writable.',
        'about_message': "I'm Moaz (pronounced Mu'adh), or Abulbara', a G12 student at STEM October. I'm into tech, problem-solving, and I enjoy building projects that make a real difference.",
        'ytdlp_installed': 'yt-dlp installé avec succès!',
        'ytdlp_install_failed': "Échec de l'installation de yt-dlp.",
        'ffmpeg_missing': 'ffmpeg est manquant ! Les téléchargements audio ne fonctionneront pas. Veuillez placer ffmpeg.exe dans le dossier de l\'application ou installer ffmpeg et l\'ajouter à votre PATH.',
        'merge_failed': 'La fusion a échoué ! La vidéo n\'a pas pu être téléchargée ou fusionnée. Veuillez vous assurer que ffmpeg est disponible.',
        'reset': 'Reset',
        'reset_settings': 'Réinitialiser les Paramètres',
        'reset_confirm_title': 'Confirmer la Réinitialisation',
        'reset_confirm_message': 'Êtes-vous sûr de vouloir réinitialiser tous les paramètres à leurs valeurs par défaut ? Cette action est irréversible.',
        'settings_reset_message': 'Les paramètres ont été réinitialisés à leurs valeurs par défaut.',
    },
    'de': {
        'title': 'Moaz Video-Downloader',
        'url_label': 'Video-URL:',
        'output_dir_label': 'Download-Verzeichnis:',
        'browse': 'Durchsuchen',
        'download': 'Herunterladen',
        'batch_download': 'Stapel-Download',
        'quality': 'Qualität:',
        'format': 'Format:',
        'custom_format': 'Benutzerdefiniertes Format:',
        'audio_only': 'Nur Audio (MP3)',
        'playlist': 'Playlist herunterladen',
        'settings': 'Einstellungen',
        'help': 'Hilfe',
        'about': 'Über',
        'save': 'Speichern',
        'cancel': 'Abbrechen',
        'language': 'Sprache:',
        'theme': 'Thema:',
        'light': 'Hell',
        'dark': 'Dunkel',
        'cookie_file': 'Cookie-Datei:',
        'validate': 'Validieren',
        'cookie_valid': 'Cookie-Datei erfolgreich validiert!',
        'cookie_invalid': 'Cookie-Datei ist ungültig oder leer.',
        'drag_drop': 'URLs hierher ziehen',
        'notification_success': 'Download abgeschlossen!',
        'notification_fail': 'Download fehlgeschlagen!',
        'invalid_url': 'Ungültige URL',
        'output_dir_missing': 'Download-Verzeichnis existiert nicht',
        'downloading': 'Wird heruntergeladen...',
        'done': 'Fertig!',
        'failed': 'Fehlgeschlagen.',
        'batch_urls': 'Stapel-URLs (eine pro Zeile):',
        'add_urls': 'URLs hinzufügen',
        'parallel_downloads': 'Parallele Downloads:',
        'about_text': 'Universeller Video-Downloader\nErstellt mit Python & yt-dlp\nAutor: Ihr Name',
        'help_text': 'Fügen Sie URLs ein oder ziehen Sie sie. Optionen konfigurieren. Klicken Sie auf Herunterladen. Für Stapel, eine URL pro Zeile.',
        'detect_formats': 'Formate erkennen',
        'log': 'Protokoll:',
        'progress': 'Fortschritt:',
        'status': 'Status:',
        'proxy': 'Proxy:',
        'schedule': 'Download planen',
        'schedule_time': 'Geplante Zeit (HH:MM):',
        'enable_notifications': 'Benachrichtigungen aktivieren',
        'check_updates': 'Nach yt-dlp-Updates suchen',
        'update_available': 'yt-dlp-Update verfügbar!',
        'up_to_date': 'yt-dlp ist aktuell.',
        'export_settings': 'Einstellungen exportieren',
        'import_settings': 'Einstellungen importieren',
        'log_level': 'Protokollstufe:',
        'clear_log': 'Protokoll löschen',
        'file_template': 'Dateinamensvorlage:',
        'pause': 'Pause',
        'resume': 'Fortsetzen',
        'scheduled_for': 'Geplant für',
        'now': 'Jetzt',
        'user_agent': 'User-Agent:',
        'bandwidth': 'Bandbreitenlimit (K/s):',
        'plugin_dir': 'Plugin-Verzeichnis:',
        'history': 'Verlauf',
        'recent_downloads': 'Downloads kürzlich',
        'clear_history': 'Verlauf löschen',
        'remove_recent_downloads': 'Letzte Downloads entfernen',
        'skip_downloaded': 'Bereits heruntergeladene Videos überspringen',
        'install_ytdlp': 'yt-dlp installieren',
        'not_found': 'Nicht gefunden',
        'auto_detect_qualities_formats': 'Qualitäten & Formate automatisch erkennen',
        'copy_log': 'Protokoll kopieren',
        'export_log': 'Protokoll exportieren',
        'open_log_file': 'Protokolldatei öffnen',
        'ready': 'Bereit.',
        'detected_formats': 'Erkannte Formate:',
        'no_formats_detected': 'Keine Formate erkannt.',
        'best': 'Beste',
        'worst': 'Schlechteste',
        'tooltip_quality': "Wählen Sie die gewünschte Videoqualität für Ihren Download. 'Beste' lädt die höchste verfügbare Qualität herunter.",
        'tooltip_format': "Wählen Sie das gewünschte Dateiformat für Ihren Download. 'mp4' wird für die meisten Benutzer empfohlen.",
        'tooltip_download': "Starten Sie den Download des Videos von der obigen URL.",
        'tooltip_cancel': "Den aktuellen Download abbrechen.",
        'tooltip_log': "Dieser Bereich zeigt Protokolle und den Download-Fortschritt an.",
        'tooltip_progress': "Zeigt den Download-Fortschritt an.",
        'tooltip_recent': "Wählen Sie eine kürzlich verwendete URL aus.",
        'dir_not_writable': 'Download-Verzeichnis ist nicht writable.',
        'about_message': "I'm Moaz (pronounced Mu'adh), or Abulbara', a G12 student at STEM October. I'm into tech, problem-solving, and I enjoy building projects that make a real difference.",
        'ytdlp_installed': 'yt-dlp installiert!',
        'ytdlp_install_failed': 'Installation von yt-dlp fehlgeschlagen.',
        'ffmpeg_missing': 'ffmpeg fehlt! Audio-Downloads funktionieren nicht. Bitte legen Sie ffmpeg.exe im Anwendungsordner ab oder installieren Sie ffmpeg und fügen Sie es Ihrem PATH hinzu.',
        'merge_failed': 'Zusammenführung fehlgeschlagen! Das Video konnte nicht heruntergeladen oder zusammengeführt werden. Bitte stellen Sie sicher, dass ffmpeg verfügbar ist.',
        'reset': 'Reset',
        'reset_settings': 'Einstellungen zurücksetzen',
        'reset_confirm_title': 'Zurücksetzen bestätigen',
        'reset_confirm_message': 'Möchten Sie wirklich alle Einstellungen auf die Standardwerte zurücksetzen? Dies kann nicht rückgängig gemacht werden.',
        'settings_reset_message': 'Die Einstellungen wurden auf die Standardwerte zurückgesetzt.',
    },
    'ar': {
        'title': 'برنامج معاذالشامل لتحميل الفيديوهات',
        'url_label': 'رابط الفيديو:',
        'output_dir_label': 'مجلد التحميل:',
        'browse': 'تصفح',
        'download': 'تحميل',
        'batch_download': 'تحميل دفعة',
        'quality': 'الجودة:',
        'format': 'الصيغة:',
        'custom_format': 'صيغة مخصصة:',
        'audio_only': 'صوت فقط (MP3)',
        'playlist': 'تحميل قائمة التشغيل',
        'settings': 'الإعدادات',
        'help': 'مساعدة',
        'about': 'حول',
        'save': 'حفظ',
        'cancel': 'إلغاء',
        'language': 'اللغة:',
        'theme': 'السمة:',
        'light': 'فاتح',
        'dark': 'داكن',
        'cookie_file': 'ملف الكوكيز:',
        'validate': 'تحقق',
        'cookie_valid': 'تم التحقق من ملف الكوكيز بنجاح!',
        'cookie_invalid': 'ملف الكوكيز غير صالح أو فارغ.',
        'drag_drop': 'اسحب وأسقط الروابط هنا',
        'notification_success': 'تم التحميل بنجاح!',
        'notification_fail': 'فشل التحميل!',
        'invalid_url': 'رابط غير صالح',
        'output_dir_missing': 'مجلد التحميل غير موجود',
        'downloading': 'جاري التحميل...',
        'done': 'تم!',
        'failed': 'فشل.',
        'batch_urls': 'روابط دفعة (رابط في كل سطر):',
        'add_urls': 'إضافة روابط',
        'parallel_downloads': 'عدد التحميلات المتزامنة:',
        'about_text': 'برنامج تحميل الفيديو الشامل\nتم تطويره بواسطة Python و yt-dlp\nالمطور: اسمك',
        'help_text': 'الصق أو اسحب الروابط. اضبط الخيارات. اضغط تحميل. للدفعات، ضع رابط في كل سطر.',
        'detect_formats': 'كشف الصيغ',
        'log': 'السجل:',
        'progress': 'التقدم:',
        'status': 'الحالة:',
        'proxy': 'بروكسي:',
        'schedule': 'جدولة التحميل',
        'schedule_time': 'وقت الجدولة (ساعة:دقيقة):',
        'enable_notifications': 'تفعيل الإشعارات',
        'check_updates': 'التحقق من تحديثات yt-dlp',
        'update_available': 'تحديث yt-dlp متوفر!',
        'up_to_date': 'yt-dlp محدث.',
        'export_settings': 'تصدير الإعدادات',
        'import_settings': 'استيراد الإعدادات',
        'log_level': 'مستوى السجل:',
        'clear_log': 'مسح السجل',
        'file_template': 'قالب اسم الملف:',
        'pause': 'إيقاف مؤقت',
        'resume': 'استئناف',
        'scheduled_for': 'مجدول لـ',
        'now': 'الآن',
        'user_agent': 'وكيل المستخدم:',
        'bandwidth': 'حد سرعة التحميل (ك.ب/ث):',
        'plugin_dir': 'مجلد الإضافات:',
        'history': 'السجل',
        'recent_downloads': 'تحميلات مؤخرا',
        'clear_history': 'مسح السجل',
        'remove_recent_downloads': 'إزالة التحميلات الأخيرة',
        'skip_downloaded': 'تخطي الفيديوهات التي تم تحميلها مسبقاً',
        'install_ytdlp': 'تثبيت yt-dlp',
        'not_found': 'لم يتم العثور عليه',
        'auto_detect_qualities_formats': 'تحديث جودة وصيغة مخصصة تلقائياً',
        'copy_log': 'نسخ السجل',
        'export_log': 'تصدير السجل',
        'open_log_file': 'فتح ملف السجل',
        'ready': 'جاهز.',
        'detected_formats': 'تم الكشف عن الصيغ:',
        'no_formats_detected': 'لم يتم الكشف عن أي صيغ.',
        'best': 'أفضل',
        'worst': 'أسوأ',
        'tooltip_quality': "اختر جودة الفيديو المطلوبة للتنزيل. 'أفضل' ستقوم بتنزيل أعلى جودة متاحة.",
        'tooltip_format': "اختر صيغة الملف المطلوبة للتنزيل. 'mp4' موصى به لمعظم المستخدمين.",
        'tooltip_download': "ابدأ تنزيل الفيديو من الرابط أعلاه.",
        'tooltip_cancel': "إلغاء التنزيل الحالي.",
        'tooltip_log': "تعرض هذه المنطقة السجلات وتقدم التنزيل.",
        'tooltip_progress': "يعرض تقدم التنزيل.",
        'tooltip_recent': "اختر رابطًا تم استخدامه مؤخرًا.",
        'dir_not_writable': 'مجلد التحميل غير موجود',
        'about_message': "I'm Moaz (pronounced Mu'adh), or Abulbara', a G12 student at STEM October. I'm into tech, problem-solving, and I enjoy building projects that make a real difference.",
        'ytdlp_installed': 'yt-dlp مثبت بنجاح!',
        'ytdlp_install_failed': 'فشل تثبيت yt-dlp.',
        'ffmpeg_missing': 'ffmpeg غير موجود! لن تعمل تنزيلات الصوت. يرجى وضع ffmpeg.exe في مجلد التطبيق أو تثبيت ffmpeg وإضافته إلى مسار النظام.',
        'merge_failed': 'فشل الدمج! تعذر تنزيل الفيديو أو دمجه. يرجى التأكد من توفر ffmpeg.',
        'reset': 'Reset',
        'reset_settings': 'إعادة ضبط الإعدادات',
        'reset_confirm_title': 'تأكيد إعادة الضبط',
        'reset_confirm_message': 'هل أنت متأكد أنك تريد إعادة ضبط جميع الإعدادات إلى قيمها الافتراضية؟ لا يمكن التراجع عن هذا الإجراء.',
        'settings_reset_message': 'تمت إعادة ضبط الإعدادات إلى قيمها الافتراضية.',
    },
    'it': {
        'title': 'Moaz Downloader di Video',
        'url_label': 'URL del video:',
        'output_dir_label': 'Cartella di download:',
        'browse': 'Sfoglia',
        'download': 'Scarica',
        'batch_download': 'Download multiplo',
        'quality': 'Qualità:',
        'format': 'Formato:',
        'custom_format': 'Formato personalizzato:',
        'audio_only': 'Solo audio (MP3)',
        'playlist': 'Scarica playlist',
        'settings': 'Impostazioni',
        'help': 'Aiuto',
        'about': 'Informazioni',
        'save': 'Salva',
        'cancel': 'Annulla',
        'language': 'Lingua:',
        'theme': 'Tema:',
        'light': 'Chiaro',
        'dark': 'Scuro',
        'cookie_file': 'File cookie:',
        'validate': 'Valida',
        'cookie_valid': 'File cookie validato con successo!',
        'cookie_invalid': 'File cookie non valido o vuoto.',
        'drag_drop': 'Trascina e rilascia gli URL qui',
        'notification_success': 'Download completato!',
        'notification_fail': 'Download fallito!',
        'invalid_url': 'URL non valido',
        'output_dir_missing': "La cartella di download non esiste",
        'downloading': 'Download in corso...',
        'done': 'Fatto!',
        'failed': 'Fallito.',
        'batch_urls': 'URL multipli (uno per riga):',
        'add_urls': 'Aggiungi URL',
        'parallel_downloads': 'Downloads paralelos:',
        'about_text': 'Downloader Universale di Video\nSviluppato con Python & yt-dlp\nAutor: Il tuo nome',
        'help_text': 'Incolla o trascina gli URL. Configura le opzioni. Clicca su Scarica. Per i batch, un URL per riga.',
        'detect_formats': 'Rileva formati',
        'log': 'Log:',
        'progress': 'Avanzamento:',
        'status': 'Stato:',
        'proxy': 'Proxy:',
        'schedule': 'Programma download',
        'schedule_time': 'Orario programmato (HH:MM):',
        'enable_notifications': 'Abilita notifiche',
        'check_updates': 'Controlla aggiornamenti yt-dlp',
        'update_available': 'Aggiornamento yt-dlp disponível!',
        'up_to_date': 'yt-dlp è aggiornato.',
        'export_settings': 'Esporta impostazioni',
        'import_settings': 'Importa impostazioni',
        'log_level': 'Livello log:',
        'clear_log': 'Pulisci log',
        'file_template': 'Template nome file:',
        'pause': 'Pausa',
        'resume': 'Retomar',
        'scheduled_for': 'Programmato per',
        'now': 'Agora',
        'user_agent': 'Agente utente:',
        'bandwidth': 'Bandwidth limit (K/s):',
        'plugin_dir': 'Cartella plugin:',
        'history': 'Cronologia',
        'recent_downloads': 'Scaricamenti recenti',
        'clear_history': 'Cancella cronologia',
        'remove_recent_downloads': 'Rimuovi download recenti',
        'skip_downloaded': 'Salta i video già scaricati',
        'install_ytdlp': 'Installa yt-dlp',
        'not_found': 'Non trovato',
        'auto_detect_qualities_formats': 'Rileva automaticamente qualità e formati',
        'copy_log': 'Copia Log',
        'export_log': 'Esporta Log',
        'open_log_file': 'Apri file di log',
        'ready': 'Pronto.',
        'detected_formats': 'Formati rilevati:',
        'no_formats_detected': 'Nessun formato rilevato.',
        'best': 'Migliore',
        'worst': 'Pior',
        'tooltip_quality': "Seleziona la qualità video desiderata per il download. 'Migliore' scaricherà la qualità più alta disponibile.",
        'tooltip_format': "Seleziona il formato file desiderato per il download. 'mp4' è consigliato per la maggior parte degli utenti.",
        'tooltip_download': "Inizia a scaricare il video dall'URL sopra.",
        'tooltip_cancel': "Annulla il download corrente.",
        'tooltip_log': "Quest'area mostra i log e l'avanzamento del download.",
        'tooltip_progress': "Mostra l'avanzamento del download.",
        'tooltip_recent': "Seleziona un URL usato di recente.",
        'dir_not_writable': "La cartella di download non esiste",
        'about_message': "I'm Moaz (pronounced Mu'adh), or Abulbara', a G12 student at STEM October. I'm into tech, problem-solving, and I enjoy building projects that make a real difference.",
        'ytdlp_installed': 'yt-dlp installato con successo!',
        'ytdlp_install_failed': 'Installazione di yt-dlp non riuscita.',
        'ffmpeg_missing': 'ffmpeg è mancante! I download audio non funzioneranno. Per favore, inserisci ffmpeg.exe nella cartella dell\'app o installa ffmpeg e aggiungilo al tuo PATH.',
        'merge_failed': 'Unione fallita! Il video non può essere scaricato o unito. Assicurati che ffmpeg sia disponibile.',
        'reset': 'Reset',
        'reset_settings': 'Reimposta Impostazioni',
        'reset_confirm_title': 'Conferma Reimpostazione',
        'reset_confirm_message': 'Sei sicuro di voler reimpostare tutte le impostazioni ai valori predefiniti? Questa operazione non può essere annullata.',
        'settings_reset_message': 'Le impostazioni sono state reimpostate ai valori predefiniti.',
    },
    'pt': {
        'title': 'Moaz Baixador de Vídeos',
        'url_label': 'URL do vídeo:',
        'output_dir_label': 'Pasta de download:',
        'browse': 'Procurar',
        'download': 'Baixar',
        'batch_download': 'Download em lote',
        'quality': 'Qualidade:',
        'format': 'Formato:',
        'custom_format': 'Formato personalizado:',
        'audio_only': 'Apenas áudio (MP3)',
        'playlist': 'Baixar playlist',
        'settings': 'Configurações',
        'help': 'Ajuda',
        'about': 'Sobre',
        'save': 'Salvar',
        'cancel': 'Cancelar',
        'language': 'Idioma:',
        'theme': 'Tema:',
        'light': 'Claro',
        'dark': 'Escuro',
        'cookie_file': 'Arquivo de cookie:',
        'validate': 'Validar',
        'cookie_valid': 'Arquivo de cookie validado com sucesso!',
        'cookie_invalid': 'Arquivo de cookie inválido ou vazio.',
        'drag_drop': 'Arraste e solte URLs aqui',
        'notification_success': 'Download concluído!',
        'notification_fail': 'Falha no download!',
        'invalid_url': 'URL inválido',
        'output_dir_missing': "A pasta de download não existe",
        'downloading': 'Baixando...',
        'done': 'Concluído!',
        'failed': 'Falhou.',
        'batch_urls': 'URLs em lote (um por linha):',
        'add_urls': 'Adicionar URLs',
        'parallel_downloads': 'Downloads paralelos:',
        'about_text': 'Baixador Universal de Vídeos\nDesenvolvido com Python & yt-dlp\nAutor: Seu nome',
        'help_text': 'Cole ou arraste URLs. Configure as opções. Clique em Baixar. Para lotes, um URL por linha.',
        'detect_formats': 'Detectar formatos',
        'log': 'Log:',
        'progress': 'Progresso:',
        'status': 'Status:',
        'proxy': 'Proxy:',
        'schedule': 'Agendar download',
        'schedule_time': 'Horário agendado (HH:MM):',
        'enable_notifications': 'Ativar notificações',
        'check_updates': 'Verificar atualizações do yt-dlp',
        'update_available': 'Atualização do yt-dlp disponível!',
        'up_to_date': 'yt-dlp está atualizado.',
        'export_settings': 'Exportar configurações',
        'import_settings': 'Importar configurações',
        'log_level': 'Nível de log:',
        'clear_log': 'Limpar log',
        'file_template': 'Modelo de nome de arquivo:',
        'pause': 'Pausar',
        'resume': 'Retomar',
        'scheduled_for': 'Agendado para',
        'now': 'Agora',
        'user_agent': 'Agente do usuário:',
        'bandwidth': 'Bandwidth limit (K/s):',
        'plugin_dir': 'Pasta de plugins:',
        'history': 'Histórico',
        'recent_downloads': 'Downloads recentes',
        'clear_history': 'Limpar histórico',
        'remove_recent_downloads': 'Remover downloads recentes',
        'skip_downloaded': 'Pular vídeos já baixados',
        'install_ytdlp': 'Instalar yt-dlp',
        'not_found': 'Não encontrado',
        'auto_detect_qualities_formats': 'Detectar automaticamente qualidades e formatos',
        'copy_log': 'Copiar Log',
        'export_log': 'Exportar Log',
        'open_log_file': 'Abrir arquivo de log',
        'ready': 'Pronto.',
        'detected_formats': 'Formatos detectados:',
        'no_formats_detected': 'Nenhum formato detectado.',
        'best': 'Melhor',
        'worst': 'Pior',
        'tooltip_quality': "Selecione a qualidade de vídeo desejada para o download. 'Melhor' irá baixar a maior qualidade disponível.",
        'tooltip_format': "Selecione o formato de arquivo desejado para o download. 'mp4' é recomendado para a maioria dos usuários.",
        'tooltip_download': "Inicie o download do vídeo a partir do URL acima.",
        'tooltip_cancel': "Cancelar o download atual.",
        'tooltip_log': "Esta área mostra os logs e o progresso do download.",
        'tooltip_progress': "Mostra o progresso do download.",
        'tooltip_recent': "Selecione um URL usado recentemente.",
        'dir_not_writable': 'Pasta de download não é writable.',
        'about_message': "I'm Moaz (pronounced Mu'adh), or Abulbara', a G12 student at STEM October. I'm into tech, problem-solving, and I enjoy building projects that make a real difference.",
        'ytdlp_installed': 'yt-dlp instalado com sucesso!',
        'ytdlp_install_failed': 'Falha ao instalar o yt-dlp.',
        'ffmpeg_missing': 'O ffmpeg está faltando! Os downloads de áudio não funcionarão. Coloque o ffmpeg.exe na pasta do aplicativo ou instale o ffmpeg e adicione-o ao seu PATH.',
        'merge_failed': 'A fusão falhou! O vídeo não pôde ser baixado ou mesclado. Certifique-se de que o ffmpeg esteja disponível.',
        'reset': 'Reset',
        'reset_settings': 'Redefinir Configurações',
        'reset_confirm_title': 'Confirmar Redefinição',
        'reset_confirm_message': 'Tem certeza de que deseja redefinir todas as configurações para os padrões? Isso não pode ser desfeito.',
        'settings_reset_message': 'As configurações foram redefinidas para os valores padrão.',
    },
    'ru': {
        'title': 'Муаз Загрузчик Видео',
        'url_label': 'Ссылка на видео:',
        'output_dir_label': 'Папка загрузки:',
        'browse': 'Обзор',
        'download': 'Скачать',
        'batch_download': 'Пакетная загрузка',
        'quality': 'Качество:',
        'format': 'Формат:',
        'custom_format': 'Пользовательский формат:',
        'audio_only': 'Только аудио (MP3)',
        'playlist': 'Скачать плейлист',
        'settings': 'Настройки',
        'help': 'Помощь',
        'about': 'О программе',
        'save': 'Сохранить',
        'cancel': 'Отмена',
        'language': 'Язык:',
        'theme': 'Тема:',
        'light': 'Светлая',
        'dark': 'Тёмная',
        'cookie_file': 'Файл cookie:',
        'validate': 'Проверить',
        'cookie_valid': 'Файл cookie успешно проверен!',
        'cookie_invalid': 'Файл cookie недействителен или пуст.',
        'drag_drop': 'Перетащите ссылки сюда',
        'notification_success': 'Загрузка завершена!',
        'notification_fail': 'Ошибка загрузки!',
        'invalid_url': 'Недействительная ссылка',
        'output_dir_missing': "Папка загрузки не существует",
        'downloading': 'Загрузка...',
        'done': 'Готово!',
        'failed': 'Ошибка.',
        'batch_urls': 'Пакет ссылок (по одной в строке):',
        'add_urls': 'Добавить ссылки',
        'parallel_downloads': 'Параллельные загрузки:',
        'about_text': 'Универсальный загрузчик видео\nРазработан на Python & yt-dlp\nАвтор: Ваше имя',
        'help_text': 'Вставьте или перетащите ссылки. Настройте параметры. Нажмите Скачать. Для пакета — одна ссылка в строке.',
        'detect_formats': 'Определить форматы',
        'log': 'Журнал:',
        'progress': 'Прогресс:',
        'status': 'Статус:',
        'proxy': 'Прокси:',
        'schedule': 'Запланировать загрузку',
        'schedule_time': 'Время (ЧЧ:ММ):',
        'enable_notifications': 'Включить уведомления',
        'check_updates': 'Проверить обновления yt-dlp',
        'update_available': 'Доступно обновление yt-dlp!',
        'up_to_date': 'yt-dlp обновлен.',
        'export_settings': 'Экспорт настроек',
        'import_settings': 'Импорт настроек',
        'log_level': 'Уровень журнала:',
        'clear_log': 'Очистить журнал',
        'file_template': 'Шаблон имени файла:',
        'pause': 'Пауза',
        'resume': 'Продолжить',
        'scheduled_for': 'Запланировано на',
        'now': 'Сейчас',
        'user_agent': 'Пользовательский агент:',
        'bandwidth': 'Ограничение скорости (K/s):',
        'plugin_dir': 'Папка плагинов:',
        'history': 'История',
        'recent_downloads': 'Недавние загрузки',
        'clear_history': 'Очистить историю',
        'remove_recent_downloads': 'Удалить недавние загрузки',
        'skip_downloaded': 'Пропускать уже загруженные видео',
        'install_ytdlp': 'Установить yt-dlp',
        'not_found': 'Не найдено',
        'auto_detect_qualities_formats': 'Автоматически определить качество и формат',
        'copy_log': 'Копировать журнал',
        'export_log': 'Экспортировать журнал',
        'open_log_file': 'Открыть файл журнала',
        'ready': 'Готово.',
        'detected_formats': 'Обнаруженные форматы:',
        'no_formats_detected': 'Форматы не обнаружены.',
        'best': 'Лучший',
        'worst': 'Наименее качественный',
        'tooltip_quality': "Выберите желаемое качество видео для загрузки. 'Лучший' скачает наилучшее доступное качество.",
        'tooltip_format': "Выберите желаемый формат файла для загрузки. 'mp4' рекомендуется для большинства пользователей.",
        'tooltip_download': "Начать загрузку видео по указанной выше ссылке.",
        'tooltip_cancel': "Отменить текущую загрузку.",
        'tooltip_log': "Эта область отображает журнал и ход загрузки.",
        'tooltip_progress': "Показывает ход загрузки.",
        'tooltip_recent': "Выберите недавно использованный URL.",
        'dir_not_writable': 'Папка загрузки не writable.',
        'about_message': "I'm Moaz (pronounced Mu'adh), or Abulbara', a G12 student at STEM October. I'm into tech, problem-solving, and I enjoy building projects that make a real difference.",
        'ytdlp_installed': 'yt-dlp установлен!',
        'ytdlp_install_failed': 'Не удалось установить yt-dlp.',
        'ffmpeg_missing': 'ffmpeg отсутствует! Загрузка аудио не будет работать. Пожалуйста, поместите ffmpeg.exe в папку приложения или установите ffmpeg и добавьте его в системный PATH.',
        'merge_failed': 'Слияние не удалось! Не удалось загрузить или объединить видео. Убедитесь, что ffmpeg доступен.',
        'reset': 'Reset',
        'reset_settings': 'Сбросить настройки',
        'reset_confirm_title': 'Подтвердите сброс',
        'reset_confirm_message': 'Вы уверены, что хотите сбросить все настройки до значений по умолчанию? Это действие нельзя отменить.',
        'settings_reset_message': 'Настройки были сброшены до значений по умолчанию.',
    },
    'zh': {
        'title': '莫阿兹视频下载器',
        'url_label': '视频链接：',
        'output_dir_label': '下载文件夹：',
        'browse': '浏览',
        'download': '下载',
        'batch_download': '批量下载',
        'quality': '质量：',
        'format': '格式：',
        'custom_format': '自定义格式：',
        'audio_only': '仅音频 (MP3)',
        'playlist': '下载播放列表',
        'settings': '设置',
        'help': '帮助',
        'about': '关于',
        'save': '保存',
        'cancel': '取消',
        'language': '语言：',
        'theme': '主题：',
        'light': '浅色',
        'dark': '深色',
        'cookie_file': 'Cookie 文件：',
        'validate': '验证',
        'cookie_valid': 'Cookie 文件验证成功！',
        'cookie_invalid': 'Cookie 文件无效或为空。',
        'drag_drop': '拖放链接到此处',
        'notification_success': '下载完成！',
        'notification_fail': '下载失败！',
        'invalid_url': '无效链接',
        'output_dir_missing': "下载文件夹不存在",
        'downloading': '正在下载...',
        'done': '完成！',
        'failed': '失败。',
        'batch_urls': '批量链接（每行一个）：',
        'add_urls': '添加链接',
        'parallel_downloads': '并行下载：',
        'about_text': '通用视频下载器\n基于 Python & yt-dlp\n作者：你的名字',
        'help_text': '粘贴或拖动链接。配置选项。点击下载。批量时每行一个链接。',
        'detect_formats': '检测格式',
        'log': '日志：',
        'progress': '进度：',
        'status': '状态：',
        'proxy': '代理：',
        'schedule': '计划下载',
        'schedule_time': '计划时间（HH:MM）：',
        'enable_notifications': '启用通知',
        'check_updates': '检查 yt-dlp 更新',
        'update_available': 'yt-dlp 有可用更新！',
        'up_to_date': 'yt-dlp 已是最新。',
        'export_settings': '导出设置',
        'import_settings': '导入设置',
        'log_level': '日志级别：',
        'clear_log': '清除日志',
        'file_template': '文件名模板：',
        'pause': '暂停',
        'resume': '继续',
        'scheduled_for': '计划于',
        'now': '现在',
        'user_agent': '用户代理:',
        'bandwidth': '带宽限制 (K/s)：',
        'plugin_dir': '插件文件夹：',
        'history': '历史',
        'recent_downloads': '最近下载',
        'clear_history': '清除历史记录',
        'remove_recent_downloads': '移除最近下载',
        'skip_downloaded': '跳过已下载的视频',
        'install_ytdlp': '安装 yt-dlp',
        'not_found': '未找到',
        'auto_detect_qualities_formats': '自动检测质量和格式',
        'copy_log': '复制日志',
        'export_log': '导出日志',
        'open_log_file': '打开日志文件',
        'ready': '准备就绪.',
        'detected_formats': '检测到的格式:',
        'no_formats_detected': '未检测到格式.',
        'best': '最佳',
        'worst': '最差',
        'tooltip_quality': "选择所需的视频质量进行下载。'最佳'将下载可用的最高质量。",
        'tooltip_format': "选择所需的文件格式进行下载。'mp4'推荐给大多数用户。",
        'tooltip_download': "从上面的链接开始下载视频。",
        'tooltip_cancel': "取消当前下载。",
        'tooltip_log': "此区域显示日志和下载进度。",
        'tooltip_progress': "显示下载进度。",
        'tooltip_recent': "选择最近使用的链接。",
        'dir_not_writable': "下载文件夹不存在",
        'about_message': "I'm Moaz (pronounced Mu'adh), or Abulbara', a G12 student at STEM October. I'm into tech, problem-solving, and I enjoy building projects that make a real difference.",
        'ytdlp_installed': 'yt-dlp 已安装！',
         'ytdlp_install_failed': '安装 yt-dlp 失败。',
        'ffmpeg_missing': '缺少 ffmpeg！音频下载将无法工作。请将 ffmpeg.exe 放置在应用程序文件夹中，或安装 ffmpeg 并将其添加到您的 PATH。',
        'merge_failed': '合并失败！视频无法下载或合并。请确保 ffmpeg 可用。',
        'reset': 'Reset',
        'reset_settings': '重置设置',
        'reset_confirm_title': '确认重置',
        'reset_confirm_message': '您确定要将所有设置重置为默认值吗？此操作无法撤销。',
        'settings_reset_message': '设置已重置为默认值。',
    },
    'ja': {
        'title': 'モアズ動画ダウンローダー',
        'url_label': '動画URL：',
        'output_dir_label': 'ダウンロードフォルダ：',
        'browse': '参照',
        'download': 'ダウンロード',
        'batch_download': '一括ダウンロード',
        'quality': '品質：',
        'format': '形式：',
        'custom_format': 'カスタム形式：',
        'audio_only': '音声のみ (MP3)',
        'playlist': 'プレイリストをダウンロード',
        'settings': '設定',
        'help': 'ヘルプ',
        'about': '情報',
        'save': '保存',
        'cancel': 'キャンセル',
        'language': '言語：',
        'theme': 'テーマ：',
        'light': 'ライト',
        'dark': 'ダーク',
        'cookie_file': 'Cookieファイル：',
        'validate': '検証',
        'cookie_valid': 'Cookieファイルが正常に検証されました！',
        'cookie_invalid': 'Cookieファイルが無効または空です。',
        'drag_drop': 'ここにURLをドラッグ＆ドロップ',
        'notification_success': 'ダウンロード完了！',
        'notification_fail': 'ダウンロード失敗！',
        'invalid_url': '無効なURL',
        'output_dir_missing': "ダウンロードフォルダが存在しません",
        'downloading': 'ダウンロード中...',
        'done': '完了！',
        'failed': '失敗。',
        'batch_urls': '一括URL（1行に1つ）：',
        'add_urls': 'URLを追加',
        'parallel_downloads': '並列ダウンロード：',
        'about_text': 'ユニバーサル動画ダウンローダー\nPython & yt-dlpで作成\n作者：あなたの名前',
        'help_text': 'URLを貼り付けるかドラッグ。オプションを設定。ダウンロードをクリック。一括は1行に1つ。',
        'detect_formats': '形式を検出',
        'log': 'ログ：',
        'progress': '進捗：',
        'status': 'ステータス：',
        'proxy': 'プロキシ：',
        'schedule': 'ダウンロードをスケジュール',
        'schedule_time': 'スケジュール時刻（HH:MM）：',
        'enable_notifications': '通知を有効にする',
        'check_updates': 'yt-dlpの更新を確認',
        'update_available': 'yt-dlpの更新があります！',
        'up_to_date': 'yt-dlpは最新です。',
        'export_settings': '設定をエクスポート',
        'import_settings': '設定をインポート',
        'log_level': 'ログレベル：',
        'clear_log': 'ログをクリア',
        'file_template': 'ファイル名テンプレート：',
        'pause': '一時停止',
        'resume': '再開',
        'scheduled_for': 'スケジュール：',
        'now': '今',
        'user_agent': 'User-Agent:',
        'bandwidth': '帯域制限 (K/s)：',
        'plugin_dir': 'プラグインフォルダ：',
        'history': '履歴',
        'recent_downloads': '最近のダウンロード',
        'clear_history': '履歴をクリア',
        'remove_recent_downloads': '最近のダウンロードを削除',
        'skip_downloaded': '既にダウンロードした動画をスキップ',
        'install_ytdlp': 'yt-dlpをインストール',
        'not_found': '見つかりません',
        'auto_detect_qualities_formats': '自動的に品質と形式を検出',
        'copy_log': 'ログをコピー',
        'export_log': 'ログをエクスポート',
        'open_log_file': 'ログファイルを開く',
        'ready': '準備完了.',
        'detected_formats': '検出された形式:',
        'no_formats_detected': '形式が検出されません.',
        'best': '最高',
        'worst': '最低',
        'tooltip_quality': "ダウンロードする動画の品質を選択します。「最高」は利用可能な最高品質をダウンロードします。",
        'tooltip_format': "ダウンロードするファイル形式を選択します。「mp4」はほとんどのユーザーに推奨されます。",
        'tooltip_download': "上記のURLから動画のダウンロードを開始します。",
        'tooltip_cancel': "現在のダウンロードをキャンセルします。",
        'tooltip_log': "このエリアにはログとダウンロードの進捗が表示されます。",
        'tooltip_progress': "ダウンロードの進捗を表示します。",
        'tooltip_recent': "最近使用したURLを選択します。",
        'dir_not_writable': 'ダウンロードフォルダが存在しません',
        'about_message': "I'm Moaz (pronounced Mu'adh), or Abulbara', a G12 student at STEM October. I'm into tech, problem-solving, and I enjoy building projects that make a real difference.",
        'ytdlp_installed': 'yt-dlpが正常にインストールされました！',
        'ytdlp_install_failed': 'yt-dlp のインストールに失敗しました。',
        'ffmpeg_missing': 'ffmpegが見つかりません！音声のダウンロードは機能しません。ffmpeg.exeをアプリのフォルダに配置するか、ffmpegをインストールしてPATHに追加してください。',
        'merge_failed': 'マージに失敗しました！動画をダウンロードまたはマージできませんでした。ffmpegが利用可能であることを確認してください。',        'reset': 'Reset',
        'reset_settings': '設定をリセット',
        'reset_confirm_title': 'リセットの確認',
        'reset_confirm_message': '本当にすべての設定をデフォルト値にリセットしますか？この操作は元に戻せません。',
        'settings_reset_message': '設定がデフォルト値にリセットされました。',
    },
}

# --- Utils ---
def is_valid_url(url: str) -> bool:
    """Basic URL validation."""
    url_pattern = re.compile(
        r'^https?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url_pattern.match(url) is not None

# --- Settings Management ---
class Settings:
    """Handles loading and saving user settings."""
    def __init__(self, path: Optional[Path] = None):
        self.path = path or Path.home() / ".video_downloader_settings.json"
        self.data: Dict[str, Any] = {
            "language": "en",
            "theme": "light",
            "output_dir": str(Path.home() / "Downloads"),
            "parallel": 2,
            "postprocess_script": "",
            "format": "mp4",
            "custom_format": "",
            "cookie_file": "",
            "recent_urls": [],
            "recent_batch_files": [],
            "playlist": False,
            "proxy": "",
            "enable_notifications": True,
            "log_level": "INFO",
            "file_template": "%(uploader)s - %(id)s.%(ext)s",
            "user_agent": "",
            "bandwidth": "",
            "plugin_dir": "",
            "download_history": [],
            "skip_downloaded": True,
        }
        self.load()

    def load(self):
        if self.path.exists():
            try:
                import json
                with open(self.path, 'r') as f:
                    self.data.update(json.load(f))
            except Exception as e:
                print(f"Failed to load settings: {e}")

    def save(self):
        try:
            import json
            with open(self.path, 'w') as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            print(f"Failed to save settings: {e}")

    def add_recent_url(self, url: str):
        if url and url not in self.data['recent_urls']:
            self.data['recent_urls'] = ([url] + self.data['recent_urls'])[:10]
            self.save()

    def add_recent_batch_file(self, path: str):
        if path and path not in self.data['recent_batch_files']:
            self.data['recent_batch_files'] = ([path] + self.data['recent_batch_files'])[:5]
            self.save()

    def add_history(self, entry: dict):
        self.data['download_history'] = ([entry] + self.data['download_history'])[:100]
        self.save()

    def export_settings(self, export_path: str):
        import json
        with open(export_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2)

    def import_settings(self, import_path: str):
        import json
        with open(import_path, 'r', encoding='utf-8') as f:
            self.data.update(json.load(f))
        self.save()

# --- Downloader Core ---
class VideoDownloader:
    """Handles the actual download logic, including post-processing plugin support."""
    def __init__(self, logger: Optional[logging.Logger] = None, postprocess_script: Optional[str] = None, proxy: Optional[str] = None, user_agent: Optional[str] = None, bandwidth: Optional[str] = None, plugin_dir: Optional[str] = None):
        self.logger = logger or logging.getLogger(__name__)
        self.postprocess_script = postprocess_script
        self.proxy = proxy
        self.user_agent = user_agent
        self.bandwidth = bandwidth
        self.plugin_dir = plugin_dir
        self.CREATE_NO_WINDOW = subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
        
        # Try to find or install yt-dlp
        try:
            self.ytdlp_cmd = self.find_ytdlp()
        except FileNotFoundError:
            # If find_ytdlp fails, try one more time with explicit installation
            if not self.install_ytdlp():
                raise FileNotFoundError("Failed to install yt-dlp. Please install it manually using: pip install yt-dlp")

    def find_ytdlp(self) -> List[str]:
        """Find yt-dlp command or install it if not found."""
        candidates = [
            ["yt-dlp"],
            [sys.executable, "-m", "yt_dlp"],
            ["python", "-m", "yt_dlp"],
            ["py", "-m", "yt_dlp"]
        ]
        for cmd in candidates:
            try:
                subprocess.run(cmd + ["--version"], capture_output=True, check=True, creationflags=self.CREATE_NO_WINDOW)
                return cmd
            except Exception:
                continue
        
        # If yt-dlp is not found, try to install it
        try:
            self.logger.info("yt-dlp not found. Attempting to install...")
            subprocess.run([sys.executable, "-m", "pip", "install", "--user", "yt-dlp"], 
                         capture_output=True, check=True, creationflags=self.CREATE_NO_WINDOW)
            self.logger.info("yt-dlp installed successfully!")
            
            # Try to find yt-dlp again after installation
            for cmd in candidates:
                try:
                    subprocess.run(cmd + ["--version"], capture_output=True, check=True, creationflags=self.CREATE_NO_WINDOW)
                    return cmd
                except Exception:
                    continue
        except Exception as e:
            self.logger.error(f"Failed to install yt-dlp: {e}")
            
        raise FileNotFoundError("yt-dlp not found and automatic installation failed. Please install it manually using: pip install yt-dlp")

    def install_ytdlp(self) -> bool:
        """Install yt-dlp using pip."""
        try:
            # Try to install with --user flag first
            result = subprocess.run([sys.executable, "-m", "pip", "install", "--user", "yt-dlp"], 
                                 capture_output=True, text=True, creationflags=self.CREATE_NO_WINDOW)
            
            if result.returncode != 0:
                # If --user installation fails, try without it
                result = subprocess.run([sys.executable, "-m", "pip", "install", "yt-dlp"], 
                                     capture_output=True, text=True, creationflags=self.CREATE_NO_WINDOW)
            
            if result.returncode == 0:
                self.logger.info("✓ yt-dlp installed successfully")
                # Update the command after successful installation
                self.ytdlp_cmd = [sys.executable, "-m", "yt_dlp"]
                try:
                    subprocess.run(self.ytdlp_cmd + ["--version"], 
                                 capture_output=True, check=True, creationflags=self.CREATE_NO_WINDOW)
                    self.logger.info("✓ yt-dlp verified and ready to use")
                    return True
                except Exception as e:
                    self.logger.error(f"⚠ yt-dlp installed but verification failed: {e}")
            else:
                self.logger.error(f"⚠ Failed to install yt-dlp: {result.stderr}")
        except Exception as e:
            self.logger.error(f"⚠ Error during yt-dlp installation: {e}")
        return False

    def set_postprocess_script(self, script_path: Optional[str]):
        self.postprocess_script = script_path

    def run_postprocess(self, filepath: str):
        """Run the post-processing script on the downloaded file."""
        if self.postprocess_script and os.path.exists(self.postprocess_script):
            try:
                result = subprocess.run([sys.executable, self.postprocess_script, filepath], 
                                     capture_output=True, text=True, creationflags=self.CREATE_NO_WINDOW)
                self.logger.info(f"Post-process output: {result.stdout.strip()}")
                if result.returncode == 0:
                    return True, result.stdout.strip()
                else:
                    return False, result.stderr.strip()
            except Exception as e:
                self.logger.error(f"Post-process error: {e}")
                return False, str(e)
        return True, "No post-process script set."

    def set_proxy(self, proxy: Optional[str]):
        self.proxy = proxy

    def set_user_agent(self, ua: Optional[str]):
        self.user_agent = ua

    def set_bandwidth(self, bw: Optional[str]):
        self.bandwidth = bw

    def set_plugin_dir(self, path: Optional[str]):
        self.plugin_dir = path

    def run_plugin_dir(self, filepath: str):
        if self.plugin_dir and os.path.isdir(self.plugin_dir):
            for fname in os.listdir(self.plugin_dir):
                if fname.endswith('.py'):
                    try:
                        subprocess.run([sys.executable, os.path.join(self.plugin_dir, fname), filepath], 
                                    capture_output=True, text=True, creationflags=self.CREATE_NO_WINDOW)
                    except Exception as e:
                        self.logger.error(f"Plugin error: {e}")

    def check_for_updates(self) -> bool:
        import requests
        try:
            resp = requests.get('https://pypi.org/pypi/yt-dlp/json', timeout=5)
            latest = resp.json()['info']['version']
            result = subprocess.run(self.ytdlp_cmd + ['--version'], capture_output=True, text=True, 
                                 creationflags=self.CREATE_NO_WINDOW)
            current = result.stdout.strip().splitlines()[0]
            return latest != current
        except Exception:
            return False

    def download(self, url: str, output_dir: str, quality: str = "best", audio_only: bool = False, playlist: bool = False, cookie_file: Optional[str] = None, progress_callback: Optional[Callable[[str], None]] = None, proxy: Optional[str] = None, file_template: Optional[str] = None, user_agent: Optional[str] = None, bandwidth: Optional[str] = None, plugin_dir: Optional[str] = None, download_archive: Optional[str] = None) -> Tuple[bool, Optional[str]]:
        """Download a single video and run post-processing if set. Now works without ffmpeg for video-only downloads."""
        last_file = None
        try:
            # Create output directory if it doesn't exist
            os.makedirs(output_dir, exist_ok=True)
            # Always resolve output_path to an absolute path
            output_template = file_template or "%(uploader)s - %(id)s.%(ext)s"
            output_path = os.path.abspath(os.path.join(output_dir, output_template))
            if progress_callback:
                progress_callback(f"[DEBUG] Using output path: {output_path}")
            cmd = self.ytdlp_cmd + [
                url,
                "-o", output_path,
                "--ignore-errors",
                "--retries", "3",
                "--newline"
            ]
            
            if FFMPEG_PATH:
                cmd.extend(["--ffmpeg-location", FFMPEG_PATH])
            
            if proxy or self.proxy:
                cmd.extend(["--proxy", proxy or self.proxy])
            if user_agent or self.user_agent:
                cmd.extend(["--user-agent", user_agent or self.user_agent])
            if bandwidth or self.bandwidth:
                cmd.extend(["--limit-rate", f"{bandwidth or self.bandwidth}K"])
            if not playlist:
                cmd.append("--no-playlist")
            # Check for ffmpeg availability
            ffmpeg_available = FFMPEG_PATH is not None
            if audio_only:
                cmd.extend(["--extract-audio", "--audio-format", "mp3", "--audio-quality", "192K"])
            else:
                if ffmpeg_available:
                    if quality == "worst":
                        cmd.extend(["-f", "worst"])
                    elif quality != "best":
                        height = quality.replace('p', '')
                        cmd.extend(["-f", f"bestvideo[height<={height}]+bestaudio/best[height<={height}]"])
                    else:
                        cmd.extend(["-f", "best"])
                else:
                    # If ffmpeg is missing, force yt-dlp to only download single-file formats (no merging)
                    if quality == "worst":
                        cmd.extend(["-f", "worst[acodec!=none][vcodec!=none]/worst"])
                    elif quality != "best":
                        height = quality.replace('p', '')
                        # Only select formats that have both audio and video (progressive)
                        cmd.extend(["-f", f"best[height<={height}][acodec!=none][vcodec!=none]/best[height<={height}]"])
                    else:
                        # Default: best progressive
                        cmd.extend(["-f", "best[acodec!=none][vcodec!=none]/best"])
            if cookie_file and os.path.exists(cookie_file):
                cmd.extend(["--cookies", cookie_file])
            if download_archive and os.path.exists(download_archive):
                cmd.extend(["--download-archive", download_archive])
                
            # Log the yt-dlp command for debugging
            if progress_callback:
                progress_callback(f"yt-dlp command: {' '.join(cmd)}")
            process = subprocess.Popen(
                cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT,
                universal_newlines=True, 
                creationflags=self.CREATE_NO_WINDOW,
                bufsize=1
            )
            
            while True:
                line = process.stdout.readline()
                if not line and process.poll() is not None:
                    break
                    
                line = line.strip()
                if line:
                    if progress_callback:
                        if not progress_callback(line):
                            # Cancel was requested
                            process.terminate()
                            try:
                                process.wait(timeout=5)
                            except subprocess.TimeoutExpired:
                                process.kill()
                            return False, last_file
                            
                    # Track downloaded file
                    # We parse the output to find the final filename, which might be different
                    # from the initial destination if merging or audio extraction occurs.
                    if '[download] Destination:' in line:
                        last_file = line.split('Destination: ', 1)[1]
                    elif '[Merger] Merging formats into "' in line:
                        last_file = line.split('[Merger] Merging formats into "', 1)[1].rstrip('"')
                    elif '[ExtractAudio] Destination:' in line:
                        last_file = line.split('[ExtractAudio] Destination: ', 1)[1]
                    elif 'has already been downloaded' in line:
                        last_file = line.split('[download] ', 1)[1].split(' has already')[0]
                        
            # Use process return code for success
            success = (process.returncode == 0)
            if not success and progress_callback:
                # Check for merge/ffmpeg error in output
                if not ffmpeg_available:
                    progress_callback("[ERROR] No single-file format available for this video/quality. Try a lower quality or install ffmpeg.")
                else:
                    progress_callback(f"Process failed with return code {process.returncode}")
            
            # Run post-processing if successful
            if success and last_file and os.path.exists(last_file):
                if self.postprocess_script:
                    self.run_postprocess(last_file)
                if self.plugin_dir:
                    self.run_plugin_dir(last_file)
                    
            return success, last_file
        
        except subprocess.SubprocessError as e:
            if progress_callback:
                progress_callback(f"Download process error: {str(e)}")
            return False, last_file
        except OSError as e:
            if progress_callback:
                progress_callback(f"File system error: {str(e)}")
            return False, last_file
        except Exception as e:
            if progress_callback:
                progress_callback(f"Unexpected error: {str(e)}")
            return False, last_file

    def batch_download(self, urls: List[str], output_dir: str, quality: str, audio_only: bool, playlist: bool, cookie_file: Optional[str], parallel: int, progress_callback: Optional[Callable[[str], None]] = None) -> Dict[str, bool]:
        """Download multiple videos in parallel."""
        try:
            # Create output directory if it doesn't exist
            os.makedirs(output_dir, exist_ok=True)
            
            results = {}
            total = len(urls)
            completed = 0
            
            def update_progress():
                if progress_callback:
                    progress = (completed / total) * 100 if total > 0 else 0
                    progress_callback(f"Overall Progress: {progress:.1f}% ({completed}/{total})")
            
            def download_single(url: str) -> bool:
                nonlocal completed
                try:
                    if progress_callback:
                        progress_callback(f"Starting download: {url}")
                        
                    success, final_filepath = self.download(
                        url=url,
                        output_dir=output_dir,
                        quality=quality,
                        audio_only=audio_only,
                        playlist=playlist,
                        cookie_file=cookie_file,
                        progress_callback=lambda msg: progress_callback(f"[{url}] {msg}") if progress_callback else None,
                    )
                    
                    completed += 1
                    update_progress()
                    return success, final_filepath
                    
                except Exception as e:
                    if progress_callback:
                        progress_callback(f"Error downloading {url}: {str(e)}")
                    completed += 1
                    update_progress()
                    return False, None
            
            # Use ThreadPoolExecutor for parallel downloads
            with ThreadPoolExecutor(max_workers=min(parallel, 8)) as executor:
                future_to_url = {executor.submit(download_single, url): url for url in urls}
                for future in as_completed(future_to_url):
                    url = future_to_url[future]
                    try:
                        success, final_filepath = future.result()
                        results[url] = success
                    except Exception as e:
                        if progress_callback:
                            progress_callback(f"Failed to process {url}: {str(e)}")
                        results[url] = False
            
            # Final status
            success_count = sum(1 for success in results.values() if success)
            if progress_callback:
                progress_callback(f"Batch download completed: {success_count}/{total} successful")
            
            return results
            
        except Exception as e:
            if progress_callback:
                progress_callback(f"Batch download error: {str(e)}")
            return {url: False for url in urls}

    def detect_formats(self, url: str) -> List[str]:
        """Detect available formats for a given URL using yt-dlp."""
        if not url or not is_valid_url(url):
            return []
        try:
            cmd = self.ytdlp_cmd + [url, "--list-formats", "--no-download"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            formats = []
            if result.returncode == 0:
                for line in result.stdout.splitlines():
                    if line.strip() and not line.startswith('[') and '|' in line:
                        parts = line.split()
                        if len(parts) > 0 and parts[0] not in ['format', 'code']:
                            format_id = parts[0]
                            if format_id.isdigit() or '+' in format_id:
                                formats.append(format_id)
            return formats[:20]
        except Exception:
            return []

    def validate_cookie_file(self, path: str) -> bool:
        if not os.path.exists(path):
            return False
        try:
            with open(path, 'r') as f:
                content = f.read().strip()
                if not content:
                    return False
                lines = content.split('\n')
                valid_lines = 0
                for line in lines:
                    if line.strip() and not line.startswith('#'):
                        parts = line.split('\t')
                        if len(parts) >= 6:
                            valid_lines += 1
                return valid_lines > 0
        except Exception:
            return False

    def check_dependencies(self) -> Dict[str, str]:
        """Check yt-dlp and ffmpeg availability. Returns dict with status."""
        status = {"yt-dlp": "Not found", "ffmpeg": "Not found"}
        # yt-dlp
        try:
            subprocess.run(["yt-dlp", "--version"], capture_output=True, check=True, creationflags=self.CREATE_NO_WINDOW)
            status["yt-dlp"] = "Installed"
        except Exception:
            try:
                subprocess.run([sys.executable, "-m", "yt_dlp", "--version"], capture_output=True, check=True, creationflags=self.CREATE_NO_WINDOW)
                status["yt-dlp"] = "Installed"
            except Exception:
                status["yt-dlp"] = "Not found"
        
        # ffmpeg
        if FFMPEG_PATH:
            try:
                subprocess.run([FFMPEG_PATH, "-version"], capture_output=True, check=True, creationflags=self.CREATE_NO_WINDOW)
                status["ffmpeg"] = "Installed"
            except Exception:
                status["ffmpeg"] = "Found but seems broken"
        else:
            status["ffmpeg"] = "Not found"
            
        return status

# --- GUI ---
class DownloaderGUI:
    """Tkinter-based GUI for the downloader, with post-processing plugin support."""
    def __init__(self, settings: Settings, downloader: VideoDownloader):
        self.settings = settings
        self.downloader = downloader
        self.language = self.settings.data.get('language', 'en')
        if HAS_THEMES:
            self.root = ThemedTk(theme="arc")
        else:
            self.root = tk.Tk()
        self.root.title('Moaz Video Downloader')
        self.root.geometry('800x600')
        self.root.minsize(700, 500)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.url_var = tk.StringVar()
        self.output_dir_var = tk.StringVar(value=str(Path.home() / "Downloads"))
        os.makedirs(self.output_dir_var.get(), exist_ok=True)
        # self.quality_var = tk.StringVar(value="best")
        self.single_quality_var = tk.StringVar(value="best")
        self.batch_quality_var = tk.StringVar(value="best")
        self.audio_only_var = tk.BooleanVar()
        self.playlist_var = tk.BooleanVar()
        self.progress_text = tk.StringVar(value="Ready.")
        self.progress_percent = tk.StringVar(value="0%")
        self.batch_urls_var = tk.StringVar()
        self.parallel_var = tk.IntVar(value=self.settings.data.get('parallel', 2))
        self.postprocess_script_var = tk.StringVar(value=self.settings.data.get('postprocess_script', ''))
        self.theme = self.settings.data.get('theme', 'light')
        self.theme_var = tk.StringVar(value=self.theme)
        self.format_var = tk.StringVar(value=self.settings.data.get('format', 'mp4'))
        self.custom_format_var = tk.StringVar(value=self.settings.data.get('custom_format', ''))
        self.cookie_file_var = tk.StringVar(value=self.settings.data.get('cookie_file', ''))
        self.proxy_var = tk.StringVar(value=self.settings.data.get('proxy', ''))
        self.enable_notifications_var = tk.BooleanVar(value=self.settings.data.get('enable_notifications', True))
        self.log_level_var = tk.StringVar(value=self.settings.data.get('log_level', 'INFO'))
        self.file_template_var = tk.StringVar(value=self.settings.data.get('file_template', '%(uploader)s - %(id)s.%(ext)s'))
        self.scheduled_time_var = tk.StringVar(value="")
        self.log_lines = []
        self.recent_urls = self.settings.data.get('recent_urls', [])
        self.recent_batch_files = self.settings.data.get('recent_batch_files', [])
        self.download_threads = []
        self.protocol_set = False
        self.user_agent_var = tk.StringVar(value=self.settings.data.get('user_agent', ''))
        self.bandwidth_var = tk.StringVar(value=self.settings.data.get('bandwidth', ''))
        self.plugin_dir_var = tk.StringVar(value=self.settings.data.get('plugin_dir', ''))
        self.cancel_requested = False
        self.status_message = tk.StringVar(value="Welcome to Moaz Downloader!")
        self.language_var = tk.StringVar(value=self.language)

        # Theme name mapping
        self.theme = self.settings.data.get('theme', 'light')
        self.theme_value_map = {self.t('light'): 'light', self.t('dark'): 'dark'}
        self.theme_display_map = {v: k for k, v in self.theme_value_map.items()}
        display_theme = self.theme_display_map.get(self.theme, self.theme)
        self.theme_var.set(display_theme)

        # Language mapping definitions (moved from setup_settings_tab)
        self.language_short_names = ['En', 'Es', 'Fr', 'De', 'It', 'Pt', 'Ru', 'Zh', 'Ja', 'Ar']
        self.language_short_to_code = dict(zip(self.language_short_names, [
            'en', 'es', 'fr', 'de', 'it', 'pt', 'ru', 'zh', 'ja', 'ar'
        ]))
        self.language_code_to_short = {v: k for k, v in self.language_short_to_code.items()}
        self.language_code_map = {
            'Moaz Video Downloader': 'en',
            'Moaz Descargador de Videos': 'es',
            'Moaz Téléchargeur de Vidéos': 'fr',
            'Moaz Video-Downloader': 'de',
            'Moaz Downloader di Video': 'it',
            'Moaz Baixador de Vídeos': 'pt',
            'Муаз Загрузчик Видео': 'ru',
            '莫阿兹视频下载器': 'zh',
            'モアズ動画ダウンローダー': 'ja',
            'معاذ لتحميل الفيديو': 'ar'
        }
        self.language_display_map = {v: k for k, v in self.language_code_map.items()}
        self.quality_value_map = {
            self.t('best'): 'best',
            self.t('worst'): 'worst',
            '1080p': '1080p',
            '720p': '720p',
            '480p': '480p',
            '360p': '360p',
            '240p': '240p',
        }
        self.quality_display_map = {v: k for k, v in self.quality_value_map.items()}
        self.setup_ui()
        self.language_var.set(self.language_code_to_short.get(self.language, 'En'))
        self.apply_theme()
        self.check_dependencies()
        self.set_protocol()
        try:
            self.root.iconbitmap(ICON_PATH)
        except tk.TclError:
            print("Note: .ico files are only supported on Windows.")
        self.root.title(f"{APP_NAME} v{APP_VERSION}")
        if FFMPEG_PATH is None:
            from tkinter import messagebox
            messagebox.showerror(self.t('error'), self.t('ffmpeg_missing'))

    def t(self, key: str) -> str:
        return LANGUAGES.get(self.language, LANGUAGES['en']).get(key, key)

    def setup_ui(self):
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.main_frame = ttk.Frame(self.root, padding=15)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.nb = ttk.Notebook(self.main_frame)
        self.nb.grid(row=0, column=0, sticky="nsew")
        # --- Single Download Tab ---
        self.download_group = ttk.LabelFrame(self.nb, text=self.t('download'), padding=0)
        self.nb.add(self.download_group, text=self.t('download'))
        # Add a solid background frame for dark mode
        self.download_bg_frame = tk.Frame(self.download_group, bd=0, highlightthickness=0)
        self.download_bg_frame.pack(fill=tk.BOTH, expand=True)
        self.download_bg_frame.pack_propagate(0)
        self.download_bg_frame.grid_columnconfigure(1, weight=1)
        self.url_label = ttk.Label(self.download_bg_frame, text=self.t('url_label'))
        self.url_label.grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
        self.url_entry = ttk.Entry(self.download_bg_frame, textvariable=self.url_var, width=60)
        self.url_entry.grid(row=0, column=1, sticky=tk.EW, pady=5, padx=5)
        self.detect_formats_btn = ttk.Button(self.download_bg_frame, text=self.t('detect_formats'), command=self.detect_formats)
        self.detect_formats_btn.grid(row=0, column=2, padx=5)
        self.recent_combo = ttk.Combobox(self.download_bg_frame, values=self.recent_urls, postcommand=self.update_recent_urls)
        self.recent_combo.grid(row=0, column=3, sticky=tk.W, padx=5)
        self.recent_combo.bind('<<ComboboxSelected>>', self.select_recent_url)
        # --- Make quality selection more prominent ---
        self.quality_label = ttk.Label(self.download_bg_frame, text=self.t('quality'))
        self.quality_label.grid(row=1, column=0, sticky=tk.W, pady=5, padx=5)
        self.quality_combo = ttk.Combobox(self.download_bg_frame, textvariable=self.single_quality_var, values=list(self.quality_value_map.keys()), width=15, state="readonly")
        self.quality_combo.grid(row=1, column=1, sticky=tk.W, pady=5, padx=5)
        ToolTip(self.quality_combo, self.t('tooltip_quality'))
        self.quality_detect_btn = ttk.Button(self.download_bg_frame, text=self.t('auto_detect_qualities_formats'), command=self.detect_formats)
        self.quality_detect_btn.grid(row=1, column=2, padx=5)
        # --- Make format selection more prominent ---
        self.format_label = ttk.Label(self.download_bg_frame, text=self.t('format'))
        self.format_label.grid(row=2, column=0, sticky=tk.W, pady=5, padx=5)
        self.format_combo = ttk.Combobox(self.download_bg_frame, textvariable=self.format_var, values=["mp4", "webm", "mkv", "avi", "mov", "flv"], width=15, state="readonly")
        self.format_combo.grid(row=2, column=1, sticky=tk.W, pady=5, padx=5)
        ToolTip(self.format_combo, self.t('tooltip_format'))
        # --- End prominent quality/format selection ---
        self.output_dir_label = ttk.Label(self.download_bg_frame, text=self.t('output_dir_label'))
        self.output_dir_label.grid(row=3, column=0, sticky=tk.W, pady=5, padx=5)
        self.output_dir_entry = ttk.Entry(self.download_bg_frame, textvariable=self.output_dir_var, width=40)
        self.output_dir_entry.grid(row=3, column=1, sticky=tk.EW, pady=5, padx=5)
        self.browse_dir_btn = ttk.Button(self.download_bg_frame, text=self.t('browse'), command=self.browse_dir)
        self.browse_dir_btn.grid(row=3, column=2, padx=5)
        self.custom_format_label = ttk.Label(self.download_bg_frame, text=self.t('custom_format'))
        self.custom_format_label.grid(row=4, column=0, sticky=tk.W, pady=5, padx=5)
        self.custom_format_entry = ttk.Entry(self.download_bg_frame, textvariable=self.custom_format_var, width=30)
        self.custom_format_entry.grid(row=4, column=1, sticky=tk.W, pady=5, padx=5)
        self.audio_only_cb = ttk.Checkbutton(self.download_bg_frame, text=self.t('audio_only'), variable=self.audio_only_var)
        self.audio_only_cb.grid(row=5, column=0, sticky=tk.W, pady=5, padx=5)
        self.audio_only_cb.config(command=self.on_audio_only_toggle)
        self.playlist_cb = ttk.Checkbutton(self.download_bg_frame, text=self.t('playlist'), variable=self.playlist_var)
        self.playlist_cb.grid(row=5, column=1, sticky=tk.W, pady=5, padx=5)
        self.cookie_file_label = ttk.Label(self.download_bg_frame, text=self.t('cookie_file'))
        self.cookie_file_label.grid(row=6, column=0, sticky=tk.W, pady=5, padx=5)
        self.cookie_entry = ttk.Entry(self.download_bg_frame, textvariable=self.cookie_file_var, width=30)
        self.cookie_entry.grid(row=6, column=1, sticky=tk.W, pady=5, padx=5)
        self.browse_cookie_btn = ttk.Button(self.download_bg_frame, text=self.t('browse'), command=self.browse_cookie_file)
        self.browse_cookie_btn.grid(row=6, column=2, padx=5)
        self.validate_cookie_btn = ttk.Button(self.download_bg_frame, text=self.t('validate'), command=self.validate_cookie_file)
        self.validate_cookie_btn.grid(row=6, column=3, padx=5)
        self.button_frame = ttk.Frame(self.download_bg_frame)
        self.button_frame.grid(row=7, column=1, pady=10, columnspan=2)
        self.download_btn = ttk.Button(self.button_frame, text=self.t('download'), command=self.start_download)
        self.download_btn.pack(side=tk.LEFT, padx=5)
        self.cancel_btn = ttk.Button(self.button_frame, text=self.t('cancel'), command=self.cancel_download, state=tk.DISABLED)
        self.cancel_btn.pack(side=tk.LEFT, padx=5)
        self.status_label = ttk.Label(self.download_bg_frame, text=self.t('status'))
        self.status_label.grid(row=8, column=0, sticky=tk.W, pady=5, padx=5)
        ttk.Label(self.download_bg_frame, textvariable=self.progress_text, foreground="blue").grid(row=8, column=1, sticky=tk.W, pady=5, padx=5)
        self.progress_title_label = ttk.Label(self.download_bg_frame, text=self.t('progress'))
        self.progress_title_label.grid(row=9, column=0, sticky=tk.W, pady=5, padx=5)
        self.progress_canvas = tk.Canvas(self.download_bg_frame, height=20, width=300, highlightthickness=0, bd=0)
        self.progress_canvas.grid(row=9, column=1, columnspan=3, sticky=tk.W, pady=5, padx=5)
        self.progress_percent.set('0%')
        self.draw_progress_bar(0)
        self.download_log_label = ttk.Label(self.download_bg_frame, text=self.t('log'))
        self.download_log_label.grid(row=10, column=0, sticky=tk.W, pady=5, padx=5)
        self.output_text = scrolledtext.ScrolledText(self.download_bg_frame, height=8, width=80, wrap=tk.WORD)
        self.output_text.grid(row=11, column=0, columnspan=4, sticky=tk.EW, pady=5, padx=5)
        # --- Status Bar ---
        self.status_bar = ttk.Label(self.root, textvariable=self.status_message, relief=tk.SUNKEN, anchor=tk.W, padding=5)
        self.status_bar.grid(row=1, column=0, sticky="ew")
        # --- Batch Download Tab ---
        self.batch_frame = ttk.Frame(self.nb, padding=10)
        self.nb.add(self.batch_frame, text=self.t('batch_download'))
        self.batch_frame.columnconfigure(0, weight=1)
        self.batch_frame.rowconfigure(1, weight=1)
        self.batch_urls_label = ttk.Label(self.batch_frame, text=self.t('batch_urls'))
        self.batch_urls_label.grid(row=0, column=0, sticky=tk.W)
        self.batch_text = scrolledtext.ScrolledText(self.batch_frame, height=8, width=60, wrap=tk.WORD)
        self.batch_text.grid(row=1, column=0, columnspan=3, sticky="nsew")
        self.batch_output_dir_label = ttk.Label(self.batch_frame, text=self.t('output_dir_label'))
        self.batch_output_dir_label.grid(row=2, column=0, sticky=tk.W)
        self.batch_output_dir_entry = ttk.Entry(self.batch_frame, textvariable=self.output_dir_var, width=40)
        self.batch_output_dir_entry.grid(row=2, column=1, sticky=tk.EW)
        self.batch_browse_dir_btn = ttk.Button(self.batch_frame, text=self.t('browse'), command=self.browse_dir)
        self.batch_browse_dir_btn.grid(row=2, column=2)
        self.batch_quality_label = ttk.Label(self.batch_frame, text=self.t('quality'))
        self.batch_quality_label.grid(row=3, column=0, sticky=tk.W)
        self.batch_quality_combo = ttk.Combobox(self.batch_frame, textvariable=self.batch_quality_var, values=list(self.quality_value_map.keys()))
        self.batch_quality_combo.grid(row=3, column=1, sticky=tk.W)
        self.batch_audio_only_cb = ttk.Checkbutton(self.batch_frame, text=self.t('audio_only'), variable=self.audio_only_var)
        self.batch_audio_only_cb.grid(row=4, column=0, sticky=tk.W)
        self.batch_playlist_cb = ttk.Checkbutton(self.batch_frame, text=self.t('playlist'), variable=self.playlist_var)
        self.batch_playlist_cb.grid(row=4, column=1, sticky=tk.W)
        self.parallel_label = ttk.Label(self.batch_frame, text=self.t('parallel_downloads'))
        self.parallel_label.grid(row=5, column=0, sticky=tk.W)
        self.parallel_spinbox = ttk.Spinbox(self.batch_frame, from_=1, to=8, textvariable=self.parallel_var, width=5)
        self.parallel_spinbox.grid(row=5, column=1, sticky=tk.W)
        self.batch_download_btn = ttk.Button(self.batch_frame, text=self.t('batch_download'), command=self.start_batch_download)
        self.batch_download_btn.grid(row=6, column=1, pady=10)
        self.batch_progress_label = ttk.Label(self.batch_frame, textvariable=self.progress_text, foreground="blue")
        self.batch_progress_label.grid(row=7, column=0, columnspan=3, sticky=tk.W)
        self.recent_batch_label = ttk.Label(self.batch_frame, text=self.t('recent_batch'))
        self.recent_batch_label.grid(row=8, column=0, sticky=tk.W)
        self.recent_batch_combo = ttk.Combobox(self.batch_frame, values=self.recent_batch_files, postcommand=self.update_recent_batch_files)
        self.recent_batch_combo.grid(row=8, column=1, sticky=tk.W)
        self.recent_batch_combo.bind('<<ComboboxSelected>>', self.select_recent_batch_file)
        self.select_batch_btn = ttk.Button(self.batch_frame, text=self.t('select_batch'), command=self.browse_batch_file)
        self.select_batch_btn.grid(row=8, column=2, sticky=tk.W)
        # --- Menu ---
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        self.settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=self.t('settings'), menu=self.settings_menu)
        self.settings_menu.add_command(label=self.t('settings'), command=self.open_settings_dialog)
        self.help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=self.t('help'), menu=self.help_menu)
        self.help_menu.add_command(label=self.t('help'), command=self.show_help)
        self.help_menu.add_command(label=self.t('about'), command=self.show_about)
        self.help_menu.add_command(label=self.t('open_log_file'), command=self.open_log_file)
        # --- Settings Tab ---
        self.settings_frame = ttk.Frame(self.nb, padding=10)
        self.nb.add(self.settings_frame, text=self.t('settings'))
        self.settings_frame.columnconfigure(0, weight=1)
        self.settings_frame.rowconfigure(0, weight=1)

        # Add a canvas and scrollbar for a scrollable settings area
        self.settings_canvas = tk.Canvas(self.settings_frame, borderwidth=0)
        scrollbar = ttk.Scrollbar(self.settings_frame, orient="vertical", command=self.settings_canvas.yview)
        scrollable_frame = ttk.Frame(self.settings_canvas)
        scrollable_frame.columnconfigure(0, weight=1)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: self.settings_canvas.configure(
                scrollregion=self.settings_canvas.bbox("all")
            )
        )

        canvas_frame_id = self.settings_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        self.settings_canvas.configure(yscrollcommand=scrollbar.set)

        def on_canvas_configure(event):
            self.settings_canvas.itemconfig(canvas_frame_id, width=event.width)

        self.settings_canvas.bind("<Configure>", on_canvas_configure)

        self.settings_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        def _on_mouse_scroll(event):
            if hasattr(event, 'delta') and event.delta != 0:
                # Windows and macOS
                scroll_val = event.delta
                if sys.platform == 'win32':
                    scroll_val = event.delta // 120
                self.settings_canvas.yview_scroll(-1 * scroll_val, 'units')
            elif event.num == 4: # Linux scroll up
                self.settings_canvas.yview_scroll(-1, 'units')
            elif event.num == 5: # Linux scroll down
                self.settings_canvas.yview_scroll(1, 'units')

        def _bind_to_mousewheel(event):
            self.root.bind_all("<MouseWheel>", _on_mouse_scroll)
            self.root.bind_all("<Button-4>", _on_mouse_scroll)
            self.root.bind_all("<Button-5>", _on_mouse_scroll)

        def _unbind_from_mousewheel(event):
            self.root.unbind_all("<MouseWheel>")
            self.root.unbind_all("<Button-4>")
            self.root.unbind_all("<Button-5>")

        self.settings_frame.bind("<Enter>", _bind_to_mousewheel)
        self.settings_frame.bind("<Leave>", _unbind_from_mousewheel)
        
        # --- Appearance Settings ---
        appearance_frame = ttk.LabelFrame(scrollable_frame, text="Appearance", padding=(10, 5))
        appearance_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        appearance_frame.columnconfigure(1, weight=1)

        self.theme_label = ttk.Label(appearance_frame, text=self.t('theme'))
        self.theme_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        themes = ['light', 'dark']
        if HAS_THEMES:
            try:
                themes.extend(sorted(self.root.get_themes()))
            except Exception:
                pass
        self.theme_combo = ttk.Combobox(appearance_frame, textvariable=self.theme_var, values=themes, state='readonly')
        self.theme_combo.grid(row=0, column=1, sticky=tk.EW, pady=5, padx=5)
        self.theme_combo.bind('<<ComboboxSelected>>', self.change_theme)

        self.language_label = ttk.Label(appearance_frame, text=self.t('language'))
        self.language_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        self.lang_combo = ttk.Combobox(appearance_frame, textvariable=self.language_var, values=self.language_short_names, state='readonly')
        self.lang_combo.grid(row=1, column=1, sticky=tk.EW, pady=5, padx=5)
        self.lang_combo.bind('<<ComboboxSelected>>', self.change_language)

        # --- Dependencies ---
        deps_frame = ttk.LabelFrame(scrollable_frame, text="Dependencies", padding=(10, 5))
        deps_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        deps_frame.columnconfigure(1, weight=1)

        self.ytdlp_label = ttk.Label(deps_frame, text="yt-dlp:")
        self.ytdlp_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        self.ytdlp_status = ttk.Label(deps_frame, text=self.t('not_found'))
        self.ytdlp_status.grid(row=0, column=1, sticky=tk.W, pady=5)
        self.install_ytdlp_btn = ttk.Button(deps_frame, text=self.t('install_ytdlp'), command=self.install_ytdlp)
        self.install_ytdlp_btn.grid(row=0, column=2, sticky=tk.E, padx=5, pady=5)

        self.ffmpeg_label = ttk.Label(deps_frame, text="ffmpeg:")
        self.ffmpeg_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        self.ffmpeg_status = ttk.Label(deps_frame, text=self.t('not_found'))
        self.ffmpeg_status.grid(row=1, column=1, sticky=tk.W, pady=5)

        # --- Network Settings ---
        network_frame = ttk.LabelFrame(scrollable_frame, text="Network", padding=(10, 5))
        network_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        network_frame.columnconfigure(1, weight=1)

        self.proxy_label = ttk.Label(network_frame, text=self.t('proxy'))
        self.proxy_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        self.proxy_entry = ttk.Entry(network_frame, textvariable=self.proxy_var, width=40)
        self.proxy_entry.grid(row=0, column=1, sticky=tk.EW, pady=5, padx=5)

        self.user_agent_label = ttk.Label(network_frame, text=self.t('user_agent'))
        self.user_agent_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        self.user_agent_entry = ttk.Entry(network_frame, textvariable=self.user_agent_var, width=40)
        self.user_agent_entry.grid(row=1, column=1, sticky=tk.EW, pady=5, padx=5)

        self.bandwidth_label = ttk.Label(network_frame, text=self.t('bandwidth'))
        self.bandwidth_label.grid(row=2, column=0, sticky=tk.W, pady=5)
        self.bandwidth_entry = ttk.Entry(network_frame, textvariable=self.bandwidth_var, width=10)
        self.bandwidth_entry.grid(row=2, column=1, sticky=tk.W, pady=5, padx=5)

        # --- File & Download Settings ---
        file_frame = ttk.LabelFrame(scrollable_frame, text="Downloads", padding=(10, 5))
        file_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        file_frame.columnconfigure(1, weight=1)

        self.file_template_label = ttk.Label(file_frame, text=self.t('file_template'))
        self.file_template_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        self.file_template_entry = ttk.Entry(file_frame, textvariable=self.file_template_var, width=40)
        self.file_template_entry.grid(row=0, column=1, columnspan=2, sticky=tk.EW, pady=5, padx=5)

        self.skip_downloaded_var = tk.BooleanVar(value=self.settings.data.get('skip_downloaded', True))
        self.skip_downloaded_cb = ttk.Checkbutton(file_frame, text=self.t('skip_downloaded'), variable=self.skip_downloaded_var)
        self.skip_downloaded_cb.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=5)

        self.plugin_dir_label = ttk.Label(file_frame, text=self.t('plugin_dir'))
        self.plugin_dir_label.grid(row=2, column=0, sticky=tk.W, pady=5)
        self.plugin_dir_entry = ttk.Entry(file_frame, textvariable=self.plugin_dir_var, width=40)
        self.plugin_dir_entry.grid(row=2, column=1, sticky=tk.EW, pady=5, padx=5)
        self.browse_plugin_dir_btn = ttk.Button(file_frame, text=self.t('browse'), command=self.browse_plugin_dir)
        self.browse_plugin_dir_btn.grid(row=2, column=2, sticky=tk.E, padx=5, pady=5)

        self.notifications_cb = ttk.Checkbutton(file_frame, text=self.t('enable_notifications'), variable=self.enable_notifications_var)
        self.notifications_cb.grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # --- Other Settings ---
        other_frame = ttk.LabelFrame(scrollable_frame, text="Other", padding=(10, 5))
        other_frame.grid(row=4, column=0, padx=10, pady=10, sticky="ew")
        other_frame.columnconfigure(1, weight=1)

        self.log_level_label = ttk.Label(other_frame, text=self.t('log_level'))
        self.log_level_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        self.log_level_combo = ttk.Combobox(other_frame, textvariable=self.log_level_var, values=["DEBUG", "INFO", "WARNING", "ERROR"])
        self.log_level_combo.grid(row=0, column=1, sticky=tk.W, pady=5, padx=5)

        # Add action buttons frame at the bottom
        self.action_btn_frame = ttk.Frame(scrollable_frame, padding=(0, 10))
        self.action_btn_frame.grid(row=5, column=0, columnspan=2, pady=15, sticky="ew")

        self.export_btn = ttk.Button(self.action_btn_frame, text=self.t('export_settings'), command=self.export_settings)
        self.export_btn.pack(side=tk.LEFT, padx=5)
        self.import_btn = ttk.Button(self.action_btn_frame, text=self.t('import_settings'), command=self.import_settings)
        self.import_btn.pack(side=tk.LEFT, padx=5)
        self.check_updates_btn = ttk.Button(self.action_btn_frame, text=self.t('check_updates'), command=self.check_updates)
        self.check_updates_btn.pack(side=tk.LEFT, padx=5)
        self.clear_log_btn = ttk.Button(self.action_btn_frame, text=self.t('clear_log'), command=self.clear_log)
        self.clear_log_btn.pack(side=tk.LEFT, padx=5)

        self.reset_btn = ttk.Button(self.action_btn_frame, text=self.t('reset_settings'), command=self.reset_settings)
        self.reset_btn.pack(side=tk.LEFT, padx=5)
        
        def save_tab_settings():
            # Update all UI variables and settings from the tab
            display_theme = self.theme_var.get()
            canonical_theme = self.theme_value_map.get(display_theme, display_theme)
            self.settings.data['theme'] = canonical_theme
            
            self.settings.data['language'] = self.language_code_to_short.get(self.language_var.get(), 'en')
            # Update current theme and language variables
            if self.theme_var.get().lower() == 'dark' or self.theme_var.get() == self.t('dark'):
                self.current_theme = 'dark'
            else:
                self.current_theme = 'light'
            # Update both self.language and self.current_language for translation
            if self.language_var.get() in self.language_short_to_code:
                self.language = self.language_short_to_code[self.language_var.get()]
                self.current_language = self.language_short_to_code[self.language_var.get()]
            else:
                self.language = 'en'
                self.current_language = 'en'
            self.settings.data['output_dir'] = self.output_dir_var.get()
            self.settings.data['parallel'] = self.parallel_var.get()
            self.settings.data['postprocess_script'] = self.postprocess_script_var.get() if hasattr(self, 'postprocess_script_var') else ''
            self.settings.data['format'] = self.format_var.get()
            self.settings.data['custom_format'] = self.custom_format_var.get()
            self.settings.data['cookie_file'] = self.cookie_file_var.get()
            self.settings.data['proxy'] = self.proxy_var.get()
            self.settings.data['enable_notifications'] = self.enable_notifications_var.get()
            self.settings.data['log_level'] = self.log_level_var.get()
            self.settings.data['file_template'] = self.file_template_var.get()
            self.settings.data['user_agent'] = self.user_agent_var.get()
            self.settings.data['bandwidth'] = self.bandwidth_var.get()
            self.settings.data['plugin_dir'] = self.plugin_dir_var.get()
            self.settings.data['skip_downloaded'] = self.skip_downloaded_var.get()
            self.settings.save()
            self.refresh_ui()

        self.save_btn = ttk.Button(self.action_btn_frame, text=self.t('save'), command=save_tab_settings)
        self.save_btn.pack(side=tk.LEFT, padx=5)

        # Add download history tab
        self.history_frame = ttk.Frame(self.nb, padding=10)
        self.nb.add(self.history_frame, text=self.t('history'))
        self.history_text = scrolledtext.ScrolledText(self.history_frame, height=20, width=100, wrap=tk.WORD)
        self.history_text.pack(fill=tk.BOTH, expand=True)
        # Add Clear History button
        self.clear_history_btn = ttk.Button(self.history_frame, text=self.t('clear_history'), command=self.clear_history)
        self.clear_history_btn.pack(pady=5)
        self.update_history()
        self.history_label = ttk.Label(self.history_frame, text=self.t('history'))
        self.history_label.pack_forget()  # Not shown, but for refresh_ui completeness
        # Add tooltips to main controls
        ToolTip(self.download_btn, self.t('tooltip_download'))
        ToolTip(self.cancel_btn, self.t('tooltip_cancel'))
        ToolTip(self.output_text, self.t('tooltip_log'))
        ToolTip(self.progress_canvas, self.t('tooltip_progress'))
        ToolTip(self.recent_combo, self.t('tooltip_recent'))
        # Add percentage label to progress bar
        # self.percent_label = ttk.Label(self.progress_bar.master, textvariable=self.progress_percent, width=6, anchor='w')
        # self.percent_label.grid(row=8, column=0, sticky=tk.W, padx=5)
        # Add Copy Log and Export Log buttons
        self.log_btn_frame = ttk.Frame(self.download_bg_frame)
        self.log_btn_frame.grid(row=12, column=3, sticky=tk.E, pady=5)
        self.copy_log_btn = ttk.Button(self.log_btn_frame, text=self.t('copy_log'), command=self.copy_log)
        self.copy_log_btn.pack(side=tk.LEFT, padx=2)
        self.export_log_btn = ttk.Button(self.log_btn_frame, text=self.t('export_log'), command=self.export_log)
        self.export_log_btn.pack(side=tk.LEFT, padx=2)
        ToolTip(self.copy_log_btn, "Copy the log to clipboard.")
        ToolTip(self.export_log_btn, "Export the log to a file.")
        # --- Recent Downloads Tab ---
        self.recent_frame = ttk.Frame(self.nb, padding=10)
        self.nb.add(self.recent_frame, text=self.t('recent_downloads') if 'recent_downloads' in LANGUAGES['en'] else "Recent Downloads")
        self.recent_listbox = tk.Listbox(self.recent_frame, height=10, activestyle='dotbox')
        self.recent_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.recent_listbox.bind('<Double-Button-1>', self.open_recent_download)
        # Add Remove Recent Downloads button
        self.remove_recent_btn = ttk.Button(self.recent_frame, text=self.t('remove_recent_downloads'), command=self.remove_recent_downloads)
        self.remove_recent_btn.pack(pady=5)
        self.update_recent_downloads()
        self.recent_downloads_label = ttk.Label(self.recent_frame, text=self.t('recent_downloads') if 'recent_downloads' in LANGUAGES['en'] else "Recent Downloads")
        self.recent_downloads_label.pack_forget()  # Not shown, but for refresh_ui completeness

    def reset_settings(self):
        """Resets all settings to their default values after confirmation."""
        if messagebox.askyesno(self.t('reset_confirm_title'), self.t('reset_confirm_message')):
            # Get default settings by creating a new temporary Settings instance
            default_settings = Settings().data
            self.settings.data = default_settings.copy()
            self.settings.save()

            # Update all the tk Variables to reflect the reset
            self.theme_var.set(self.settings.data.get('theme', 'light'))
            self.language_var.set(self.language_code_to_short.get(self.settings.data.get('language', 'en'), 'En'))
            self.output_dir_var.set(self.settings.data.get("output_dir", str(Path.home() / "Downloads")))
            self.parallel_var.set(self.settings.data.get('parallel', 2))
            self.postprocess_script_var.set(self.settings.data.get('postprocess_script', ''))
            self.format_var.set(self.settings.data.get('format', 'mp4'))
            self.custom_format_var.set(self.settings.data.get('custom_format', ''))
            self.cookie_file_var.set(self.settings.data.get('cookie_file', ''))
            self.proxy_var.set(self.settings.data.get('proxy', ''))
            self.enable_notifications_var.set(self.settings.data.get('enable_notifications', True))
            self.log_level_var.set(self.settings.data.get('log_level', 'INFO'))
            self.file_template_var.set(self.settings.data.get('file_template', '%(uploader)s - %(id)s.%(ext)s'))
            self.user_agent_var.set(self.settings.data.get('user_agent', ''))
            self.bandwidth_var.set(self.settings.data.get('bandwidth', ''))
            self.plugin_dir_var.set(self.settings.data.get('plugin_dir', ''))
            self.skip_downloaded_var.set(self.settings.data.get('skip_downloaded', True))

            self.refresh_ui()
            messagebox.showinfo(self.t('success'), self.t('settings_reset_message'))

    def apply_theme(self):
        style = ttk.Style()
        display_theme = self.theme_var.get()
        canonical_theme = self.theme_value_map.get(display_theme, display_theme)

        # Define styles for custom light theme
        def apply_light_theme():
            bg_main = '#f8f9fa'
            bg_widget = '#ffffff'
            bg_button = '#e5e9f0'
            fg_text = '#2e3440'
            accent = '#5e81ac'
            bg_labelframe = '#ebedf0'
            self.root.configure(bg=bg_main)
            style.theme_use('default')
            style.configure('.', background=bg_main, foreground=fg_text)
            style.configure('TFrame', background=bg_main)
            style.configure('TLabel', background=bg_main, foreground=fg_text)
            style.configure('TButton', background=bg_button, foreground=fg_text)
            style.configure('TEntry', fieldbackground=bg_widget, foreground=fg_text)
            style.configure('TCombobox', fieldbackground=bg_widget, foreground=fg_text)
            style.configure('TCheckbutton', background=bg_main, foreground=fg_text)
            style.configure('TRadiobutton', background=bg_main, foreground=fg_text)
            style.configure('TLabelFrame', background=bg_labelframe, foreground=fg_text)
            style.configure('TLabelFrame.Label', background=bg_labelframe, foreground=fg_text)
            style.configure('TNotebook', background=bg_main)
            style.configure('TNotebook.Tab', background=bg_widget, foreground=fg_text)
            style.configure('Horizontal.TProgressbar', background=accent)
            # Apply to non-ttk widgets
            for widget in [self.download_bg_frame]:
                if widget and isinstance(widget, tk.Frame):
                    widget.configure(bg=bg_main)
            for text_widget in [self.output_text, self.batch_text, self.history_text]:
                if text_widget: text_widget.configure(bg=bg_widget, fg=fg_text, insertbackground=fg_text)
            if hasattr(self, 'progress_canvas'): self.progress_canvas.configure(bg=bg_widget, highlightbackground=bg_main)
            if hasattr(self, 'settings_canvas'): self.settings_canvas.configure(bg=bg_main, highlightbackground=bg_main)
            if hasattr(self, 'recent_listbox'): self.recent_listbox.configure(bg=bg_widget, fg=fg_text)
        
        # Define styles for custom dark theme
        def apply_dark_theme():
            bg_main = '#181a1b'
            bg_widget = '#23272e'
            bg_button = '#3b4252'
            fg_text = '#eceff4'
            accent = '#5e81ac'
            bg_labelframe = '#23272e'
            self.root.configure(bg=bg_main)
            style.theme_use('clam')
            style.configure('.', background=bg_main, foreground=fg_text)
            style.configure('TFrame', background=bg_main)
            style.configure('TLabel', background=bg_main, foreground=fg_text)
            style.configure('TButton', background=bg_button, foreground=fg_text)
            style.map('TButton', background=[('active', accent)])
            style.configure('TEntry', fieldbackground=bg_widget, foreground=fg_text, insertcolor=fg_text)
            style.configure('TCombobox', fieldbackground=bg_widget, foreground=fg_text)
            style.map('TCombobox', fieldbackground=[('readonly', bg_widget)])
            style.configure('TCheckbutton', background=bg_main, foreground=fg_text)
            style.configure('TRadiobutton', background=bg_main, foreground=fg_text)
            style.configure('TLabelFrame', background=bg_labelframe, foreground=fg_text)
            style.configure('TLabelFrame.Label', background=bg_labelframe, foreground=fg_text)
            style.configure('TNotebook', background=bg_main)
            style.configure('TNotebook.Tab', background=bg_widget, foreground=fg_text)
            style.map('TNotebook.Tab', background=[('selected', accent)])
            style.configure('Horizontal.TProgressbar', background=accent)
            # Apply to non-ttk widgets
            for widget in [self.download_bg_frame]:
                if widget and isinstance(widget, tk.Frame):
                    widget.configure(bg=bg_main)

            for text_widget in [self.output_text, self.batch_text, self.history_text]:
                if text_widget: text_widget.configure(bg=bg_widget, fg=fg_text, insertbackground=fg_text)
            if hasattr(self, 'progress_canvas'): self.progress_canvas.configure(bg=bg_widget, highlightbackground=bg_main)
            if hasattr(self, 'settings_canvas'): self.settings_canvas.configure(bg=bg_widget, highlightbackground=bg_main)
            if hasattr(self, 'recent_listbox'): self.recent_listbox.configure(bg=bg_widget, fg=fg_text)

        if canonical_theme == 'dark':
            apply_dark_theme()
        elif canonical_theme == 'light':
            apply_light_theme()
        elif HAS_THEMES:
            try:
                self.root.set_theme(canonical_theme)
                # Sync non-ttk widgets with the theme
                bg = style.lookup('TFrame', 'background')
                fg = style.lookup('TLabel', 'foreground')
                entry_bg = style.lookup('TEntry', 'fieldbackground')

                style.configure('TLabelFrame', background=bg, foreground=fg)
                style.configure('TLabelFrame.Label', background=bg, foreground=fg)

                self.root.configure(bg=bg)
                if hasattr(self, 'download_bg_frame'): self.download_bg_frame.configure(bg=bg)
                # TTK frames are handled by the theme, no need to loop
                for text_widget in [self.output_text, self.batch_text, self.history_text]:
                    if text_widget: text_widget.configure(bg=entry_bg, fg=fg, insertbackground=fg)
                if hasattr(self, 'progress_canvas'): self.progress_canvas.configure(bg=entry_bg, highlightbackground=bg)
                if hasattr(self, 'settings_canvas'): self.settings_canvas.configure(bg=bg, highlightbackground=bg)
                if hasattr(self, 'recent_listbox'): self.recent_listbox.configure(bg=entry_bg, fg=fg)
            except tk.TclError:
                # Fallback for themes that don't define all the elements we need to style.
                # Instead of reverting to light theme, just let it be partially applied.
                print(f"Warning: Theme '{canonical_theme}' may not be fully supported.")
        else:
            apply_light_theme()

    def change_theme(self, event=None):
        display_theme = self.theme_var.get()
        canonical_theme = self.theme_value_map.get(display_theme, display_theme)
        self.settings.data['theme'] = canonical_theme
        self.apply_theme()

    def browse_dir(self):
        directory = filedialog.askdirectory(initialdir=self.output_dir_var.get())
        if directory:
            self.output_dir_var.set(directory)

    def on_drop_url(self, event):
        data = event.data.strip()
        if data.startswith('http'):
            self.url_var.set(data)
            self.status_message.set("URL dropped.")
        elif data.endswith('.txt'):
            try:
                with open(data, 'r') as f:
                    self.batch_text.delete(1.0, tk.END)
                    self.batch_text.insert(tk.END, f.read())
                self.status_message.set("Batch file loaded.")
            except Exception as e:
                self.status_message.set(f"Failed to load file: {e}")

    def on_drop_batch(self, event):
        self.on_drop_url(event)

    def cancel_download(self):
        """Cancel the current download."""
        self.cancel_requested = True
        self.progress_text.set(self.t('cancelling'))
        self.cancel_btn.config(state=tk.DISABLED)
        
    def start_download(self):
        output_dir = self.output_dir_var.get().strip()
        if not output_dir or not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir, exist_ok=True)
            except Exception as e:
                messagebox.showerror(self.t('error'), f"{self.t('output_dir_missing')}: {e}")
                return
        if not os.access(output_dir, os.W_OK):
            messagebox.showerror(self.t('error'), "Download directory is not writable.")
            return
        output_template = os.path.join(output_dir, "%(uploader)s - %(id)s.%(ext)s")
        self.log_message(f"Expected output path: {output_template}")
        if not self.url_var.get():
            messagebox.showerror(self.t('error'), self.t('url_required'))
            return
        self.cancel_requested = False
        self.download_btn.config(state=tk.DISABLED)
        self.cancel_btn.config(state=tk.NORMAL)
        self.update_progress_bar(0)
        def progress_cb(msg):
            if self.cancel_requested:
                return False
            self.parse_progress(msg)
            self.root.update()
            return True
        def run():
            file_path = None
            try:
                # Patch: get file path from progress callback
                def progress_cb_with_file(msg):
                    nonlocal file_path
                    if '[download] Destination:' in msg:
                        file_path = msg.split('Destination: ', 1)[1]
                    return progress_cb(msg)
                # Add download archive option
                archive_file = os.path.join(str(Path.home()), "moaz_download_archive.txt")
                extra_opts = {}
                if self.skip_downloaded_var.get():
                    extra_opts['download_archive'] = archive_file
                quality_display = self.quality_combo.get()
                quality_value = self.quality_value_map.get(quality_display, 'best')
                success, final_filepath = self.downloader.download(
                    url=self.url_var.get(),
                    output_dir=self.output_dir_var.get(),
                    quality=quality_value,
                    audio_only=self.audio_only_var.get(),
                    playlist=self.playlist_var.get(),
                    cookie_file=self.cookie_file_var.get() or None,
                    progress_callback=progress_cb_with_file,
                    proxy=self.proxy_var.get() or None,
                    file_template=self.file_template_var.get(),
                    user_agent=self.user_agent_var.get() or None,
                    bandwidth=self.bandwidth_var.get() or None,
                    plugin_dir=self.plugin_dir_var.get() or None,
                    **extra_opts
                )
                now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                
                if self.cancel_requested:
                    self.progress_text.set(self.t('cancelled'))
                    self.settings.add_history({
                        "time": now,
                        "url": self.url_var.get(),
                        "status": "Cancelled",
                        "file": final_filepath or "unknown path"
                    })
                    if HAS_NOTIFICATIONS and self.enable_notifications_var.get():
                        try:
                            notification.notify(
                            title=self.t('title'),
                            message=self.t('download_cancelled'),
                                app_name=APP_NAME,
                                app_icon=ICON_PATH,
                            timeout=3
                        )
                        except Exception as e:
                            self.log_message(f"Notification Error: {e}")

                elif final_filepath and os.path.exists(final_filepath):
                    self.progress_text.set(self.t('download_completed'))
                    self.update_progress_bar(100)
                    self.settings.add_recent_url(self.url_var.get())
                    self.settings.add_history({
                        "time": now,
                        "url": self.url_var.get(),
                        "status": "Success",
                        "file": final_filepath
                    })
                    if HAS_NOTIFICATIONS and self.enable_notifications_var.get():
                        try:
                            notification.notify(
                            title=self.t('title'),
                            message=self.t('download_completed'),
                                app_name=APP_NAME,
                                app_icon=ICON_PATH,
                            timeout=3
                        )
                        except Exception as e:
                            self.log_message(f"Notification Error: {e}")
                    self.root.after(0, lambda: messagebox.showinfo(self.t('success'), self.t('download_completed')))

                else:
                    # Smart file detection: look for files that match yt-dlp naming pattern
                    def find_downloaded_file():
                        output_dir = os.path.dirname(final_filepath) if final_filepath else self.output_dir_var.get()
                        if not os.path.isdir(output_dir):
                            return None
                        
                        # Extract video ID from expected filename
                        expected_filename = os.path.basename(final_filepath) if final_filepath else ""
                        print(f"[DEBUG] Expected filename: {expected_filename}")
                        
                        # Try to extract video ID (between last ' - ' and extension)
                        video_id = ""
                        if " - " in expected_filename and "." in expected_filename:
                            base = expected_filename.rsplit(" - ", 1)[-1]
                            video_id = base.split(".")[0].strip()
                        print(f"[DEBUG] Looking for video ID: {video_id}")
                        
                        # Get expected extension
                        expected_ext = ""
                        if "." in expected_filename:
                            expected_ext = "." + expected_filename.split(".")[-1]
                        print(f"[DEBUG] Expected extension: {expected_ext}")
                        
                        # Look for files that contain the video ID and extension
                        for f in os.listdir(output_dir):
                            full_path = os.path.join(output_dir, f)
                            if os.path.isfile(full_path) and video_id in f and f.endswith(expected_ext):
                                print(f"[DEBUG] Found file with video ID: {f}")
                                return full_path
                        return None
                    
                    # Try to find the downloaded file
                    found_file = find_downloaded_file()
                    
                    if found_file:
                            self.progress_text.set(self.t('download_completed'))
                            self.update_progress_bar(100)
                            self.settings.add_recent_url(self.url_var.get())
                            self.settings.add_history({
                                "time": now,
                                "url": self.url_var.get(),
                                "status": "Success",
                            "file": found_file
                            })
                            if HAS_NOTIFICATIONS and self.enable_notifications_var.get():
                                try:
                                    notification.notify(
                                    title=self.t('title'),
                                    message=self.t('download_completed'),
                                    app_name=APP_NAME,
                                    app_icon=ICON_PATH,
                                    timeout=3
                                )
                                except Exception as e:
                                    self.log_message(f"Notification Error: {e}")
                                    self.root.after(0, lambda: messagebox.showinfo(self.t('success'), self.t('download_completed')))
                            else:
                                self.progress_text.set(self.t('download_failed'))
                                self.update_progress_bar(0)
                                self.settings.add_history({
                                "time": now,
                                "url": self.url_var.get(),
                                "status": "Failed",
                                "file": final_filepath or "unknown path"
                            })
                            if HAS_NOTIFICATIONS and self.enable_notifications_var.get():
                                try:
                                    notification.notify(
                                        title=self.t('title'),
                                        message=self.t('download_failed'),
                                        app_name=APP_NAME,
                                        app_icon=ICON_PATH,
                                        timeout=3
                                    )
                                except Exception as e:
                                    self.log_message(f"Notification Error: {e}")
                        # Show error message
                                    if FFMPEG_PATH is None:
                                        self.root.after(0, lambda: messagebox.showerror(
                                            self.t('error'),
                                            "No single-file format is available for this video/quality without ffmpeg.\nTry a lower quality, or install ffmpeg for best results."
                                        ))
                                    else:
                                        self.root.after(0, lambda: messagebox.showerror(self.t('error'), self.t('merge_failed')))

            except Exception as e:
                self.progress_text.set(f"{self.t('error')}: {str(e)}")
                self.log_message(f"Error: {str(e)}")
                self.update_progress_bar(0)
                now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                output_template = os.path.abspath(os.path.join(self.output_dir_var.get(), self.file_template_var.get()))
                self.settings.add_history({
                    "time": now,
                    "url": self.url_var.get(),
                    "status": "Error",
                    "file": final_filepath or output_template
                })
            finally:
                self.download_btn.config(state=tk.NORMAL)
                self.cancel_btn.config(state=tk.DISABLED)
                self.cancel_requested = False
                self.update_history()
                self.update_recent_downloads()
        threading.Thread(target=run, daemon=True).start()

    def start_batch_download(self):
        output_dir = self.output_dir_var.get().strip()
        if not output_dir or not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir, exist_ok=True)
            except Exception as e:
                messagebox.showerror(self.t('error'), f"{self.t('output_dir_missing')}: {e}")
                return
        if not os.access(output_dir, os.W_OK):
            messagebox.showerror(self.t('error'), "Download directory is not writable.")
            return
        output_template = os.path.join(output_dir, "%(uploader)s - %(id)s.%(ext)s")
        self.log_message(f"Expected output path: {output_template}")
        batch_text = self.batch_text.get(1.0, tk.END).strip()
        urls = [line.strip() for line in batch_text.split('\n') if is_valid_url(line.strip())]
        parallel = self.parallel_var.get()
        self.progress_text.set(self.t('downloading'))
        self.update_progress_bar(0)
        def progress_cb(msg):
            self.parse_progress(msg)
            self.root.update_idletasks()
        def run():
            results = {}
            file_paths = {}
            def per_url_progress_cb(url):
                def cb(msg):
                    if '[download] Destination:' in msg:
                        file_paths[url] = msg.split('Destination: ', 1)[1]
                    return progress_cb(msg)
                return cb
            try:
                archive_file = os.path.join(str(Path.home()), "moaz_download_archive.txt")
                extra_opts = {}
                if self.skip_downloaded_var.get():
                    extra_opts['download_archive'] = archive_file
                for url in urls:
                    quality_display = self.batch_quality_combo.get()
                    quality_value = self.quality_value_map.get(quality_display, 'best')
                    ok, final_filepath = self.downloader.download(
                        url=url,
                        output_dir=output_dir,
                        quality=quality_value,
                        audio_only=self.audio_only_var.get(),
                        playlist=self.playlist_var.get(),
                        cookie_file=self.cookie_file_var.get(),
                        progress_callback=per_url_progress_cb(url),
                        proxy=self.proxy_var.get() or None,
                        file_template=self.file_template_var.get(),
                        user_agent=self.user_agent_var.get() or None,
                        bandwidth=self.bandwidth_var.get() or None,
                        plugin_dir=self.plugin_dir_var.get() or None,
                        **extra_opts
                    )
                    
                    # Smart file detection for batch downloads
                    def find_downloaded_file_batch():
                        if not os.path.isdir(output_dir):
                            return None
                        
                        # Extract video ID from expected filename
                        expected_filename = os.path.basename(final_filepath) if final_filepath else ""
                        print(f"[DEBUG] Batch - Expected filename: {expected_filename}")
                        
                        # Try to extract video ID (between last ' - ' and extension)
                        video_id = ""
                        if " - " in expected_filename and "." in expected_filename:
                            base = expected_filename.rsplit(" - ", 1)[-1]
                            video_id = base.split(".")[0].strip()
                        print(f"[DEBUG] Batch - Looking for video ID: {video_id}")
                        
                        # Get expected extension
                        expected_ext = ""
                        if "." in expected_filename:
                            expected_ext = "." + expected_filename.split(".")[-1]
                        print(f"[DEBUG] Batch - Expected extension: {expected_ext}")
                        
                        # Look for files that contain the video ID and extension
                        for f in os.listdir(output_dir):
                            full_path = os.path.join(output_dir, f)
                            if os.path.isfile(full_path) and video_id in f and f.endswith(expected_ext):
                                print(f"[DEBUG] Batch - Found file with video ID: {f}")
                                return full_path
                        return None
                    
                    # Check if download was successful using smart detection
                    found_file = find_downloaded_file_batch()
                    download_success = found_file is not None or (final_filepath and os.path.exists(final_filepath))
                    
                    results[url] = download_success
                    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                    actual_file = found_file or file_paths.get(url, final_filepath or "unknown path")
                    self.settings.add_history({
                        "time": now,
                        "url": url,
                        "status": "Success" if download_success else "Failed",
                        "file": actual_file
                    })
                success_count = sum(1 for ok in results.values() if ok)
                self.progress_text.set(f"{self.t('done')} {success_count}/{len(urls)}")
                if HAS_NOTIFICATIONS and self.enable_notifications_var.get():
                    try:
                        notification.notify(
                            title=self.t('title'),
                            message=f"{self.t('notification_success')} {success_count}/{len(urls)}",
                                app_name=APP_NAME,
                                app_icon=ICON_PATH,
                            timeout=3
                        )
                    except Exception as e:
                        self.log_message(f"Notification Error: {e}")
                if success_count == len(urls):
                    self.log_message(self.t('batch_completed'))
                    self.update_progress_bar(100)
                else:
                    self.log_message(self.t('batch_failed'))
                    self.update_progress_bar(0)
            except Exception as e:
                self.log_message(f"{self.t('error')}: {e}")
                messagebox.showerror(self.t('error'), str(e))
                self.update_progress_bar(0)
            finally:
                self.update_history()
                self.update_recent_downloads()
        t = threading.Thread(target=run, daemon=True)
        t.start()
        self.download_threads.append(t)

    def open_settings_dialog(self):
        # Always initialize dialog fields from current UI variables for sync
        dlg = tk.Toplevel(self.root)
        dlg.title(self.t('settings'))
        ttk.Label(dlg, text=self.t('output_dir_label')).grid(row=0, column=0, sticky=tk.W)
        out_var = tk.StringVar(value=self.output_dir_var.get())
        ttk.Entry(dlg, textvariable=out_var, width=40).grid(row=0, column=1)
        ttk.Label(dlg, text=self.t('language')).grid(row=1, column=0, sticky=tk.W)
        lang_var = tk.StringVar(value=self.language_var.get())
        ttk.Combobox(dlg, textvariable=lang_var, values=list(LANGUAGES.keys())).grid(row=1, column=1)
        ttk.Label(dlg, text=self.t('parallel_downloads')).grid(row=2, column=0, sticky=tk.W)
        par_var = tk.IntVar(value=self.parallel_var.get())
        ttk.Spinbox(dlg, from_=1, to=8, textvariable=par_var, width=5).grid(row=2, column=1)
        ttk.Label(dlg, text="Post-process script (Python)").grid(row=3, column=0, sticky=tk.W)
        post_var = tk.StringVar(value=self.postprocess_script_var.get())
        ttk.Entry(dlg, textvariable=post_var, width=40).grid(row=3, column=1)
        def browse_script():
            path = filedialog.askopenfilename(title="Select Python Script", filetypes=[("Python files", "*.py"), ("All files", "*.*")])
            if path:
                post_var.set(path)
        ttk.Button(dlg, text=self.t('browse'), command=browse_script).grid(row=3, column=2)
        def save():
            # Update all UI variables and settings from dialog
            self.output_dir_var.set(out_var.get())
            self.language_var.set(lang_var.get())
            self.language = lang_var.get()
            self.parallel_var.set(par_var.get())
            self.postprocess_script_var.set(post_var.get())
            self.settings.data['output_dir'] = out_var.get()
            self.settings.data['language'] = lang_var.get()
            self.settings.data['parallel'] = par_var.get()
            self.settings.data['postprocess_script'] = post_var.get()
            self.settings.save()
            self.downloader.set_postprocess_script(post_var.get())
            self.refresh_ui()
            dlg.destroy()
        ttk.Button(dlg, text=self.t('save'), command=save).grid(row=4, column=0, padx=10, pady=10)
        ttk.Button(dlg, text=self.t('cancel'), command=dlg.destroy).grid(row=4, column=1, padx=10, pady=10)

    def show_help(self):
        messagebox.showinfo(self.t('help'), self.t('help_text'))

    def show_about(self):
        messagebox.showinfo(self.t('about'), "I'm Moaz (pronounced Mu'adh), or Abulbara', a G12 student at STEM October. I'm into tech, problem-solving, and I enjoy building projects that make a real difference.")

    def browse_cookie_file(self):
        file_path = filedialog.askopenfilename(title="Select Cookie File", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            self.cookie_file_var.set(file_path)

    def validate_cookie_file(self):
        path = self.cookie_file_var.get().strip()
        if not path:
            messagebox.showwarning(self.t('title'), self.t('cookie_invalid'))
            return
        if self.downloader.validate_cookie_file(path):
            messagebox.showinfo(self.t('title'), self.t('cookie_valid'))
        else:
            messagebox.showerror(self.t('title'), self.t('cookie_invalid'))

    def detect_formats(self):
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror(self.t('title'), self.t('invalid_url'))
            return
        formats = self.downloader.detect_formats(url)
        if formats:
            self.custom_format_var.set(formats[0])
            # Update the quality combobox with detected formats (if they look like resolutions)
            resolutions = [f for f in formats if f.endswith('p') or f in ["best", "worst"]]
            if resolutions:
                self.quality_combo['values'] = list(dict.fromkeys(["best"] + resolutions + ["worst"]))
                self.quality_combo.set(resolutions[0])
            # Update the format combobox with detected file extensions if possible
            file_formats = [f for f in formats if f in ["mp4", "webm", "mkv", "avi", "mov", "flv"]]
            if file_formats:
                self.format_combo['values'] = list(dict.fromkeys(["mp4"] + file_formats))
                self.format_combo.set(file_formats[0])
            messagebox.showinfo(self.t('title'), f"{self.t('detected_formats')} {', '.join(formats)}")
        else:
            messagebox.showwarning(self.t('title'), self.t('no_formats_detected'))

    def log_message(self, message: str):
        self.log_lines.append(message)
        self.output_text.insert(tk.END, message + '\n')
        self.output_text.see(tk.END)
        self.root.update_idletasks()
        # Also log to file
        with open(str(Path.home() / 'video_downloader_gui.log'), 'a', encoding='utf-8') as f:
            f.write(message + '\n')

    def update_recent_urls(self):
        self.recent_combo['values'] = self.settings.data.get('recent_urls', [])

    def select_recent_url(self, event):
        url = self.recent_combo.get()
        if url:
            self.url_var.set(url)

    def check_dependencies(self):
        status = self.downloader.check_dependencies()
        self.ytdlp_status.config(text=status['yt-dlp'])
        self.ffmpeg_status.config(text=status['ffmpeg'])

    def install_ytdlp(self):
        ok = self.downloader.install_ytdlp()
        if ok:
            messagebox.showinfo(self.t('title'), 'yt-dlp installed successfully!')
        else:
            messagebox.showerror(self.t('title'), 'Failed to install yt-dlp.')
        self.check_dependencies()

    def set_protocol(self):
        if not self.protocol_set:
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            self.protocol_set = True

    def on_closing(self):
        # Graceful shutdown and cleanup
        for t in self.download_threads:
            if t.is_alive():
                # No direct way to kill threads, but we can wait a bit
                t.join(timeout=1)
        self.settings.save()
        self.root.destroy()

    def run(self):
        self.root.mainloop()

    def update_recent_batch_files(self):
        self.recent_batch_combo['values'] = self.settings.data.get('recent_batch_files', [])

    def select_recent_batch_file(self, event):
        path = self.recent_batch_combo.get()
        if path:
            try:
                with open(path, 'r') as f:
                    self.batch_text.delete(1.0, tk.END)
                    self.batch_text.insert(tk.END, f.read())
            except Exception as e:
                messagebox.showerror(self.t('error'), str(e))

    def browse_batch_file(self):
        path = filedialog.askopenfilename(title=self.t('select_batch'), filetypes=[('Text files', '*.txt'), ('All files', '*.*')])
        if path:
            self.settings.add_recent_batch_file(path)
            self.update_recent_batch_files()
            try:
                with open(path, 'r') as f:
                    self.batch_text.delete(1.0, tk.END)
                    self.batch_text.insert(tk.END, f.read())
            except Exception as e:
                messagebox.showerror(self.t('error'), str(e))

    def schedule_download(self):
        import datetime, time
        tstr = self.scheduled_time_var.get().strip()
        if not tstr:
            messagebox.showwarning(self.t('warning'), self.t('schedule_time'))
            return
        try:
            now = datetime.datetime.now()
            h, m = map(int, tstr.split(':'))
            scheduled = now.replace(hour=h, minute=m, second=0, microsecond=0)
            if scheduled < now:
                scheduled += datetime.timedelta(days=1)
            delay = (scheduled - now).total_seconds()
            self.log_message(f"{self.t('scheduled_for')}: {scheduled.strftime('%Y-%m-%d %H:%M')}")
            self.root.after(int(delay * 1000), self.start_download)
        except Exception as e:
            messagebox.showerror(self.t('error'), str(e))

    def check_updates(self):
        if self.downloader.check_for_updates():
            messagebox.showinfo(self.t('info'), self.t('update_available'))
        else:
            messagebox.showinfo(self.t('info'), self.t('up_to_date'))

    def export_settings(self):
        path = filedialog.asksaveasfilename(defaultextension='.json', filetypes=[('JSON files', '*.json')])
        if path:
            self.settings.export_settings(path)
            messagebox.showinfo(self.t('success'), self.t('export_settings'))

    def import_settings(self):
        path = filedialog.askopenfilename(filetypes=[('JSON files', '*.json')])
        if path:
            self.settings.import_settings(path)
            messagebox.showinfo(self.t('success'), self.t('import_settings'))

    def clear_log(self):
        self.output_text.delete(1.0, tk.END)
        self.log_lines.clear()

    def browse_plugin_dir(self):
        path = filedialog.askdirectory(title=self.t('plugin_dir'))
        if path:
            self.plugin_dir_var.set(path)

    def update_history(self):
        self.history_text.delete(1.0, tk.END)
        for entry in self.settings.data.get('download_history', []):
            self.history_text.insert(tk.END, f"{entry['time']} | {entry['url']} | {entry['status']} | {entry.get('file', '')}\n")

    def setup_settings_tab(self):
        settings_frame = self.settings_frame
        settings_frame.columnconfigure(1, weight=1)
        row = 0
        # Theme selection
        self.theme_label = ttk.Label(settings_frame, text='Moaz Theme:')
        self.theme_label.grid(row=row, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 5))
        themes = ['Light', 'Dark']
        if HAS_THEMES:
            try:
                # Sort themes for consistent ordering
                themes.extend(sorted(self.root.get_themes()))
            except Exception:
                # Fallback in case ttkthemes is not fully functional
                pass
        self.theme_combo = ttk.Combobox(settings_frame, textvariable=self.theme_var,
                                       values=themes, state='readonly')
        self.theme_combo.grid(row=row, column=1, sticky="ew")
        self.theme_combo.bind('<<ComboboxSelected>>', self.change_theme)
        row += 1
        # Language selection
        self.language_label = ttk.Label(settings_frame, text='Moaz Language:')
        self.language_label.grid(row=row, column=0, sticky=tk.W, padx=(0, 10), pady=5)
        # Use display names with 'Moaz' in the script of each language
        self.language_display_names = [
            'Moaz Video Downloader',                # English
            'Moaz Descargador de Videos',           # Spanish
            'Moaz Téléchargeur de Vidéos',          # French
            'Moaz Video-Downloader',                # German
            'Moaz Downloader di Video',             # Italian
            'Moaz Baixador de Vídeos',              # Portuguese
            'Муаз Загрузчик Видео',                 # Russian
            '莫阿兹视频下载器',                        # Chinese
            'モアズ動画ダウンローダー',                 # Japanese
            'معاذ لتحميل الفيديو'                    # Arabic
        ]
        self.language_code_map = {
            'Moaz Video Downloader': 'en',
            'Moaz Descargador de Videos': 'es',
            'Moaz Téléchargeur de Vidéos': 'fr',
            'Moaz Video-Downloader': 'de',
            'Moaz Downloader di Video': 'it',
            'Moaz Baixador de Vídeos': 'pt',
            'Муаз Загрузчик Видео': 'ru',
            '莫阿兹视频下载器': 'zh',
            'モアズ動画ダウンローダー': 'ja',
            'معاذ لتحميل الفيديو': 'ar'
        }
        self.language_display_map = {v: k for k, v in self.language_code_map.items()}
        # Set the initial value of the combobox to the translated app title in the current language
        self.language_var.set(self.language_display_map.get(self.language, 'Moaz Video Downloader'))
        self.lang_combo = ttk.Combobox(settings_frame, textvariable=self.language_var,
                                      values=self.language_display_names, state='readonly')
        self.lang_combo.grid(row=row, column=1, sticky="ew")
        self.lang_combo.bind('<<ComboboxSelected>>', self.change_language)
        row += 1
        # ... rest of setup_settings_tab ...
        # Add Save and Cancel buttons at the end of the settings tab
        def save_tab_settings():
            # Update all UI variables and settings from the tab
            display_theme = self.theme_var.get()
            canonical_theme = self.theme_value_map.get(display_theme, display_theme)
            self.settings.data['theme'] = canonical_theme
            
            self.settings.data['language'] = self.language_code_to_short.get(self.language_var.get(), 'en')
            # Update current theme and language variables
            if self.theme_var.get().lower() == 'dark' or self.theme_var.get() == self.t('dark'):
                self.current_theme = 'dark'
            else:
                self.current_theme = 'light'
            # Update both self.language and self.current_language for translation
            if self.language_var.get() in self.language_short_to_code:
                self.language = self.language_short_to_code[self.language_var.get()]
                self.current_language = self.language_short_to_code[self.language_var.get()]
            else:
                self.language = 'en'
                self.current_language = 'en'
            self.settings.data['output_dir'] = self.output_dir_var.get()
            self.settings.data['parallel'] = self.parallel_var.get()
            self.settings.data['postprocess_script'] = self.postprocess_script_var.get() if hasattr(self, 'postprocess_script_var') else ''
            self.settings.data['format'] = self.format_var.get()
            self.settings.data['custom_format'] = self.custom_format_var.get()
            self.settings.data['cookie_file'] = self.cookie_file_var.get()
            self.settings.data['proxy'] = self.proxy_var.get()
            self.settings.data['enable_notifications'] = self.enable_notifications_var.get()
            self.settings.data['log_level'] = self.log_level_var.get()
            self.settings.data['file_template'] = self.file_template_var.get()
            self.settings.data['user_agent'] = self.user_agent_var.get()
            self.settings.data['bandwidth'] = self.bandwidth_var.get()
            self.settings.data['plugin_dir'] = self.plugin_dir_var.get()
            self.settings.data['skip_downloaded'] = self.skip_downloaded_var.get()
            self.settings.save()
            self.refresh_ui()
        save_btn = ttk.Button(settings_frame, text=self.t('save'), command=save_tab_settings)
        save_btn.grid(row=row, column=0, pady=10, padx=10, sticky=tk.W)
        row += 1

    def change_language(self, event=None):
        selected = self.language_var.get()
        if selected in self.language_short_to_code:
            self.language = self.language_short_to_code[selected]
            self.current_language = self.language_short_to_code[selected]
        else:
            self.language = 'en'
            self.current_language = 'en'
        self.refresh_ui()

    def refresh_ui(self):
        self.root.title(f"{self.t('title')} v{APP_VERSION}")
        # Tabs
        self.nb.tab(0, text=self.t('download'))
        self.nb.tab(1, text=self.t('batch_download'))
        self.nb.tab(2, text=self.t('settings'))
        self.nb.tab(3, text=self.t('history'))
        self.nb.tab(4, text=self.t('recent_downloads') if 'recent_downloads' in LANGUAGES['en'] else "Recent Downloads")
        # Download tab
        self.download_group.config(text=self.t('download'))
        self.url_label.config(text=self.t('url_label'))
        self.detect_formats_btn.config(text=self.t('detect_formats'))
        self.output_dir_label.config(text=self.t('output_dir_label'))
        self.browse_dir_btn.config(text=self.t('browse'))
        self.quality_label.config(text=self.t('quality'))
        self.format_label.config(text=self.t('format'))
        self.custom_format_label.config(text=self.t('custom_format'))
        self.audio_only_cb.config(text=self.t('audio_only'))
        self.playlist_cb.config(text=self.t('playlist'))
        self.cookie_file_label.config(text=self.t('cookie_file'))
        self.browse_cookie_btn.config(text=self.t('browse'))
        self.validate_cookie_btn.config(text=self.t('validate'))
        self.download_btn.config(text=self.t('download'))
        self.cancel_btn.config(text=self.t('cancel'))
        self.status_label.config(text=self.t('status'))
        self.progress_title_label.config(text=self.t('progress'))
        self.download_log_label.config(text=self.t('log'))
        
        # Batch tab
        self.batch_frame.config()
        self.batch_urls_label.config(text=self.t('batch_urls'))
        self.batch_output_dir_label.config(text=self.t('output_dir_label'))
        self.batch_browse_dir_btn.config(text=self.t('browse'))
        self.batch_quality_label.config(text=self.t('quality'))
        self.batch_audio_only_cb.config(text=self.t('audio_only'))
        self.batch_playlist_cb.config(text=self.t('playlist'))
        self.parallel_label.config(text=self.t('parallel_downloads'))
        self.batch_download_btn.config(text=self.t('batch_download'))
        self.batch_progress_label.config(textvariable=self.progress_text)
        self.recent_batch_label.config(text=self.t('recent_batch'))
        self.select_batch_btn.config(text=self.t('select_batch'))
        # Settings tab
        self.theme_label.config(text=self.t('theme'))
        self.language_label.config(text=self.t('language'))
        self.proxy_label.config(text=self.t('proxy'))
        self.notifications_cb.config(text=self.t('enable_notifications'))
        self.log_level_label.config(text=self.t('log_level'))
        self.file_template_label.config(text=self.t('file_template'))
        self.user_agent_label.config(text=self.t('user_agent'))
        self.bandwidth_label.config(text=self.t('bandwidth'))
        self.plugin_dir_label.config(text=self.t('plugin_dir'))
        self.browse_plugin_dir_btn.config(text=self.t('browse'))
        # Action buttons
        self.export_btn.config(text=self.t('export_settings'))
        self.import_btn.config(text=self.t('import_settings'))
        self.check_updates_btn.config(text=self.t('check_updates'))
        self.clear_log_btn.config(text=self.t('clear_log'))
        self.save_btn.config(text=self.t('save'))
        if hasattr(self, 'reset_btn'):
            self.reset_btn.config(text=self.t('reset_settings'))
        # History tab
        self.history_label.config(text=self.t('history'))
        self.clear_history_btn.config(text=self.t('clear_history'))
        # Recent tab
        self.recent_downloads_label.config(text=self.t('recent_downloads') if 'recent_downloads' in LANGUAGES['en'] else "Recent Downloads")
        self.remove_recent_btn.config(text=self.t('remove_recent_downloads'))
        # Menus
        self.settings_menu.entryconfig(0, label=self.t('settings'))
        self.help_menu.entryconfig(0, label=self.t('help'))
        self.help_menu.entryconfig(1, label=self.t('about'))
        self.help_menu.entryconfig(2, label=self.t('open_log_file'))
        # Theme/language combobox values
        themes = [self.t('light'), self.t('dark')]
        if HAS_THEMES:
            try:
                # Sort themes for consistent ordering
                themes.extend(sorted(self.root.get_themes()))
            except Exception:
                pass
        self.theme_combo.config(values=themes)
        # Language combobox values
        self.lang_combo.config(values=self.language_short_names)
        
        # Preserve theme selection across language change
        canonical_theme = self.settings.data.get('theme', 'light')
        display_theme = self.theme_display_map.get(canonical_theme, canonical_theme)
        self.theme_var.set(display_theme)

        # Update theme to ensure colors are correct
        self.apply_theme()
        # Update combobox values to translated names
        if hasattr(self, 'theme_combo'):
            self.theme_combo.config(values=themes)
        if hasattr(self, 'lang_combo'):
            self.lang_combo.config(values=self.language_short_names)
        # Set combobox to the short code for the current language
        self.language_var.set(self.language_code_to_short.get(self.language, 'En'))
        # Update quality comboboxes with new translations
        prev_quality_display = self.quality_combo.get()
        prev_batch_quality_display = self.batch_quality_combo.get()

        prev_quality_val = list(self.quality_value_map.keys())[list(self.quality_value_map.values()).index(prev_quality_display)] if prev_quality_display in self.quality_value_map.values() else None
        prev_batch_quality_val = list(self.quality_value_map.keys())[list(self.quality_value_map.values()).index(prev_batch_quality_display)] if prev_batch_quality_display in self.quality_value_map.values() else None


        self.quality_value_map = {
            self.t('best'): 'best',
            self.t('worst'): 'worst',
            '1080p': '1080p',
            '720p': '720p',
            '480p': '480p',
            '360p': '360p',
            '240p': '240p',
        }
        self.quality_display_map = {v: k for k, v in self.quality_value_map.items()}
        self.quality_combo['values'] = list(self.quality_value_map.keys())
        self.batch_quality_combo['values'] = list(self.quality_value_map.keys())
        
        # Restore previous selection if possible
        if prev_quality_val and prev_quality_val in self.quality_display_map:
            self.quality_combo.set(self.quality_display_map[prev_quality_val])
        else:
            self.quality_combo.set(self.t('best'))

        if prev_batch_quality_val and prev_batch_quality_val in self.quality_display_map:
            self.batch_quality_combo.set(self.quality_display_map[prev_batch_quality_val])
        else:
            self.batch_quality_combo.set(self.t('best'))

        # Update skip_downloaded_cb label
        self.skip_downloaded_cb.config(text=self.t('skip_downloaded'))

    def open_log_file(self):
        import webbrowser
        if os.path.exists(LOG_PATH):
            webbrowser.open(LOG_PATH)
        else:
            messagebox.showerror("Error", f"Could not find log file: {LOG_PATH}")

    def draw_progress_bar(self, percent):
        self.progress_canvas.delete('all')
        fill_w = 300 * percent / 100
        # Draw the green fill
        self.progress_canvas.create_rectangle(0, 0, fill_w, 20, fill="green", outline="")
        # Draw the border on top
        self.progress_canvas.create_rectangle(0, 0, 300, 20, outline="#24292E", width=2)
        # Draw the percentage text on top
        percent_text = f"{int(percent)}%"
        self.progress_canvas.create_text(150, 10, text=percent_text, fill="white", font=(None, 12, 'bold'))

    def update_progress_bar(self, percent):
        self.progress_percent.set(f"{int(percent)}%")
        self.draw_progress_bar(percent)

    def copy_log(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.output_text.get(1.0, tk.END))
        self.status_message.set("Log copied to clipboard.")

    def export_log(self):
        path = filedialog.asksaveasfilename(defaultextension='.txt', filetypes=[('Text files', '*.txt')])
        if path:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(self.output_text.get(1.0, tk.END))
            self.status_message.set(f"Log exported to {path}")

    def update_recent_downloads(self):
        self.recent_listbox.delete(0, tk.END)
        for entry in self.settings.data.get('download_history', [])[:10]:
            file_path = entry.get('file', '')
            status = entry.get('status', '')
            display = f"{entry['time']} | {entry['url']} | {status} | {file_path}"
            self.recent_listbox.insert(tk.END, display)

    def open_recent_download(self, event):
        selection = self.recent_listbox.curselection()
        if not selection:
            return
        idx = selection[0]
        entry = self.settings.data.get('download_history', [])[idx]
        file_path = entry.get('file', '')
        if file_path and os.path.exists(file_path):
            webbrowser.open(file_path)
        elif file_path:
            folder = os.path.dirname(file_path)
            if os.path.exists(folder):
                webbrowser.open(folder)
            else:
                self.status_message.set("File/folder not found.")
        else:
            self.status_message.set("No file path available.")

    def parse_progress(self, line):
        """Parse progress information from yt-dlp output and update the progress bar"""
        try:
            if '%' in line and 'ETA' in line:
                percent_match = re.search(r'(\d+\.?\d*)%', line)
                if percent_match:
                    percentage = float(percent_match.group(1))
                    self.update_progress_bar(percentage)
                    self.progress_text.set(f"Downloading... {percentage:.1f}%")
                    self.log_message(line)
                    return
            if any(keyword in line.lower() for keyword in ['downloading', 'extracting', 'merging']):
                self.progress_text.set(line.split(']')[-1].strip() if ']' in line else line)
                self.log_message(line)
        except Exception as e:
            self.log_message(f"Progress parsing error: {e}")

    def on_audio_only_toggle(self):
        if self.audio_only_var.get():
            self.quality_combo.config(state='disabled')
            self.format_combo.config(state='disabled')
            self.custom_format_entry.config(state='disabled')
        else:
            self.quality_combo.config(state='readonly')
            self.format_combo.config(state='readonly')
            self.custom_format_entry.config(state='normal')

    def clear_history(self):
        self.settings.data['download_history'] = []
        self.settings.save()
        self.update_history()
        self.update_recent_downloads()

    def remove_recent_downloads(self):
        selection = self.recent_listbox.curselection()
        if not selection:
            return
        # Remove selected entries from download_history
        history = self.settings.data['download_history']
        # The listbox shows the first 10 entries of download_history
        indices_to_remove = list(selection)
        # Remove from the start of the list (most recent first)
        for idx in sorted(indices_to_remove, reverse=True):
            if idx < len(history):
                del history[idx]
        self.settings.data['download_history'] = history
        self.settings.save()
        self.update_recent_downloads()

# --- CLI ---
def run_cli():
    import argparse
    parser = argparse.ArgumentParser(description="Universal Video Downloader (Advanced)")
    parser.add_argument("url", nargs="?", help="Video URL to download")
    parser.add_argument("-o", "--output", default=".", help="Output directory")
    parser.add_argument("-q", "--quality", default="best", choices=["best", "worst", "1080p", "720p", "480p", "360p", "240p"], help="Video quality")
    parser.add_argument("--audio", action="store_true", help="Download audio only (MP3)")
    parser.add_argument("--playlist", action="store_true", help="Download entire playlist")
    parser.add_argument("--cookies", help="Path to cookie file")
    parser.add_argument("--format", default="mp4", help="Video format (mp4, webm, etc.)")
    parser.add_argument("--custom-format", default="", help="Custom yt-dlp format string")
    parser.add_argument("--batch", help="File    containing URLs (one per line)")
    parser.add_argument("--parallel", type=int, default=2, help="Parallel downloads for batch")
    parser.add_argument("--user-agent", default="", help="Custom User-Agent string")
    parser.add_argument("--bandwidth", default="", help="Bandwidth limit in K/s")
    parser.add_argument("--plugin-dir", default="", help="Directory of post-processing plugins")
    args = parser.parse_args()
    logger = logging.getLogger("cli")
    downloader = VideoDownloader(logger, postprocess_script=args.cookies, user_agent=args.user_agent, bandwidth=args.bandwidth)
    if args.batch:
        with open(args.batch, 'r') as f:
            urls = [line.strip() for line in f if is_valid_url(line.strip())]
        results = downloader.batch_download(
            urls,
            args.output,
            args.quality,
            args.audio,
            args.playlist,
            args.cookies,
            args.parallel,
            print
        )
        success_count = sum(1 for ok in results.values() if ok)
        print(f"Batch done: {success_count}/{len(urls)} successful")
        if HAS_NOTIFICATIONS:
            try:
                notification.notify(
                    title="Universal Video Downloader",
                    message=f"Batch done: {success_count}/{len(urls)} successful",
                    timeout=3
                )
            except Exception as e:
                print(f"Notification Error: {e}")
        sys.exit(0 if success_count == len(urls) else 1)
    elif args.url:
        ok, _ = downloader.download(
            args.url,
            args.output,
            args.quality,
            args.audio,
            args.playlist,
            args.cookies,
            print
        )
        if HAS_NOTIFICATIONS:
            try:
                notification.notify(
                    title="Universal Video Downloader",
                    message="Download completed!" if ok else "Download failed!",
                    timeout=3
                )
            except Exception as e:
                print(f"Notification Error: {e}")
        sys.exit(0 if ok else 1)
    else:
        print("No URL or batch file provided.")
        sys.exit(1)

# --- Main Entrypoint ---
def main():
    global FFMPEG_PATH
    
    if len(sys.argv) > 1 and not sys.argv[1].endswith('.py'):
        run_cli()
    else:
        # If running as a PyInstaller bundle, add the bundled ffmpeg to the PATH
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            # The path to the temporary folder created by PyInstaller
            bundle_dir = getattr(sys, '_MEIPASS')
            # Add the bundle directory to the system's PATH
            os.environ['PATH'] += os.pathsep + bundle_dir
            
        # Now set FFMPEG_PATH after PATH is updated
        FFMPEG_PATH = get_ffmpeg_path()
            
        # Setup logging
        log_dir = Path.home() / "MoazDownloader"
        log_dir.mkdir(exist_ok=True)
        global LOG_PATH
        LOG_PATH = log_dir / "downloader.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(LOG_PATH, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        
        settings = Settings()
        # Set log level from settings
        log_level = settings.data.get('log_level', 'INFO').upper()
        logging.getLogger().setLevel(log_level)

        downloader = VideoDownloader(
            logger=logging.getLogger("Downloader"),
            postprocess_script=settings.data.get('postprocess_script', ''),
            proxy=settings.data.get('proxy', ''),
            user_agent=settings.data.get('user_agent', ''),
            bandwidth=settings.data.get('bandwidth', ''),
            plugin_dir=settings.data.get('plugin_dir', '')
        )
        gui = DownloaderGUI(settings, downloader)
        gui.run()

# --- Installer/Resource Helper ---
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_ffmpeg_path():
    """Get the path to ffmpeg, prioritizing the bundled one."""
    ffmpeg_name = 'ffmpeg.exe' if sys.platform == 'win32' else 'ffmpeg'
    
    # If running as a PyInstaller bundle, check the bundle directory first
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        bundle_dir = getattr(sys, '_MEIPASS')
        bundled_ffmpeg_path = os.path.join(bundle_dir, ffmpeg_name)
        if os.path.exists(bundled_ffmpeg_path):
            return bundled_ffmpeg_path
    
    # Path for bundled ffmpeg (for development)
    bundled_ffmpeg_path = resource_path(ffmpeg_name)
    
    # Check if the bundled ffmpeg exists
    if os.path.exists(bundled_ffmpeg_path):
        return bundled_ffmpeg_path
        
    # If not bundled, check the system's PATH
    return shutil.which('ffmpeg')

ICON_PATH = resource_path('moaz.ico')  # Place moaz.ico in your project root
# FFMPEG_PATH will be set in main() after PATH is updated
FFMPEG_PATH = None  # Will be initialized in main()

# --- ToolTip class for Tkinter widgets ---
class ToolTip(object):
    def __init__(self, widget, text='widget info'):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0
        self.widget.bind('<Enter>', self.enter)
        self.widget.bind('<Leave>', self.leave)

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(500, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        try:
            x, y, cx, cy = self.widget.bbox("insert")
        except Exception:
            x = y = 0
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                         background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()
if __name__ == "__main__":
    main()