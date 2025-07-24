"""
Простое веб-приложение для управления задачами
Flask + SQLite + Bootstrap

Технологии: Python Flask, SQLite, HTML/CSS/JS
Архитектура: Monolithic Web Application
"""

from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
import sqlite3
from datetime import datetime
import os

# Создаем Flask приложение
app = Flask(__name__)
app.secret_key = 'your-secret-key-for-flash-messages'

# Конфигурация базы данных
DATABASE = 'tasks.db'

def init_db():
    """Инициализация базы данных"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Создаем таблицу задач
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            priority TEXT DEFAULT 'medium',
            status TEXT DEFAULT 'todo',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP
        )
    ''')
    
    # Добавляем тестовые данные, если таблица пустая
    cursor.execute('SELECT COUNT(*) FROM tasks')
    if cursor.fetchone()[0] == 0:
        sample_tasks = [
            ('Изучить Flask', 'Освоить основы веб-разработки на Python', 'high', 'todo'),
            ('Создать веб-приложение', 'Разработать систему управления задачами', 'medium', 'in_progress'),
            ('Написать документацию', 'Создать README для проекта', 'low', 'todo'),
            ('Подготовить презентацию', 'Показать проект преподавателю', 'medium', 'todo'),
        ]
        
        cursor.executemany(
            'INSERT INTO tasks (title, description, priority, status) VALUES (?, ?, ?, ?)', 
            sample_tasks
        )
    
    conn.commit()
    conn.close()

def get_db_connection():
    """Получить соединение с базой данных"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Позволяет обращаться к столбцам по имени
    return conn

@app.route('/')
def index():
    """Главная страница"""
    conn = get_db_connection()
    tasks = conn.execute('''
        SELECT * FROM tasks 
        ORDER BY 
            CASE 
                WHEN priority = 'high' THEN 1
                WHEN priority = 'medium' THEN 2
                WHEN priority = 'low' THEN 3
            END,
            created_at DESC
    ''').fetchall()
    conn.close()
    
    # Статистика для главной страницы
    total_tasks = len(tasks)
    completed_tasks = len([t for t in tasks if t['status'] == 'done'])
    todo_tasks = len([t for t in tasks if t['status'] == 'todo'])
    in_progress_tasks = len([t for t in tasks if t['status'] == 'in_progress'])
    
    stats = {
        'total': total_tasks,
        'completed': completed_tasks,
        'todo': todo_tasks,
        'in_progress': in_progress_tasks,
        'completion_rate': round((completed_tasks / total_tasks * 100) if total_tasks > 0 else 0, 1)
    }
    
    return render_template('index.html', tasks=tasks, stats=stats)

@app.route('/tasks')
def tasks():
    """Страница всех задач"""
    conn = get_db_connection()
    
    # Фильтрация по статусу и приоритету
    status_filter = request.args.get('status', '')
    priority_filter = request.args.get('priority', '')
    
    query = 'SELECT * FROM tasks WHERE 1=1'
    params = []
    
    if status_filter:
        query += ' AND status = ?'
        params.append(status_filter)
    
    if priority_filter:
        query += ' AND priority = ?'
        params.append(priority_filter)
    
    query += ' ORDER BY created_at DESC'
    
    tasks = conn.execute(query, params).fetchall()
    conn.close()
    
    return render_template('tasks.html', tasks=tasks, 
                         current_status=status_filter, 
                         current_priority=priority_filter)

@app.route('/add_task', methods=['GET', 'POST'])
def add_task():
    """Добавить новую задачу"""
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        priority = request.form['priority']
        
        if not title:
            flash('Название задачи обязательно!', 'error')
            return redirect(url_for('add_task'))
        
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO tasks (title, description, priority) VALUES (?, ?, ?)',
            (title, description, priority)
        )
        conn.commit()
        conn.close()
        
        flash('Задача успешно добавлена!', 'success')
        return redirect(url_for('index'))
    
    return render_template('add_task.html')

@app.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    """Редактировать задачу"""
    conn = get_db_connection()
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        priority = request.form['priority']
        status = request.form['status']
        
        # Если задача помечена как выполненная, добавляем время завершения
        completed_at = None
        if status == 'done':
            completed_at = datetime.now().isoformat()
        
        conn.execute(
            'UPDATE tasks SET title=?, description=?, priority=?, status=?, completed_at=? WHERE id=?',
            (title, description, priority, status, completed_at, task_id)
        )
        conn.commit()
        conn.close()
        
        flash('Задача обновлена!', 'success')
        return redirect(url_for('index'))
    
    task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    conn.close()
    
    if not task:
        flash('Задача не найдена!', 'error')
        return redirect(url_for('index'))
    
    return render_template('edit_task.html', task=task)

