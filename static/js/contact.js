document.addEventListener('DOMContentLoaded', function() {
  const serviceSelect = document.getElementById('service');
  const container = document.getElementById('dynamic-questions');
  const webFields = document.getElementById('web-fields');
  const sysFields = document.getElementById('sys-fields');
  const robloxFields = document.getElementById('roblox-fields');
  const btnText = document.getElementById('submit-btn-text');

  // Guard: only run form logic if the form elements exist (user is authenticated)
  if (!serviceSelect || !container) return;

  function handleServiceChange() {
    const service = serviceSelect.value;

    // Hide all dynamic sections
    if (webFields) webFields.classList.add('hidden');
    if (sysFields) sysFields.classList.add('hidden');
    if (robloxFields) robloxFields.classList.add('hidden');
    container.classList.add('hidden');

    if (service === 'Desenvolvimento Web') {
      container.classList.remove('hidden');
      if (webFields) webFields.classList.remove('hidden');
      if (btnText) btnText.innerHTML = '🚀 Solicitar orçamento';
    } else if (service === 'Sistema') {
      container.classList.remove('hidden');
      if (sysFields) sysFields.classList.remove('hidden');
      if (btnText) btnText.innerHTML = '🚀 Solicitar orçamento';
    } else if (service === 'Roblox') {
      container.classList.remove('hidden');
      if (robloxFields) robloxFields.classList.remove('hidden');
      if (btnText) btnText.innerHTML = '🚀 Solicitar orçamento';
    } else if (service === 'Aplicativo' || service === 'API') {
      if (btnText) btnText.innerHTML = '🚀 Solicitar orçamento';
    } else if (service === 'Consultoria' || service === 'Outro') {
      if (btnText) btnText.innerHTML = '💬 Vamos conversar';
    }
  }

  function handleBudgetSelect(radio) {
    // Remove active state from all labels
    document.querySelectorAll('.budget-label').forEach(function(label) {
      label.removeAttribute('data-selected');
      label.style.borderColor = '';
      label.style.backgroundColor = '';
      label.style.boxShadow = '';
      label.style.color = '';
    });

    if (radio && radio.checked) {
      var label = radio.closest('.budget-label');
      if (label) {
        label.setAttribute('data-selected', 'true');
        label.style.borderColor = 'rgb(6 182 212)'; // cyan-500
        label.style.backgroundColor = 'rgba(6, 182, 212, 0.12)';
        label.style.boxShadow = '0 0 0 2px rgba(6, 182, 212, 0.25), 0 0 12px rgba(6, 182, 212, 0.15)';
        // Also update the text color inside
        var span = label.querySelector('span');
        if (span) span.style.color = 'rgb(103 232 249)'; // cyan-300
      }
    }
  }

  // Reset label text colors when deselected
  function resetBudgetLabels() {
    document.querySelectorAll('.budget-label span').forEach(function(span) {
      span.style.color = '';
    });
  }

  // Listen to both 'change' and 'input' for maximum browser compatibility
  serviceSelect.addEventListener('change', handleServiceChange);
  serviceSelect.addEventListener('input', handleServiceChange);

  document.querySelectorAll('input[name="budget"]').forEach(function(radio) {
    radio.addEventListener('change', function() {
      resetBudgetLabels();
      handleBudgetSelect(this);
    });
  });

  // Make the entire label area clickable and react immediately (fixes mobile/touch issues)
  document.querySelectorAll('.budget-label').forEach(function(label) {
    label.addEventListener('click', function() {
      var radio = this.querySelector('input[type="radio"]');
      if (radio) {
        radio.checked = true;
        resetBudgetLabels();
        handleBudgetSelect(radio);
      }
    });
  });

  // Initialise on load
  handleServiceChange();
  var checkedBudget = document.querySelector('input[name="budget"]:checked');
  if (checkedBudget) {
    handleBudgetSelect(checkedBudget);
  }
});
