/* Handle native selection explicitly: cloud read failures and rejected files must be visible. */
(function () {
  let generation = 0;
  function update(id, props) {
    if (window.dash_clientside && window.dash_clientside.set_props) window.dash_clientside.set_props(id, props);
  }
  function message(text) {
    const el = document.getElementById('pred-upload-local');
    if (el) el.textContent = text;
  }
  function select(event, files) {
    const ticket = ++generation;
    event.preventDefault(); event.stopPropagation(); event.stopImmediatePropagation();
    update('pred-upload', {contents: null, filename: null});
    update('pred-run', {disabled: true}); update('explain-run', {disabled: true});
    update('pred-result', {children: null}); update('explain-result', {children: null});
    const consent = document.querySelector('#pred-consent input:checked');
    if (!consent) {message('Marca la confirmación antes de seleccionar una imagen.'); return;}
    if (!files || files.length !== 1) {message('Selecciona una sola imagen PNG o JPG.'); return;}
    const file = files[0];
    if (!file.size) {message('El archivo está vacío o no está descargado. Descárgalo desde Drive/iCloud y vuelve a seleccionarlo.'); return;}
    if (file.size > 2 * 1024 * 1024) {message('No se cargó «' + file.name + '»: supera 2 MB. Selecciona un recorte RGB de 128 × 128 píxeles.'); return;}
    const extension = /\.(png|jpe?g)$/i.exec(file.name);
    const type = file.type || (extension ? (/png/i.test(extension[1]) ? 'image/png' : 'image/jpeg') : '');
    if (!['image/png', 'image/jpeg'].includes(type)) {message('Formato no admitido. Usa PNG o JPG; HEIC, TIFF y PDF no se aceptan.'); return;}
    message('Leyendo «' + file.name + '»…');
    const reader = new FileReader();
    reader.onerror = function () {if (ticket === generation) message('No se pudo leer el archivo. Descárgalo al computador desde Drive/iCloud y vuelve a seleccionarlo.');};
    reader.onabort = reader.onerror;
    reader.onload = function () {
      if (ticket !== generation) return;
      const data = String(reader.result).replace(/^data:[^;]*;/, 'data:' + type + ';');
      message('Archivo leído. La validación del servidor aparece debajo.');
      update('pred-upload', {contents: data, filename: file.name, last_modified: file.lastModified / 1000});
    };
    reader.readAsDataURL(file);
  }
  document.addEventListener('change', function (event) {
    if (event.target.matches('input[type=file]') && event.target.closest('#pred-upload')) select(event, event.target.files);
  }, true);
  document.addEventListener('drop', function (event) {
    if (event.target.closest && event.target.closest('#pred-upload')) select(event, event.dataTransfer.files);
  }, true);
})();
