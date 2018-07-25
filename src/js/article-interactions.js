'use strict'

var article = article || {}

article.interactions = (function () {
  var self = {
    onDetailsView: false,
    init: function () {
      document.dispatchEvent(new Event('articleInteractions:ready'))
    },
    load: function () {
      this.attachedEvents()
    },
    attachedEvents: function () {
      utils.addEventListenerByClass('js-favourites', 'click', this.setArticleAsFavourite.bind(this))
      utils.addEventListenerByClass('js-follow-user', 'click', this.followUsers.bind(this))
    },
    setArticleAsFavourite: function (event) {
      var idArticle = event.target.getAttribute('data-article-id')
      var callback = function (response) {
        if (response) {
          if (event.target.classList.contains('fa-heart-o')) {
            if (document.querySelector('#favourite-counter-' + idArticle)) {
              document.querySelector('#favourite-counter-' + idArticle).innerHTML++
            }
            event.target.classList.remove('fa-heart-o')
            event.target.classList.add('fa-heart')
          } else {
            if (document.querySelector('#favourite-counter-' + idArticle)) {
              document.querySelector('#favourite-counter-' + idArticle).innerHTML--
            }
            event.target.classList.remove('fa-heart')
            event.target.classList.add('fa-heart-o')
          }
        }
      }
      event.preventDefault()
      ajax.post(URLS.FAVORITES.url, {article: idArticle}, callback)
    },
    followUsers: function (event) {
      let self = this
      let followed = event.target.getAttribute('data-user-id')
      let elementsForChange
      let callback = function (response) {
        if (response) {
          if (!event.target.classList.contains('following')) {
            if (self.onDetailsView) {
              elementsForChange = document.querySelectorAll('.follow')
              for (var i = 0; i < elementsForChange.length; i++) {
                elementsForChange[i].classList.remove('follow')
                elementsForChange[i].classList.add('following')
              }
              var elements = document.querySelectorAll('.following')
              for (var i = 0; i < elements.length; i++) {
                elements[i].innerHTML = 'Following'
              }
            } else {
              event.target.classList.remove('follow')
              event.target.classList.add('following')
              event.target.innerHTML = 'Following'
            }
          } else {
            if (self.onDetailsView) {
              elementsForChange = document.querySelectorAll('.following')
              for (var i = 0; i < elementsForChange.length; i++) {
                elementsForChange[i].classList.remove('following')
                elementsForChange[i].classList.add('follow')
              }
              var elements = document.querySelectorAll('.follow')
              for (var i = 0; i < elements.length; i++) {
                elements[i].innerHTML = 'Follow'
              }
            } else {
              event.target.classList.remove('following')
              event.target.classList.add('follow')
              event.target.innerHTML = 'Follow'
            }
          }
        }
      }
      ajax.post(URLS.FOLLOW.url, {followed}, callback)
    }
  }
  return self
}())

document.addEventListener('DOMContentLoaded', function () {
  article.interactions.init()
})