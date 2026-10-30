// Manim clip playback.
//
// A clip slide carries <video class="clip"> and one invisible
// <span class="fragment clip-play"></span>. Pressing "next" shows that
// fragment, which plays the clip from the start; pressing "next" again moves
// on. Going back hides the fragment and rewinds. Arriving on a slide
// backwards (fragments already shown) parks the clip on its last frame,
// which is the resting state every clip is designed to end on.
// data-pause="5.25" on the video stops it at that time; add a second
// <span class="fragment clip-resume"></span> after the clip-play one and the
// next press carries on from there.
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

    // Stop at data-pause until the clip-resume fragment is shown.
    const stopAt = new WeakMap();
    const watchPause = (v) => {
      clearInterval(stopAt.get(v));
      const t = Number(v.dataset.pause);
      if (!t) return;
      stopAt.set(v, setInterval(() => {
        if (v.currentTime < t) return;
        clearInterval(stopAt.get(v));
        v.pause();
        v.currentTime = t;
      }, 15));
    };

    Reveal.on('fragmentshown', (e) => {
      const cl = e.fragment.classList;
      if (!cl.contains('clip-play') && !cl.contains('clip-resume')) return;
      const v = clipOf(e.fragment);
      if (cl.contains('clip-play')) {
        v.currentTime = 0;
        watchPause(v);
      } else {
        clearInterval(stopAt.get(v));
      }
      v.play();
    });

    Reveal.on('fragmenthidden', (e) => {
      const cl = e.fragment.classList;
      if (!cl.contains('clip-play') && !cl.contains('clip-resume')) return;
      const v = clipOf(e.fragment);
      v.pause();
      if (cl.contains('clip-play')) {
        clearInterval(stopAt.get(v));
        v.currentTime = 0;
      } else {
        v.currentTime = Number(v.dataset.pause);
        watchPause(v);
      }
    });

    const park = (slide) => {
      if (!slide) return;
      slide.querySelectorAll('video.clip').forEach((v) => {
        const trigger = slide.querySelector('.fragment.clip-play');
        const played = trigger && trigger.classList.contains('visible');
        const resume = slide.querySelector('.fragment.clip-resume');
        const held = played && resume && !resume.classList.contains('visible');
        const toEnd = () => {
          v.currentTime = held ? Number(v.dataset.pause) : played ? Math.max(0, v.duration - 0.05) : 0;
        };
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
