var njbValidation = {
  replaceChars: function (needle, replace, haystack, flags) {
    flags = flags || '';
    var re = new RegExp(needle, flags);
    return haystack.replace(re, replace);
  }
};