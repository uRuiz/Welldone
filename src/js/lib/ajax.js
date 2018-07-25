'use strict'

var ajax = (function () {
  var self = {
    get: function (url, callback) {
      let xhttp = new XMLHttpRequest()
      xhttp.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
          let rawResponse = JSON.parse(this.responseText)
          let response
          if (rawResponse.Content) {
            response = JSON.parse(rawResponse.CONTENT)
          } else {
            response = rawResponse
          }
          if (callback) {
            callback(response)
          }
        } else if (this.readyState === 4) {
          console.log(`Error calling: ${this.url} Error text: ${this.responseText}`)
        }
      }
      xhttp.open('GET', url)
      xhttp.send()
    },
    post: function (url, objToSend, callback) {
      let xhttp = new XMLHttpRequest()
      xhttp.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 201) {
          let rawResponse = JSON.parse(this.responseText)
          let response
          if (rawResponse.Content) {
            response = JSON.parse(rawResponse.CONTENT)
          } else {
            response = rawResponse
          }
          if (callback) {
            callback(response)
          }
        } else if (this.readyState === 4) {
          console.log(`Error calling: ${this.url} Error text: ${this.responseText}`)
        }
      }
      xhttp.open('POST', url)
      xhttp.setRequestHeader('Content-Type', 'application/json')
      xhttp.setRequestHeader('X-CSRFToken', self.getCookie('csrftoken'))
      xhttp.send(JSON.stringify(objToSend))
    },
    getCookie: function (name) {
      var cookieValue = null;
      if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';')
        for (var i = 0; i < cookies.length; i++) {
          var cookie = cookies[i].trim()
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
            break
          }
        }
      }
      return cookieValue
    }
  }
  return self
}())

