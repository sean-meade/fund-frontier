setTimeout(function () {
    let messages = document.getElementById("msg");
    let alert = new bootstrap.Alert(messages);
    alert.close();
  }, 2000);

function confirmRemove() {
  const actions = document.getElementbyName('action_remove');
  if (actions.length) {
    const message = actions[0].getAttribute('data-message');
    actions[0].addEventListener('click', function (e) {
      if (!confirm(message)) {
        e.preventDefault();
      }
    });
  }
}

confirmRemove();
