from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, send_from_directory, current_app
from werkzeug.utils import secure_filename
from app import db
from app.models import Compound, SpectralData, Project
from app.utils.molecular_calculator import HighPrecisionMolecularCalculator
import os
import uuid
import logging

main_bp = Blueprint('main', __name__)

def allowed_file(filename):
    from flask import current_app
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@main_bp.route('/')
def index():
    project_id = request.args.get('project_id', type=int)
    if project_id:
        compounds = Compound.query.filter_by(project_id=project_id).order_by(Compound.updated_date.desc()).all()
        current_project = Project.query.get(project_id)
    else:
        compounds = Compound.query.order_by(Compound.updated_date.desc()).all()
        current_project = None
    
    projects = Project.query.order_by(Project.name).all()
    return render_template('index.html', compounds=compounds, projects=projects, current_project=current_project)

@main_bp.route('/compound/<int:compound_id>')
def compound_detail(compound_id):
    compound = Compound.query.get_or_404(compound_id)
    return render_template('compound_detail.html', compound=compound)

@main_bp.route('/add_compound', methods=['GET', 'POST'])
def add_compound():
    if request.method == 'POST':
        name = request.form['name']
        molecular_formula = request.form.get('molecular_formula', '').strip()
        molecular_weight_str = request.form.get('molecular_weight', '').strip()
        notes = request.form.get('notes', '')
        project_id = request.form.get('project_id') or None
        
        # 分子量の処理：空文字列またはNoneの場合はNoneを設定
        molecular_weight = None
        if molecular_weight_str:
            try:
                molecular_weight = float(molecular_weight_str)
            except ValueError:
                molecular_weight = None
        
        # 分子式が空文字列の場合はNoneを設定
        if not molecular_formula:
            molecular_formula = None
        
        compound = Compound(
            name=name,
            molecular_formula=molecular_formula,
            molecular_weight=molecular_weight,
            project_id=project_id,
            notes=notes
        )
        
        # 構造式画像のアップロード
        if 'structure_image' in request.files:
            file = request.files['structure_image']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                unique_filename = str(uuid.uuid4()) + '_' + filename
                file_path = os.path.join('structures', unique_filename)
                full_path = os.path.join(current_app.config['UPLOAD_FOLDER'], file_path)
                file.save(full_path)
                compound.structure_image = file_path
        
        db.session.add(compound)
        db.session.commit()
        flash('化合物が正常に追加されました。', 'success')
        return redirect(url_for('main.compound_detail', compound_id=compound.id))
    
    projects = Project.query.order_by(Project.name).all()
    return render_template('add_compound.html', projects=projects)

@main_bp.route('/upload_data/<int:compound_id>', methods=['POST'])
def upload_spectral_data(compound_id):
    compound = Compound.query.get_or_404(compound_id)
    
    if 'data_file' not in request.files:
        flash('ファイルが選択されていません。', 'error')
        return redirect(url_for('main.compound_detail', compound_id=compound_id))
    
    file = request.files['data_file']
    if file.filename == '':
        flash('ファイルが選択されていません。', 'error')
        return redirect(url_for('main.compound_detail', compound_id=compound_id))
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        unique_filename = str(uuid.uuid4()) + '_' + filename
        file_path = os.path.join('data', unique_filename)
        full_path = os.path.join(current_app.config['UPLOAD_FOLDER'], file_path)
        file.save(full_path)
        
        spectral_data = SpectralData(
            compound_id=compound_id,
            data_type=request.form.get('data_type', ''),
            filename=unique_filename,
            original_filename=filename,
            file_path=file_path,
            notes=request.form.get('data_notes', '')
        )
        
        db.session.add(spectral_data)
        db.session.commit()
        flash('スペクトルデータが正常にアップロードされました。', 'success')
    else:
        flash('許可されていないファイル形式です。', 'error')
    
    return redirect(url_for('main.compound_detail', compound_id=compound_id))

@main_bp.route('/download/<int:data_id>')
def download_file(data_id):
    spectral_data = SpectralData.query.get_or_404(data_id)
    return send_from_directory(
        current_app.config['UPLOAD_FOLDER'],
        spectral_data.file_path,
        as_attachment=True,
        download_name=spectral_data.original_filename
    )

