// Global JS for rifas
document.addEventListener('DOMContentLoaded', function() {
    initGlobal();
});

function initGlobal() {

  const modal = document.getElementById('imageModal');
  const modalImg = document.getElementById('modalImage');
  const closeBtn = document.querySelector('.modal__close');

  document.querySelectorAll('.gallery__item img').forEach(img => {
    img.addEventListener('click', () => {
      modal.style.display = 'flex';
      modalImg.src = img.src;
    });
  });

  closeBtn.addEventListener('click', () => {
    modal.style.display = 'none';
  });

  // Cierra el modal al hacer clic fuera de la imagen
  modal.addEventListener('click', (e) => {
    if (e.target === modal) {
      modal.style.display = 'none';
    }
  });

};
