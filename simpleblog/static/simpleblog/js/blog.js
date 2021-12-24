hljs.highlightAll();

window.GistEmbed.init();

mermaid.initialize({ startOnLoad: true });

var galleries = document.querySelectorAll('.lightgallery');
galleries.forEach(function(el){
  lightGallery(el); 
});
