# 🧪 Compound Management System v2.2

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-2.3+-green.svg)](https://flask.palletsprojects.com/)
[![GitHub release](https://img.shields.io/github/release/hashi-yu/py-compound-manager.svg)](https://github.com/hashi-yu/py-compound-manager/releases)
[![GitHub stars](https://img.shields.io/github/stars/hashi-yu/py-compound-manager.svg)](https://github.com/hashi-yu/py-compound-manager/stargazers)

**A modern, Apple-inspired chemical compound database system with hierarchical folder organization and advanced molecular weight calculations.**

[English](#english) • [日本語](#japanese) • [Demo](#demo) • [Installation](#installation) • [Documentation](#documentation)

![Screenshot](screenshot/main-interface.png)

</div>

---

## English

### 🚀 Overview

Compound Management System is a sophisticated web-based application designed for chemists, researchers, and laboratories to efficiently organize, manage, and analyze chemical compounds. Built with Flask and featuring an Apple-inspired design, it provides an intuitive interface for compound database management.

### ✨ Key Features

#### 🔬 **Compound Management**
- **Smart Organization**: Add, edit, and categorize chemical compounds with ease
- **Structure Visualization**: Upload and manage molecular structure images
- **Molecular Calculations**: Automatic molecular weight calculation with high precision
- **Formula Validation**: Real-time molecular formula validation and error checking
- **Rich Annotations**: Comprehensive notes and comments system
- **Data Integration**: Spectral data file management with 50+ supported formats

#### 📁 **Hierarchical Organization**
- **Nested Folders**: Create unlimited nested folder structures
- **Finder-Style Interface**: Intuitive sidebar navigation inspired by macOS Finder
- **Drag & Drop**: Seamless compound organization with drag-and-drop functionality
- **Smart Filtering**: Folder-specific views without subfolder content mixing
- **Visual Hierarchy**: Clean folder tree visualization with compound count badges
- **Quick Navigation**: AJAX-powered navigation with smooth transitions

#### 🎨 **Modern Interface**
- **Apple Design Language**: Refined UI following Apple's design principles
- **Responsive Design**: Optimized for desktop, tablet, and mobile devices
- **Enhanced Search**: Powerful search and local sorting capabilities
- **Visual Feedback**: Loading states and smooth animations
- **Form Validation**: Real-time input validation with helpful error messages
- **Accessibility**: Screen reader friendly with proper ARIA labels

#### ⚡ **Advanced Capabilities**
- **High-Precision Calculations**: Accurate molecular weight computations
- **File Management**: Comprehensive support for scientific data formats
- **Extension-less Files**: Support for formats like `fid`, `log`, `propcar`
- **Feedback System**: Built-in user feedback and issue reporting
- **Auto-startup**: macOS integration with automatic startup options
- **Export Features**: Data export in multiple formats

### 🛠 Installation

#### Quick Start (Recommended)
```bash
# Clone the repository
git clone https://github.com/hashi-yu/py-compound-manager.git
cd py-compound-manager

# One-click setup (macOS/Linux)
./start.command
```

#### Manual Installation
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Initialize database
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"

# Run application
python run.py
```

#### Docker Installation
```bash
# Build and run with Docker
docker build -t compound-manager .
docker run -p 8081:8081 compound-manager
```

### 📖 Usage Guide

#### Getting Started
1. **Access the Application**: Navigate to `http://localhost:8081`
2. **Create Folders**: Organize your compounds using the hierarchical folder system
3. **Add Compounds**: Use the "Add Compound" button to create new entries
4. **Upload Data**: Attach molecular structures and spectral data files
5. **Organize**: Use drag-and-drop to move compounds between folders

#### Advanced Features
- **Molecular Weight Calculation**: Enter formulas like `C6H6` for automatic calculation
- **Batch Operations**: Select multiple compounds for bulk actions
- **Data Export**: Export compound data in CSV format
- **Feedback System**: Report issues or suggest improvements via the built-in feedback modal

### 🗂 Supported File Formats

#### Spectral Data
- **NMR Data**: `fid` (extension-less), `.jdx`, `.dx`
- **Binary Data**: `.bin`, `.dat`, `.raw`, `.spc`
- **Text Data**: `.txt`, `.csv`, `.log`, `propcar`, `text`
- **Archives**: `.zip`, `.tar`, `.gz`, `.bz2`
- **Scientific**: `.h5`, `.hdf5`, `.npz`, `.npy`, `.mat`
- **Documents**: `.pdf`, `.xlsx`, `.xls`, `.docx`, `.doc`, `.ppt`, `.pptx`

#### Structure Images
- **Images**: `.png`, `.jpg`, `.jpeg`, `.gif`

### 🔧 Configuration

#### Environment Variables
Create a `.env` file in the root directory:
```env
# Security
SECRET_KEY=your-secret-key-here

# Database
DATABASE_URL=sqlite:///instance/compounds.db

# File Uploads
MAX_CONTENT_LENGTH=16777216

# Server
HOST=127.0.0.1
PORT=8081
DEBUG=False
```

#### Production Deployment
```bash
# Using Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8081 "app:create_app()"
```

### 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### 🆘 Support

- **Documentation**: [Wiki](https://github.com/hashi-yu/py-compound-manager/wiki)
- **Issues**: [GitHub Issues](https://github.com/hashi-yu/py-compound-manager/issues)
- **Discussions**: [GitHub Discussions](https://github.com/hashi-yu/py-compound-manager/discussions)

### 🙏 Acknowledgments

- Built with [Flask](https://flask.palletsprojects.com/) and [SQLAlchemy](https://www.sqlalchemy.org/)
- UI inspired by Apple's design principles
- Molecular weight calculations using scientific databases
- Community contributions and feedback

---

## Japanese

### 🚀 概要

化合物管理システムは、化学者、研究者、研究室向けに設計された高度なWebベースアプリケーションです。化学化合物の効率的な整理、管理、分析を可能にします。FlaskとAppleインスパイアドデザインで構築され、化合物データベース管理のための直感的なインターフェースを提供します。

### ✨ 主要機能

#### 🔬 **化合物管理**
- **スマート整理**: 化学化合物の追加、編集、分類を簡単に
- **構造可視化**: 分子構造画像のアップロードと管理
- **分子計算**: 高精度な分子量の自動計算
- **式検証**: リアルタイム分子式検証とエラーチェック
- **豊富な注釈**: 包括的なメモとコメントシステム
- **データ統合**: 50以上のフォーマットに対応したスペクトルデータファイル管理

#### 📁 **階層組織**
- **ネストフォルダ**: 無制限のネストフォルダ構造作成
- **Finderスタイル**: macOS Finderにインスパイアされた直感的サイドバーナビゲーション
- **ドラッグ&ドロップ**: ドラッグ&ドロップ機能によるシームレスな化合物整理
- **スマートフィルタリング**: サブフォルダ内容を混在させないフォルダ固有ビュー
- **視覚的階層**: 化合物数バッジ付きのクリーンなフォルダツリー可視化
- **クイックナビゲーション**: AJAX駆動のスムーズな遷移ナビゲーション

#### 🎨 **モダンインターフェース**
- **Appleデザイン言語**: Appleのデザイン原則に従った洗練されたUI
- **レスポンシブデザイン**: デスクトップ、タブレット、モバイルデバイス最適化
- **拡張検索**: 強力な検索とローカルソート機能
- **視覚的フィードバック**: ローディング状態とスムーズなアニメーション
- **フォーム検証**: 役立つエラーメッセージ付きリアルタイム入力検証
- **アクセシビリティ**: 適切なARIAラベル付きスクリーンリーダー対応

#### ⚡ **高度な機能**
- **高精度計算**: 正確な分子量計算
- **ファイル管理**: 科学データフォーマットの包括的サポート
- **拡張子なしファイル**: `fid`、`log`、`propcar`などのフォーマット対応
- **フィードバックシステム**: 内蔵ユーザーフィードバックと問題報告
- **自動スタートアップ**: 自動スタートアップオプション付きmacOS統合
- **エクスポート機能**: 複数フォーマットでのデータエクスポート

### 🛠 インストール

#### クイックスタート（推奨）
```bash
# リポジトリをクローン
git clone https://github.com/hashi-yu/py-compound-manager.git
cd py-compound-manager

# ワンクリックセットアップ（macOS/Linux）
./start.command
```

#### 手動インストール
```bash
# 仮想環境作成
python -m venv venv

# 仮想環境アクティベート
source venv/bin/activate  # macOS/Linux
# または
venv\Scripts\activate     # Windows

# 依存関係インストール
pip install -r requirements.txt

# データベース初期化
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"

# アプリケーション実行
python run.py
```

#### Docker インストール
```bash
# Docker でビルドと実行
docker build -t compound-manager .
docker run -p 8081:8081 compound-manager
```

### 📖 使用ガイド

#### はじめに
1. **アプリケーションアクセス**: `http://localhost:8081` にアクセス
2. **フォルダ作成**: 階層フォルダシステムを使用して化合物を整理
3. **化合物追加**: "化合物を追加" ボタンで新しいエントリを作成
4. **データアップロード**: 分子構造とスペクトルデータファイルを添付
5. **整理**: ドラッグ&ドロップでフォルダ間の化合物移動

#### 高度な機能
- **分子量計算**: `C6H6` のような式を入力して自動計算
- **バッチ操作**: 複数化合物を選択してバルクアクション
- **データエクスポート**: CSV形式での化合物データエクスポート
- **フィードバックシステム**: 内蔵フィードバックモーダルで問題報告や改善提案

### 🗂 対応ファイル形式

#### スペクトルデータ
- **NMRデータ**: `fid`（拡張子なし）、`.jdx`、`.dx`
- **バイナリデータ**: `.bin`、`.dat`、`.raw`、`.spc`
- **テキストデータ**: `.txt`、`.csv`、`.log`、`propcar`、`text`
- **アーカイブ**: `.zip`、`.tar`、`.gz`、`.bz2`
- **科学データ**: `.h5`、`.hdf5`、`.npz`、`.npy`、`.mat`
- **ドキュメント**: `.pdf`、`.xlsx`、`.xls`、`.docx`、`.doc`、`.ppt`、`.pptx`

#### 構造画像
- **画像**: `.png`、`.jpg`、`.jpeg`、`.gif`

### 🔧 設定

#### 環境変数
ルートディレクトリに `.env` ファイルを作成:
```env
# セキュリティ
SECRET_KEY=your-secret-key-here

# データベース
DATABASE_URL=sqlite:///instance/compounds.db

# ファイルアップロード
MAX_CONTENT_LENGTH=16777216

# サーバー
HOST=127.0.0.1
PORT=8081
DEBUG=False
```

#### 本番環境デプロイ
```bash
# Gunicornを使用
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8081 "app:create_app()"
```

### 🤝 コントリビューション

コントリビューションを歓迎します！詳細は[コントリビューションガイドライン](CONTRIBUTING.md)をご覧ください。

1. リポジトリをフォーク
2. フィーチャーブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを開く

### 📝 ライセンス

このプロジェクトはMITライセンスの下でライセンスされています - 詳細は[LICENSE](LICENSE)ファイルをご覧ください。

### 🆘 サポート

- **ドキュメント**: [Wiki](https://github.com/hashi-yu/py-compound-manager/wiki)
- **問題**: [GitHub Issues](https://github.com/hashi-yu/py-compound-manager/issues)
- **ディスカッション**: [GitHub Discussions](https://github.com/hashi-yu/py-compound-manager/discussions)

### 🙏 謝辞

- [Flask](https://flask.palletsprojects.com/) と [SQLAlchemy](https://www.sqlalchemy.org/) で構築
- Appleのデザイン原則にインスパイアされたUI
- 科学データベースを使用した分子量計算
- コミュニティのコントリビューションとフィードバック

---

<div align="center">

**Made with ❤️ for the scientific community**

</div>