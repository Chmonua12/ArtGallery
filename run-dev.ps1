# run-dev.ps1
Write-Host "Запуск Art Gallery System..." -ForegroundColor Green

# Проверяем, запущен ли Docker Desktop
Write-Host "1. Проверка Docker Desktop..." -ForegroundColor Cyan
$dockerInfo = docker info 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Ошибка: Docker Desktop не запущен!" -ForegroundColor Red
    Write-Host "Пожалуйста, запустите Docker Desktop и повторите попытку." -ForegroundColor Yellow
    exit 1
}

Write-Host "2. Остановка предыдущих контейнеров..." -ForegroundColor Cyan
docker-compose down

Write-Host "3. Сборка и запуск контейнеров..." -ForegroundColor Cyan
docker-compose up -d --build

Write-Host "`n4. Ожидание запуска SQL Server (30 секунд)..." -ForegroundColor Cyan
Start-Sleep -Seconds 30

Write-Host "`n5. Проверка статуса контейнеров..." -ForegroundColor Cyan
docker-compose ps

Write-Host "`n6. Проверка работы Liquibase..." -ForegroundColor Cyan
docker logs artgallery-liquibase --tail 10

Write-Host "`n7. API доступно по адресам:" -ForegroundColor Green
Write-Host "   - HTTP:  http://localhost:5000" -ForegroundColor Yellow
Write-Host "   - HTTPS: https://localhost:5001" -ForegroundColor Yellow
Write-Host "   - Swagger UI: https://localhost:5001/swagger" -ForegroundColor Yellow

Write-Host "`n8. Примеры запросов:" -ForegroundColor Cyan
Write-Host "   - Получить всех художников: curl http://localhost:5000/api/artists" -ForegroundColor Gray
Write-Host "   - Получить все музеи: curl http://localhost:5000/api/museums" -ForegroundColor Gray
Write-Host "   - Получить все картины: curl http://localhost:5000/api/paintings" -ForegroundColor Gray

Write-Host "`nГотово! Система Art Gallery запущена." -ForegroundColor Green