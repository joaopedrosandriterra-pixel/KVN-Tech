document.addEventListener('DOMContentLoaded', function() {
  const serviceSelect = document.getElementById('service');
  const container = document.getElementById('dynamic-questions');
  const webFields = document.getElementById('web-fields');
  const sysFields = document.getElementById('sys-fields');
  const robloxFields = document.getElementById('roblox-fields');
  const btnText = document.getElementById('submit-btn-text');

  function handleServiceChange() {
    const service = serviceSelect.value;
    // Hide all dynamic sections
    webFields.classList.add('hidden');
    sysFields.classList.add('hidden');
    robloxFields.classList.add('hidden');
    container.classList.add('hidden');

    if (service === 'Desenvolvimento Web') {
      container.classList.remove('hidden');
      webFields.classList.remove('hidden');
      btnText.textContent = '🚀 Solicitar orçamento';
    } else if (service === 'Sistema') {
      container.classList.remove('hidden');
      sysFields.classList.remove('hidden');
      btnText.textContent = '🚀 Solicitar orçamento';
    } else if (service === 'Roblox') {
      container.classList.remove('hidden');
      robloxFields.classList.remove('hidden');
      btnText.textContent = '🚀 Solicitar orçamento';
    } else if (service === 'Aplicativo' || service === 'API') {
      btnText.textContent = '🚀 Solicitar orçamento';
    } else if (service === 'Consultoria' || service === 'Outro') {
      btnText.textContent = '💬 Vamos conversar';
    }
  }

  function handleBudgetSelect(radio) {
    document.querySelectorAll('.budget-label').forEach(label => {
      label.classList.remove('border-cyan-500', 'bg-cyan-500/10', 'ring-2', 'ring-cyan-500/20');
      label.classList.add('border-slate-800', 'bg-slate-950');
    });
    if (radio.checked) {
      const label = radio.closest('.budget-label');
      label.classList.remove('border-slate-800', 'bg-slate-950');
      label.classList.add('border-cyan-500', 'bg-cyan-500/10', 'ring-2', 'ring-cyan-500/20');
    }
  }

  if (serviceSelect) {
    serviceSelect.addEventListener('change', handleServiceChange);
  }
  document.querySelectorAll('input[name="budget"]').forEach(radio => {
    radio.addEventListener('change', function() {
      handleBudgetSelect(this);
    });
  });

  // Initialise on load
  handleServiceChange();
  const checkedBudget = document.querySelector('input[name="budget"]:checked');
  if (checkedBudget) {
    handleBudgetSelect(checkedBudget);
  }
});
