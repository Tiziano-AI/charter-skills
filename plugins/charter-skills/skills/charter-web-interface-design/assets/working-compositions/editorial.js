/* Adapted from Codrops OnScrollTypographyAnimations effect3 (vertical scale)
   and effect10 (blur/opacity reveal), MIT; see licenses/Codrops-MIT.txt.
   This implementation is original vanilla JS: no text-splitting, GSAP,
   smooth-scroll or analytics dependencies. Content is visible without JS. */
const titles = [...document.querySelectorAll('[data-effect3], [data-effect10]')];
const motion = matchMedia('(prefers-reduced-motion: reduce)');
const activeAnimations = new Set();
for (const title of titles) {
  for (const line of title.querySelectorAll('[data-line]')) {
    const words = line.textContent.split(' ');
    line.replaceChildren();
    words.forEach((word, index) => {
      if (index) line.append(' ');
      const wrapper = document.createElement('span');
      wrapper.className = 'word';
      for (const letter of word) {
        const char = document.createElement('span');
        char.className = 'char';
        char.textContent = letter;
        wrapper.append(char);
      }
      line.append(wrapper);
    });
  }
}
function reveal(title) {
  if (motion.matches) return;
  const chars = [...title.querySelectorAll('.char')];
  chars.forEach((char, index) => {
    const isScale = title.hasAttribute('data-effect3');
    const animation = char.animate(isScale
      ? [{ transform: 'scaleY(.35)' }, { transform: 'scaleY(1)' }]
      : [{ opacity: .5, filter: 'blur(8px)' }, { opacity: 1, filter: 'blur(0)' }],
    { duration: isScale ? 440 : 350, delay: isScale ? index * 13 : ((index * 7) % chars.length) * 12, easing: 'cubic-bezier(.2,.7,.2,1)', fill: 'backwards' });
    activeAnimations.add(animation);
    animation.finished.finally(() => activeAnimations.delete(animation)).catch(() => {});
  });
}
if ('IntersectionObserver' in window) {
  const observer = new IntersectionObserver(entries => {
    for (const entry of entries) if (entry.isIntersecting) {
      reveal(entry.target);
      observer.unobserve(entry.target);
    }
  }, { threshold: .35 });
  titles.forEach(title => observer.observe(title));
}
motion.addEventListener('change', () => { if (motion.matches) activeAnimations.forEach(animation => animation.cancel()); });
document.querySelector('#replay').addEventListener('click', () => {
  const title = titles[0];
  title.scrollIntoView({ block: 'center', behavior: 'instant' });
  title.tabIndex = -1;
  title.focus({ preventScroll: true });
  reveal(title);
  document.querySelector('#motion-status').textContent = motion.matches ? 'Reduced motion is enabled. The title remains still.' : 'Title animation replayed.';
});