@main_bp.route('/structure_image/<path:filename>')
def structure_image(filename):
    return send_from_directory(
        os.path.join(current_app.config['UPLOAD_FOLDER'], 'structures'),
        filename
    )

@main_bp.route('/edit_compound/<int:compound_id>', methods=['GET', 'POST'])
def edit_compound(compound_id):
    compound = Compound.query.get_or_404(compound_id)
    
    if request.method == 'POST':
        compound.name = request.form['name']
        
        molecular_formula = request.form.get('molecular_formula', '').strip()
        molecular_weight_str = request.form.get('molecular_weight', '').strip()
        compound.notes = request.form.get('notes', '')
        compound.project_id = request.form.get('project_id') or None
        
        # 分子量の処理
        compound.molecular_weight = None
        if molecular_weight_str:
            try:
                compound.molecular_weight = float(molecular_weight_str)
            except ValueError:
                compound.molecular_weight = None
        
        # 分子式の処理
        compound.molecular_formula = molecular_formula if molecular_formula else None
        
        # 構造式画像の更新
        if 'structure_image' in request.files:
            file = request.files['structure_image']
            if file and file.filename != '' and allowed_file(file.filename):
                # 古い画像ファイルを削除
                if compound.structure_image:
                    old_file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], compound.structure_image)
                    if os.path.exists(old_file_path):
                        os.remove(old_file_path)
                
                filename = secure_filename(file.filename)
                unique_filename = str(uuid.uuid4()) + '_' + filename
                file_path = os.path.join('structures', unique_filename)
                full_path = os.path.join(current_app.config['UPLOAD_FOLDER'], file_path)
                file.save(full_path)
                compound.structure_image = file_path
        
        db.session.commit()
        flash('化合物情報が更新されました。', 'success')
        return redirect(url_for('main.compound_detail', compound_id=compound_id))
    
    projects = Project.query.order_by(Project.name).all()
    return render_template('edit_compound.html', compound=compound, projects=projects)

@main_bp.route('/delete_structure/<int:compound_id>', methods=['POST'])
def delete_structure(compound_id):
    compound = Compound.query.get_or_404(compound_id)
    
    if compound.structure_image:
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], compound.structure_image)
        if os.path.exists(file_path):
            os.remove(file_path)
        compound.structure_image = None
        db.session.commit()
        flash('構造式画像が削除されました。', 'success')
    else:
        flash('削除する構造式画像がありません。', 'error')
    
    return redirect(url_for('main.compound_detail', compound_id=compound_id))

@main_bp.route('/delete_spectral_data/<int:data_id>', methods=['POST'])
def delete_spectral_data(data_id):
    spectral_data = SpectralData.query.get_or_404(data_id)
    compound_id = spectral_data.compound_id
    
    # ファイルを削除
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], spectral_data.file_path)
    if os.path.exists(file_path):
        os.remove(file_path)
    
    db.session.delete(spectral_data)
    db.session.commit()
    flash('スペクトルデータが削除されました。', 'success')
    
    return redirect(url_for('main.compound_detail', compound_id=compound_id))

@main_bp.route('/delete_compound/<int:compound_id>', methods=['POST'])
def delete_compound(compound_id):
    compound = Compound.query.get_or_404(compound_id)
    compound_name = compound.name  # 削除前に名前を保存
    
    # 構造式画像ファイルを削除
    if compound.structure_image:
        structure_file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], compound.structure_image)
        if os.path.exists(structure_file_path):
            os.remove(structure_file_path)
    
    # 関連するスペクトルデータのファイルを削除
    for spectral_data in compound.spectral_data:
        data_file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], spectral_data.file_path)
        if os.path.exists(data_file_path):
            os.remove(data_file_path)
    
    # データベースから化合物を削除（関連するスペクトルデータも自動削除される）
    db.session.delete(compound)
    db.session.commit()
    
    flash(f'化合物「{compound_name}」が削除されました。', 'success')
    return redirect(url_for('main.index'))

@main_bp.route('/projects')
def projects():
    projects = Project.query.order_by(Project.updated_date.desc()).all()
    return render_template('projects.html', projects=projects)

@main_bp.route('/add_project', methods=['GET', 'POST'])
def add_project():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form.get('description', '')
        
        project = Project(
            name=name,
            description=description
        )
        
        db.session.add(project)
        db.session.commit()
        flash('プロジェクトが正常に追加されました。', 'success')
        return redirect(url_for('main.projects'))
    
    return render_template('add_project.html')

