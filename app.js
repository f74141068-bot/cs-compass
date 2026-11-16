(function () {
'use strict';
const search = document.querySelector('#search');
if (search) {
  const cards = [...document.querySelectorAll('.note-card')];
  const buttons = [...document.querySelectorAll('[data-filter]')];
  let category = 'all';
  function update() {
    const query = search.value.trim().toLocaleLowerCase();
    let count = 0;
    for (const card of cards) {
      const matched = (category === 'all' || card.dataset.category === category) && card.dataset.search.toLocaleLowerCase().includes(query);
      card.hidden = !matched;
      if (matched) count++;
    }
    document.querySelector('#result-count').textContent = `共 ${count} 篇筆記`;
    document.querySelector('#empty').hidden = count !== 0;
  }
  buttons.forEach(button => button.addEventListener('click', () => {
    category = button.dataset.filter;
    buttons.forEach(b => b.setAttribute('aria-pressed', String(b === button)));
    update();
  }));
  search.addEventListener('input', update);
}

})();