@app.route('/delete_task/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    """Удалить задачу"""
    conn = get_db_connection()
    conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    
    flash('Задача удалена!', 'success')
    return redirect(url_for('index'))

@app.route('/toggle_task/<int:task_id>', methods=['POST'])
def toggle_task(task_id):
    """Быстро изменить статус задачи (выполнено/не выполнено)"""
    conn = get_db_connection()
    task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    
    if task:
        new_status = 'done' if task['status'] != 'done' else 'todo'
        completed_at = datetime.now().isoformat() if new_status == 'done' else None
        
        conn.execute(
            'UPDATE tasks SET status = ?, completed_at = ? WHERE id = ?',
            (new_status, completed_at, task_id)
        )
        conn.commit()
    
    conn.close()
    return redirect(url_for('index'))

# API endpoints для AJAX запросов
@app.route('/api/tasks', methods=['GET'])
def api_get_tasks():
    """API: Получить все задачи в JSON формате"""
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tasks ORDER BY created_at DESC').fetchall()
    conn.close()
    
    # Конвертируем в список словарей
    tasks_list = []
    for task in tasks:
        tasks_list.append({
            'id': task['id'],
            'title': task['title'],
            'description': task['description'],
            'priority': task['priority'],
            'status': task['status'],
            'created_at': task['created_at'],
            'completed_at': task['completed_at']
        })
    
    return jsonify(tasks_list)

@app.route('/api/tasks', methods=['POST'])
def api_create_task():
    """API: Создать новую задачу"""
    data = request.get_json()
    
    if not data or not data.get('title'):
        return jsonify({'error': 'Title is required'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO tasks (title, description, priority) VALUES (?, ?, ?)',
        (data['title'], data.get('description', ''), data.get('priority', 'medium'))
    )
    
    task_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return jsonify({'id': task_id, 'message': 'Task created successfully'}), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def api_update_task(task_id):
    """API: Обновить задачу"""
    data = request.get_json()
    
    conn = get_db_connection()
    
    # Проверяем существование задачи
    task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    if not task:
        conn.close()
        return jsonify({'error': 'Task not found'}), 404
    
    # Обновляем задачу
    completed_at = None
    if data.get('status') == 'done':
        completed_at = datetime.now().isoformat()
    
    conn.execute(
        'UPDATE tasks SET title=?, description=?, priority=?, status=?, completed_at=? WHERE id=?',
        (
            data.get('title', task['title']),
            data.get('description', task['description']),
            data.get('priority', task['priority']),
            data.get('status', task['status']),
            completed_at,
            task_id
        )
    )
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Task updated successfully'})

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def api_delete_task(task_id):
    """API: Удалить задачу"""
    conn = get_db_connection()
    
    # Проверяем существование задачи
    task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    if not task:
        conn.close()
        return jsonify({'error': 'Task not found'}), 404
    
    # Удаляем задачу
    conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Task deleted successfully'})

@app.route('/api/stats')
def api_stats():
    """API: Получить статистику задач"""
    conn = get_db_connection()
    
    stats = {}
    stats['total'] = conn.execute('SELECT COUNT(*) FROM tasks').fetchone()[0]
    stats['todo'] = conn.execute('SELECT COUNT(*) FROM tasks WHERE status = "todo"').fetchone()[0]
    stats['in_progress'] = conn.execute('SELECT COUNT(*) FROM tasks WHERE status = "in_progress"').fetchone()[0]
    stats['done'] = conn.execute('SELECT COUNT(*) FROM tasks WHERE status = "done"').fetchone()[0]
    
    # Статистика по приоритетам
    stats['high_priority'] = conn.execute('SELECT COUNT(*) FROM tasks WHERE priority = "high"').fetchone()[0]
    stats['medium_priority'] = conn.execute('SELECT COUNT(*) FROM tasks WHERE priority = "medium"').fetchone()[0]
    stats['low_priority'] = conn.execute('SELECT COUNT(*) FROM tasks WHERE priority = "low"').fetchone()[0]
    
    conn.close()
    
    return jsonify(stats)

if __name__ == '__main__':
    # Инициализируем базу данных при запуске
    init_db()
    
    # Запускаем веб-сервер
    print("🚀 Запуск веб-приложения...")
    print("📱 Откройте браузер: http://localhost:5000")
    print("📊 API документация: http://localhost:5000/api/tasks")
    print("❌ Для остановки нажмите Ctrl+C")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 