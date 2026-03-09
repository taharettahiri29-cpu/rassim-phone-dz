<script>
  // كود يجعل الهاتف يتعامل مع الموقع كتطبيق مستقل
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      navigator.serviceWorker.register('/sw.js');
    });
  }
</script>
