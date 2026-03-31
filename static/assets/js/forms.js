document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.django-form').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();

      var loading = form.querySelector('.loading');
      var errorMsg = form.querySelector('.error-message');
      var sentMsg = form.querySelector('.sent-message');

      if (loading) loading.style.display = 'block';
      if (errorMsg) { errorMsg.style.display = 'none'; errorMsg.textContent = ''; }
      if (sentMsg) sentMsg.style.display = 'none';

      var formData = new FormData(form);

      fetch(form.action, {
        method: 'POST',
        body: formData,
        headers: {
          'X-Requested-With': 'XMLHttpRequest'
        }
      })
        .then(function (response) { return response.json().then(function (data) { return { ok: response.ok, data: data }; }); })
        .then(function (result) {
          if (loading) loading.style.display = 'none';
          if (result.ok && result.data.success) {
            if (sentMsg) { sentMsg.textContent = result.data.message; sentMsg.style.display = 'block'; }
            form.reset();
          } else {
            if (errorMsg) { errorMsg.textContent = result.data.message || 'Une erreur est survenue.'; errorMsg.style.display = 'block'; }
          }
        })
        .catch(function () {
          if (loading) loading.style.display = 'none';
          if (errorMsg) { errorMsg.textContent = 'Erreur de connexion. Veuillez réessayer.'; errorMsg.style.display = 'block'; }
        });
    });
  });
});
