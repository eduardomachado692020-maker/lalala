MG ERP — Estrutura Separada (Skeleton)
======================================

Como rodar (Windows PowerShell):
1) cd "C:\caminho\para\MG_ERP_v2_skeleton"
2) python -m venv .venv
3) .\.venv\Scripts\Activate.ps1
4) pip install -r requirements.txt
5) python init_db.py   (opcional — cria um erp.db de exemplo)
6) python app.py
Abra: http://127.0.0.1:5000  e/ou  http://127.0.0.1:5000/dashboard

Pasta/Arquivos
- app.py                -> app Flask
- init_db.py            -> cria erp.db com tabelas mínimas e dados de exemplo
- requirements.txt      -> dependências
- templates/            -> HTML (base.html, dashboard.html)
- static/css/style.css  -> estilos
- static/js/app.js      -> JS
- scripts/start_dev.ps1 / start_dev.bat -> inícios rápidos

Observações
- Esta é uma base limpa para colar/portar o código das suas rotas e templates antigos.
- Se você já tem um erp.db seu, basta copiar para esta mesma pasta e pular o init_db.py.
