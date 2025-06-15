"""
化学構造画像の解析と分子情報抽出モジュール

このモジュールは以下の機能を提供します：
1. OCRによるテキスト抽出
2. 化学式のパターンマッチング  
3. 外部API（PubChem等）を使用した分子データ取得
4. 画像前処理と最適化
"""

import re
import logging
from typing import Dict, Optional, Any
from PIL import Image
import requests

# OpenCV関連（条件付きインポート）
try:
    import cv2
    import numpy as np
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    logging.warning("OpenCV not available. Some image processing features will be limited.")

# Tesseract OCR関連（条件付きインポート）
try:
    import pytesseract
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False
    logging.warning("Tesseract not available. OCR features will be limited.")


class ChemicalImageAnalyzer:
    """化学構造画像解析クラス"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # 化学式のパターン（基本的なパターン）
        self.molecular_formula_patterns = [
            r'C\d*H\d*(?:O\d*)?(?:N\d*)?(?:S\d*)?(?:P\d*)?(?:Cl\d*)?(?:Br\d*)?(?:F\d*)?',
            r'[A-Z][a-z]?\d*(?:[A-Z][a-z]?\d*)*',
        ]
        
        # 分子量のパターン
        self.molecular_weight_patterns = [
            r'MW?\s*[=:]\s*(\d+\.?\d*)',
            r'(\d+\.?\d*)\s*(?:g/mol|Da|u)',
            r'(?:分子量|Molecular\s+Weight)[：:]\s*(\d+\.?\d*)',
        ]

    def analyze_image(self, image_path: str) -> Dict[str, Any]:
        """
        画像を解析して化学情報を抽出
        
        Args:
            image_path: 解析する画像のパス
            
        Returns:
            解析結果を含む辞書
        """
        result = {
            'success': False,
            'molecular_formula': None,
            'molecular_weight': None,
            'confidence': 0.0,
            'method': None,
            'error': None
        }
        
        try:
            # 1. OCRによるテキスト抽出を試行
            if TESSERACT_AVAILABLE:
                ocr_result = self._extract_text_with_ocr(image_path)
                if ocr_result['success']:
                    parsed_data = self._parse_chemical_text(ocr_result['text'])
                    if parsed_data['molecular_formula'] or parsed_data['molecular_weight']:
                        result.update(parsed_data)
                        result['success'] = True
                        result['method'] = 'OCR'
                        result['confidence'] = ocr_result['confidence']
                        return result
            
            # 2. 化学データベースAPIでの検索を試行
            api_result = self._search_chemical_databases(image_path)
            if api_result['success']:
                result.update(api_result)
                return result
                
            # 3. 基本的な画像解析
            basic_result = self._basic_image_analysis(image_path)
            if basic_result['success']:
                result.update(basic_result)
                return result
                
            result['error'] = '化学情報を抽出できませんでした'
            
        except Exception as e:
            self.logger.error(f"Image analysis failed: {str(e)}")
            result['error'] = f'解析エラー: {str(e)}'
        
        return result

    def _extract_text_with_ocr(self, image_path: str) -> Dict[str, Any]:
        """OCRを使用してテキストを抽出"""
        result = {'success': False, 'text': '', 'confidence': 0.0}
        
        if not TESSERACT_AVAILABLE:
            result['error'] = 'OCR機能が利用できません（Tesseractがインストールされていません）'
            return result
        
        try:
            # 画像の前処理
            processed_image = self._preprocess_image(image_path)
            
            # OCR実行（英語のみ）
            config = r'--oem 3 --psm 6 -l eng'
            text = pytesseract.image_to_string(processed_image, config=config)
            
            # 信頼度取得
            try:
                data = pytesseract.image_to_data(processed_image, output_type=pytesseract.Output.DICT)
                confidences = [int(conf) for conf in data['conf'] if int(conf) > 0]
                avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            except:
                avg_confidence = 50  # デフォルト値
            
            result = {
                'success': True,
                'text': text.strip(),
                'confidence': avg_confidence / 100.0
            }
            
        except Exception as e:
            self.logger.error(f"OCR extraction failed: {str(e)}")
            result['error'] = str(e)
        
        return result

    def _preprocess_image(self, image_path: str) -> Image.Image:
        """画像の前処理（コントラスト調整、ノイズ除去等）"""
        image = Image.open(image_path)
        
        if not CV2_AVAILABLE:
            return image
        
        # PIL画像をOpenCV形式に変換
        img_array = np.array(image)
        if len(img_array.shape) == 3:
            img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        else:
            img_cv = img_array
        
        # グレースケール変換
        if len(img_cv.shape) == 3:
            gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        else:
            gray = img_cv
        
        # ノイズ除去
        denoised = cv2.medianBlur(gray, 3)
        
        # コントラスト調整
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(denoised)
        
        # 二値化
        _, thresh = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # OpenCV画像をPIL画像に変換して返す
        return Image.fromarray(thresh)

    def _parse_chemical_text(self, text: str) -> Dict[str, Any]:
        """抽出されたテキストから化学情報を解析"""
        result = {
            'molecular_formula': None,
            'molecular_weight': None,
            'confidence': 0.7
        }
        
        # 分子式の抽出
        for pattern in self.molecular_formula_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                # 最も妥当な分子式を選択（長さと化学的妥当性で判断）
                formula = self._select_best_formula(matches)
                if formula:
                    result['molecular_formula'] = formula
                    break
        
        # 分子量の抽出
        for pattern in self.molecular_weight_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                try:
                    weight = float(matches[0])
                    if 10 <= weight <= 2000:  # 妥当な分子量範囲
                        result['molecular_weight'] = weight
                        break
                except ValueError:
                    continue
        
        return result

    def _select_best_formula(self, formulas: list) -> Optional[str]:
        """複数の分子式候補から最適なものを選択"""
        if not formulas:
            return None
        
        # 化学的に妥当な分子式の特徴で評価
        scored_formulas = []
        for formula in formulas:
            score = 0
            
            # 炭素から始まるか
            if formula.startswith('C'):
                score += 3
            
            # 適切な長さか
            if 3 <= len(formula) <= 20:
                score += 2
            
            # 一般的な元素を含むか
            common_elements = ['C', 'H', 'O', 'N']
            for element in common_elements:
                if element in formula:
                    score += 1
            
            scored_formulas.append((formula, score))
        
        # 最高スコアの分子式を返す
        best_formula = max(scored_formulas, key=lambda x: x[1])
        return best_formula[0] if best_formula[1] > 0 else None

    def _search_chemical_databases(self, image_path: str) -> Dict[str, Any]:
        """外部化学データベースAPIを使用した検索"""
        result = {
            'success': False,
            'molecular_formula': None,
            'molecular_weight': None,
            'method': 'API',
            'confidence': 0.8
        }
        
        try:
            # PubChem APIを使用（構造検索は制限があるため、テキスト抽出結果を使用）
            ocr_result = self._extract_text_with_ocr(image_path)
            if not ocr_result['success']:
                return result
            
            # 抽出されたテキストから化合物名を推定
            compound_names = self._extract_compound_names(ocr_result['text'])
            
            for name in compound_names:
                pubchem_result = self._query_pubchem(name)
                if pubchem_result['success']:
                    result.update(pubchem_result)
                    result['success'] = True
                    break
                    
        except Exception as e:
            self.logger.error(f"Database search failed: {str(e)}")
            result['error'] = str(e)
        
        return result

    def _extract_compound_names(self, text: str) -> list:
        """テキストから化合物名を抽出"""
        # 一般的な化合物名のパターン
        compound_patterns = [
            r'\b[A-Z][a-z]*(?:[-\s][a-z]+)*\b',  # 化合物名らしき文字列
            r'\b\d+[A-Z][a-z]*\b',  # 数字付きの化合物名
        ]
        
        names = []
        for pattern in compound_patterns:
            matches = re.findall(pattern, text)
            names.extend(matches)
        
        # 重複除去と妥当性チェック
        unique_names = []
        for name in names:
            if len(name) >= 3 and name not in unique_names:
                unique_names.append(name)
        
        return unique_names[:5]  # 上位5件に制限

    def _query_pubchem(self, compound_name: str) -> Dict[str, Any]:
        """PubChem APIで化合物情報を検索"""
        result = {'success': False}
        
        try:
            # PubChem REST APIで化合物検索
            search_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{compound_name}/property/MolecularFormula,MolecularWeight/JSON"
            
            response = requests.get(search_url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                
                if 'PropertyTable' in data and 'Properties' in data['PropertyTable']:
                    props = data['PropertyTable']['Properties'][0]
                    
                    result = {
                        'success': True,
                        'molecular_formula': props.get('MolecularFormula'),
                        'molecular_weight': props.get('MolecularWeight'),
                        'method': 'PubChem API',
                        'confidence': 0.9
                    }
                    
        except Exception as e:
            self.logger.error(f"PubChem query failed: {str(e)}")
        
        return result

    def _basic_image_analysis(self, image_path: str) -> Dict[str, Any]:
        """基本的な画像解析（フォールバック機能）"""
        result = {
            'success': False,
            'method': 'Basic Analysis',
            'confidence': 0.3
        }
        
        try:
            # 画像の基本情報から推測
            image = Image.open(image_path)
            
            # 画像サイズやファイル名から情報を推測
            # これは非常に限定的な機能
            result['success'] = True
            result['molecular_formula'] = None  # 推測不可
            result['molecular_weight'] = None   # 推測不可
            result['error'] = '画像から自動的に分子情報を抽出できませんでした。手動入力をお願いします。'
            
        except Exception as e:
            result['error'] = str(e)
        
        return result

    def validate_molecular_formula(self, formula: str) -> bool:
        """分子式の妥当性検証（molecular_calculatorを使用）"""
        try:
            from app.utils.molecular_calculator import HighPrecisionMolecularCalculator
            calculator = HighPrecisionMolecularCalculator()
            is_valid, _ = calculator.validate_molecular_formula(formula)
            return is_valid
        except Exception:
            return False

    def calculate_molecular_weight_from_formula(self, formula: str) -> Optional[float]:
        """分子式から分子量を計算（molecular_calculatorを使用）"""
        try:
            from app.utils.molecular_calculator import HighPrecisionMolecularCalculator
            calculator = HighPrecisionMolecularCalculator()
            result = calculator.calculate_molecular_weight(formula)
            return result.molecular_weight
        except Exception:
            return None