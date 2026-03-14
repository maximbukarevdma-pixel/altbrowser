import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWebEngineCore import *

class ALTBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))
        self.setCentralWidget(self.browser)
        self.showMaximized()
        
        # Настройка навигационной панели
        self.setup_navigation_bar()
        
        # Настройка закладок
        self.bookmarks = []
        self.setup_bookmarks_bar()
        
        # Применение стилей
        self.apply_styles()
        
        # Установка иконки и названия
        self.setWindowTitle("ALTBrowser - Альтернативный браузер")
        self.setWindowIcon(QIcon("icon.png") if os.path.exists("icon.png") else QIcon())
        
        # Подключение сигналов
        self.browser.urlChanged.connect(self.update_urlbar)
        self.browser.loadProgress.connect(self.update_progress)
        self.browser.loadFinished.connect(self.load_finished)
        
    def setup_navigation_bar(self):
        """Создание красивой навигационной панели"""
        # Основная панель навигации
        nav_bar = QToolBar("Навигация")
        nav_bar.setIconSize(QSize(32, 32))
        nav_bar.setMovable(False)
        nav_bar.setStyleSheet("""
            QToolBar {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2b5876, stop:1 #4e4376);
                padding: 5px;
                border: none;
                spacing: 5px;
            }
            QToolButton {
                background-color: rgba(255, 255, 255, 0.1);
                border: none;
                border-radius: 5px;
                padding: 5px;
                color: white;
            }
            QToolButton:hover {
                background-color: rgba(255, 255, 255, 0.2);
            }
            QToolButton:pressed {
                background-color: rgba(255, 255, 255, 0.3);
            }
        """)
        self.addToolBar(nav_bar)
        
        # Кнопка назад
        back_btn = QAction(QIcon.fromTheme("go-previous"), "Назад", self)
        back_btn.triggered.connect(self.browser.back)
        back_btn.setShortcut(QKeySequence.Back)
        nav_bar.addAction(back_btn)
        
        # Кнопка вперед
        forward_btn = QAction(QIcon.fromTheme("go-next"), "Вперед", self)
        forward_btn.triggered.connect(self.browser.forward)
        forward_btn.setShortcut(QKeySequence.Forward)
        nav_bar.addAction(forward_btn)
        
        # Кнопка обновления
        reload_btn = QAction(QIcon.fromTheme("view-refresh"), "Обновить", self)
        reload_btn.triggered.connect(self.browser.reload)
        reload_btn.setShortcut(QKeySequence.Refresh)
        nav_bar.addAction(reload_btn)
        
        # Кнопка домой
        home_btn = QAction(QIcon.fromTheme("go-home"), "Домой", self)
        home_btn.triggered.connect(self.navigate_home)
        nav_bar.addAction(home_btn)
        
        # Строка URL
        self.urlbar = QLineEdit()
        self.urlbar.setPlaceholderText("Введите URL или поисковый запрос...")
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        self.urlbar.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 20px;
                padding: 8px 15px;
                font-size: 14px;
                selection-background-color: #4e4376;
                min-width: 400px;
            }
            QLineEdit:focus {
                border: 2px solid #4e4376;
                background-color: #f8f9fa;
            }
        """)
        nav_bar.addWidget(self.urlbar)
        
        # Кнопка добавления в закладки
        bookmark_btn = QAction(QIcon.fromTheme("bookmark-new"), "Закладка", self)
        bookmark_btn.triggered.connect(self.add_bookmark)
        nav_bar.addAction(bookmark_btn)
        
        # Кнопка меню
        menu_btn = QAction(QIcon.fromTheme("open-menu"), "Меню", self)
        menu_btn.triggered.connect(self.show_menu)
        nav_bar.addAction(menu_btn)
        
        # Индикатор загрузки
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximumWidth(100)
        self.progress_bar.setMaximumHeight(15)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 7px;
                background-color: rgba(255, 255, 255, 0.1);
                text-align: center;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00b09b, stop:1 #96c93d);
                border-radius: 5px;
            }
        """)
        nav_bar.addWidget(self.progress_bar)
        
    def setup_bookmarks_bar(self):
        """Создание панели закладок"""
        self.bookmarks_bar = QToolBar("Закладки")
        self.bookmarks_bar.setIconSize(QSize(20, 20))
        self.bookmarks_bar.setStyleSheet("""
            QToolBar {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4568DC, stop:1 #B06AB3);
                padding: 2px;
                border: none;
            }
            QToolButton {
                background-color: rgba(255, 255, 255, 0.1);
                border: none;
                border-radius: 3px;
                color: white;
                padding: 3px;
            }
            QToolButton:hover {
                background-color: rgba(255, 255, 255, 0.2);
            }
        """)
        self.addToolBarBreak()
        self.addToolBar(self.bookmarks_bar)
        
        # Добавляем стандартные закладки
        self.add_default_bookmarks()
        
    def add_default_bookmarks(self):
        """Добавление стандартных закладок"""
        bookmarks = [
            ("Google", "https://www.google.com", QIcon.fromTheme("web-browser")),
            ("YouTube", "https://www.youtube.com", QIcon.fromTheme("video")),
            ("GitHub", "https://github.com", QIcon.fromTheme("applications-development")),
            ("StackOverflow", "https://stackoverflow.com", QIcon.fromTheme("help-contents")),
        ]
        
        for name, url, icon in bookmarks:
            self.add_bookmark_to_bar(name, url, icon)
            
    def add_bookmark_to_bar(self, name, url, icon=None):
        """Добавление закладки на панель"""
        action = QAction(icon if icon else QIcon.fromTheme("bookmark"), name, self)
        action.setData(url)
        action.triggered.connect(lambda: self.browser.setUrl(QUrl(url)))
        self.bookmarks_bar.addAction(action)
        
    def add_bookmark(self):
        """Добавление текущей страницы в закладки"""
        url = self.browser.url().toString()
        title = self.browser.page().title()
        
        if url not in self.bookmarks:
            self.bookmarks.append(url)
            self.add_bookmark_to_bar(title, url)
            QMessageBox.information(self, "Закладка добавлена", 
                                   f"Страница '{title}' добавлена в закладки!")
        
    def navigate_home(self):
        """Переход на домашнюю страницу"""
        self.browser.setUrl(QUrl("https://www.google.com"))
        
    def navigate_to_url(self):
        """Навигация по URL или поиск"""
        text = self.urlbar.text()
        
        # Проверяем, является ли введенный текст URL
        if "." in text and not text.startswith(" "):
            if not text.startswith("http"):
                text = "http://" + text
            url = QUrl(text)
        else:
            # Иначе ищем в Google
            url = QUrl(f"https://www.google.com/search?q={text}")
            
        self.browser.setUrl(url)
        
    def update_urlbar(self, url):
        """Обновление URL строки"""
        self.urlbar.setText(url.toString())
        self.urlbar.setCursorPosition(0)
        
    def update_progress(self, progress):
        """Обновление индикатора прогресса"""
        self.progress_bar.setValue(progress)
        self.progress_bar.setVisible(progress < 100)
        
    def load_finished(self):
        """Действия после завершения загрузки страницы"""
        self.progress_bar.setVisible(False)
        
    def show_menu(self):
        """Показ меню браузера"""
        menu = QMenu(self)
        
        # Создаем стилизованное меню
        menu.setStyleSheet("""
            QMenu {
                background-color: white;
                border: 1px solid #4e4376;
                border-radius: 5px;
                padding: 5px;
            }
            QMenu::item {
                padding: 5px 20px;
                border-radius: 3px;
            }
            QMenu::item:selected {
                background-color: #4e4376;
                color: white;
            }
            QMenu::separator {
                height: 1px;
                background: #cccccc;
                margin: 5px 0px;
            }
        """)
        
        # Добавляем пункты меню
        new_window = menu.addAction(QIcon.fromTheme("window-new"), "Новое окно")
        new_window.triggered.connect(self.new_window)
        
        incognito = menu.addAction(QIcon.fromTheme("incognito"), "Режим инкогнито")
        incognito.triggered.connect(self.incognito_mode)
        
        menu.addSeparator()
        
        history = menu.addAction(QIcon.fromTheme("document-open-recent"), "История")
        downloads = menu.addAction(QIcon.fromTheme("download"), "Загрузки")
        
        menu.addSeparator()
        
        settings = menu.addAction(QIcon.fromTheme("preferences-system"), "Настройки")
        about = menu.addAction(QIcon.fromTheme("help-about"), "О программе")
        
        menu.exec_(QCursor.pos())
        
    def new_window(self):
        """Открытие нового окна"""
        new_browser = ALTBrowser()
        new_browser.show()
        
    def incognito_mode(self):
        """Открытие окна в режиме инкогнито"""
        QMessageBox.information(self, "Режим инкогнито", 
                               "Режим инкогнито будет доступен в следующей версии!")
        
    def apply_styles(self):
        """Применение общих стилей к окну"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QStatusBar {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2b5876, stop:1 #4e4376);
                color: white;
                padding: 2px;
            }
        """)
        
        # Создаем строку состояния
        status_bar = QStatusBar()
        status_bar.showMessage("Готов к работе")
        self.setStatusBar(status_bar)

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("ALTBrowser")
    app.setOrganizationName("ALTSoft")
    
    # Устанавливаем глобальный стиль
    app.setStyle('Fusion')
    
    # Создаем и показываем главное окно
    browser = ALTBrowser()
    browser.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()