@main_bp.route('/edit_project/<int:project_id>', methods=['GET', 'POST'])
def edit_project(project_id):
    project = Project.query.get_or_404(project_id)
    
    if request.method == 'POST':
        project.name = request.form['name']
        project.description = request.form.get('description', '')
        
        db.session.commit()
        flash('プロジェクトが更新されました。', 'success')
        return redirect(url_for('main.projects'))
    
    return render_template('edit_project.html', project=project)

@main_bp.route('/delete_project/<int:project_id>', methods=['POST'])
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    project_name = project.name
    
    # プロジェクトに属する化合物のproject_idをNullに設定
    compounds = Compound.query.filter_by(project_id=project_id).all()
    for compound in compounds:
        compound.project_id = None
    
    db.session.delete(project)
    db.session.commit()
    
    flash(f'プロジェクト「{project_name}」が削除されました。関連する化合物は未分類になりました。', 'success')
    return redirect(url_for('main.projects'))

# =====================================
# API エンドポイント（画像解析機能）
# =====================================

@main_bp.route('/api/analyze-image', methods=['POST'])
def analyze_image_api():
    """画像解析APIエンドポイント（無効化）"""
    return jsonify({
        'success': False,
        'error': '画像解析機能は現在無効化されています'
    }), 503

@main_bp.route('/api/calculate-molecular-weight', methods=['POST'])
def calculate_molecular_weight_api():
    """高精度分子量計算APIエンドポイント"""
    try:
        data = request.get_json()
        if not data or 'formula' not in data:
            return jsonify({
                'success': False,
                'error': '分子式が指定されていません'
            }), 400
        
        formula = data['formula'].strip()
        if not formula:
            return jsonify({
                'success': False,
                'error': '分子式が空です'
            }), 400
        
        # 高精度分子量計算システムを使用
        calculator = HighPrecisionMolecularCalculator()
        
        # 分子式の妥当性チェック
        is_valid, validation_error = calculator.validate_molecular_formula(formula)
        if not is_valid:
            return jsonify({
                'success': False,
                'error': validation_error or '無効な分子式です'
            }), 400
        
        # 高精度分子量計算実行
        result = calculator.calculate_molecular_weight(formula)
        
        if result.molecular_weight is None:
            return jsonify({
                'success': False,
                'error': result.error or '分子量を計算できませんでした',
                'method': result.method,
                'source': result.source
            }), 400
        
        return jsonify({
            'success': True,
            'molecular_weight': result.molecular_weight,
            'formula': result.formula,
            'confidence': result.confidence,
            'method': result.method,
            'source': result.source,
            'precision': result.precision,
            'compound_name': result.compound_name,
            'cas_number': result.cas_number,
            'calculation_info': {
                'precision_digits': result.precision,
                'confidence_percent': round(result.confidence * 100, 1),
                'data_source': result.source,
                'calculation_method': result.method
            }
        })
        
    except Exception as e:
        logging.error(f"High-precision molecular weight calculation API error: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'計算処理でエラーが発生しました: {str(e)}'
        }), 500

@main_bp.route('/api/validate-molecular-formula', methods=['POST'])
def validate_molecular_formula_api():
    """分子式検証APIエンドポイント"""
    try:
        data = request.get_json()
        if not data or 'formula' not in data:
            return jsonify({
                'success': False,
                'error': '分子式が指定されていません'
            }), 400
        
        formula = data['formula'].strip()
        calculator = HighPrecisionMolecularCalculator()
        
        is_valid, error_message = calculator.validate_molecular_formula(formula)
        
        return jsonify({
            'success': True,
            'is_valid': is_valid,
            'error_message': error_message,
            'formula': formula
        })
        
    except Exception as e:
        logging.error(f"Formula validation API error: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'検証処理でエラーが発生しました: {str(e)}'
        }), 500

@main_bp.route('/api/calculation-info', methods=['GET'])
def get_calculation_info_api():
    """計算システム情報取得APIエンドポイント"""
    try:
        calculator = HighPrecisionMolecularCalculator()
        info = calculator.get_calculation_info()
        
        return jsonify({
            'success': True,
            'info': info
        })
        
    except Exception as e:
        logging.error(f"Calculation info API error: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'情報取得でエラーが発生しました: {str(e)}'
        }), 500