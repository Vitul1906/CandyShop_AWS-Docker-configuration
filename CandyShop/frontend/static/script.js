let allProducts = [];
let currentFilter = 'all';

const totalCountEl = document.getElementById('total-count');
const lowstockCountEl = document.getElementById('lowstock-count');
const lastUpdatedEl = document.getElementById('last-updated');
const productsListEl = document.getElementById('products-list');
const tabButtons = document.querySelectorAll('.tab-btn');
const qInput = document.getElementById('q-input');
const refreshBtn = document.getElementById('refresh-btn');

document.addEventListener('DOMContentLoaded', ()=>{
    setupEventListeners();
    loadProducts();
});

function setupEventListeners(){
    tabButtons.forEach(btn => btn.addEventListener('click', function(){
        if(this.id === 'refresh-btn') return;
        currentFilter = this.dataset.filter;
        updateActiveTab(this);
        applyFilters();
    }));

    if(qInput) qInput.addEventListener('input', ()=> applyFilters());
    if(refreshBtn) refreshBtn.addEventListener('click', ()=> loadProducts());
}

function updateActiveTab(activeBtn){
    tabButtons.forEach(b => b.classList.remove('active'));
    activeBtn.classList.add('active');
}

async function loadProducts(){
    try{
        showLoading();
        const res = await fetch('/api/products');
        if(!res.ok) throw new Error('Erro ao buscar produtos');
        const data = await res.json();
        allProducts = data.products || [];
        totalCountEl.textContent = allProducts.length;
        lastUpdatedEl.textContent = formatDateTime(new Date().toISOString());

        try{
            const lowRes = await fetch('/api/products/lowstock?threshold=10');
            if(lowRes.ok){
                const lowData = await lowRes.json();
                lowstockCountEl.textContent = lowData.count || 0;
            } else {
                lowstockCountEl.textContent = '—';
            }
        } catch(e){ lowstockCountEl.textContent = '—'; }

        applyFilters();
        }catch(err){
            console.error(err);
            showError('Não foi possível carregar os produtos da nossa loja');
        }
}

function applyFilters(){
    const q = qInput ? qInput.value.trim().toLowerCase() : '';
    let filtered = allProducts.slice();

    if(currentFilter === 'lowstock'){
        filtered = filtered.filter(p => (p.stock||0) <= 10);
    } else if(currentFilter === 'doce'){
        filtered = filtered.filter(p => (p.category||'').toLowerCase() === 'doce');
    } else if(currentFilter === 'torta'){
        filtered = filtered.filter(p => (p.category||'').toLowerCase() === 'torta');
    }

    if(q){
        filtered = filtered.filter(p => (p.name||'').toLowerCase().includes(q) || (p.flavor||'').toLowerCase().includes(q));
    }

    renderProducts(filtered);
}

function renderProducts(products){
    if(!products || products.length === 0){
        productsListEl.innerHTML = '<div class="loading">Nenhum produto encontrado<br><small>Tente ajustar os filtros de pesquisa</small></div>';
        return;
    }

    const html = products.map(p => productHTML(p)).join('');
    productsListEl.innerHTML = html;

    document.querySelectorAll('.order-btn').forEach(btn => btn.addEventListener('click', onOrderClicked));
}

function productHTML(p){
    const stockClass = (p.stock||0) <= 10 ? 'stock-low' : 'stock-ok';
    return `
        <div class="product-item">
            <div class="product-info">
                <h3>${escapeHtml(p.name)}</h3>
                <p>${escapeHtml(p.category || '')} • ${escapeHtml(p.flavor || '')}</p>
            </div>
            <div class="product-meta">
                <div class="price">R$ ${formatPrice(p.price)}</div>
                <div class="stock ${stockClass}">Estoque: ${p.stock || 0}</div>
                <div style="margin-top:8px">
                    <input type="number" min="1" value="1" class="order-qty" data-id="${p.id}" style="width:72px;padding:6px;border-radius:6px;border:1px solid #e6d7e9;margin-right:6px" />
                    <button class="tab-btn order-btn" data-id="${p.id}">Fazer pedido</button>
                </div>
            </div>
        </div>
    `;
}

function showLoading(){ productsListEl.innerHTML = '<div class="loading">Carregando nossos doces deliciosos...</div>'; }
function showError(msg){ productsListEl.innerHTML = `<div class="error">${escapeHtml(msg)}<br><small>Tente novamente em alguns instantes</small></div>`; }

function formatPrice(v){ try{ if(typeof v === 'number') return v.toFixed(2); return Number(v).toFixed(2);} catch(e){ return v; }}
function escapeHtml(str){ if(!str && str!==0) return ''; return String(str).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])); }

function formatDateTime(isoString) {
    try {
        const date = new Date(isoString);
        const day = String(date.getDate()).padStart(2, '0');
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const year = date.getFullYear();
        const hours = String(date.getHours()).padStart(2, '0');
        const minutes = String(date.getMinutes()).padStart(2, '0');
        
        return `${day}/${month}/${year} ${hours}:${minutes}`;
    } catch (e) {
        return isoString;
    }
}

async function onOrderClicked(e){
    const id = Number(e.currentTarget.dataset.id);
    const qtyInput = document.querySelector(`.order-qty[data-id="${id}"]`);
    const qty = Math.max(1, parseInt(qtyInput.value||'1',10));

    try{
        const payload = { items: [{ product_id: id, quantity: qty }], customer: { name: 'Loja Admin'} };
        const res = await fetch('/api/orders', { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify(payload) });
        if(!res.ok){
            const txt = await res.text();
            throw new Error(txt || 'Erro ao criar pedido');
        }
        const data = await res.json();
        alert('Pedido criado com sucesso!\nTotal: R$ ' + (data.order ? data.order.total : '—') + '\n\nObrigado pela preferência!');
        await loadProducts();
    }catch(err){
        console.error(err);
        alert('Falha ao criar pedido: ' + (err.message||err) + '\n\nTente novamente ou entre em contato conosco!');
    }
}
