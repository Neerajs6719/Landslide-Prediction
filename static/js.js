window.onload = function () {
    let currentSlide = 0;
    const slider = document.getElementById('imageSlider');
    const slides = slider.children;
  
    function updateSlider() {
      const slideWidth = slider.clientWidth;
      slider.style.transform = `translateX(-${currentSlide * slideWidth}px)`;
    }
  
    window.moveSlide = function (direction) {
      currentSlide = (currentSlide + direction + slides.length) % slides.length;
      updateSlider();
    };
  
    window.addEventListener('resize', updateSlider);
    setInterval(() => moveSlide(1), 4000);
    updateSlider();
  };
  