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

