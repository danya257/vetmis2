#!/bin/bash

set -e  # Прервать при ошибке

PROJECT_NAME="vetmis2"
REPO_URL="https://github.com/danya257/vetmis2.git"
ANALYSIS_DIR="vetmis2_analysis"

echo "🔍 Анализ проекта $PROJECT_NAME..."

# 1. Очистка и создание директории анализа
rm -rf "$ANALYSIS_DIR"
mkdir -p "$ANALYSIS_DIR"
cd "$ANALYSIS_DIR"

# 2. Клонирование репозитория
echo "📥 Клонирование репозитория..."
git clone "$REPO_URL" .
if [ ! -f "manage.py" ]; then
    echo "❌ manage.py не найден — убедитесь, что репозиторий содержит Django-проект."
    exit 1
fi

# 3. Поиск имени Django-проекта (папки с settings.py)
DJANGO_PROJECT=$(find . -name "settings.py" | head -n1 | sed 's|/settings.py||' | sed 's|./||')
if [ -z "$DJANGO_PROJECT" ]; then
    echo "❌ Не найден settings.py"
    exit 1
fi
echo "📁 Найден Django-проект: $DJANGO_PROJECT"

# 4. Создание .env (если отсутствует)
if [ ! -f ".env" ]; then
    echo "🔧 Создание .env для анализа..."
    cat > .env <<EOF
DEBUG=True
SECRET_KEY=analysis-temp-secret-key-for-local-use-only
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=*
EOF
fi

# 5. Установка зависимостей
if [ -f "requirements.txt" ]; then
    echo "📦 Установка зависимостей..."
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    pip install python-dotenv  # на случай, если используется
else
    echo "⚠️  requirements.txt не найден — пропускаем установку."
fi

# 6. Генерация структуры проекта
echo "🌳 Генерация структуры проекта..."
tree -I "__pycache__|*.pyc|venv|.git|node_modules" > project_structure.txt

# 7. Настройка Django (временно)
export DJANGO_SETTINGS_MODULE="${DJANGO_PROJECT}.settings"
export DATABASE_URL="sqlite:///db_analysis.sqlite3"

# 8. Создание и применение миграций
echo "🔄 Применение миграций..."
python manage.py migrate --run-syncdb

# 9. Информация о моделях
echo "📋 Список моделей и таблиц..."
python manage.py showmigrations > migrations_status.txt
python manage.py sqlmigrate $(grep -l "class.*\(models\.Model\)" */models.py | head -n1 | cut -d'/' -f1) 0001 > sample_model_sql.txt 2>/dev/null || echo "Не удалось извлечь SQL миграции" > sample_model_sql.txt

# 10. Сохранение ключевых файлов
cp manage.py .
cp -r "$DJANGO_PROJECT" ./django_project/
if [ -d "apps" ]; then cp -r apps/ ./; fi
if [ -f "requirements.txt" ]; then cp requirements.txt .; fi

# 11. Финал
echo
echo "✅ Анализ завершён!"
echo "📁 Результаты сохранены в: $(pwd)"
echo "📄 Основные файлы:"
echo "   - project_structure.txt"
echo "   - django_project/ (копия settings, urls, wsgi и т.д.)"
echo "   - db_analysis.sqlite3 (пустая БД с миграциями)"
echo "   - migrations_status.txt"