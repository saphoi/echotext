// SOBRE AS BARRINHAS DE ACESSIBILIDADE
const hamburguer = document.querySelector('.hamburguer');
const hamburguerIcon = document.querySelector('.hamburguer i');
const dropDownMenu = document.querySelector('.dropdown-menu');

hamburguer.addEventListener('click', function () {
  dropDownMenu.classList.toggle('open');
  const isOpen = dropDownMenu.classList.contains('open');
  
  // Alterna entre o ícone de barras e o X
  if (isOpen) {
    hamburguerIcon.classList.remove('fa-bars');
    hamburguerIcon.classList.add('fa-x');
  } else {
    hamburguerIcon.classList.remove('fa-x');
    hamburguerIcon.classList.add('fa-bars');
  }
});

// SOBRE O CURSOR! NAO MEXEEEEE!

document.addEventListener('DOMContentLoaded', () => {
  // Cria o elemento da bola
  const cursor = document.createElement('div');
  cursor.classList.add('cursor');
  document.body.appendChild(cursor);

  // Atualiza a posição da bola com base no movimento do mouse
  document.addEventListener('mousemove', (e) => {
    cursor.style.left = `${e.pageX}px`;
    cursor.style.top = `${e.pageY}px`;
  });
});

// SOBRE O ALTO CONTRASTE:

// Seleciona o checkbox e o body
const toggleSwitch = document.querySelector('.toggle-switch input[type="checkbox"]');
const body = document.body;

// Adiciona um evento de clique ao checkbox
toggleSwitch.addEventListener('change', () => {
    body.classList.toggle('high-contrast'); // Alterna a classe


    if (body.classList.contains('high-contrast')) {
        localStorage.setItem('high-contrast', 'enabled');
    } else {
        localStorage.removeItem('high-contrast');
    }
});

// Verifica se a configuração de alto contraste foi salva anteriormente
if (localStorage.getItem('high-contrast') === 'enabled') {
    body.classList.add('high-contrast');
    toggleSwitch.checked = true;
}

// Lógica de controlar o aúdio
function sendCommand(command) {
    fetch("/audio/control", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ command })
    })
    .then(response => response.json())
    .then(data => updateStatus(data.status || data.error))
    .catch(err => console.error(err));
}

function updateStatus(status) {
    document.getElementById("status").textContent = `Status: ${status}`;
}

document.getElementById("play-btn").addEventListener("click", function () {
    sendCommand("play");
    document.getElementById("pause-btn").disabled = false;
    document.getElementById("stop-btn").disabled = false;

    updateStatus("Áudio carregado, reproduzindo...");
});

document.getElementById("pause-btn").addEventListener("click", function () {
    sendCommand("pause");
    document.getElementById("unpause-btn").disabled = false;

    updateStatus("Pausado");
});

document.getElementById("unpause-btn").addEventListener("click", function () {
    sendCommand("unpause");
    document.getElementById("unpause-btn").disabled = true;

    updateStatus("Continuando...");
});

document.getElementById("stop-btn").addEventListener("click", function () {
    sendCommand("stop");
    document.getElementById("pause-btn").disabled = true;
    document.getElementById("unpause-btn").disabled = true;
    document.getElementById("stop-btn").disabled = true;

    updateStatus("Áudio parado");
});