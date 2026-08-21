// Função para alternar visibilidade de formulários
function toggleForm(formId) {
    const form = document.getElementById(formId);
    if (form) {
        form.classList.toggle('hidden');
    }
}

// Fechar alertas automaticamente após 5 segundos
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => {
                alert.style.display = 'none';
            }, 300);
        }, 5000);
    });

    // Confirmação antes de deletar
    const deleteButtons = document.querySelectorAll('.btn-delete');
    deleteButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            if (!confirm('Tem certeza que deseja deletar este item?')) {
                e.preventDefault();
            }
        });
    });

    // Validação de formulários
    const forms = document.querySelectorAll('.form-main');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;

            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    field.style.borderColor = '#e74c3c';
                    isValid = false;
                } else {
                    field.style.borderColor = '';
                }
            });

            if (!isValid) {
                e.preventDefault();
                showAlert('Por favor, preencha todos os campos obrigatórios!', 'danger');
            }
        });
    });

    // Validação de datas
    const dateInputs = document.querySelectorAll('input[type="date"]');
    dateInputs.forEach(input => {
        input.addEventListener('change', function() {
            const date = new Date(this.value);
            const today = new Date();
            today.setHours(0, 0, 0, 0);

            if (this.name.includes('limite') && date < today) {
                showAlert('Data limite não pode ser no passado!', 'warning');
            }
        });
    });

    // Busca em tabelas
    const searchInputs = document.querySelectorAll('.search-input');
    searchInputs.forEach(input => {
        input.addEventListener('keyup', function() {
            filterTable(this);
        });
    });
});

// Função para mostrar alertas dinâmicos
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.innerHTML = `
        <i class="fas fa-${getIconByType(type)}"></i>
        <span>${message}</span>
    `;

    const mainContent = document.querySelector('.main-content');
    if (mainContent) {
        mainContent.insertBefore(alertDiv, mainContent.firstChild);

        setTimeout(() => {
            alertDiv.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => {
                alertDiv.remove();
            }, 300);
        }, 5000);
    }
}

// Função para retornar ícone baseado no tipo de alerta
function getIconByType(type) {
    const icons = {
        'success': 'check-circle',
        'danger': 'exclamation-circle',
        'warning': 'exclamation-triangle',
        'info': 'info-circle'
    };
    return icons[type] || 'info-circle';
}

// Função para filtrar tabelas
function filterTable(input) {
    const table = input.closest('.table-container')?.querySelector('.table');
    if (!table) return;

    const filter = input.value.toLowerCase();
    const rows = table.querySelectorAll('tbody tr');

    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(filter) ? '' : 'none';
    });
}

// Função para formatar data no padrão brasileiro
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('pt-BR');
}

// Função para formatar moeda
function formatCurrency(value) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(value);
}

// Função para validar email
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Função para formatar telefone
function formatPhone(phone) {
    const cleaned = phone.replace(/\D/g, '');
    if (cleaned.length === 11) {
        return `(${cleaned.slice(0, 2)}) ${cleaned.slice(2, 7)}-${cleaned.slice(7)}`;
    }
    return phone;
}

// Função para exportar tabela para CSV
function exportTableToCSV(tableId, filename = 'tabela.csv') {
    const table = document.getElementById(tableId);
    if (!table) return;

    let csv = [];
    const rows = table.querySelectorAll('tr');

    rows.forEach(row => {
        const cols = row.querySelectorAll('td, th');
        const csvRow = [];
        cols.forEach(col => {
            csvRow.push('"' + col.textContent.replace(/"/g, '""') + '"');
        });
        csv.push(csvRow.join(','));
    });

    downloadCSV(csv.join('\n'), filename);
}

// Função para fazer download de CSV
function downloadCSV(csv, filename) {
    const csvFile = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(csvFile);
    link.setAttribute('href', url);
    link.setAttribute('download', filename);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// Função para imprimir tabela
function printTable(tableId) {
    const table = document.getElementById(tableId);
    if (!table) return;

    const printWindow = window.open('', '', 'height=400,width=800');
    printWindow.document.write('<html><head><title>Imprimir Tabela</title>');
    printWindow.document.write('<link rel="stylesheet" href="{{ url_for("static", filename="css/style.css") }}">');
    printWindow.document.write('</head><body>');
    printWindow.document.write(table.outerHTML);
    printWindow.document.write('</body></html>');
    printWindow.document.close();
    printWindow.print();
}

// Função para gerar relatório
function generateReport(reportType) {
    const data = {
        tipo: reportType,
        data_inicio: document.getElementById('data_inicio')?.value,
        data_fim: document.getElementById('data_fim')?.value
    };

    fetch('/api/relatorio', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showAlert('Relatório gerado com sucesso!', 'success');
            downloadCSV(data.csv, `relatorio_${reportType}.csv`);
        } else {
            showAlert('Erro ao gerar relatório: ' + data.message, 'danger');
        }
    })
    .catch(error => {
        showAlert('Erro na comunicação com o servidor', 'danger');
    });
}

// Animação de carregamento
function showLoading(show = true) {
    let loader = document.getElementById('loader');
    if (!loader) {
        loader = document.createElement('div');
        loader.id = 'loader';
        loader.className = 'loader';
        loader.innerHTML = '<div class="spinner"></div>';
        document.body.appendChild(loader);
    }
    loader.style.display = show ? 'flex' : 'none';
}

// Função para validar força da senha
function validatePassword(password) {
    const strength = {
        weak: /^.{1,5}$/.test(password),
        medium: /^.{6,10}$/.test(password),
        strong: /^.{11,}$/.test(password) && /[a-z]/.test(password) && /[A-Z]/.test(password) && /[0-9]/.test(password)
    };
    return strength;
}

// Função para atualizar contador de caracteres
function updateCharCount(input, maxLength = null) {
    const counter = input.nextElementSibling;
    if (counter && counter.classList.contains('char-count')) {
        const count = input.value.length;
        counter.textContent = maxLength ? `${count}/${maxLength}` : `${count}`;
    }
}

// Função para sincronizar hora e data em tempo real
function updateDateTime() {
    const now = new Date();
    const dateTimeElements = document.querySelectorAll('.current-datetime');
    dateTimeElements.forEach(el => {
        el.textContent = now.toLocaleString('pt-BR');
    });
}

// Atualizar data e hora a cada segundo
setInterval(updateDateTime, 1000);

// Animação de slide out para alertas
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOut {
        to {
            transform: translateY(-20px);
            opacity: 0;
        }
    }
    
    .loader {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.7);
        display: none;
        align-items: center;
        justify-content: center;
        z-index: 9999;
    }
    
    .spinner {
        border: 4px solid #f3f3f3;
        border-top: 4px solid #3498db;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
`;
document.head.appendChild(style);
