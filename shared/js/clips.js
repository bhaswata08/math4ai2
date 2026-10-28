// Manim clip playback.
//
// A clip slide carries <video class="clip"> and one invisible
// <span class="fragment clip-play"></span>. Pressing "next" shows that
// fragment, which plays the clip from the start; pressing "next" again moves
// on. Going back hides the fragment and rewinds. Arriving on a slide
// backwards (fragments already shown) parks the clip on its last frame,
// which is the resting state every clip is designed to end on.
// Clicking a clip pauses or resumes it. data-rate="0.6" on the video plays
// it slower (or faster) than recorded.
window.Clips = {
  attach(Reveal) {
    const clipOf = (el) => el.closest('section').querySelector('video.clip');

    document.querySelectorAll('.reveal video.clip').forEach((v) => {
      v.muted = true;
      v.playsInline = true;
      v.preload = 'auto';
      if (v.dataset.rate) v.defaultPlaybackRate = v.playbackRate = Number(v.dataset.rate);
      v.addEventListener('click', () => (v.paused ? v.play() : v.pause()));
    });

    Reveal.on('fragmentshown', (e) => {
      if (!e.fragment.classList.contains('clip-play')) return;
      const v = clipOf(e.fragment);
      v.currentTime = 0;
      v.play();
    });

    Reveal.on('fragmenthidden', (e) => {
      if (!e.fragment.classList.contains('clip-play')) return;
      const v = clipOf(e.fragment);
      v.pause();
      v.currentTime = 0;
    });

    const park = (slide) => {
      if (!slide) return;
      slide.querySelectorAll('video.clip').forEach((v) => {
        const trigger = slide.querySelector('.fragment.clip-play');
        const played = trigger && trigger.classList.contains('visible');
        const toEnd = () => { v.currentTime = played ? Math.max(0, v.duration - 0.05) : 0; };
        if (v.readyState >= 1) toEnd(); else v.addEventListener('loadedmetadata', toEnd, { once: true });
      });
    };

    Reveal.on('slidechanged', (e) => {
      e.previousSlide?.querySelectorAll('video.clip').forEach((v) => v.pause());
      park(e.currentSlide);
    });
    park(Reveal.getCurrentSlide());
  },
};
