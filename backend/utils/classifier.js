exports.classifyMessage = (text) => {
  if (text.includes('ingreso')) return 'ingreso';
  if (text.includes('salida')) return 'salida';
  return 'otro';
};
