'use strict'

var loginModal = loginModal || {}

loginModal = (function () {
  let self = {
    modal: undefined,
    closeIcon: undefined,
    init: function () {
      document.dispatchEvent(new Event('loginModal:ready'))
    },
    load: function () {
      this.modal = document.getElementById('js-login-modal')
      this.closeIcon = document.getElementById('js-login-modal-close')
      this.attachedEvents()
    },
    attachedEvents: function () {
      utils.addEventListenerByClass('js-handle-login-modal', 'click', this.openModal.bind(this))
      this.closeIcon.addEventListener('click', this.closeModal.bind(this))
      window.addEventListener('click', this.closeModal.bind(this))
    },
    openModal: function (event) {
      event.preventDefault()
      self.modal.style.display = 'block'
    },
    closeModal: function (event) {
      if (event.target === this.modal || event.target === this.closeIcon) {
        self.modal.style.display = 'none'
      }
    }
  }
  return self
}())

document.addEventListener('DOMContentLoaded', function () {
  loginModal.init()
})