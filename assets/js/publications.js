(() => {
  const form = document.querySelector('[data-publication-filters]');
  if (!form) return;

  const search = form.querySelector('[name="q"]');
  const type = form.querySelector('[name="type"]');
  const year = form.querySelector('[name="year"]');
  const reset = form.querySelector('[data-filter-reset]');
  const items = [...document.querySelectorAll('[data-publication]')];
  const groups = [...document.querySelectorAll('[data-year-group]')];
  const summary = document.querySelector('[data-results-summary]');
  const empty = document.querySelector('[data-empty-results]');

  const normalize = (value) => value.toLocaleLowerCase().trim();

  const update = () => {
    const query = normalize(search?.value || '');
    const selectedType = type?.value || 'all';
    const selectedYear = year?.value || 'all';
    let visible = 0;

    items.forEach((item) => {
      const matchesQuery = !query || normalize(item.dataset.search || '').includes(query);
      const matchesType = selectedType === 'all' || item.dataset.type === selectedType;
      const matchesYear = selectedYear === 'all' || item.dataset.year === selectedYear;
      const show = matchesQuery && matchesType && matchesYear;
      item.hidden = !show;
      if (show) visible += 1;
    });

    groups.forEach((group) => {
      group.hidden = !group.querySelector('[data-publication]:not([hidden])');
    });

    if (summary) {
      summary.textContent = `${visible} publication${visible === 1 ? '' : 's'} shown`;
    }
    if (empty) empty.style.display = visible ? 'none' : 'block';
  };

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    update();
  });
  form.addEventListener('input', update);
  form.addEventListener('change', update);
  reset?.addEventListener('click', () => {
    form.reset();
    search?.focus();
    update();
  });

  update();
})();
