from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, send_from_directory, current_app
from werkzeug.utils import secure_filename
from app import db
from app.models import Compound, SpectralData
import os
import uuid

main_bp = Blueprint('main', __name__)

def allowed_file(filename):
    from flask import current_app
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@main_bp.route('/')
def index():
    compounds = Compound.query.order_by(Compound.updated_date.desc()).all()
    return render_template('index.html', compounds=compounds)

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
    
    return render_template('add_compound.html')

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
        print(f"POST request received for compound {compound_id}")
        print(f"Form data: {dict(request.form)}")
        compound.name = request.form['name']
        
        molecular_formula = request.form.get('molecular_formula', '').strip()
        molecular_weight_str = request.form.get('molecular_weight', '').strip()
        compound.notes = request.form.get('notes', '')
        
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
    
    return render_template('edit_compound.html', compound=compound)

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