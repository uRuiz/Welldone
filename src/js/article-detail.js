'use strict'

/**
 * @requires ../../node_modules/scrollmonitor/scrollMonitor.js
 * @requires ../../node_modules/moment/min/moment-with-locales.js
 */

var article = article || {}

article.detail = (function () {
  var self = {
    self: this,
    idArticle: undefined,
    locale: window.navigator.userLanguage || window.navigator.language,
    commentsViewed: false,
    lastIndex: 0,
    comments: undefined,
    init: function () {
      document.dispatchEvent(new Event('articleDetails:ready'))
      moment.locale(self.locale)
    },
    load: function () {
      this.attachedEvents()
    },
    attachedEvents: function () {
      document.querySelector('#coment-form').addEventListener('submit', this.submitCommentForm)
      var elementWatcher = scrollMonitor.create(document.querySelector('#article-comments'))
      elementWatcher.enterViewport(function () {
        if (!this.commentsViewed) {
          this.commentsViewed = true
          document.querySelector('#article-comments').innerHTML = 'Cargando...'
          self.loadComments()
        }
      })
    },
    loadComments: function () {
      let self = this
      var callback = function (response) {
        self.comments = response
        document.querySelector('#article-comments').innerHTML = ''
        self.showComments()
      }
      ajax.get(URLS.COMMENTS.url.replace('{0}', this.idArticle), callback)
    },
    showComments: function () {
      let commentsHTML = ''
      let comments = this.comments
      if (document.querySelector('#js-button-show-more-comments')) {
        document.querySelector('#js-button-show-more-comments').remove()
      }
      if (comments.length > (this.lastIndex + 10)) {
        let maxIndex = this.lastIndex + 10
        for (this.lastIndex; this.lastIndex < maxIndex; this.lastIndex++) {
          commentsHTML += self.getCommentAsHtml(comments[this.lastIndex])
        }
        this.showButtonMore()
      } else {
        for (this.lastIndex; this.lastIndex < comments.length; this.lastIndex++) {
          commentsHTML += self.getCommentAsHtml(comments[this.lastIndex])
        }
      }
      let temporaryElement = document.createElement('div')
      temporaryElement.innerHTML = commentsHTML
      while (temporaryElement.firstChild) {
        document.querySelector('#article-comments').insertBefore(temporaryElement.firstChild, null)
      }
    },
    showButtonMore: function () {
      let buttonShowMore = '<button id="js-button-show-more-comments" class="btn btn-article-action">Ver mas comentarios</button>'
      let temporaryElement = document.createElement('div')
      temporaryElement.innerHTML = buttonShowMore
      while (temporaryElement.firstChild) {
        let referenceNode = document.querySelector('#article-comments')
        referenceNode.parentNode.insertBefore(temporaryElement.firstChild, referenceNode.nextSibling)
      }
      document.querySelector('#js-button-show-more-comments').addEventListener('click', this.showComments.bind(this))
    },
    submitCommentForm: function (event) {
      event.preventDefault()
      var obj = {
        text: document.querySelector('#comment-text').value,
        article: self.idArticle
      }
      var callback = function (response) {
        document.querySelector('#article-comments').insertAdjacentHTML('afterbegin', self.getCommentAsHtml(response))
        document.querySelector('#comments-counter').innerHTML++
        document.querySelector('#comment-text').value = ''
      }
      ajax.post(URLS.COMMENTS.url.replace('{0}', self.idArticle), obj, callback)
    },
    getCommentAsHtml: function (comment) {
      let moment_created_date = moment(comment.create_date)
      let format = "MMM D, YYYY"
      if (moment().isSame(moment_created_date, 'year')) {
        format = "MMM D"
      }
      let created_date = moment_created_date.format(format)
      return `<div>
<p class="comments-text">${comment.text}</p>
<p><a href="/@${comment.user.username}">
<span class="comment-user">${ comment.user.first_name } ${ comment.user.last_name }</span>
</a> · <span class="comment-date">${created_date}</span>
</p>
</div>`
    }
  }
  return self
}())

document.addEventListener('DOMContentLoaded', function () {
  article.detail.init()
})