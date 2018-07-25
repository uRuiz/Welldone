'use strict'

var utils = (function () {
	var self = {
  addEventListenerByClass: function (className, event, fn) {
    var list = document.getElementsByClassName(className)
    for (var i = 0, len = list.length; i < len; i++) {
      list[i].addEventListener(event, fn, false)
    }
  },
  removeClassFromElements: function (elements, classToRemove) {
    for (var i = 0; i < elements.length; i++) {
      elements[i].classList.remove(classToRemove)
    }
  }
}
  return self
}());
