'use strict'

var mainMenu = mainMenu || {}

mainMenu = (function () {
  let self = {
    init: function () {
      document.dispatchEvent(new Event('mainMenu:ready'))
    },
    load: function () {
      this.attachedEvents()
    },
    attachedEvents: function () {
      let menuIcon = document.querySelector('#pull')
      let mainMenu = document.querySelector('#main-menu')
      menuIcon.addEventListener('click', function (event) {
        event.preventDefault()
        mainMenu.classList.toggle('fold')
      })
      window.addEventListener('resize', function () {
        mainMenu.classList.add('fold')
      })
    }
  }
  return self
}())

document.addEventListener('DOMContentLoaded', function () {
  mainMenu.init()
})
