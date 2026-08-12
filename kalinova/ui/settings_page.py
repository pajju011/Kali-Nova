# pyrefly: ignore [missing-import]
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QFrame, QMessageBox
)
# pyrefly: ignore [missing-import]
from PyQt6.QtCore import Qt
from config import load_config, save_config, resolve_api_key
from core.ai_copilot import AIWorkerThread

class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("settingsPageContainer")

        # Cyber Dark Theme Styling
        self.setStyleSheet("""
            QWidget#settingsPageContainer {
                background-color: #0b1220;
            }
            QFrame.settingsCard {
                background-color: #0e1728;
                border: 1px solid #1c2a47;
                border-radius: 12px;
                padding: 20px;
            }
            QLabel.settingLabel {
                color: #8ea2c5;
                font-family: 'Segoe UI', sans-serif;
                font-size: 13px;
                font-weight: 600;
            }
            QLineEdit, QComboBox {
                background-color: #152238;
                border: 1px solid #283a5e;
                border-radius: 8px;
                color: #e2e8f0;
                padding: 10px;
                font-family: 'Segoe UI', monospace;
                font-size: 13px;
            }
            QLineEdit:focus, QComboBox:focus {
                border-color: #00f0ff;
            }
            QPushButton.primaryBtn {
                background-color: #00f0ff;
                color: #0b1220;
                font-weight: bold;
                padding: 12px 24px;
                border-radius: 8px;
                border: none;
                font-size: 13px;
            }
            QPushButton.primaryBtn:hover {
                background-color: #38bdf8;
            }
            QPushButton.secondaryBtn {
                background-color: #1e293b;
                color: #94a3b8;
                font-weight: bold;
                padding: 12px 24px;
                border-radius: 8px;
                border: 1px solid #334155;
                font-size: 13px;
            }
            QPushButton.secondaryBtn:hover {
                background-color: #334155;
                color: #f8fafc;
            }
        """)

        # Main Layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(24, 20, 24, 20)
        main_layout.setSpacing(20)

        # Header Title
        header_title = QLabel("⚙️ SYSTEM & AI COPILOT SETTINGS")
        header_title.setStyleSheet("font-size: 22px; font-weight: 800; color: #00f0ff; letter-spacing: 1px;")
        
        header_sub = QLabel("Configure per-user AI providers, API credentials, and runtime application behavior.")
        header_sub.setStyleSheet("font-size: 12px; color: #64748b;")

        main_layout.addWidget(header_title)
        main_layout.addWidget(header_sub)

        # Settings Form Card
        card = QFrame()
        card.setProperty("class", "settingsCard")
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(16)

        # 1. AI Provider Choice
        provider_lbl = QLabel("AI Copilot Provider:")
        provider_lbl.setProperty("class", "settingLabel")
        self.provider_combo = QComboBox()
        self.provider_combo.addItems([
            "Google Gemini API",
            "OpenAI API",
            "Ollama (Local Offline)",
            "Heuristic Rules (Offline)"
        ])
        self.provider_combo.currentIndexChanged.connect(self._on_provider_changed)

        # 2. API Key Entry
        apikey_lbl = QLabel("AI Provider API Key:")
        apikey_lbl.setProperty("class", "settingLabel")
        
        key_layout = QHBoxLayout()
        self.apikey_input = QLineEdit()
        self.apikey_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.apikey_input.setPlaceholderText("Enter your Gemini or OpenAI API key...")

        self.toggle_key_btn = QPushButton("Show")
        self.toggle_key_btn.setFixedWidth(60)
        self.toggle_key_btn.setStyleSheet("background: #1e293b; color: #94a3b8; border-radius: 6px; padding: 6px;")
        self.toggle_key_btn.clicked.connect(self._toggle_key_visibility)

        key_layout.addWidget(self.apikey_input)
        key_layout.addWidget(self.toggle_key_btn)

        # 3. Model Name Input
        model_lbl = QLabel("Model Name / Identifier:")
        model_lbl.setProperty("class", "settingLabel")
        self.model_input = QLineEdit()
        self.model_input.setPlaceholderText("e.g. gemini-1.5-flash, gpt-4o-mini, llama3:8b, deepseek-r1")

        # 4. Ollama URL Input
        ollama_lbl = QLabel("Ollama Base URL (Local AI):")
        ollama_lbl.setProperty("class", "settingLabel")
        self.ollama_input = QLineEdit()
        self.ollama_input.setPlaceholderText("http://localhost:11434")

        # 5. App Mode
        mode_lbl = QLabel("Application Execution Mode:")
        mode_lbl.setProperty("class", "settingLabel")
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Professional", "Beginner"])

        # Assembly to Card
        card_layout.addWidget(provider_lbl)
        card_layout.addWidget(self.provider_combo)
        
        card_layout.addWidget(apikey_lbl)
        card_layout.addLayout(key_layout)

        card_layout.addWidget(model_lbl)
        card_layout.addWidget(self.model_input)

        card_layout.addWidget(ollama_lbl)
        card_layout.addWidget(self.ollama_input)

        card_layout.addWidget(mode_lbl)
        card_layout.addWidget(self.mode_combo)

        main_layout.addWidget(card)

        # Action Buttons Layout
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)

        self.save_btn = QPushButton("💾 Save Configuration")
        self.save_btn.setProperty("class", "primaryBtn")
        self.save_btn.clicked.connect(self.save_settings)

        self.test_btn = QPushButton("🧪 Test AI Connection")
        self.test_btn.setProperty("class", "secondaryBtn")
        self.test_btn.clicked.connect(self.test_ai_connection)

        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.test_btn)
        btn_layout.addStretch()

        main_layout.addLayout(btn_layout)

        # Status Label
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("font-size: 13px; font-weight: bold; padding-top: 8px;")
        main_layout.addWidget(self.status_label)

        main_layout.addStretch()
        self.setLayout(main_layout)

        # Load existing config into fields
        self.load_settings_to_ui()

    def load_settings_to_ui(self):
        config = load_config()
        provider = config.get("ai_provider", "gemini").lower()

        provider_map = {
            "gemini": 0,
            "openai": 1,
            "ollama": 2,
            "heuristic": 3
        }
        self.provider_combo.setCurrentIndex(provider_map.get(provider, 0))
        self.apikey_input.setText(config.get("api_key", ""))
        self.model_input.setText(config.get("model", "gemini-1.5-flash"))
        self.ollama_input.setText(config.get("ollama_url", "http://localhost:11434"))

        mode = config.get("app_mode", "Professional")
        self.mode_combo.setCurrentIndex(0 if mode == "Professional" else 1)

        self._on_provider_changed()


    def _on_provider_changed(self):
        idx = self.provider_combo.currentIndex()
        if idx == 0:  # Gemini
            self.apikey_input.setEnabled(True)
            self.model_input.setEnabled(True)
            self.ollama_input.setEnabled(False)
            env_key = resolve_api_key("gemini")
            if env_key and not self.apikey_input.text():
                self.apikey_input.setPlaceholderText("Loaded from environment (GEMINI_API_KEY / GOOGLE_API_KEY)")
            else:
                self.apikey_input.setPlaceholderText("Enter your Gemini API key...")
            if not self.model_input.text() or self.model_input.text() in ["gpt-4o-mini", "llama3:8b", "gemini-1.5-flash"]:
                self.model_input.setText("gemini-2.0-flash")
        elif idx == 1:  # OpenAI
            self.apikey_input.setEnabled(True)
            self.model_input.setEnabled(True)
            self.ollama_input.setEnabled(False)
            env_key = resolve_api_key("openai")
            if env_key and not self.apikey_input.text():
                self.apikey_input.setPlaceholderText("Loaded from environment (OPENAI_API_KEY)")
            else:
                self.apikey_input.setPlaceholderText("Enter your OpenAI API key...")
            if not self.model_input.text() or self.model_input.text() in ["gemini-1.5-flash", "gemini-2.0-flash", "llama3:8b"]:
                self.model_input.setText("gpt-4o-mini")
        elif idx == 2:  # Ollama
            self.apikey_input.setEnabled(False)
            self.model_input.setEnabled(True)
            self.ollama_input.setEnabled(True)
            if not self.model_input.text() or self.model_input.text() in ["gemini-1.5-flash", "gemini-2.0-flash", "gpt-4o-mini"]:
                self.model_input.setText("llama3:8b")
        else:  # Heuristic
            self.apikey_input.setEnabled(False)
            self.model_input.setEnabled(False)
            self.ollama_input.setEnabled(False)


    def _toggle_key_visibility(self):
        if self.apikey_input.echoMode() == QLineEdit.EchoMode.Password:
            self.apikey_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.toggle_key_btn.setText("Hide")
        else:
            self.apikey_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.toggle_key_btn.setText("Show")

    def save_settings(self):
        idx = self.provider_combo.currentIndex()
        provider_keys = ["gemini", "openai", "ollama", "heuristic"]
        selected_provider = provider_keys[idx]

        config = {
            "ai_provider": selected_provider,
            "api_key": self.apikey_input.text().strip(),
            "model": self.model_input.text().strip(),
            "ollama_url": self.ollama_input.text().strip(),
            "app_mode": self.mode_combo.currentText()
        }

        if save_config(config):
            self.status_label.setText("✅ Configuration saved successfully to user-isolated storage!")
            self.status_label.setStyleSheet("color: #2ecc71; font-size: 13px; font-weight: bold;")
        else:
            self.status_label.setText("❌ Failed to save configuration.")
            self.status_label.setStyleSheet("color: #f43f5e; font-size: 13px; font-weight: bold;")

    def test_ai_connection(self):
        self.save_settings()
        self.status_label.setText("🔄 Testing AI connection...")
        self.status_label.setStyleSheet("color: #00f0ff; font-size: 13px; font-weight: bold;")
        self.test_btn.setEnabled(False)

        self.worker = AIWorkerThread(context_info="Test diagnostic ping.", user_prompt="Respond with 'System Online' if connection is active.")
        self.worker.finished_signal.connect(self._on_test_finished)
        self.worker.error_signal.connect(self._on_test_error)
        self.worker.start()

    def _on_test_finished(self, response: str):
        self.test_btn.setEnabled(True)
        if "Error" in response or "❌" in response or "⚠️" in response:
            self.status_label.setText(f"{response[:120]}...")
            self.status_label.setStyleSheet("color: #f43f5e; font-size: 13px; font-weight: bold;")
        else:
            self.status_label.setText("✅ AI Connection Test Successful!")
            self.status_label.setStyleSheet("color: #2ecc71; font-size: 13px; font-weight: bold;")
            QMessageBox.information(self, "AI Connection Test", f"Response from AI:\n\n{response[:300]}")

    def _on_test_error(self, err_msg: str):
        self.test_btn.setEnabled(True)
        self.status_label.setText(f"❌ Connection Error: {err_msg}")
        self.status_label.setStyleSheet("color: #f43f5e; font-size: 13px; font-weight: bold;")