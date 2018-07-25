'use strict'

// Dropdowns
document.addEventListener('click', function (event) {
  if (event.target.classList.contains('dropdown-toggle')) {
    bootstrap.hideAllDropdowns()
    event.target.parentElement.classList.add('show')
  } else {
    bootstrap.hideAllDropdowns()
  }
})

var bootstrap = (function () {
  var self = {
    hideAllDropdowns: function () {
      utils.removeClassFromElements(document.querySelectorAll('.dropdown'), 'show')
    }
  }
  return self
})()
