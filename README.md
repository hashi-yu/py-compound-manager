# 化合物データ管理システム

研究用の化合物データを効率的に管理するためのWebアプリケーションです。化合物の構造式、分子情報、スペクトルデータ（NMR、IR、MS、HPLC等）を一元管理し、プロジェクトごとに分類できます。

## 技術スタック

- **Backend**: Python 3.12, Flask 2.3.3
- **Database**: SQLite (SQLAlchemy ORM)
- **Frontend**: HTML5, Bootstrap 5.1.3, JavaScript
- **File Upload**: Werkzeug
- **Image Processing**: Pillow

## 機能概要

### ✅ 実装済み機能

#### 化合物管理
- **化合物登録**: 名前、分子式、分子量、構造式画像、メモの登録
- **化合物編集**: 全ての情報の更新が可能
- **化合物削除**: 化合物本体とすべての関連データの完全削除
- **化合物一覧**: カード形式での視覚的な一覧表示

#### プロジェクト管理
- **プロジェクト作成**: プロジェクト名と説明で分類を作成
- **プロジェクト編集**: プロジェクト情報の更新
- **プロジェクト削除**: プロジェクト削除（関連化合物は未分類になる）
- **プロジェクト別表示**: ドロップダウンでプロジェクト別に化合物をフィルタリング

#### スペクトルデータ管理
- **対応データ種類**: 1H NMR, 13C NMR, IR, MS, HPLC, その他
- **ファイルアップロード**: 各種スペクトルデータファイルの保存
- **ファイルダウンロード**: アップロードしたデータの取得
- **データ削除**: 不要なスペクトルデータの削除

#### 構造式管理
- **画像アップロード**: PNG, JPG, JPEG, GIF形式の構造式画像
- **画像表示**: 一覧および詳細画面での構造式表示
- **画像更新**: 既存画像の置き換え
- **画像削除**: 構造式画像の削除

#### UI/UX
- **レスポンシブデザイン**: Bootstrap使用のモバイル対応
- **直感的ナビゲーション**: 分かりやすいメニュー構成
- **視覚的フィードバック**: 操作結果のフラッシュメッセージ
- **確認ダイアログ**: 削除操作時の安全確認

## データベース設計

### テーブル構成

#### Project（プロジェクト）
- `id`: 主キー
- `name`: プロジェクト名（必須）
- `description`: 説明（任意）
- `created_date`: 作成日時
- `updated_date`: 更新日時

#### Compound（化合物）
- `id`: 主キー
- `name`: 化合物名（必須）
- `molecular_formula`: 分子式（任意）
- `molecular_weight`: 分子量（任意）
- `structure_image`: 構造式画像パス（任意）
- `notes`: メモ（任意）
- `project_id`: プロジェクト外部キー（任意）
- `created_date`: 作成日時
- `updated_date`: 更新日時

#### SpectralData（スペクトルデータ）
- `id`: 主キー
- `compound_id`: 化合物外部キー（必須）
- `data_type`: データ種類（1H NMR, 13C NMR等）
- `filename`: 保存ファイル名
- `original_filename`: 元ファイル名
- `file_path`: ファイルパス
- `notes`: メモ（任意）
- `upload_date`: アップロード日時

## プロジェクト構造

```
py-compound-manager/
├── app/
│   ├── __init__.py              # Flaskアプリケーション初期化
│   ├── models/                  # データモデル
│   │   ├── __init__.py
│   │   ├── compound.py          # 化合物・スペクトルデータモデル
│   │   └── project.py           # プロジェクトモデル
│   ├── routes/                  # ルーティング
│   │   ├── __init__.py
│   │   └── main.py              # メインルート（全機能）
│   ├── static/                  # 静的ファイル
│   │   └── css/
│   │       └── style.css        # カスタムCSS
│   ├── templates/               # テンプレート
│   │   ├── base.html            # ベーステンプレート
│   │   ├── index.html           # ホーム画面
│   │   ├── add_compound.html    # 化合物登録
│   │   ├── edit_compound.html   # 化合物編集
│   │   ├── compound_detail.html # 化合物詳細
│   │   ├── projects.html        # プロジェクト一覧
│   │   ├── add_project.html     # プロジェクト登録
│   │   └── edit_project.html    # プロジェクト編集
│   └── uploads/                 # アップロードファイル
│       ├── structures/          # 構造式画像
│       └── data/                # スペクトルデータ
├── config/
│   └── config.py                # アプリケーション設定
├── requirements.txt             # Python依存関係
├── run.py                       # アプリケーション起動
├── .env.example                 # 環境変数例
├── .gitignore                   # Git除外設定
└── README.md                    # このファイル
```

## セットアップ手順

### 1. 環境準備

```bash
# リポジトリクローン
git clone <repository-url>
cd py-compound-manager

# 仮想環境作成・有効化
python -m venv venv
source venv/bin/activate  # macOS/Linux
# または
venv\Scripts\activate     # Windows

# 依存関係インストール
pip install -r requirements.txt
```

### 2. 環境変数設定（任意）

```bash
# .envファイル作成（.env.exampleを参考）
cp .env.example .env
```

### 3. アプリケーション起動

```bash
python run.py
```

アプリケーションが `http://localhost:8080` で起動します。

## 使用方法

### 基本的なワークフロー

1. **プロジェクト作成**
   - ナビゲーション「プロジェクト」→「新しいプロジェクトを追加」
   - プロジェクト名と説明を入力

2. **化合物登録**
   - 「化合物追加」をクリック
   - 必要な情報を入力（プロジェクト選択も可能）
   - 構造式画像をアップロード

3. **スペクトルデータ追加**
   - 化合物詳細画面で「データアップロード」
   - データ種類を選択してファイルをアップロード

4. **プロジェクト別表示**
   - ホーム画面のプロジェクトセレクターで絞り込み

## 開発履歴

### v1.0.0 - 初期実装 (コミット: 8eda9d8)
- 基本的な化合物管理機能
- 構造式画像機能
- スペクトルデータ管理
- CRUD操作の完全実装

### v1.1.0 - プロジェクト機能追加 (コミット: 4ceff99)
- プロジェクトモデルの追加
- 化合物のプロジェクト分類機能
- プロジェクト管理UI
- フィルタリング機能

## 今後の拡張可能性

### 提案される機能

#### 検索・フィルタリング強化
- [ ] 化合物名での部分一致検索
- [ ] 分子式・分子量範囲での検索
- [ ] 複合条件での詳細検索

#### データ分析機能
- [ ] プロジェクト統計情報
- [ ] スペクトルデータ統計
- [ ] エクスポート機能（CSV、PDF）

#### ユーザー管理
- [ ] ユーザー認証システム
- [ ] プロジェクトアクセス権限管理
- [ ] ユーザー別履歴管理

#### データ拡張
- [ ] 化合物の物理的性質データ
- [ ] 実験ノート機能
- [ ] 化学反応情報

#### UI/UX改善
- [ ] ダークモード対応
- [ ] ドラッグ&ドロップアップロード
- [ ] 高度な画像表示機能

## ライセンス

このプロジェクトは研究・教育目的で開発されました。

## 技術サポート

### 依存関係更新

```bash
pip freeze > requirements.txt
```

### データベース操作

```bash
# データベースリセット（開発時のみ）
rm -f instance/compounds.db
python -c "from run import app, db; app.app_context().push(); db.create_all()"
```

### 開発時の注意事項

- アップロードファイルは `.gitignore` で除外済み
- 本番環境では `SECRET_KEY` とデータベース設定を変更すること
- SQLiteは開発用途、本番ではPostgreSQL等を推奨

---

**最終更新**: 2025年6月14日  
**開発者**: Claude Code Assistant